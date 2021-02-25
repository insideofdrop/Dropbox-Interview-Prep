"""
Dropbox

Usually a phone screen question.

Folder Access:
Given child-parent folder relationships, the user has access to folders in the access set. 
If the user has access to a parent, then the user has access to all the children too.
Find whether the user has access to a particular folder.
/A
|____/B
   |___ /C <-- access
   |___ /D
|____/E <-- access
   |___ /F 
|___/G
folders = [
('A', None), 
('B', 'A'),
('C', 'B'),
('D', 'B'),
('E', 'A'), 
('F', 'E')
]
access = ['C', 'E']
has_access(String folder_name) -> boolean has_access("B") -> false
has_access("C") -> true

What if the child folder has children? Is this a transitive relationship?
Can a folder has more than one parent? If so, how is it represented? 
Would it be possible a circular child-parent relationship? (Not really unless you have sym links)

Tradeoff: The following is a top-down approach which looks down the tree and gives permissions
to all children folders.
You might not have transitive relationships. You also might want to consider a bottom-up approach
where search is O(h) (height of the folder tree), but space is O(A) (# folders you initially have access to)
"""

class FolderAccess:

    def __init__(self, folder_to_parent, access):
        #folder_to_parent is a list (child folder, parent folder)
        #access is a set of folders that you have access to
        self.parent_to_childen = collections.defaultdict(list)
        self.access = access
        for child, parent in folder_to_parent:
            self.parent_to_childen[parent].append(child)
        self.process_folders()

    def process_folders(self):
        """Grants access to all children, allows for constant time access lookup, breadth-first"""
        current_access = set(self.access)
        while current_access:
            next_access = set()
            for file in current_access:
                children = self.parent_to_childen.get(file, None)
                if children is not None:
                    for child in children:
                        if child not in self.access:
                            next_access.add(child)
            self.access.update(next_access)
            current_access = next_access

    def has_access(self, folder_name):
        return folder_name in self.access


"""
folder_access_obj = FolderAccess(folder_to_parent, access_list)
print(folder.has_access("A"))
...
"""