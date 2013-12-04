import re
import json
import sys

CLEAN_EXIT = 0
IOERROR_FILE_NOT_FOUND = 1
IOERROR_FILE_NOT_WRITABLE = 2

def main():
    
    # Get file name
    if len(sys.argv) > 1: #Command line support
     fileName = sys.argv[1] 
    else: fileName = raw_input("What file would you like to turn into JSON? (example.txt) ")
    
    # Open file
    try:
        f = open(fileName, "r")
    except IOError:
        print("File not found: \"%s\"" % fileName)
        return IOERROR_FILE_NOT_FOUND
    
    # Read into memory
    textList = f.readlines()

    # Close file
    f.close()
    
    # Clean text
    textList = clean(textList)

    # Process text
    textDict = process(textList)
    
    # Output JSON to file
    try:
        fh = open(re.match("^[\w\- ]+",fileName).group()+".json", "w")
        fh.write(json.dumps(textDict,sort_keys=True,indent=4, separators=(',', ': ')))
    except IOError:
        print("Error: Cannot save JSON file")
        return IOERROR_FILE_NOT_WRITABLE
    else:
        print(fileName +" -----> "+ re.match("^[\w\- ]+",fileName).group()+".json conversion complete.")

    return CLEAN_EXIT

def clean(inputText):
    """Cleans list of strings and returns a new list"""
    outputText = []
    
    # Get rid of first 12 characters and '/n' character at the end
    for line in inputText:
        line = line[12:-1]
        outputText.append(line)
    
    return outputText

def process(inputText):
    """Determine depth of terms in list and returns a dict hierarchy"""
    outputText = {}
    
    inputTextWithIDs = {}
    i = 1
    for line in inputText:
        inputTextWithIDs[i] = {'line': line, 'parent': 0}
        i += 1
    #print inputTextWithIDs
    
    recentNodeForLevel = {0:0}
    for i in inputTextWithIDs:
        currentLevel = inputTextWithIDs[i]['line'].count('    ')
        
        #Remove indentation
        inputTextWithIDs[i]['line'] = re.sub(r'    ',r'',inputTextWithIDs[i]['line'],currentLevel)
        
        inputTextWithIDs[i]['parent'] = recentNodeForLevel[currentLevel-1] if currentLevel > 0 else 0
        
        recentNodeForLevel[currentLevel] = i
    
    #Generate tree structure - based on http://stackoverflow.com/a/4844073
    treeStructure = {}
    for i in inputTextWithIDs:
        try:
            treeStructure[inputTextWithIDs[i]['parent']]
        except KeyError:
            treeStructure[inputTextWithIDs[i]['parent']] = []
        treeStructure[inputTextWithIDs[i]['parent']].append(inputTextWithIDs[i])
    
    for i in inputTextWithIDs:
        try:
            inputTextWithIDs[i]['children'] = treeStructure[i]
        except KeyError:
            pass
    
    # Create final dict for JSON conversion
    outputText = treeToDict(treeStructure[0])
    
    return outputText

def treeToDict(treeStructureList):
    outputText = {}    
    
    for item in treeStructureList:
        getKeyAndValue = item['line'].split(' ')        
        try:
            item['children']
            # Do stuff specific to nodes with children
            keyValue = getKeyAndValue.pop(0)
            outputText[keyValue] = {"value": None,"properties":None}
            if len(getKeyAndValue) > 2:
                # There is a key, value, and additional parameters       
                outputText[keyValue]["value"] = parse(getKeyAndValue.pop(0))
                outputText[keyValue]["properties"] = getKeyAndValue
            elif len(getKeyAndValue) > 1:
                # There is a key and value
                outputText[keyValue]["value"] = parse(getKeyAndValue.pop())
            
            outputText[keyValue].update(treeToDict(item['children']))
        
        except KeyError:
            # Do stuff specific to nodes without children
            keyValue = getKeyAndValue.pop(0)
            if len(getKeyAndValue) > 0:
                # There is a key and value
                outputText[keyValue] = parse(getKeyAndValue.pop())
            else:
                outputText[keyValue] = None
        
        

    #print outputText
    return outputText

def parse(data):
    """Converts string values into their respective data types"""
    try:
        return int(data)
    except ValueError:
        try:
            return float(data)
        except ValueError:
            if data == "True":
                return True
            elif data == "False":
                return False
            elif data == "*nullString*":
                return ""
            elif data == "*nullArray*":
                return []
            else:
                return data

main()
