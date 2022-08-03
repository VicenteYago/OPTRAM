#!/bin/bash

mkdir -p  indices
mkdir -p l1c
mkdir -p l2a
mkdir -p tmp

Rscript s2.R $1 $2 $3 $4 $5

