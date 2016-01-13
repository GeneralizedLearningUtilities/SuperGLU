
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

sudo apt-get update

sudo apt-get -y install mongodb-org
sudo apt-get -y install python3
sudo apt-get -y install gcc
sudo apt-get -y install python-dev
sudo apt-get -y install python3-dev
sudo apt-get install -qy python-setuptools
sudo easy_install pip
pip install virtualenv

sudo service mongod start

mkdir log
echo 'this is a log file' > log/Re.log 