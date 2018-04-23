hadoop fs -mkdir -p /user/cloudera/wordcount /user/cloudera/wordcount/input
echo "Hadoop is an elephant" > file0
echo "Hadoop is as yellow as can be" > file1
echo "Oh what a yellow fellow is Hadoop" > file2
hadoop fs -put file* /user/cloudera/wordcount/input
mkdir -p build
hadoop jar wordcount.jar org.myorg.WordCount /user/cloudera/wordcount/input /user/cloudera/wordcount/output 
hadoop fs -cat /user/cloudera/wordcount/output/*
