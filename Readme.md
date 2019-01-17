# Disk Usage Utility

### Description
This utility takes a mount point directory as a parameter and returns the list of files and their sizes (in JSON format) on that specific mount point.

### Requirements
* Python 3.6+

### Usage
```bash
$ python3 diskusage.py [-h] [-i INT] [--debug] MOUNT_POINT
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

### Other Improvements
* Formal packaging using `setuptools`
* More virtualized and isolated environment (using [venv](https://docs.python.org/3/library/venv.html#an-example-of-extending-envbuilder))
* Multi-Threading support
* Process priority argument
* Improved Tests (using [pyfakefs](https://pypi.org/project/pyfakefs/))