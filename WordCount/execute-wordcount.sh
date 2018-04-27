#!/bin/bash
hadoop fs -rm -r /user/cloudera/wordcount/output
hadoop fs -rm -r /user/cloudera/wordcount/input
hadoop fs -mkdir -p /user/cloudera/wordcount /user/cloudera/wordcount/input
hadoop fs -put my_hadoop_data_file* /user/cloudera/wordcount/input
mkdir -p build
hadoop jar wordcount.jar org.myorg.WordCount /user/cloudera/wordcount/input /user/cloudera/wordcount/output 
#hadoop fs -cat /user/cloudera/wordcount/output/*
rm temp.txt
hadoop fs -copyToLocal /user/cloudera/wordcount/output/part-r-00000 temp.txt
mv temp.txt count.txt
rm temp.txt
