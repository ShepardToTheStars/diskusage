import json
import argparse
import logging, time
import os

#class Logger: 

class ArgumentParser:
  def Parse(self):
    parser = argparse.ArgumentParser(description='diskusage.py is a script that takes a mount point as a parameter and returns a json object containing all of the files on that mount point.')
    parser.add_argument('mount_point', action='store', help='the mount point to scan', metavar='MOUNT_POINT')
    parser.add_argument('--debug', action='store_true', help='enable debug output') 
    args = parser.parse_args()
    return args

class Validation:
  def ValidateMountPoint(self, path):
    return os.path.ismount(path)

if __name__ == "__main__":
  args = ArgumentParser().Parse()

  if args.debug:
    print("Arguments:", args)

  valid_mount_point = Validation().ValidateMountPoint(args.mount_point)

  if args.debug:
    print("Is Valid Mount Point:", valid_mount_point)