import re

class numConvert():

    def __init__(self):
        self.romanNumeralTable = [['M',1000],['CM',900],['D',500],['CD',400],['C',100],['XC',90],['L',50],['XL',40],['X',10],['IX',9],['V',5],['IV',4],['I',1]]
        
    def intToRoman (self,integer):
        #Roman Numberals have no 0, so just return string
        if integer == 0:
            return '0'
        
        #set up the string to return
        returnString=''
    
        for pair in self.romanNumeralTable:
            #substract out integer the most number of times. This could also be done with a integer division and then add letter number of times.
            while integer - pair[1] >= 0:
                integer -= pair[1]
                returnString += pair[0]
    
        return returnString
    
    
    
    def romanToInt(self,string):
        #set up the integer to return
        returnInt=0
        
        for pair in self.romanNumeralTable:
            potentialMatch = True
            while potentialMatch:
                #if the length of the string is longer than the roman numeral, check to see if roman numeral matches beginning of string
                if len(string) >= len(pair[0]):
                    #check if beginning of string matches roman numeral, add to int, reduce string.  Else does not match
                    if string[0:len(pair[0])] == pair[0]:
                        returnInt += pair[1]
                        string = string[len(pair[0]):]
                    else: 
                        potentialMatch = False
                else: 
                    potentialMatch = False
    
        return returnInt
    
    
    def numToWords(self,num):
        #establish number lists
        units = ["", "one", "two", "three", "four",  "five", 
        "six", "seven", "eight", "nine"]
    
        teens = ["", "eleven", "twelve", "thirteen",  "fourteen", 
            "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        
        tens = ["", "ten", "twenty", "thirty", "forty",
            "fifty", "sixty", "seventy", "eighty", "ninety"]
        
        thousands = ["","thousand", "million",  "billion",  "trillion"]
        
        #set up words list
        words = []
        if num == 0:
            words.append("zero")
        else:
            #convert number into a string and number of groups of 3. As multipliers change every 100 multipliers.
            numStr = "%d" % num
            numStrLen = len(numStr)
            groups = (numStrLen + 2) / 3
            #add preceding 0s to numStr
            numStr = numStr.zfill(groups * 3)
            
            
            for i in range(0, groups*3, 3):
                hundreds = int(numStr[i])
                tens = int(numStr[i+1])
                unit = int(numStr[i+2])
                multiplierNum = groups - (i / 3 + 1)
                
                #if something in the hundreds of the group, add unit and hundred
                if hundreds >= 1:
                    words.append(units[hundreds])
                    words.append("hundred")
                
                #if unit in the tens, find right word, if 1, find right teen number
                #else add unit digit
                if tens > 1:
                    words.append(tens[tens])
                    if unit >= 1:
                        words.append(units[unit])
                elif tens == 1:
                    if unit >= 1:
                        words.append(teens[unit])
                    else:
                        words.append(tens[tens])
                else:
                    if unit >= 1:
                        words.append(units[unit])
                
                #find multiplier and add that to string
                if multiplierNum >= 1 and (hundreds + tens + unit) > 0:
                    words.append(thousands[multiplierNum])
                    
        #join list together into string with spaces
        return " ".join(words)
    
    def wordToInt(self,string):
        #replace - to account for syntax errors
        string = string.replace('-',' ')
        
        #establish a dictionary for units to lookup when converting, these are the base numbers that will be re-used
        units = {'one':1,
                 'two':2,
                 'three':3,
                 'four':4,
                 'five':5,
                 'six':6,
                 'seven':7,
                 'eight':8,
                 'nine':9,
                 'ten':10,
                 'eleven':11,
                 'twelve':12,
                 'thirteen':13,
                 'fourteen':14,
                 'fifteen':15,
                 'sixteen':16,
                 'seventeen':17,
                 'eighteen':18,
                 'ninteen':19,
                 'twenty':20,
                 'thirty':30,
                 'forty':40,
                 'fifty':50,
                 'sixty':60,
                 'seventy':70,
                 'eighty':80,
                 'ninety':90,}
        
        #dictionary of mutlipliers
        multipliers = {'hundred':100,
                       'thousand':1000,
                       'million':1000000,
                       'billion':1000000000}
        number = 0
        lastUnit = 0
        
        #last multiplier used set to something that will always be greater than the largest multiplier
        lastMultiplier = Ellipsis 
        
        #separate words into an iterable
        words = string.lower().split(" ")
        for word in words:
            #if word represents a unit, add it to number
            if word in units:
                lastUnit = units[word]
                number += units[word]
            
            elif word in multipliers:
                #if word is a multiplier and less than the last multiplier, multiply the entire number by it. 
                #Ex. Two Hundred Million
                if lastMultiplier < multipliers[word]:
                    number = number*multipliers[word]
                    lastMultiplier = multipliers[word]
                #if multiplier is less than last multiplier, add the last unit * the multiplier. 
                #Ex. Two Hundred
                else:
                    number -= lastUnit
                    number += multipliers[word]*lastUnit
                    lastMultiplier = multipliers[word]
        
        return number
    
    def convert(self,value,fromType,toType):
        #convert into number
        if fromType == 'Roman Numeral':
            number = self.romanToInt(value)
        elif fromType == 'Word':
            number = self.wordToInt(value)
        elif fromType == 'Number':
            number = value
        
        #convert to other type
        if toType == 'Roman Numeral':
            return self.intToRoman(number)
        elif toType == 'Word':
            return self.intToWord(number)
        elif toType == 'Number':
            return number
        elif toType == 'All':
            return {'Number':number,'Word': self.numToWords(number),'Roman Numeral':self.intToRoman(number)}
        
    def findNumbers(self,string):
        #see if any word is a digit
        return [int(s) for s in string.split(' ') if s.isdigit()]
    
    def findRomanNumerals(self,string):
        #find a string that could be a roman numeral, this has obvious issues for I since it might not be a number.
        regex = re.compile('M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
        return [s for s in string.split(' ') if re.match(regex,s)]
    
    def findWords(self,string):
        #find all the potential words and add them together
        regex = re.compile('(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|million|billion)', re.IGNORECASE)
        words = []
        tempWord = ''
        #replace - for syntax purposes to convert seventy-five into seventy five.
        string = string.replace('-',' ')
        for s in string.split(' '):
            #if currently assembling a word, the current word is and, & or a digit, continue assembling word.
            if (tempWord != '' and s in ['and','&']) or re.match(regex,s):
                tempWord += s + ' '
            #if not continuing the word and number was being assembled, add to wordList and restart tempWord
            else:
                if tempWord != '':
                    words.append(tempWord[:-1])
                    tempWord = ''
        if tempWord != '':
            words.append(tempWord[:-1])
        return words
    
    def allOptions(self,string):
        #get all the replacements
        replacementDict = {}
        options = []
        #this currently does not handle something like The 7 VII Seven. It is currently assuming a singular syntax. 
        for match in self.findNumbers(string):
            replacementDict[match] = self.convert(match, 'Number', 'All') 
        for match in self.findRomanNumerals(string):
            replacementDict[match] = self.convert(match, 'Roman Numeral', 'All') 
        for match in self.findWords(string):
            replacementDict[match] = self.convert(match, 'Word', 'All') 
        
        if replacementDict == {}:
            return [string]
        

        for type in ['Number','Roman Numeral','Word']:
            tempString = string
            for match in replacementDict.keys():
                tempString = tempString.replace(str(match),str(replacementDict[match][type]))
            options.append(tempString)
        return options



