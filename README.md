# Log Rotation in Python
An enterprise grade log rotation solution so that the log files do not fill up all the space on the file system.

The code implements log ration in Python based on time or size of the log files such that old log contents are not deleted from existing log files. The existing log is moved to a new log, compressed, and the new logs are continuously written to the original log file. A simple cron job is used to move the compressed files to another location to free up space. 

## Time based Log Rotation
To implement time based log rotation, I used `TimedRotatingFileHandler` class implemented in Python which allows us to specify the log file name, the type of time interval, its value and the number of maximum backup log files. 

The code in `time_based_log_rotation.py` sets the format and level of logging records and rotates the log files every `30 seconds` while keeping at most `5` backup files. Whenever a new log file is created, it is named exactly as the original log file concatenated with the local date and time. The file is then compressed using `zlib` module available in python. The code also has a simple loop that keeps on writing to the log file. 

## Size based Log Rotation
To implement size based log rotation, I used `RotatingFileHandler` class implemented in Python which allows us to specify the log file name, maximum number of bytes in the log file and the number of maximum backup log files. 

The code in `size_based_log_rotation.py` sets the format and level of logging records and rotates the log files whenever their size exceeds `250` bytes while keeping at most `5` backup files. Whenever a new log file is created, it is named exactly as the original log file concatenated with the local date and time. The file is then compressed using `zlib` module available in python. The code also has a simple loop that keeps on writing to the log file. 
