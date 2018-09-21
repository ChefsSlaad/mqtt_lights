#! /bin/bash

webrpl=$"/home/marc/projects/webrepl/webrepl_cli.py"


ADDR=$1 
PASSWD=$2 
shift 2 # ignore the first two arguments; treat the rest as filenames

if [[ $# -eq 0 ]]; then
    echo "no files to transfer supplied. at least one file is needed."
    echo "use * to copy all files in the current directory" 
elif [[ $# -eq 1 ]]; then
    if [[ -d $1 ]]; then
        echo "copying all files in directory $1"
        FILES=$(ls -d1 $1*)
    elif [[ -f $1 ]]; then
        FILES=$@
    fi
else
    FILES=$@
fi

re='^(0*(1?[0-9]{1,2}|2([0-4][0-9]|5[0-5]))\.){3}'
 re+='0*(1?[0-9]{1,2}|2([‌​0-4][0-9]|5[0-5]))$'

helptext="copy many files to an esp8266 board in a single go
usage:
$0 <ip-adress> <esp8266 password> FILES"


# check valid ip adress

if [[ ! $ADDR =~ $re ]]; then
    echo $helptext
    echo "the adress $ADDR is not a valid IP adress"
    exit 1
fi
echo $PASSWD


for FILE in $FILES; do
    echo "copying $FILE to $ADDR"
    $webrpl -p $PASSWD $FILE $ADDR:/
done



