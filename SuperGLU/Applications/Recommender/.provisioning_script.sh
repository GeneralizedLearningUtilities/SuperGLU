#!/bin/bash

# Install stuff I know you'll need
sudo apt-get upgrade
sudo apt-get -y install build-essential git python-dev python-pip python-virtualenv
sudo apt-get -y install python3 python3-dev python3-pip python-pip-whl
sudo apt-get -y install libffi-dev libssl-dev
sudo apt-get -y install libyaml-dev

sudo pip install --upgrade requests[security]
sudo pip install --upgrade pip

# Make symbolic links to the sync'ed directory for more "natural" work
ln -s ~/Application ./SuperGLU/Applications/Recommender/ 
ln -s ~/SuperGLU ./SuperGLU/

# Remove Ubuntu's landscape stuff and clear login messages
sudo apt-get purge -y landscape-client landscape-common
sudo rm -f /etc/update-motd/*
sudo rm -f /etc/motd
sudo touch /etc/motd

# Spit out some messages for the user - to do this we'll need to create a message
# of the day (motd) file, and change the sshd_config file
cat << EOF | sudo tee /etc/motd

==============================================================================
Some helpful hints for working with gluten:

 * If you are familiar with vagrant, you need to know that we create a link
   from /vagrant to ~/gluten. If you are NOT familiar with vagrant, you
   create our VM, log into it, and then access the code like this:

    $ vagrant up
    $ vagrant ssh
    $ cd gluten

 * READ the README.md file!!! You need to supply a test.config file before
   you can really test things out.

 * You can use your favorite code editor and version control application in
   the host operating system - you can just use this little login to test,
   start, or stop the application.

 * First things first: log in and set up the test environment

   $ vagrant ssh
   $ cd gluten
   $ ./setup.sh

 * To run the test servers in the background (keeps you from running with
   "real" AWS services) :

   $ vagrant ssh
   $ cd gluten
   $ test/local_test_services.sh

 * To run the server in development mode:

    $ vagrant ssh
    $ cd gluten
    $ ./local.sh

 * To run unit tests:

    $ vagrant ssh
    $ cd gluten
    $ ./run_tests.sh

 * Connect to gluten from your host operating system at:

    http://127.0.0.1:5533/
==============================================================================

EOF

PDIR="$HOME/.provision"
mkdir -p $PDIR

SSHDSRC="/etc/ssh/sshd_config"
SSHDBASE="$PDIR/sshd_config"

# Note that below we set the SSH variable PrintMotd to no - which is odd because
# that's exactly what we want to happen. However, Ubuntu configures a PAM motd
# module that will print the motd file on login. If we don't set the sshd config
# variable PrintMotd to no, our message would be displayed twice

cp $SSHDSRC $SSHDBASE.old
grep -v PrintMotd $SSHDBASE.old > $SSHDBASE.new
printf "\n\nPrintMotd no\n" >> $SSHDBASE.new
sudo cp $SSHDBASE.new $SSHDSRC
