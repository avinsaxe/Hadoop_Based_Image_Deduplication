import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

class Main{
	static long lastUpdateTimeStamp = -1; //last update time stamp of new_data.txt
    final static long POLLING_INTERVAL = 3 * 1000; //30 sec
    final static String NEW_DATA_FILE = "new_data.txt"; //file where application would add data to be processsed
    final static String HADOOP_DATA_FILE = "my_hadoop_data_file.txt";
    final static String FILE_LIST[] = {"file0", "file1", "file2"};
    final static String HADOOP_BASH_SCRIPT_FILENAME = "execute-wordcount.sh"; //filename of hadoop bash script to be run to execute hadoop process
    
    public static void main(String args[]){
    	createNewDataFile(NEW_DATA_FILE);
    	//updateNewDataFileTimeStamp(); //lets update local timestamp of new data file
    	poll(); //lets start polling
    }

    /**
     * method to poll data in input file
     * If timestamp of NEW_DATA_FILE is updated the function starts hadoop processing.
     */
    static void poll() {
    	System.out.println("Server is polling now...");
    	File newDataFile = new File(NEW_DATA_FILE);
    	while(true) {
		//System.out.println("Polling "+newDataFile.lastModified()+" and "+lastUpdateTimeStamp);
    		//check if timestamp of new_data.txt is updated. If yes! well fresh to brew! Let's do it!
		long update_timestamp=newDataFile.lastModified();
    		if(update_timestamp > lastUpdateTimeStamp) {
			    System.out.println("We have new data, invoking hadoop to process it...");
    			runHadoop();
			    lastUpdateTimeStamp=update_timestamp;
    			//updateNewDataFileTimeStamp();
    		}
    		
    		try{Thread.sleep(POLLING_INTERVAL);}catch(InterruptedException e){}  
    	}
    }
    
    /**
     * Function runs WordCount hadoop script
     */
    public static void runHadoop() {
    	
    	deleteFileIfExists(HADOOP_DATA_FILE); //delete hadoop data file, if it exists
    	//createNewDataFile(HADOOP_DATA_FILE); //create hadoop data file
    	copyFile(new File(NEW_DATA_FILE), new File(HADOOP_DATA_FILE)); //lets copy data from new_data.txt to hadoop_data.txt
    	
    	//All set! Let's set the ball rolling!
    	runBashScript();
    	System.out.println("Completed Hadoop process\n");
    }
    
    static void runBashScript() {
    	String[] cmd = new String[]{"/bin/sh", HADOOP_BASH_SCRIPT_FILENAME};
    	try {
    	    Process pr = Runtime.getRuntime().exec(cmd);
			pr.waitFor();
		} catch (IOException | InterruptedException e) {
		}
    }
    
    private static void copyFile(File source, File dest){
        try {
			Files.copy(source.toPath(), dest.toPath());
		} catch (IOException e) {}
    }
    
    static void deleteFileIfExists(String path) {
    	try {
			Files.deleteIfExists(Paths.get(path));
		} catch (IOException e) {
		}
    }
    
    /**
     * Check is file new_data.txt exists, if not create it and send creation response
     * @return
     */
    public static boolean createNewDataFile(String filename) {
    	File file = new File(filename);
    	if (!file.exists()) {
			try {
				return file.createNewFile();
			} catch (IOException e) {
				return false;
			}
    	}
    	return true;
    }
    
    /**
     * In the event of new data read or file creation timestamp is updated
     */
    public static void updateNewDataFileTimeStamp() {
    	lastUpdateTimeStamp = new File(NEW_DATA_FILE).lastModified();
    }
}
