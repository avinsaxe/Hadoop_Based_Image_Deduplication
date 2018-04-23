
#!/bin/bash

echo "hadoop fs -mkdir / input"
hadoop fs -mkdir / input
echo "Hadoop is an elephant" > file0
echo "Hadoop is as yellow as can be" > file1
echo "Oh what a yellow fellow is Hadoop" > file2
echo "hadoop fs -put file* input"
hadoop fs -put file* input/
echo "mkdir -p build"
mkdir -p build
echo "hadoop jar wordcount.jar org.myorg.WordCount input output"
hadoop jar wordcount.jar org.myorg.WordCount input output
echo "hadoop fs -cat output/*"
hadoop fs -cat output/*


