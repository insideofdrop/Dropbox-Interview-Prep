"""
This question is usually used in a phone screen. 

The sky is divided into a big grid and we are snapping pictures of the grid pieces.
Each image has a row number and a column number corresponding to its place in the grid.
We want to save the images to a disk, and read them too!
Assume each piece of data is 1 MB. 
Write an API to do this.
"""

"""
We also want to have constant-time access to the last file we saved. If we haven't saved all the files yet,
then just return any file that we haven't saved. Assume the sky is 1000 x 1000.
"""

class SpacePanorama:

    def __init__(self):
        self.ordered_files = collections.OrderedDict((row, col) for row in range(1000) for col in range(1000))
        #Yes, it takes R * C time to instantiate.
        #Also know that this is an LRU cache, and that an LRU cache is a hashmap that maps into a deque

    def write(self, image_data, row, col):
        try:
            with open(f"{row}_{col}.png", "wb") as file_object:
                file_object.write(image_data)
            #Remove the item from the ordered files, then set it again so that it's at the head
            del self.ordered_files[(row, col)] 
            self.ordered_files[(row, col)] = None #The value that we assign doesn't matter
        except Exception as exc:
            raise UnableToWriteImageException(exc)
    
    def read(self, row, col):
        if not os.path.exists(f"{row}_{col}.png"):
            raise FileDoesNotExistError(f"No image at {row}, {col}")
        with open(f"{row}_{col}.png", "rb") as file_object:
            return file_object.read() #You can read the whole thing because it's 1 MB

    def get_last_updated_image:
        return self.ordered_files.tail() #This isn't an actual method. Your interviewer might
        #Ask you to implement the LRU cache. Just know that you have constant time access to the tail.
"""
Now suppose that we have expanded the size to be 1,000,000 x 1,000,000. What do we do about saving the pictures?

Answer: Use a pool of disks. Have 1000 x 1000 disks so that each disk is assigned to a row.
Then when you get a query to save or retrieve an image in that row, you immediately go to the correct disk.ArithmeticError

What about last updated image?

Answer: Set up another LRU cache for the disks. This will update the disk LRU cache each time you update a disk.
Then within each disk, you have an LRU cache for the last updated image on the disk. 
So the answer is disk_LRU_cache.get_tail().get_tail()
"""