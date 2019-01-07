# Log Rotation in Python
It is an enterprise grade log rotation solution so that the log files do not fill up all the space on the file system.

The code implements log rotation in Python based on time or size of the log files such that old log contents are not deleted from existing log files but are moved to a new log file which is then compressed. The new logs are continuously written to the original log file. A simple cron job is used to move the compressed files to another location to free up space. 

## Time based Log Rotation
To implement time based log rotation, I used `TimedRotatingFileHandler` class implemented in Python which allows us to specify the log file name, the type of time interval, its value and the number of maximum backup log files. 

The code in `time_based_log_rotation.py` sets the format and level of logging records and rotates the log files every `30 seconds` while keeping at most `5` backup files. Whenever a new log file is created, it is named exactly as the original log file concatenated with the local date and time. The file is then compressed using `zlib` module available in python. The code also has a simple loop that writes to the log file. 

## Size based Log Rotation
To implement size based log rotation, I used `RotatingFileHandler` class implemented in Python which allows us to specify the log file name, maximum number of bytes in the log file and the number of maximum backup log files. 

The code in `size_based_log_rotation.py` sets the format and level of logging records and rotates the log files whenever their size equals to or exceeds `250` bytes while keeping at most `5` backup files. Whenever a new log file is created, it is named exactly as the original log file concatenated with the number of backup file. The file is then compressed using `zlib` module available in python. The code also has a simple loop that writes to the log file. 

## Cron job to move compressed files
To move compressed files from the `home` directory to `tmp` directory, add the following code to `/usr/local/bin/movelogs.sh/` and modify the permissions of the file to make it executable.

```
#!/bin/bash
sDirectory="/home/username/logs"
sLogs="/tmp/logs"
find $sDirectory -type f -maxdepth 1 -name "*.gz" -exec mv {} $sLogs \;
```

The first line sets bash as our shell for the script from within the script itself. The rest of the code finds all the files with the extension `.gz` in `sDirectory` till the maximum depth of `1` i.e. it does not look for the files in subfolders, and then moves all the found files to `sLogs`.

To run the above script after specific time intervals regularly, we need to add the following command to `crontab` file.

```
0,10,20,30,40,50 * * * * /usr/local/bin/movemedia.sh >> /var/log/movelogs.log 2>&1
```

The above command runs the `/usr/local/bin/movelogs.sh` script after every `5` minutes. The output for the script is written in `/var/log/movelogs.log` and `2>&1` is used to redirect both `stdout` and `stderr` to the same place i.e. `/var/log/movelogs.log`.

To add the above command to `crontab` file, open your `crontab` file in editing mode by typing in `crontab -e` in terminal, add the above command at the end of that file and save it. After adding the above command, type `sudo service cron reload` to reload configuration files for periodic command scheduler cron.

Since we are using Linux therefore we want to rotate the `/var/log/movelogs.log` file each day by creating a file: `/etc/logrotate.d/movelogs` containing:

```
rotate 5
daily
size 30K
missingok
```

The above configuration of the `/etc/logrotate.d/movelogs` file specifies the maximum number of rotated files that will be kept, the frequency of rotation, the maximum size of the log file and that if there is no log file then it ok.

## Test your Implementation

### Case 1

Test your implementation for the simplest case where your process does not generate any logs i.e. the log file is empty, no compressed files are formed and the cron job has no files to move. To test this case, run `size_based_test_1.py` and `time_based_test_1.py` files separately. While running the above files, see if the original log file remains empty and no compressed files are generated.

### Case 2

Test your implementation for the case where your process does generate logs such that at most `5` backup files are generated (you can change the number as needed). While running the `size_based_test_2.py` and `time_based_test_2.py` files, check if new log file is generated after every `1 minute` or when the file size is equal to `250 bytes` respectively. At most `5` backup log files should be there in both the cases. To see the content of the compressed log files, use the following command: 

```
zlib-flate -uncompress < filename.gz
```

Match the content of the original log file and check the timestamps to see if the original log file contains the new messages and the compressed files contain the old ones. After every `10 minutes`, check if the backup log files with `.gz` extension have been moved to `/tmp/logs`. You can also change the `crontab` command such that the files with `.gz` extension are moved every minute by adding `* * * * * /usr/local/bin/movemedia.sh >> /var/log/movelogs.log 2>&1` to the `crontab` file.


