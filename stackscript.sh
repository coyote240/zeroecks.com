#!/bin/bash


# Servers
echo 'deb http://ftp.debian.org/debian jessie-backports main' >> /etc/apt/sources.list
apt-get install -y -t jessie-backports install nginx redis-server postgresql-9.6

# Python3 and libs
apt-get update
apt-get upgrade
apt-get install -y python3-pip python3-virtualenv

# Virtual Environment for Python
if [ ! -d '~/env' ]; then
    mkdir '~/env'
fi
virtualenv -p python3 ~/env/zeroecks
source ~/env/zeroecks/bin/activate
