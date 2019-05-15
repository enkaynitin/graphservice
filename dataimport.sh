#!/bin/bash

export IFS=";"
cat $1 | while read graph node top left bottom right; do echo "$node, $graph, $top, $left, $bottom, $right" > "$1_updated.csv"; done;


RES=$( curl --request POST \
                --url http://127.0.0.1:8000/graph/graphs/upload/ \
                --header 'cache-control: no-cache' \
                --header 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
                --form file=@/home/nk/Projects/mavenoid/graphservice/$1_updated.csv\
                --form title=Graph123
)

status=$?

if [ "$?" -eq 0 ];
    then
        echo "Success"
        exit $status
    else
        echo "Failed"
        exit $status
fi