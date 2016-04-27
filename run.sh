#!/bin/bash

echo $0
echo $1
echo $#
echo $*
echo $@
echo $?
echo $$


if [ -n "$1" ]
then
	  echo Hello $1,glad to meet you.
else
	    echo "Sorry,you didn't identify yourself."
fi


$*|tee $1 






#python sendmail.py
