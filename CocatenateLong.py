# Satish Venkob
#merged
try:
    import sys
    import timeit
    import time
except ImportError as err:
    print("ERROR: Unable to import module {0} in path {1}".format(err.name,err.path))
    quit()
    
class TrieNode:
    def __init__(self, character=None, isLastNode=False):
        self.childList={}
        self.character=character
        self.isLastNode=isLastNode
        
    def setLastNode(self):
        self.isLastNode=True
              
        
        
class Trie:
    count=0
    def __init__(self):
        self.rootNode=TrieNode('')
 
    def insertWordIntoTrie(self, word):
        Trie.count+=1
        temp=self.rootNode
        for chr1 in word:
          
            if chr1 not in temp.childList:
                #print("not in")
                temp.childList[chr1]=TrieNode(chr1)
            temp=temp.childList[chr1]
          
        temp.isLastNode=True
        
        
#Return all prefixes of the word
#It will not add the whole word, as one of the prefix, into the list, firstRecur helps to keep track of this

def findPrefixes(myTrie,word, firstRecur):
    prefix=''
    allprefixes=[] 
    curr=myTrie.rootNode
    
    for chr1 in word:
        
        #if not in Trie, return prefixes accumulated so far
        if chr1 not in curr.childList:
            #print("Satish, return what you have so far")
            return allprefixes
        
        #add to prefix move on to next child node
        prefix+=chr1
        curr=curr.childList[chr1]
        
        #Last Node means this is a prefix
        if curr.isLastNode==True:
            
            #we don't want to add the full word as prefix, since this means there are no 
            #valid shorter words as prefix for this specific word
            if(prefix==word) and (firstRecur==1): 
                return allprefixes
            else:
                allprefixes.append(prefix)
            
    return allprefixes
        
#Recursive call
#This gets the longest prefix of the word, gets the suffix after the longest prefix,
#then recursively calls this procedure on the suffix
# returns True if prefixes found else false
#for a given word, eventual return of True, means that the word is entirely composed of shorter words
def findPrefixLongestConcatWord(myTrie, word, firstRecur=1):
    
    #end of word raeched so the word is contatenated one return True.
    if word=='' and firstRecur==0:
        return True
    
    #reset prefixes list for this word
    prefixes=[]
    
    #find prefixes for this word
    #Note reversed to save time, I look from the longest prefix and then use that to recurse on the suffixes
    prefixes=findPrefixes(myTrie,word, firstRecur)
    
    #print("PREFIXES",prefixes, "For",word, "FirstRecur",firstRecur)
    
     #No Valid shorter prefix, return false
    if len(prefixes)==0:    
        #print("no prefixes for this word",word)
        return False
    
    #Iterate all prefixes for this word and recursively call the procedure on the suffix
    for p in reversed(prefixes):
        res=findPrefixLongestConcatWord(myTrie,word[len(p):], 0) 
        
        #Continue to the next largest prefix
        if res==False:
            continue
        else:
            return True
        
    # we have tried all prefixes for this word, nothing got us to the end hence return False
    return False
  

def processFileCreateTrieAndHashList(filename,noOfLongestWordsToFind):
    if filename==[]:
        print("Empty Filename !")
        return 0  
    try:
        filestream=open(filename,'r')  
    except (UnicodeDecodeError):
        print("ERROR:UNICODE ERROR FILE {0} IS NOT DECODABLE".format(filename))
    except (OSError) as err:
        print("ERROR:IN OPEN SYSTEM CALL for File {0}, Error String: {1}".format(err.filename,err.strerror))
    
    #Using Trie for pattern matching:
    myTrie=Trie()
    
    #dictionary for storing the words for later processing:
    #This will help me process from the highest length words in descending order 
    #here Key is the length of the words and value is a linked list of words of the same length
    sortedWordsHash={}
    
    #sorted listed based on length, which is the key
    sortedList=[]
   
    for word in filestream:
        word=word.strip('\n\r')
        
        #Insert each word into trie
        myTrie.insertWordIntoTrie(word)
        
        #also insert each word into a hashed linked list
        #[len1]->word1->word2...
        #[len2]->word1->word2....
        if sortedWordsHash.has_key(len(word)):
            sortedWordsHash[len(word)].append(word)
        else:
            sortedWordsHash[len(word)]=[word]
    
    #sort the linkedList based on the key(length in this case)   
    sortedList = [value for (key, value) in sorted(sortedWordsHash.items(), reverse=True)]
    
    #Just dumping the sorted list in a file
    #for debugging. uncomment if you want to see sortedHashList  
    #filestream1=open("sortedWordsHash.txt",'w')
    #for s1 in sortedList:
        #print(s)
    #    filestream1.write("%s\n" % s1)
    #filestream1.close() 
    
    #Counters for keep track of n longest words and total number of words made up of smaller words
    c=0
    noOfCancatenateWords=0
        
    #Store results here: first n longest concatenated words
    results=[]
    mflag=False
    #for each list with different lengths
    for l in sortedList:  
        #flag to skip to the next length if we found a concatenated word in the current length
        foundForThisLength=0
        
        #for each word on the list with same length
        for w in l:    
            mflag=findPrefixLongestConcatWord(myTrie, w,1)
            #print("FOR WORD", w, "RESULT",mflag)
            
            #if True we have found a word, made up of shorter words
            #since this the hash is sorted by lengths we will get the first longest, second longest and so on
            if mflag==True:
                if c < noOfLongestWordsToFind and foundForThisLength==0 :
                    #print("Concatenated Word number:",c+1,"OF LENGTH:",len(w),"WORD:",w,)
                    results.append(w)
                    foundForThisLength=1
                    c+=1
                noOfCancatenateWords+=1
                
    #Print out the final results
    c=0
    for r in results:
        print("Concatenated Word number:",c+1,"OF LENGTH:",len(r),"WORD:",r,)
        c+=1
    print("Total Number of Concatenated words",noOfCancatenateWords)
            
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "This program takes two parameters: 'Filename' and 'No of Longest Concatenated words to Find', as input"
        print "Incorrect Parameters"
    else:
        filename = sys.argv[1]
        noOfLongestWordsToFind=int(sys.argv[2])
        if (noOfLongestWordsToFind <=0):
            print("Be Sane, No Negatives Or Zero for no of Longest words!")
        clktime=time.clock()
        processFileCreateTrieAndHashList(filename, noOfLongestWordsToFind)
        print("Time to run",time.clock()-clktime)
