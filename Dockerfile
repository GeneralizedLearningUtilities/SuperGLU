FROM ubuntu:14.04

RUN sudo apt-get -y install software-properties-common
RUN sudo add-apt-repository ppa:nginx/stable
RUN sudo apt-get update && sudo apt-get -y upgrade
RUN sudo apt-get -y install nginx
RUN sudo apt-get -y install python3
RUN sudo apt-get -y install git
#RUN sudo apt-get -y install python-pip
RUN sudo apt-get install -qy python-setuptools
RUN easy_install pip
RUN pip install virtualenv

#configure nginx
RUN sudo rm /etc/nginx/sites-enabled/default
RUN sudo ln -s /superglu/config/recommender.x-in-y.conf /etc/nginx/conf.d/
RUN sudo /etc/init.d/nginx restart

# Install app
ADD ./ superglu/
ADD ./config/boto.cfg /etc/boto.cfg


# Install dependencies
RUN bash ./superglu/setup.sh

RUN chmod +x ./superglu/local.sh

EXPOSE 80
EXPOSE 443
EXPOSE 5000


CMD ["bash", "./superglu/local.sh"]



