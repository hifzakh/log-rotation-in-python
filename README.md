# Log Rotation in Python
An enterprise grade log rotation solution so that the log files do not fill up all the space on the file system.

The code implements log rotation in Python based on time or size of the log files such that old log contents are not deleted from existing log files but are moved to a new log file which is compressed. The new logs are continuously written to the original log file. A simple cron job is used to move the compressed files to another location to free up space. 

## Time based Log Rotation
To implement time based log rotation, I used `TimedRotatingFileHandler` class implemented in Python which allows us to specify the log file name, the type of time interval, its value and the number of maximum backup log files. 

The code in `time_based_log_rotation.py` sets the format and level of logging records and rotates the log files every `30 seconds` while keeping at most `5` backup files. Whenever a new log file is created, it is named exactly as the original log file concatenated with the local date and time. The file is then compressed using `zlib` module available in python. The code also has a simple loop that writes to the log file. 

## Size based Log Rotation
To implement size based log rotation, I used `RotatingFileHandler` class implemented in Python which allows us to specify the log file name, maximum number of bytes in the log file and the number of maximum backup log files. 

The code in `size_based_log_rotation.py` sets the format and level of logging records and rotates the log files whenever their size exceeds `250` bytes while keeping at most `5` backup files. Whenever a new log file is created, it is named exactly as the original log file concatenated with the local date and time. The file is then compressed using `zlib` module available in python. The code also has a simple loop that writes to the log file. 

## Cron job to move compressed files
To move compressed files from the `home` directory to `tmp` directory, add the following code to `/usr/local/bin/movelogs.sh/`

```
#!/bin/bash
PATH=/opt/ros/kinetic/bin:/home/hifzakhalid/bin:/home/hifzakhalid/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/local/bin/movelogs.sh
sDirectory="/home/hifzakhalid/logs"
sLogs="/tmp/logs"
find $sDirectory -type f -maxdepth 1 -name "*.gz" -exec mv {} $sLogs \;
```
