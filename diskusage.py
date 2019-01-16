import json
import argparse
import logging, time
import os

class DiskUsage:
  def __init__(self, logLevel=logging.ERROR):
    logFormat = '%(asctime)s %(name)s %(levelname)s %(message)s'
    logging.basicConfig(level=logLevel, format=logFormat)
    self.logger = logging.getLogger(__name__)
    

  def GetDiskUsage(self, mountPointDirectory):
    self.logger.debug("Mount Point Path: %s", mountPointDirectory)
    isValidMountPoint = Validation.IsMountPoint(mountPointDirectory)
    self.logger.debug("Path Is Valid Mount Point: %s", isValidMountPoint)
    
    if not isValidMountPoint:
      self.logger.error("The path '%s' is not a valid mount point.", mountPointDirectory)
      # Maybe throw something instead?
      exit(1)
    else:
      outputObject = DiskUsageOutput()
      outputObject.Extend(self.ScanDirectoryContents(mountPointDirectory, True))
    return outputObject

         
  def ScanDirectoryContents(self, path, skipMountPointValidationCheck=False):
    if skipMountPointValidationCheck: self.logger.debug("  skipMountPointValidationCheck: %s", skipMountPointValidationCheck)
    fileList = []
    rootFiles = os.scandir(path)
    for node in rootFiles:
      # If its a direcory that isn't a symlink, we want to recursively check into those directories and get
      # their files. We also want to check if its another mount point and skip it if it is.
      # Note: The only time we would want to skip the validation check is for the root mount point node.
      if node.is_dir() and not node.is_symlink():
        if not Validation.IsMountPoint(node.path) or skipMountPointValidationCheck:
          self.logger.debug("Scanning Path: %s", path)
          fileList.extend(self.ScanDirectoryContents(node.path))
        else:
          self.logger.debug("Skipping scan of mount point: %s", mountPointDirectory)
      
      # Otherwise, if its a file, add it to the list!
      elif node.is_file() and not node.is_symlink():
        fileInfo = DiskUsageFile(node.path, node.stat().st_size)
        fileList.append(fileInfo)
      
    return fileList

class ArgumentParser:
  @staticmethod
  def Parse():
    parser = argparse.ArgumentParser(description='diskusage.py is a script that takes a mount point as a parameter and returns a json object containing all of the files on that mount point.')
    parser.add_argument('mount_point', action='store', help='the mount point to scan', metavar='MOUNT_POINT')
    parser.add_argument('--debug', action='store_true', help='enable debug output') 
    args = parser.parse_args()
    return args

class Validation:
  @staticmethod
  def IsMountPoint(path):
    return os.path.ismount(path)

class DiskUsageOutput():
  def __init__(self):
    self.files = []

  def Append(self, path, size):
    self.files.append(DiskUsageFile(path, size))

  def Extend(self, list):
    self.files.extend(list)

  def ToJson(self, indent=None):
    return json.dumps(self, cls=CustomJsonEncoder, indent=indent)

class DiskUsageFile:
  def __init__(self, path, size):
     self.path = path
     self.size = size

class CustomJsonEncoder(json.JSONEncoder):
  def default(self, o):
    return o.__dict__

if __name__ == '__main__':
  # We'll want to parse the arguments first, so we can get if the logger needs to be set to debug or not.
  args = ArgumentParser.Parse()

  # Create the logger for errors and/or debugging.
  logLevel = logging.ERROR
  if args.debug: logLevel = logging.DEBUG

  diskUsageUtil = DiskUsage(logLevel)
  outputObject = diskUsageUtil.GetDiskUsage(args.mount_point)
  print(outputObject.ToJson())