#!/bin/bash
# Job Helpdesk Advisor :-)
echo -n "What job do you want ? "
read job
case $job in
	"devops") echo "Excellent" ;;
	"dev") echo "Good" ;;
	"test") echo "not bad." ;;
	"frontend") echo "Really???" ;;
	*) echo "Make your choise once more from: devops, dev, test and frontend" ;;
esac
