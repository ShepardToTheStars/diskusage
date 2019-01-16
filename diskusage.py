import json
import argparse
import logging, time
import os

class DiskUsage:
  @staticmethod
  def Main():
    # We'll want to parse the arguments first, so we can get if the logger needs to be set to debug or not.
    args = ArgumentParser.Parse()
    mountPointDirectory = args.mount_point

    # Create the logger for errors and/or debugging.
    logLevel = logging.ERROR
    if args.debug: logLevel = logging.DEBUG

    logFormat = '%(asctime)s %(name)s %(levelname)s %(message)s'
    logging.basicConfig(level=logLevel, format=logFormat)
    logger = logging.getLogger(__name__)
    
    logger.debug("Arguments: %s", args)

    isValidMountPoint = Validation.IsMountPoint(mountPointDirectory)
    logger.debug("Is Valid Mount Point: %s", isValidMountPoint)
    
    if not isValidMountPoint:
      logger.error("The path '%s' is not a valid mount point.", mountPointDirectory)
      exit(1)
    else:
      fileArray = []
      rootFiles = os.scandir(mountPointDirectory)
      for node in rootFiles:
        if node.is_dir() and not node.is_symlink():
          if (not Validation.IsMountPoint(node.path)):
            logger.debug("%s,recurse!", node.path)

        elif node.is_file() and not node.is_symlink():
          logger.debug("%s,%s", node.path, node.stat().st_size)
         

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

if __name__ == '__main__':
  DiskUsage.Main()

