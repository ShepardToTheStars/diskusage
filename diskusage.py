import json
import argparse
import logging
import time
import os
import sys

class DiskUsage:
  """
  Class that contains the main logic behind the diskusage utility.
  """
  def __init__(self, logLevel=logging.WARNING):
    # TODO: Validate logLevel
    # Basically just sets up the logger for the error/debug output
    # The logger will not interfere with the standard output of the utility
    logFormat = '%(asctime)s %(levelname)s | %(message)s'
    logging.basicConfig(level=logLevel, format=logFormat)
    self.logger = logging.getLogger(__name__)
  
  def getDiskUsage(self, mountPointDirectory):
    """
    The 'main' function of the diskusage utility. This method will take a path, validate that
    it is a mount point, and then initiate a recursive scan of that mount point. 

    Returns a DiskUsageOutput object which can be either accessed normally or output as JSON
    using the toJson method.
    """
    self.logger.debug("Mount Point Path: %s", mountPointDirectory)
    isValidMountPoint = self.isMountPoint(mountPointDirectory)
    self.logger.debug("Path Is Valid Mount Point: %s", isValidMountPoint)
    
    if not isValidMountPoint:
      raise ValueError("The path '%s' is not a valid mount point." % mountPointDirectory)
    else:
      outputObject = DiskUsageOutput()
      outputObject.extend(self.scanDirectoryContents(mountPointDirectory, True))
    return outputObject

  def scanDirectoryContents(self, path, skipMountPointValidationCheck=False):
    """
    Function that takes a directory path and adds file info for that directory to a list. It will also recursively
    scans any child directories. Any symbolic links are not followed, because of the following reasons:
    - Any symbolic links to directories or files on the current file system will be scanned eventually. We don't want
      to "double count" a single file twice because of a symbolic link.
    - Any symbolic links to directories or files on the *different* mounted file system should not be counted as they are
      not part of the current scan.

    Returns a list of DiskUsageFile objects.
    """
    fileList = []

    # We want to check if its a different mount point and if it is, skip it and return an empty list.
    if self.isMountPoint(path) is True and skipMountPointValidationCheck is False:
      self.logger.debug("Skipping scan of mount point: %s", path)
      return fileList

    self.logger.debug("Scanning Path: %s", path)
    if skipMountPointValidationCheck: 
      self.logger.debug("  skipMountPointValidationCheck: %s", skipMountPointValidationCheck)
    
    rootFiles = os.scandir(path)
    for node in rootFiles:
      try:
        # If the node is a symlink, skip it.
        if node.is_symlink():
          pass

        # If its a direcory that isn't a symlink, we want to recursively check into those directories and get
        # their files.
        elif node.is_dir():
          fileList.extend(self.scanDirectoryContents(node.path, False))

        # Otherwise, if its a file, add it to the list!
        elif node.is_file():
          fileInfo = DiskUsageFile(node.path, node.stat().st_size)
          fileList.append(fileInfo)
      except PermissionError as ex:
        # Permission errors will happen so lets just output them as a warning. This may want to be a configurable
        # thing eventually, but for now, let's just spit out a warning.
        self.logger.warning("Permission Denied: %s", node.path)
    return fileList

  @staticmethod
  def isMountPoint(path):
    """
    True if the path specified is a mount point, otherwise, false.
    """
    return os.path.ismount(path)

class ArgumentParser:
  """
  Container class that contains all of the CLI argument declaration and parsing.
  """
  @staticmethod
  def parse():
    parser = argparse.ArgumentParser(description='diskusage.py is a script that takes a mount point as a parameter and returns a json object containing all of the files on that mount point.')
    parser.add_argument('mount_point', action='store', help='the mount point to scan', metavar='MOUNT_POINT')
    parser.add_argument('-i','--indent', action='store', default=None, type=int, help='if specified, json will be indented by the number specified', metavar='INT') 
    parser.add_argument('--debug', action='store_true', help='enable debug output') 
    args = parser.parse_args()
    return args
  
  @staticmethod
  def validate(args):
    """
    Function that validates the arguments values.
    """
    if args.indent is not None and args.indent < 0:
      raise ValueError("The indentation argument cannot be negative.")
    
class DiskUsageOutput():
  """
   A basic storage class that contains a list of DiskUsageFile objects as well
   as some functions to manipulate that list and serialize the object as JSON. 
  """
  def __init__(self):
    self.files = []

  def append(self, path, size):
    """
    Wrapper function that creates and appends a new DiskUsageOutput object to the internal list
    from the specified path and size.
    """
    # TODO: validate params
    self.files.append(DiskUsageFile(path, size))

  def extend(self, list):
    """
    Wrapper function that appends the specified existing DiskUsageOutput list to the internal list.
    """
    # TODO: validate params
    self.files.extend(list)

  def toJson(self, indent=None):
    """
    Serializes the current object and any complex child objects into a JSON representation. The custom
    encoder used will just print the internal properties of the class. By default, there is no indentation
    but that can be specified if we want the JSON to be more readable.
    """
    # TODO: validate params
    return json.dumps(self, cls=CustomJsonEncoder, indent=indent)

class DiskUsageFile:
  """
  A basic storage class that holds the file path size.
  """
  def __init__(self, path, size):
     # TODO: validate params
     self.path = path
     self.size = size

class CustomJsonEncoder(json.JSONEncoder):
  """
  Contains the custom Json Encoder to encode complex python objects that would usually throw a TypeError
  """
  def default(self, o):
    return o.__dict__

if __name__ == '__main__':
  rc = 1
  try:
    args = ArgumentParser.parse()
    # We'll want to parse the arguments first, so we can get if the logger needs to be set to debug or not.
    args = ArgumentParser.parse()

    # Create the logger for errors and/or debugging.
    logLevel = logging.WARNING
    if args.debug: logLevel = logging.DEBUG

    diskUsageUtil = DiskUsage(logLevel)
    outputObject = diskUsageUtil.getDiskUsage(args.mount_point)
    print(outputObject.toJson(args.indent))      

    rc = 0
  except Exception as ex:
    print('Error: %s' % ex, file=sys.stderr)
  sys.exit(rc)


 