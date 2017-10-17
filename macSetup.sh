#!/bin/bash

[ $SHLVL = 2 ] && echo "Usage: . ${0##*/}" && exit

if [ ! -d ~/python/crc_env ]
	then
		test -e ~/python || mkdir ~/python
		pushd .
		cd ~/python
		virtualenv crc_env
		popd
fi

source ~/python/crc_env/bin/activate

#brew install rabbitmq
#/usr/local/sbin/rabbitmq-server -detached

pip install -r requirements.txt

./crc/manage.py migrate
python ./crc/manage.py runserver '0.0.0.0:8000'
