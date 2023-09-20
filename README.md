### Veeam Test Task
### Description

The scope of the task is synchronization of two directories: source and replica. It checks for modifications, additions,
and deletions in a source directory and mirrors these changes in a target directory. The synchronization process runs in
a loop, and you can specify the synchronization interval and log file location as command-line arguments.

### Command Line Arguments

The program accepts the following command-line arguments:
1. <path-to-source>: The path to the source directory.
2. <path-to-target>: The path to the target directory.
3. <sync-interval>: The synchronization interval in seconds (a positive integer).
4. <path-to-log>: The path to the log file.

Example of running the script:
``` 
python3 main.py ./source ./replica 1 ./log.txt
```

### Algorithm
With the help of the `os.walk` function, I look through directories and their contents in both the source and target 
directories. The `zip` function is for pairing the corresponding source and target directory structures together so that
I can iterate over them simultaneously. Inside the sync() function, I have access to the roots, directories, and files. 
I compare the contents of the source and target directories and perform the necessary actions to synchronize them.

Firstly, I check if the source directory contains a file that is part of the target directory. If it does, then I check
if the file has been modified. If it has, then I update the file in the target directory. If it hasn't, then I do nothing.
If the source directory contains a file that is not part of the target directory, then I copy the file to the target
directory. 
If the target directory contains a file that is not part of the source directory, then I delete the file from the target
directory.

Secondly, I check if the source directory contains a directory that does not exist in the target directory. If it does,
then I create the directory in the target directory. 
If the target directory contains a directory that does not exist in the source directory, then I delete the directory
from the target directory.

When I rename a file or directory in the source directory, I rename the corresponding file or directory in the target and
the algorithm will recreate the file (with the new name) and delete the file (with the old name) from the target directory.
It is the same case for the renaming of directories.

To stop the synchronization process gracefully, press Ctrl+C in the terminal. The script will catch the KeyboardInterrupt 
and exit, logging a message to the specified log file.
