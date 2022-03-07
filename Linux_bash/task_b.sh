#!/bin/bash
file=$1

echo "1. From which ip were the most requests?"
awk '{print $1}' $file | sort | uniq -c | sort -gr | head -1

echo "2. What is the most requested page?"
awk '{print $7}' $file | sort | uniq -c | sort -gr | head -1

echo "3. How many requests were there from each ip?"
awk '{print $1}' $file | sort | uniq -c | sort -gr

echo "4. What non-existent pages were clients referred to?"
awk '/(304|404 )/{print $7}' $file | sort | uniq -c | sort -gr

echo "5. What time did site get the most requests?"
grep -Eo "[0-9]{4}:([0-9]{2}:){2}[0-9]{2}" $file | sort | uniq -c | sort -gr | head -1

echo "6. What search bots have accessed the site? (UA + IP)"
awk '/bot/{print $1,$12}' $file | sort | uniq -c | sort -gr


