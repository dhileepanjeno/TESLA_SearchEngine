import pickle
class StopTrieNode:
    def __init__(self):
        self.children = [None]*26
        self.isEndOfWord = False
        
class StopTrie:
    def __init__(self):
        self.root = self.getNode()
        self.ctr=0
        
    def getNode(self):
        return StopTrieNode()
 
    def charToIndex(self,ch):         
        return ord(ch)-ord('a')
    
    def insert(self,key):
        temp = self.root
        length = len(key)
        for level in range(length):
            index = self.charToIndex(key[level])
            if not temp.children[index]:
                temp.children[index] = self.getNode()
            temp = temp.children[index]
        temp.isEndOfWord = True
 
    def search(self, key):
        temp = self.root
        length = len(key)
        for level in range(length):
            index = self.charToIndex(key[level])
            if not temp.children[index]:
                return False
            temp = temp.children[index]
        if temp != None and temp.isEndOfWord:
            return True

##stop_words = {'was', 'herself', 'they', 'have', 'your', 'other', 'shouldn', 'again', 'theirs', 'you', 'him', 'y',
##              'at', 'yours', 'whom', 'how', 'them', 'same', 'it', 'm', 'ourselves', 'our', 'did', 'having', 'out',
##              'aren', 'if', 'ma', 'doing', 'we', 'hers', 'once', 'do', 'can', 'or', 'in', 'so', 'were', 'but', 'too', 'my', 'i',
##              'not', 'the', 'didn', 'will', 'own', 'its', 'under', 'should', 'wouldn', 'when', 'll', 'a', 'to', 'of', 'off',
##              'before', 'both', 'such', 'after', 's', 'ours', 'his', 'by', 'me', 'her', 'into', 'their', 'being', 'wasn',
##              'an', 'those', 'these', 'up', 'o', 'myself', 'about', 'itself', 'from', 'over', 'yourselves', 'any', 'there',
##              'himself', 'ain', 'hasn', 'yourself', 'shan', 'what', 'don', 'only', 'between', 'because', 'during', 'few',
##              'while', 'who', 'each', 'mustn', 'just', 'he', 'themselves', 'against', 'all', 'is', 'she', 'above', 'than', 'are',
##              'be', 'down', 'nor', 'very', 'where', 'which', 'why', 'had', 've', 'isn', 'been', 'has', 'as', 'then', 'with',
##              'am', 'does', 'on', 'that', 'and', 'here', 't', 'd', 'won', 'most', 're', 'until', 'for', 'needn', 'haven',
##              'doesn', 'weren', 'no', 'hadn', 'further', 'mightn', 'now', 'some', 'below', 'more', 'this', 'through', 'couldn'}
##
##
##trie_db=StopTrie()
##stop_words=list(stop_words)
##for word in stop_words:
##    trie_db.insert(word)
##with open('stop_words.pickle', 'wb') as handle:
##    pickle.dump(trie_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
    




