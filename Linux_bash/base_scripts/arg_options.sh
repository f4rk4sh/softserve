#!/bin/bash
while getopts ":ab:c:" option; do
	case $option in
		a) echo received -a ;;
		b) echo received -b with $OPTARG ;;
		c) echo received -c with $OPTARG ;;
		:) echo "option -$OPTARG needs an argument" ;;
		*) echo "invalid option -$OPTARG" ;;
	esac
done
