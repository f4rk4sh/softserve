#!/bin/bash

echo "My name is $0"
if [ $# -eq 0 ]; then
	echo "You have to give at least one parameter."
	exit 1
fi

while (( $# )); do
	echo "You gave me $1"
	shift
done


#echo "This script called $0"
#echo "1st arg: $1"
#echo "2nd arg: $2"
#echo "3rd arg: $3"
#echo "$ $$ PID of the script "
#echo "# $# count args"
#echo "? $? last return code"
#echo "* $* all the args"
