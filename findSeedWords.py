import re
import string
import sys

bip39WordList = 'BIP39-english-wordlist.txt'

originalDocument = []

def getBIP39List():
    with open(bip39WordList, 'r') as bip39file:
        bip39List = bip39file.readlines()
    
    wordList = []
    for value in bip39List:
        wordList.append(re.sub('\n', '', value))
        
    return wordList
#################################################### END: getBIP39List()

def getDocument(fileName):
    global originalDocument
    wordList = []

    with open(fileName, 'r') as inputFile:
        inputDocument = inputFile.readlines()
    
    for line in inputDocument:
        words = line.split(' ')
        for word in words:
            wordList.append(re.sub('\n', '', word))
        originalDocument += words
    
    return wordList
#################################################### END: getDocument()

def getUniqueWords(wordList):
    wordsFound = []
    i = 0
    for word in wordList:
        wordList[i] = word.strip().lower()

        if wordList[i] not in wordsFound:
            wordsFound.append(wordList[i])
        i += 1
    
    return wordsFound
#################################################### END: getUniqueWords(wordList)

def removePunctuation(wordList):
    parsedList = []

    for word in wordList:
        for letter in word:
            if letter in string.punctuation:
                word = str(word).replace(letter, '')
        parsedList.append(word)

    return parsedList
#################################################### END: removePunctuation(wordList)

def getValidSeedWords(wordList, checkList):
    seedWords = []
    numWords = 0

    i = 0
    for word in wordList:
        x = 0
        for entry in checkList:
            if entry == word:
                seedWords.append(wordList[i])
                numWords += 1
            x += 1
        i += 1

    return seedWords
#################################################### END: getValidSeedWords(wordList, checkList)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        seedWords = getValidSeedWords(getBIP39List(), getUniqueWords(removePunctuation(getDocument(sys.argv[1]))))
        
        numWords = 0
        for entry in seedWords:
            numWords += 1
        
        print('\nNumber of seed words found: ' + str(numWords) + '\n\n' + str(seedWords) + '\n')

        i = 0
        for word in seedWords:
            if i == numWords - 1:
                seedWords[i] = str(word)
            else:
                seedWords[i] = str(word) + '\n'
            i += 1

        with open('seedwords.txt', 'w') as outputFile:
            outputFile.writelines(seedWords)
    else:
        print('ERROR: No document file supplied')
        print('\n  Use `python findSeedWords.py <filename>`')
#################################################### END: __main__