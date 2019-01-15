import json
import argparse




if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='diskusage.py is a script that takes a mount point as a parameter and returns a json object containing all of the files on that mount point.')
  parser.add_argument('mount_point', nargs=1, action='store', help='The mount point to scan.', metavar='MOUNT_POINT')
  parser.add_argument('-v' ,'--verbose', action='store_true', help='Enable verbose output.')

  args = parser.parse_args()
  