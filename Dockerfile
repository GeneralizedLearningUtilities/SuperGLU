FROM ubuntu:14.04

RUN sudo apt-get -y install python3
RUN sudo apt-get -y install git
#RUN sudo apt-get -y install python-pip
RUN sudo apt-get install -qy python-setuptools
RUN easy_install pip
RUN pip install virtualenv

# Install app
ADD ./ superglu/
ADD ./config/boto.cfg /etc/boto.cfg

# Install dependencies
RUN bash ./superglu/setup.sh

RUN chmod +x ./superglu/local.sh

EXPOSE 80
EXPOSE 5000


CMD ["bash", "./superglu/local.sh"]



