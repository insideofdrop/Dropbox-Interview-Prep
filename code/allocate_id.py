"""
Dropbox

Id Allocator / Number / Phone Number

Write a class for an id allocator that can allocate and release ids
"""

class Allocator:

    def __init__(self, max_val):
        self.queue = collections.deque()
        self.first_pass_idx = 0 #your interview might not require this optimization
        self.allocated = set()
        self.max_val = max_val
        
    def allocate(self):
        """Returns an unallocated id"""
        result = None
        if self.first_pass_idx <= self.max_val:
            self.first_pass_idx += 1
            result = self.first_pass_idx - 1
        elif len(self.queue) > 0:
            result = self.queue.pop()
        if result is not None:
            self.allocated.add(result)
            return result
        else:
            raise CannotAllocateException("No ids available")

    def release(self, id):
        """Releases the id and allows it to be allocated"""
        if (not 0 <= id < self.max_val) or (id not in self.allocated):
            #You should say that you'd like to throw an exception in case of an error
            raise InvalidIdException(f"The id {id} cannot be released.")
        self.allocated.remove(id)
        self.queue.appendleft(id)

"""
FOLLOW UP:
You might be asked to estimate the amount of memory you need for the above implementation.
You will be asked to make a more space-efficient implementation in which allocate and release might take longer than O(1).
For this, you can use a boolean array (a.k.a. a BitSet in Java, a bit-vector in other languages)
This uses max_id // (8 * 1024 * 1024) MB
"""

class SpaceEfficientAllocator:

    def __init__(self, max_val):
        self.max_val = max_val
        self.bool_array = [False] * max_val

    def allocate(self):
        """Returns an unallocated id"""
        for id, value in enumerate(self.bool_array):
            if value == False: #The id has not been allocated
                self.bool_array[id] = True
                return id
        raise CannotAllocateException("No ids available")

    def release(self, id):
        """Releases the id and allows it to be allocated"""
        if (not 0 <= id < self.max_val) or (self.bool_array[id] == True):
            raise Exception(f"The id {id} cannot be released.")
        self.bool_array[id] = False

"""
FOLLOW UP:
This is the part where most people flunk. Come up with a way that is a little faster than O(n) for both allocate and release.
You can use a bit more space.

The hard way is to use an interval tree or a segment tree.
The easy way is to use a binary heap.
"""

class BinaryHeapAllocator:

    def __init__(self, max_val):
        self.max_val = max_val
        self.bool_array = [False] * (2 * max_val)

    def allocate(self):
        """Returns an unallocated id"""
        index = 0
        if self.bool_array[index] == True:
            raise CannotAllocateException("No ids available")
        while index < max_val:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            if self.bool_array[left_child_index] == False: #There's an unallocated id in the subtree
                index = left_child_index
            elif self.bool_array[right_child_index] == False: #... in the right subtree
                index = right_child_index
            else: #Both subtrees are allocated, this actually means you broke your tree
                raise CannotAllocateException("No ids available")
        id = self.get_id_from_index(index)
        self.update_tree(id)
        

    def release(self, id):
        """Releases the id and allows it to be allocated"""
        if (not 0 <= id < self.max_val) or (self.bool_array[id] == True):
            raise Exception(f"The id {id} cannot be released.")
        self.bool_array[id] = False
        self.update_tree(id)
    
    def get_index_from_id(self, id):
        return id + self.max_val - 1
    
    def get_id_from_index(self, index):
        return index - self.max_val + 1
    
    def update_tree(self, id):
        index = self.get_index_from_id(id)
        while index > 0:
            parent_index = (index - 1) // 2
            both_children_are_true = False
            if index % 2 == 1: #this is a left child
                if self.bool_array[index] == True == self.bool_array[index + 1]:
                    both_children_are_true = True
            else: #this is a right child
                if self.bool_array[index] == True == self.bool_array[index + 1]:
                    both_children_are_true = True
            self.bool_array[parent_index] = both_children_are_true
            index = parent_index
        self.bool_array[0] = self.bool_array[1] and self.bool_array[2]
