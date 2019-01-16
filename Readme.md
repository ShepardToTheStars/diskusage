# Disk Usage Utility

### Description
This utility takes a mount point directory as a parameter and returns the list of files and their sizes (in JSON format) on that specific mount point.

### Requirements
* Python 3

### Usage
```bash
$ diskusage.py [-h] [-i INT] [--debug] MOUNT_POINT
```

* Arguments
  * `MOUNT_POINT` - (REQUIRED) Path to the mount point to scan
* Flags
  * `-h` - Shows usage and help information
  * `-i [INT]` - Prettifies the JSON output and adds indentation equal the the `INT` provided  (Default: None)
  * `--debug` - Enables debug output

### TODO
* Write tests
* Additional parameter validation
* Finalize make file
* Document dependencies

### Other Ideas
* Performance Improvements
  * Multi-Threading
  * Process Priority Argument?
  * 
