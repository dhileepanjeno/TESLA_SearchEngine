class TrieNode:
    def __init__(self):
        self.children = [None]*26
        self.isEndOfWord = False
        self.ind = []
    
class Trie:
    def __init__(self):
        self.root = self.getNode()
        self.ctr=0
        
    def getNode(self):
        return TrieNode()
 
    def charToIndex(self,ch):         
        return ord(ch)-ord('a')
    
    def insert(self,key,ind):
        temp = self.root
        length = len(key)
        for level in range(length):
            index = self.charToIndex(key[level])
            if not temp.children[index]:
                temp.children[index] = self.getNode()
            temp = temp.children[index]
        temp.isEndOfWord = True
        temp.ind.append(ind)
 
    def search(self, key):
        temp = self.root
        length = len(key)
        for level in range(length):
            index = self.charToIndex(key[level])
            if not temp.children[index]:
                return []
            temp = temp.children[index]
        if temp != None and temp.isEndOfWord:
            return temp.ind
        else:
            return []
