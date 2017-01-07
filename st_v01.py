#python2


#we adding more lines to it
import sys
#we make nonsense changes

class Tree_node():
    
    def __init__(self, key, left = None, right = None, p = None):
        self.key = key
        self.summ = key
        self.left = left
        self.right = right
        self.parent = p
        

    def __str__(self):
        if self.left:
            left = self.left.key
        else: 
            left = None
        if self.right:
            right = self.right.key
        else:
            right = None
        if self.parent:
            parent = self.parent.key
        else:
            parent = None
        return "key:" + str(self.key) + " sum:" +str(self.summ) + "left:" + str(left) + ' right:' + str(right) + ' parent:' + str(parent)
        #return "key:" + str(self.key) + " left:" + self.left + ' right:' + self.right + ' parent:' + self.p
        
class Binary_tree():

    def __init__(self):
        """ it's not yet clear 
        what the structrure 
        is going to be"""
        self.root = None
        self.size = 0
        self.list_of_nodes = []

    def __str__(self):
        if self.size == 0:
            return 'Empty tree'
        else:
            #return 'root: ' + str(self.root) + ' size: ' +str(self.size)
            return 'root:' + str(self.root.key) + ' size:' + str(self.size) + str([str(node) for node in self.list_of_nodes])
    
    def __del__(self):
        #delete the instance of the Class
        pass 

    def search(self, key):
        """ iterative tree search
        where x - pointer to the root
        k - key we are searching for"""
        search_result = self.find(key)
        if not search_result:
            return None
        if search_result.key == key:
            #print 'we are here'
            return key
        else:
            return None
    
    def insert_s(self, key):
        #print 'insert_s node:' + str(key)
        n = self.find(key)
        if n == None or n.key != key:
            node = Tree_node(key)
            self._insert(node)
            self.list_of_nodes.append(node)
            self.find(node.key)
        
    def find(self, key):
        #print 'find'
        v = self.root
        last = self.root
        next_node = None
        while v != None:
            if v.key >= key and (next_node == None or v.key < next_node.key):
                next_node = v 
            last = v
            if v.key == key:
                break
            if v.key < key:
                v = v.right
            else:
                v = v.left
        self.root = self.splay(last)
        return next_node    

    def _insert(self, node):
        #print '_insert'
        #print node
        """technically, when we insert a new node we have to do the following:
            1. if tree is empty, node becomes the root
            otherwise, we need to:
            1. find the right place for the new node:
            2. update new node's parent
            3. for new node's parent update its left or right child"""
        y = None  #temp argument
        x = self.root #assign root to x
        while x != None:
            # sliding down the tree starting from the root down until we hit None
            y = x #temp y becomes x and we check its children
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
        node.parent = y # y becomes the parent for our insert node
        if y == None: #if y still None, tree is empty and our insert is the root
            self.root = node
        elif node.key < y.key: #y is the parent node. we need to decide whether node it the right or left child
            y.left = node
        else:
            y.right = node
        self.size += 1
        
    def _update(self, node):
        if node == None:
            return
        node.summ = node.key + (node.left.summ if node.left != None else 0) + (node.right.summ if node.right != None else 0)
        if node.left != None:
            node.left.parent = node
        if node.right != None:
            node.right.parent = node
            
        
    
    def next_el(self, key):
        """this function is looking for the successor element"""
        node = self.find(key)
        if node == None:
            return None
        if node.right != None: # if node has a righ child, then it's a successor
            return self._min(node.right)
        y = node.parent       
        x = node
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y
        
        
    def _min(self, node):
        """it looks for the min element at a given node"""
        x = node
        while x.left != None:
            x = x.left
        return x
    
    
    def splay(self, node):
        #print 'splay' 
        #print node
        if node == None:
            return None
        while node.parent != None:
            if node.parent.parent == None:
                #print 'we are here'
                #print node
                self.smallRotation(node)
                break
            self.bigRotation(node)
        self.root = node
        #print 'node at the end of splay'
        #print node
        return node
    
    def bigRotation(self, node):
        #print 'big rotation'
        if node.parent.left == node and node.parent.parent.left == node.parent:
            #Zig-zig
            self.smallRotation(node.parent)
            self.smallRotation(node)
        elif node.parent.right == node and node.parent.parent.right == node.parent:
            #Zig-zig
            self.smallRotation(node.parent)
            self.smallRotation(node)
        else:
            #Zig-zag
            self.smallRotation(node)
            self.smallRotation(node)
    
    def smallRotation(self, node):
        #print 'small rotation'
        """i think it include both left and right rotations"""
        parent = node.parent
        if parent == None:
            #print 'first if'
            return
        grandparent = node.parent.parent
        if parent.left == node: #if node is the left child
            #print 'second if'
            m = node.right
            node.right = parent
            parent.left = m
        else:
            #print 'second else'
            m =node.left
            node.left = parent
            parent.right = m
        self._update(parent)
        self._update(node)
        #print node
        node.parent = grandparent
        #print grandparent
        if grandparent != None:
            #print 'third if'
            if grandparent.left == parent:
                #print 'if inside third if'
                grandparent.left = node
            else:
                #print 'else indise third if'
                grandparent.right = node
                
    def split(self, key):
        #root_const = self.root
        node = self.find(key)
        if node == None:
            return (self.root, None)
        right = self.splay(node)
        left = right.left
        right.left = None
        if left != None:
            left.parent = None
        self._update(left)
        self._update(right)
        #self.root = root_const
        return (left, right)
        
    def merge(self, left, right):
        #root_const = self.root
        if left == None:
            return right
        if right == None:
            return left
        while right.left != None:
            right = right.left
        right = self.splay(right)
        right.left = left
        self._update(right)
        #self.splay(root_const)
        return right
    
    def erase(self, key):
        next_node = self.next_el(key)
        #print self
        node = self.find(key)
        if node == None:
            return
        L = node.left
        R = node.right
        if next_node == None and L == None:
            self.root = None
            self.size = 0
            self.list_of_nodes.remove(node)
            return
        if next_node == None:
            L.parent = None
            self._update(L)
            self.root = L
            self.size -= 1
            self.list_of_nodes.remove(node)
            return
        if L == None:
            R.left = L
            self._update(R)
            self.root = R
            self.size -= 1
            R.parent = None
            self.list_of_nodes.remove(node)
            return
        R.left = L
        L.parent = R
        self._update(R)
        self.root = R
        self.size -= 1
        R.parent = None
        self.list_of_nodes.remove(node)

    def summ(self, fr, to):
        answer = 0
        (left, middle) = self.split(fr)
        if middle == None:
            return 0
        (middle, right) = self.split(to + 1)
        if middle == None:
            self.merge(left, right)
            return 0
        #print "new tree"
        #print self
        answer = middle.summ
        self.merge(self.merge(left, middle),right)
        return answer

MODULO = 1000000001
n = int(sys.stdin.readline())
last_sum_result = 0
tree = Binary_tree()
for i in range(n):
    line = sys.stdin.readline().split()
    print 'line: ' + str(i)
    print 'question' + str(line)
    print tree
    if line[0] == '+':
        x = int(line[1])
        tree.insert_s((x + last_sum_result) % MODULO)
        print 'tree after insert'
        print tree
    elif line[0] == '-':
        x = int(line[1])
        tree.erase((x + last_sum_result) % MODULO)
        print 'tree after erase'
        print tree
    elif line[0] == '?':
        x = int(line[1])
        if tree.search((x + last_sum_result) % MODULO) != None:
            print 'Found'
        else:
            print 'Not Found'
        print 'tree after search'
        print tree
    elif line[0] == 's':
        l = int(line[1])
        r = int(line[2])
        res = tree.summ((l + last_sum_result) % MODULO,(r + last_sum_result) % MODULO)
        #print 'question'
        #print line
        print 'tree after summ'
        print tree
        print 'last_sum_result' + str(last_sum_result)
        print res
        print 'prior last_sum_result', last_sum_result
        last_sum_result = res % MODULO
