#!/bin/bash
LOG_DIR="./logs/"
mkdir -p  ${LOG_DIR}
mkdir -p  indices
mkdir -p l1c
mkdir -p l2a

CURRENT_DATE=$(date -d "today" +"%Y-%m-%dT%H:%M")

LOG_FILE="$LOG_DIR$CURRENT_DATE"
LOG_FILE+=".txt"
nohup Rscript s2.R $1 $2 $3 $4 $5   > ${LOG_FILE} 2> ${LOG_FILE} < /dev/null &

