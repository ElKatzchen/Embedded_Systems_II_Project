#!/bin/bash
clear
echo "----------COMPILING PROGRAM----------"
make clean
make
echo "----------PROGRAM COMPILED----------"
echo "----------UPLOADING PROGRAM----------"
sudo lm4flash gcc/katzchen.bin
echo "----------PROGRAM UPLOADEDED----------"
exec bash
