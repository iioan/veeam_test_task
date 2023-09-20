import os
import time
import sys

sync_complete = "Synchronization process complete! Exiting..."


def printConsoleLog(text):
    print(text)
    fi = open(log_path, "a")
    fi.write(text + "\n")


def sync():
    walk1 = os.walk(source_path)
    walk2 = os.walk(target_path)
    for (rootSrc, directoriesSrc, filesSrc), (rootTgt, directoriesTgt, filesTgt) in zip(walk1, walk2):
        for fileSrc in filesSrc:
            if fileSrc in filesTgt:
                pathSrc = os.path.join(rootSrc, fileSrc)
                pathTgt = os.path.join(rootTgt, fileSrc)
                # check if file has been modified
                if os.path.getmtime(pathSrc) > os.path.getmtime(pathTgt):
                    printConsoleLog("File " + pathSrc + " was modified")
                    os.remove(pathTgt)
                    command = f'copy "{pathSrc}" "{pathTgt}"'
                    os.system(command)
            else:
                # check if file has been created in source
                pathSrc = os.path.join(rootSrc, fileSrc)
                pathTgt = os.path.join(rootTgt, fileSrc)
                printConsoleLog("File " + pathSrc + " was created")
                command = f'copy "{pathSrc}" "{pathTgt}"'
                os.system(command)

        # check if file has been deleted in source
        for fileTgt in filesTgt:
            if fileTgt not in filesSrc:
                pathTgt = os.path.join(rootTgt, fileTgt)
                printConsoleLog("File " + pathTgt + " was deleted")
                os.remove(pathTgt)

        # check if directory has been created in source
        for directorySrc in directoriesSrc:
            if directorySrc not in directoriesTgt:
                pathSrc = os.path.join(rootSrc, directorySrc)
                pathTgt = os.path.join(rootTgt, directorySrc)
                printConsoleLog("Directory " + pathSrc + " was created")
                command = f'xcopy "{pathSrc}" "{pathTgt}" /E /I /H /K'
                os.system(command)

        # check if directory has been deleted in source
        for directoryTgt in directoriesTgt:
            if directoryTgt not in directoriesSrc:
                pathSrc = os.path.join(rootSrc, directoryTgt)
                pathTgt = os.path.join(rootTgt, directoryTgt)
                print(pathTgt)
                printConsoleLog("Directory " + pathSrc + " was deleted")
                command = f'rmdir "{pathTgt}" /S /Q'
                os.system(command)


if len(sys.argv) != 5:
    print("Usage: python3 main.py <path-to-source> <path-to-target> <sync-interval> <path-to-log>")
    sys.exit(1)

source_path = sys.argv[1]
target_path = sys.argv[2]

try:
    synchronize_time = int(sys.argv[3])
    if synchronize_time < 0:
        raise ValueError("Sync interval must be a positive integer.")
except ValueError:
    print("Sync interval is not a valid positive integer.")
    sys.exit(1)

log_path = sys.argv[4]

# these should come from input
print("Source Path:", source_path)
print("Target Path:", target_path)
print("Sync Interval:", synchronize_time)
print("Log Path:", log_path)

# check if the paths are valid, if not create them
if not os.path.isdir(source_path):
    os.makedirs(source_path)
if not os.path.isdir(target_path):
    os.makedirs(target_path)

# create the log file
if not os.path.isfile(log_path):
    open(log_path, "w").close()

# synchronization process
try:
    while True:
        sync()
        time.sleep(synchronize_time)
except KeyboardInterrupt:
    printConsoleLog(sync_complete)
