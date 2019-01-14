import unittest

#- Test Cases
#    - Normal Usage
#    x Empty Mountpoint / Directory
#    x Path is a file
#    x Path is a symlink / hardlink / softlink?
#    x Path does not exist
#    - Path is a network location?
#    - No permission
#    - Mount point has another mount point in a child directory

# TODO: Write tests.
# TODO: Organize tests better
class Tests(unittest.TestCase):

    def test_PathIsMountPoint(self):
        # Expected Result: No Error
        self.assertTrue(False)

    def test_PathIsNotMountPoint(self):
        # Expected Result: Error?
        self.assertTrue(False)
        
    def test_PathIsFile(self):
        # Expected Result: Error
        self.assertTrue(False)

    def test_PathIsSymLink(self):
        # Expected Result: Error
        self.assertTrue(False)
        
    def test_PathExists(self):
        # Expected Result: No Error
        self.assertTrue(False)
  
    def test_PathDoesNotExist(self):
        # Expected Result: Error
        self.assertTrue(False)

    def test_EmptyMountPoint(self):
        # Expected Result: No Error, Empty JSON array
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
