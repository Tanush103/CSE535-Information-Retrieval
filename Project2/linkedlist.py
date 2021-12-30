'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import math


class Node:

    def __init__(self, value=None, next=None):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return []
        else:
            """ Write logic to traverse the linked list.
                To be implemented."""
        
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.next
            return traversal

    def traverse_skips(self,length):
        skip_connections=[]
        if self.start_node is None:
          
          return
        else:

            """ Write logic to traverse the linked list using skip pointers.
                To be implemented."""
            n_skips,length_between_skips=self.add_skip_connections(length)
            #print(length_between_skips)            
            count=0
        
            # if length_between_skips<=1:
            #   return []
            n=self.start_node
            skip_connections.append(n.value)
            # print(skip_connections)
            # a = self.start_node
            # for _ in range(self.length-2):
            #     a = a.next
            while n is not None:
                if(count==length_between_skips):
                    skip_connections.append(n.value)
                    count=0
                n=n.next
                count=count+1
            
            return skip_connections
        
    def add_skip_connections(self,length):
        n_skips = math.floor(math.sqrt(length))
        if n_skips * n_skips == length:
            n_skips = n_skips - 1
        length_between_skips=round(math.sqrt(length),0)

        return n_skips,length_between_skips    
        
           
    

    def insert_at_end(self, value):
        new_node = Node(value=value)
        n = self.start_node

        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return

        elif self.start_node.value >= value:
            self.start_node = new_node
            self.start_node.next = n
            return

        elif self.end_node.value <= value:
            self.end_node.next = new_node
            self.end_node = new_node
            return

        else:
            while n.value < value < self.end_node.value and n.next is not None:
                n = n.next

            m = self.start_node
            while m.next != n and m.next is not None:
                m = m.next
            m.next = new_node
            new_node.next = n
            return
        self.removeDuplicates()


    def removeDuplicates(self):
        temp = self.start_node
        if temp is None:
            return
        while temp.next is not None:
            if temp.value == temp.next.value:
                new = temp.next.next
                temp.next = None
                temp.next = new
            else:
                temp = temp.next
        return self.start_node