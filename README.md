# Log Rotation in Python
An enterprise grade log rotation solution so that the log files do not fill up all the space on the file system.

The code implements log ration in Python based on time or size of the log files such that old log contents are not deleted from existing log files. The existing log is moved to a new log, compressed, and the new logs are continuously written to the original log file. A simple cron job is used to move the compressed files to another location to free up space. 

## Time based Log Rotation
To implement time based log rotation, I used `TimedRotatingFileHandler` class implemented in Python which allows us to specify the log file name, the type of time interval, its value and the number of maximum backup log files.
