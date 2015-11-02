FROM ubuntu:14.04

RUN sudo apt-get -y install python3
RUN sudo apt-get -y install git
#RUN sudo apt-get -y install python-pip
RUN sudo apt-get install -qy python-setuptools
RUN easy_install pip
RUN pip install virtualenv

# Install app
RUN rm -rf superglu/*
RUN mkdir superglu
RUN git clone https://github.com/GeneralizedLearningUtilities/SuperGLU superglu
RUN mkdir superglu/log

# Install dependencies
RUN bash ./superglu/setup.sh

RUN chmod +x ./superglu/local.sh

EXPOSE 80
EXPOSE 5000

<<<<<<< HEAD
CMD ["./superglu/local.sh"]
=======
CMD [./superglu/local.sh]
>>>>>>> 2ea1f5acbfe05cc1ddea7748bea020e47ac3b689
