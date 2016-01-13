sudo apt-get update

sudo apt-get -y install python3
sudo apt-get -y install gcc
sudo apt-get -y install python-dev
sudo apt-get -y install python3-dev
sudo apt-get install -qy python-setuptools
sudo easy_install pip
pip install virtualenv

mkdir log
echo 'this is a log file' > log/Re.log 

./setup.sh