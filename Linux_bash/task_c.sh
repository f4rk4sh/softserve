#!/bin/bash

if [ $# -eq 0 ]; then
  echo "This script creates a data backup with a frequency of one minute"
elif [ -z "$1" ]  || [ -z "$2" ]; then
  echo "You have failed to pass a parameter"
	echo "Usage: SCRIPT-NAME SOURCE-DIRECTORY BACKUP-DIRECTORY"
	echo "Hint: use only absolute paths"
fi

script=$0
source=$1
backup=$2

(crontab -l; echo "* * * * * $script $source $backup")|awk '!x[$0]++'|crontab -

echo "$(date) - creating backup - $source" >> "$backup/backup.log"

for file in $(find "$source" -type f -name "*\.*"); do
  new_file=$(echo "$file" | grep -Eo "[0-9a-zA-Z]*\.[0-9a-zA-Z]*$")
  if ! [[ -e "$backup/$new_file" ]]; then
    echo "$(date) - adding file - $new_file" >> "$backup/backup.log"
    cp "$file" "$backup/"
  fi
done

for file in $(find "$backup" -type f -name "*\.*"); do
  deleted_file=$(echo "$file" | grep -Eo "[0-9a-zA-Z]*\.[0-9a-zA-Z]*$")
  if [[ $deleted_file == "backup.log" ]]; then
      echo "$(date) - changing logs - $deleted_file" >> "$backup/backup.log"
  elif ! [[ -e "$source/$deleted_file" ]]; then
      echo "$(date) - deleting file - $deleted_file" >> "$backup/backup.log"
  fi
done

