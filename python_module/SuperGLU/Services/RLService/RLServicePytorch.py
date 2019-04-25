import os
import random
import sys
import time

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class NeuralNetwork(nn.Module):

    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.number_of_actions = 3
        self.gamma = 0.99
        self.final_epsilon = 0.0001
        self.initial_epsilon = 0.1
        self.number_of_iterations = 200
        self.replay_memory_size = 10000
        self.minibatch_size = 32
        self.conv1 = nn.Conv1d(1, 12, 1, 12)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv1d(12, 64, 1, 2)
        self.relu2 = nn.ReLU(inplace=True)
        self.conv3 = nn.Conv1d(64, 12, 1, 1)
        self.relu3 = nn.ReLU(inplace=True)
        self.fc4 = nn.Linear(12, 64)
        self.relu4 = nn.ReLU(inplace=True)
        self.fc5 = nn.Linear(64, self.number_of_actions)

    def forward(self, x):
        out = self.conv1(x)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.conv3(out)
        out = self.relu3(out)
        out = out.view(out.size()[0], -1)
        out = self.fc4(out)
        out = self.relu4(out)
        out = self.fc5(out)
        out = F.softmax(out, dim=1)
        return out

    
class State:
    def __init__(self):
        self.score = self.playerIndex = self.loopIter = 0
        self.correctAnswerCount = 0
        self.mixedAnswerCount = 0
        self.incorrectAnswerCount = 0
        self.provideHint = False  # True when hint needs to be provided
        self.provideFeedback = False  # True when feedback needs to be provided
        self.correctAnswer = False # True when user provides correct answer
        self.mixedAnswer = False # True when user provides mixed answer
        self.incorrectAnswer = False  # True when user provides incorrect answer

    def action_step(self, input_actions):
        reward = 0.0
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        # input_actions[0] == 1: Correct Answer
        # input_actions[1] == 1: Mixed Answer
        # input_actions[2] == 1: Incorrect Answer

        if input_actions[0] == 1:
            self.correctAnswer = True
            self.correctAnswerCount += 1
            reward = 1.0
        if input_actions[1] == 1:
            self.mixedAnswer = True
            self.mixedAnswerCount += 1
            reward = 0.5
        if input_actions[2] == 2:
            reward = -1.0
            self.incorrectAnswer = True
            self.incorrectAnswerCount += 1
        self.score = self.correctAnswerCount + self.incorrectAnswerCount + self.mixedAnswerCount

        nextState = torch.torch.FloatTensor([[[self.score]],
                                                      [[self.playerIndex]],
                                                      [[self.loopIter]],
                                                      [[self.correctAnswerCount]],
                                                      [[self.mixedAnswerCount]],
                                                      [[self.incorrectAnswerCount]],
                                                      [[self.provideHint]],
                                                      [[self.provideHint]],
                                                      [[self.provideFeedback]],
                                                      [[self.correctAnswer]],
                                                      [[self.mixedAnswer]],
                                                      [[self.incorrectAnswer]]])


        return nextState, reward, terminal

    def getValues(self):
        values = list()
        values.append(self.score)
        values.append(self.correctAnswerCount)
        values.append(self.mixedAnswerCount)
        values.append(self.incorrectAnswerCount)
        values.append(self.provideHint)
        values.append(self.provideFeedback)
        values.append(self.correctAnswer)
        values.append(self.mixedAnswer)
        values.append(self.incorrectAnswer)
        return values

        #[self.score, self.correctAnswerCount, self.mixedAnswerCount,
        #self.incorrectAnswerCount, self.provideHint, self.provideFeedback, self.correctAnswer,
        #self.mixedAnswer, self.incorrectAnswer]

def init_weights(m):
    if type(m) == nn.Conv2d or type(m) == nn.Linear:
        torch.nn.init.uniform_(m.weight, -0.01, 0.01)
        m.bias.data.fill_(0.01)

def train(model, start):
    # define Adam optimizer
    optimizer = optim.Adam(model.parameters(), lr=1e-6)

    # initialize mean squared error loss
    criterion = nn.MSELoss()

    #game
    main_state = State()

    # initialize replay memory
    replay_memory = []

    # initial action is do nothing
    action = torch.zeros([model.number_of_actions], dtype=torch.float32)
    action[0] = 1

    next_state, reward, terminal = main_state.action_step(action)

    # state = torch.cat((main_state, main_state, main_state, main_state)).unsqueeze(0)
    epsilon = model.initial_epsilon
    iteration = 0
    epsilon_decrements = np.linspace(model.initial_epsilon, model.final_epsilon, model.number_of_iterations)

    while iteration < model.number_of_iterations:
        # get output from the neural network
        closeState = torch.torch.FloatTensor([[[main_state.score]],
                                              [[main_state.playerIndex]],
                                              [[main_state.loopIter]],
                                              [[main_state.correctAnswerCount]],
                                              [[main_state.mixedAnswerCount]],
                                              [[main_state.incorrectAnswerCount]],
                                              [[main_state.provideHint]],
                                              [[main_state.provideHint]],
                                              [[main_state.provideFeedback]],
                                              [[main_state.correctAnswer]],
                                              [[main_state.mixedAnswer]],
                                              [[main_state.incorrectAnswer]]])
        output = model(closeState)[0]

        # initialize action
        action = torch.zeros([model.number_of_actions], dtype=torch.float32)
        if torch.cuda.is_available():  # put on GPU if CUDA is available
            action = action.cuda()

        # epsilon greedy exploration
        random_action = random.random() <= epsilon
        if random_action:
            print("Performed random action!")
        action_index = [torch.randint(model.number_of_actions, torch.Size([]), dtype=torch.int)
                        if random_action
                        else torch.argmax(output)][0]

        if torch.cuda.is_available():  # put on GPU if CUDA is available
            action_index = action_index.cuda()

        action[action_index] = 1

        # get next state and reward
        nextState, reward, terminal = main_state.action_step(action)
        # ma = torch.cat((state.squeeze(0)[1:, :, :], image_data_1)).unsqueeze(0)

        action = action.unsqueeze(0)
        reward = torch.from_numpy(np.array([reward], dtype=np.float32)).unsqueeze(0)

        # save transition to replay memory
        replay_memory.append((nextState, action, reward))

        # if replay memory is full, remove the oldest transition
        if len(replay_memory) > model.replay_memory_size:
            replay_memory.pop(0)

        # epsilon annealing
        epsilon = epsilon_decrements[iteration]

        # sample random minibatch
        minibatch = random.sample(replay_memory, min(len(replay_memory), model.minibatch_size))

        # unpack minibatch
        state_batch = torch.cat(tuple(d[0] for d in minibatch))
        action_batch = torch.cat(tuple(d[1] for d in minibatch))
        reward_batch = torch.cat(tuple(d[2] for d in minibatch))
        # state_1_batch = torch.cat(tuple(d[3] for d in minibatch))

        if torch.cuda.is_available():  # put on GPU if CUDA is available
            state_batch = state_batch.cuda()
            action_batch = action_batch.cuda()
            reward_batch = reward_batch.cuda()
            # state_1_batch = state_1_batch.cuda()

        # get output for the next state
        output_1_batch = model(state_batch)


        # extract Q-value
        # q_value = torch.sum(model(state_batch) * action_batch, dim=1)

        # PyTorch accumulates gradients by default, so they need to be reset in each pass
        optimizer.zero_grad()
        optimizer.step()

        iteration += 1

        if iteration % 25000 == 0:
            torch.save(model, "pretrained_model/current_model_" + str(iteration) + ".pth")

        print("iteration:", iteration, "elapsed time:", time.time() - start, "epsilon:", epsilon, "action:",
              action_index.cpu().detach().numpy(), "reward:", reward.numpy()[0][0], "Q max:",
              np.max(output.cpu().detach().numpy()))

    torch.save(model, "pretrained_model_" + str(iteration) + ".pth")


def main(mode):
    cuda_is_available = torch.cuda.is_available()
    print('MODE', mode)
    if mode == 'test':
        
        #DUMMY - To Be Implemented
        model = torch.load(
            'pretrained_model/current_model_200.pth',
            map_location='cpu' if not cuda_is_available else None
        ).eval()

        if cuda_is_available:  # put on GPU if CUDA is available
            model = model.cuda()

        test(model)

    elif mode == 'train':
        if not os.path.exists('pretrained_model/'):
            os.mkdir('pretrained_model/')

        model = NeuralNetwork()

        if cuda_is_available:  # put on GPU if CUDA is available
            model = model.cuda()

        #Uniform
        model.apply(init_weights)
        start = time.time()
        train(model, start)



if __name__ == "__main__":
    main(sys.argv[1])