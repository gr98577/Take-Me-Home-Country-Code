from random import randint

class NGramLevel:
    def __init__(self, layer3=False):
        self.count = 0
        if not layer3:
            self.next = dict()

BOL = '<BOL>'
EOL = '<EOL>'

def countLine(multigram, line):
    #add the BOL and EOL buffers
    words = [BOL, BOL]  + line.split() + [EOL]

    #return if blank line
    if len(words) == 3:
        return None

    for i in range(len(words)):
        word = words[i]
        #add 1 to the total count of words
        if not (word == BOL or word == EOL):
            multigram.count += 1

        #unigram count
        if not word in multigram.next:
            multigram.next[word] = NGramLevel()
        multigram.next[word].count += 1

        #bigram count
        if i > 0:
            prevWord = words[i-1]
            if not word in multigram.next[prevWord].next:
                multigram.next[prevWord].next[word] = NGramLevel()
            multigram.next[prevWord].next[word].count += 1
        
        #trigram count
        if i > 1:
            prevWord = words[i-1]
            prevPrevWord = words[i-2]
            if not word in multigram.next[prevPrevWord].next[prevWord].next:
                multigram.next[prevPrevWord].next[prevWord].next[word] = NGramLevel(True)
            multigram.next[prevPrevWord].next[prevWord].next[word].count += 1

#returns a trained multigram model
def trainModel():
    multigram = NGramLevel()
    invalid = True

    #get a valid filename
    while invalid:
        filename = str(input("Enter name of file for training the data: "))
        try:
            inputFile = open(filename, "r")   
            invalid = False
        except Exception:
            print("filename invalid, please try again")
    
    #populate the language model with counts from the file
    for line in inputFile:
        countLine(multigram, line)
    inputFile.close()

    return multigram

#returns a string generated probabilistically from the two preceding words
def genTrigram(multigram, word1, word2):
    level2 = multigram.next[word1].next[word2]
    totalCount = level2.count
    pickInt = randint(1, totalCount)
    pick = str()
    #subtracts the count of each word from the randomly generated number until <= 0
    #this is when the word has been found
    for word in level2.next:
        pickInt -= level2.next[word].count
        if pickInt <= 0:
            return word

    return None

#returns a string generated probabilistically from the preceding word
def genBigram(multigram, word1):
    level1 = multigram.next[word1]
    totalCount = level1.count
    pickInt = randint(1, totalCount)
    pick = str()
    #subtracts the count of each word from the randomly generated number until <= 0
    #this is when the word has been found
    for word in level1.next:
        pickInt -= level1.next[word].count
        if pickInt <= 0:
            return word
    
    return None

#returns a string generated probabilistically
def genUnigram(multigram):
    totalCount = multigram.count
    pickInt = randint(1, totalCount)
    pick = str()
    #subtracts the count of each word from the randomly generated number until <= 0
    #this is when the word has been found
    for word in multigram.next:
        pickInt -= multigram.next[word].count
        if pickInt <= 0:
            return word 
    return None

#prints the specified lines using unigram generation
def printUnigram(multigram, numLines):
    for i in range(numLines):

        word = genUnigram(multigram)
        while word == EOL or word == BOL:
            word = genUnigram(multigram)
        
        while not word == EOL:
            if not word == BOL:
                print(word, end=" ")
            word = genUnigram(multigram)
        
        print()    

#prints the specified lines using bigram generation
def printBigram(multigram, numLines):
    for i in range(numLines):
        word1 = BOL
        word2 = genBigram(multigram, word1)

        while not word2 == EOL:
            if not word2 == BOL:
                print(word2, end=" ")
            word1 = word2
            word2 = genBigram(multigram, word1)
        
        print() 

#prints the specified lines using trigram generation
def printTrigram(multigram, numLines):
    for i in range(numLines):
        word1 = BOL
        word2 = BOL
        word3 = genTrigram(multigram, word1, word2)

        while not word3 == EOL:
            print(word3, end=" ")
            word1 = word2
            word2 = word3
            word3 = genTrigram(multigram, word1, word2)
        
        print() 

def main():

    multigram = trainModel()


    goAgain = True

    while goAgain:
        numLines = int(input("How many lines long would you like the song to be? "))
        N = 0
        while N < 1 or N > 3:
            try:
                N = int(input("Select the value for N (1-3): "))
            except Exception:
                print("Invalid input")
        
        print("\n\t~~~~~~~~~~")
        if N == 1:
            printUnigram(multigram, numLines)
        elif N == 2:
            printBigram(multigram, numLines)
        elif N == 3:
            printTrigram(multigram, numLines)
        print("\t~~~~~~~~~~\n")
        leave = input("Enter 'quit' to leave, or anything else to generate another song: ")
        if leave == 'quit':
            goAgain = False
        



main()
    
    

