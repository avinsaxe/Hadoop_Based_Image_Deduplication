~/Downloads/hadoop-3.0.1/bin/hadoop fs -rm -r output
~/Downloads/hadoop-3.0.1/bin/hadoop fs -mkdir / input
echo "Hadoop is an elephant" > file0
echo "Hadoop is as yellow as can be" > file1
echo "Oh what a yellow fellow is Hadoop" > file2
~/Downloads/hadoop-3.0.1/bin/hadoop fs -put file* input/
mkdir -p build
~/Downloads/hadoop-3.0.1/bin/hadoop jar wordcount.jar org.myorg.WordCount input output
~/Downloads/hadoop-3.0.1/bin/hadoop fs -cat output/*

