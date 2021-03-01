"""
Dropbox

Duplicate Files

https://leetcode.com/problems/find-duplicate-file-in-system/

Given a file system, return a list of collections of duplicate files. 

Ask about:
Symbolic link, same file/dir with diff name, cannot detect cycle by visited...cycle?
-use absolute path/ skip symbolic link (if we search the whole file system)

What about invalid or malformed files e.g. permission or cannot read
-compare file by hashing (MD5, SHA)

If dir depth is large: DFS might stack overflow, use BFS; the variable to store pathname might overflow.
-Most memory consuming: MD5, read in files etc

What about race conditions, like if someone is writing the file while you are reading etc

What if the process takes a long time? 
-If error / hanging up in between: checkpoints, save states from time to time
"""

class DuplicateFiles:
    mb = 1024 * 1024

    def __init__(self, root):
        self.result = []
        self.size_to_files = {}
        self.root = root

    def get_hash(self, file):
        """Returns the SHA 256 hash of the file"""
        output_hash = hashlib.sha256()
        with open(file, "rb") as file_obj:
            mb_chunk = file_obj.read(mb)
            if mb_chunk is not None:
                output_hash.update(mb_chunk)
            else:
                break
        return output_hash.hexdigest()
    
    def add_file(self, file):
        if file.file_size in self.size_to_files:
            self.size_to_files[file.file_size].append(file)
        else:
            self.size_to_files[file.file_size] = [file]

    def group_files_by_size(self):
        """Populates self.size_to_files with the sizes and the files with those sizes"""
        queue = collections.deque()
        queue.appendleft(self.root)
        seen = set()
        while queue:
            current_folder = queue.pop()
            seen.add(current_folder)
            for content in current_folder.iter_dir(): #iterdir is the contents of the file, both files and folders
                if content.is_directory() and content not in seen:
                    queue.appendleft(content)
                    seen.add(content)
                elif content.is_file():
                    self.add_file(content)
                else:
                    #Ask the interviewer how to handle symlinks or special cases
                    pass

    def process_files(self):
        """Returns list of collections of duplicate files"""
        #First, group the files by size
        self.group_files_by_size()

        #Now you have the files grouped by size
        #For the sizes with more than one file, you need to deduplicate
        result = []
        for size, files in self.size_to_files.items():
            if len(files) > 1:
                hash_groups = {} #Map <hash: str, files with that hash: List[File]>
                for file in files:
                    file_hash = self.get_hash(file)
                    if file_hash in hash_groups:
                        hash_groups[file_hash].append(file)
                    else:
                        hash_groups[file_hash] = [file]
                for list_of_files in hash_groups.values():
                    if len(list_of_files) > 0:
                        result.append(list_of_files)
        return result

#Then call `duplicate_files = DuplicateFiles(root)` and `return duplicate_files.process()`
