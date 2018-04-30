
# Intelligent Cloud Based Image Deduplication Utility

## PROJECT DESCRIPTION:

Data duplication is one of the major challenges when optimizing image storage on cloud. One of the most challenging use-case is removing duplicate/similar images. The use-case can be broken down into two separate tasks
Identifying duplicate/similar images utilizing concepts of Image processing
Distribute the resource intensive task of image processing and comparison of an image across the whole database to scan for duplicates using Hadoop to run the image processing algorithm in step 1 parallelly to quickly find and report duplicate instances. 

After duplicates are identified, user is notified about the same with the option to delete or keep the newly uploaded duplicate image.

Unique images exists in the directory. No existing images in the directory can be similar.
Adding a new image generates a hash value for the image, which is a computationally intensive task, as that involves image processing
Whenever a new image is uploaded to the directory, it is compared with all the existing images using their hash values in our database
Tasks 2 and 3 are both done parallelly and the system ensures uniqueness of hash values


### Other applications of such a tool can be in the following domain:
Identifying if image of a person already exists in the database
Sorting images based on similarity
Identifying similar images and removing duplicates to save hard-disk space
Processing similar/related images to create a personalized video, for the user to share

As is clear from the problem statement, the challenges of data extraction and data matching increases exponentially with number of images. All this is achieved by distributing the task of image processing and image matching on a cluster of servers in parallel, utilizing Hadoop.


## PROJECT DELIVERABLES AND TECHNICAL SPECIFICATIONS: 

The following are the main components into which we are dividing our entire development cycle:

### Image Processing
We are planning to use pHash (perspectiveHash), for image processing
We will develop our code in Python 3.0

### Hadoop Cluster
For demo purpose, we will be using our team member’s laptops to host 3 servers, where image comparison tasks will run in parallel
In this cluster, the similarity coefficient for the image will be computed, and maximum value of this similarity coefficient will be returned
We will compare computed similarity coefficient with a threshold value to confirm if image is duplicate or unique

### CLI Based Interface

CLI Based:
Upload images to a directory. 
Trigger image processing job on the newly uploaded image
CLI notifies if the image is a duplicate of an existing image or not
User takes appropriate action to keep the image or move it to trash

## CHALLENGES INVOLVED:

Often the data will be segregated at multiple nodes in cluster, and communication between the cluster through master node can impact performance
Data across replicated data nodes has to be updated accordingly
The storage of the images and their hash values in the cloud present data storage challenges (which system to store? How to optimize the storage capacity so that the disks in the three laptops are evenly utilized, etc?)
Implementing an image hashing algorithm and using it to compare images with a similarity coefficient, i.e. hash of the images should be unique, but they should also be sufficiently representative of the image, in order to enable us to compute the similarity between two hashed images.


## Instructions to RUN

### The section outlines instructions to run the project using provided OVA file.

1. Download OVA file from here OVA.

2. Use Oracle VM to create three VMs for the cluster using Export appliance.

3. In Terminal in hadoop-master use command ”su” and password “nimda” to log to root.

4. Change IP address of slaves and master in /etc/hosts in all three machines. Use ifconfig to get IP address.

5. Execute hdfs namenode -format in master.
6. Execute './start-hadoop.sh' to start all hadoop processes in the cluster.

7. start python poller:
   '''cd  /home/hduser/CloudComputing/CSCE689_Project2/ 
   python2 dupSearch.py
   start java server:
   cd  /home/hduser/CloudComputing/CSCE689_Project2/ImageCounter
   javac  Main.java
   java  Main'''
   
8. Start HTML updater thread:
   'cd  /home/hduser/CloudComputing/CSCE689_Project2/'
   python2 ImageShow.py

9. Start HTML server:
   sudo python -m SimpleHTTPServer 80    
   Password: nimda
   Upload Images for Image counter processing:
   i. Switch to terminal in step 6(python poller)
   Ii. Run following commands:
   'duplicate_search -db reset   
   duplicate_search -db default    
   duplicate_search -show    
   duplicate_search -add /home/hduser/Pictures   //to add images from the directory 
   duplicate_search -add /home/hduser/Pictures1  //to add images from the directory 
   duplicate_search -add hashes_to_output        //to start image-processing and give '           
  
  //images to Java application to process for Image counting

10. From browser go to 
    localhost:90/home/hduser/CloudComputing/CSCE689_Project2
    to view duplicate images 

    For more details instructions refer to section 5.3.1 in report

Refer video for demo of the same : <video>



