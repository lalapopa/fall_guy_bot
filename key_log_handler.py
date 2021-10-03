def getTimeAndKeyFromKeylog(Keylog):
	Time = []
	Keys = []

	for Line in Keylog:
		Time.append(getTimeFromLog(Line))
		Keys.append(getKeyFromLog(Line,Time[len(Time)-1]))
	TimeWithNoDuplicates, DuplicatePositions = RemoveDuplicatesandGivePosition(Time)
	KeysWithNoDuplicates = MergeListInSpecificPosition(Keys,DuplicatePositions)
	KeysCategories = return_categories_from_key_list(KeysWithNoDuplicates)
	return TimeWithNoDuplicates, KeysCategories


def getTimeFromLog(string):
	OnlyRawTime = ''.join([n for n in string if n.isdigit()])
	CleanTime = FormatTime(OnlyRawTime)
	return CleanTime


def getKeyFromLog(string, Time):
	TrashSymbols = 'TIME = ' + Time + ' '
	if string.startswith(TrashSymbols):
		Key = string.replace(TrashSymbols, '', 1)
		Key = Key[:-1]
	return Key


def FormatTime(RawNumber, numbersAfterPoint=6):
	if len(RawNumber) == numbersAfterPoint:
		CleanNumber = '.' + RawNumber[0:]
	elif len(RawNumber) == numbersAfterPoint + 1:
		CleanNumber = RawNumber[:1] + '.' + RawNumber[1:]
	elif len(RawNumber) == numbersAfterPoint + 2:
		CleanNumber = RawNumber[:2] + '.' + RawNumber[2:]
	elif len(RawNumber) == numbersAfterPoint + 3:
		CleanNumber = RawNumber[:3] + '.' + RawNumber[3:]
	return CleanNumber


def RemoveDuplicatesandGivePosition(seq, idfun=None):
    # order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    DuplicatePositions = []

    for item in seq: 
        marker = idfun(item)
        findDuplicatePosition = []

        if marker in seen: 
            counter += 1
            findDuplicatePosition = FindPositionOfElement(seq,item)
            if findDuplicatePosition not in DuplicatePositions:
                DuplicatePositions.append(findDuplicatePosition) 
           
            if counter >= 2:
                del result[-1]
            
            continue 

        seen[marker] = 1
        result.append(item)
        counter = 0

    return result, DuplicatePositions


def FindPositionOfElement(List, Element):
	return [i for i in range(len(List)) if List[i] == Element]


def MergeListInSpecificPosition(Array, Positions, idfun=None): 
    MergedList = [] 

    if idfun is None:
        def idfun(x): return x
    seen = {}
    
    FirstIndexNumber = []
    SkipIndeces = []
    
    ReadyPair = []
    PastPair = []
    

    for Pair in Positions: 

        FirstIndexNumber.append(Pair[0])

        for PairIndex in Pair:
            marker = idfun(PairIndex)
            if marker in seen: continue 
            seen[marker] = 1 

            if PairIndex not in FirstIndexNumber or len(Pair)>= 3:
                SkipIndeces.append(PairIndex)

        if len(Pair) < 3:    
            ReadyPair.append(CombineElementToList(Array,Pair))

    for index in range(len(Array)):
        try:
            if index not in SkipIndeces:
                if index not in FirstIndexNumber:
                    MergedList.append(Array[index])
          
                else:
                    MergedList.append(ReadyPair[0])  
                    del ReadyPair[0]
        except Exception as e:
            pass
                     
    return MergedList


def CombineElementToList(Array, Positions):
    CombinedList = []

    for Position in Positions:
        CombinedList.append(Array[Position])
    return CombinedList

def return_categories_from_key_list(key_list):
    keys_categories = {
    'W':        [1,0,0,0,0,0,0],
    'A':        [0,1,0,0,0,0,0],
    'S':        [0,0,1,0,0,0,0],
    'D':        [0,0,0,1,0,0,0],
    'SPACE':    [0,0,0,0,1,0,0],
    'E':        [0,0,0,0,0,1,0],
    'SHIFT':    [0,0,0,0,0,0,1],
    'NOTHING':  [0,0,0,0,0,0,0],
    } 
    category_list = []

    for keys in key_list:
        if type(keys) is str:
            category_list.append(keys_categories[keys])
        if type(keys) is list:
            category_list.append(connection_two_categories(keys_categories[keys[0]],keys_categories[keys[1]]))

    return category_list


def connection_two_categories(category_one,category_two):
	connected = [num for num in category_one]

	for element in category_two:
		if element == 1:
			connected.insert(category_two.index(element), 1)
			connected.pop()
			break
			
	return connected
