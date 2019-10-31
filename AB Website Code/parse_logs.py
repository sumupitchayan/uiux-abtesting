def parse_logs():
    dataA, dataB = {}, {}
    fullData = []
    ids = set()
    # heroku logs --source app -n 1000 | grep --line-buffered . | grep -i AB_TEST > mylogs1.txt
    i = 1
    timestamps = set()
    with open('myfilteredlog.txt') as fp:
        line = fp.readline()
        while line:
            splitLine = line.split(' ')
            if len(splitLine) == 8:
                timestamp, version, sessionID = splitLine[0], splitLine[3], splitLine[7]
                if timestamp not in timestamps:
                    timestamps.add(timestamp)
                    fullData.append(line)
                    ids.add(sessionID)
                    if version == 'A':
                        if sessionID not in dataA:
                            dataA[sessionID] = [splitLine]
                        else:
                            dataA[sessionID].append(splitLine)
                    elif version == 'B':
                        if sessionID not in dataB:
                            dataB[sessionID] = [splitLine]
                        else:
                            dataB[sessionID].append(splitLine)
            line = fp.readline()
    i += 1
        
    return dataA, dataB

def calc_click_through_rate(data):
    numClickedThrough = 0
    uniqueIDs = set()
    for key in data.keys():
        entries = data[key]
        uniqueIDs.add(key)
        for entry in entries:
            clickedItem = entry[6] != '0'
            if clickedItem:
                numClickedThrough += 1
                break
    return numClickedThrough / len(data)

def calc_time_to_click(data):
    acc = 0
    numClicks = 0
    for key in data.keys():
        entries = data[key]
        for index in range(1,len(entries)):
            currLog = entries[index]
            prevLog = entries[index - 1]
            sameLoadTime = currLog[4] == prevLog[4]
            if sameLoadTime:
                timeDiff = (int(currLog[5]) - int(currLog[4])) / 1000
                acc += timeDiff
                numClicks += 1
    return acc / numClicks


def calc_dwell_time(data):
    acc = 0
    numDwelled = 0
    for key in data.keys():
        entries = data[key]
        for index in range(1,len(entries)):
            currLog = entries[index]
            isClick = currLog[6] != '0'
            if isClick:
                returnsToPage = index + 1 < len(entries)
                if returnsToPage:
                    dwellTime = (int(entries[index + 1][4]) - int(currLog[5])) / 1000
                    acc += dwellTime
                    numDwelled += 1
                    break
    return acc / numDwelled


def calc_return_rate(data):
    acc = 0
    for key in data.keys():
        entries = data[key]
        for index in range(1,len(entries)):
            currLog = entries[index]
            clickedAndReturned = (currLog[6] != '0') and (index + 1 < len(entries))
            if clickedAndReturned:
                acc += 1
                break
    return acc / len(data)

if __name__ == '__main__':
    dataA, dataB = parse_logs()

    clickThroughA = calc_click_through_rate(dataA)
    clickThroughB = calc_click_through_rate(dataB)

    timeToClickA = calc_time_to_click(dataA)
    timeToClickB = calc_time_to_click(dataB)

    dwellTimeA = calc_dwell_time(dataA)
    dwellTimeB = calc_dwell_time(dataB)

    returnRateA = calc_return_rate(dataA)
    returnRateB = calc_return_rate(dataB)

    print("click through rate A: " + str(clickThroughA))
    print("click through rate B: " + str(clickThroughB))
    print("time to click A: " + str(timeToClickA))
    print("time to click B: " + str(timeToClickB))
    print("dwell time A: " + str(dwellTimeA))
    print("dwell time B: " + str(dwellTimeB))
    print("return rate A: " + str(returnRateA))
    print("return rate B: " + str(returnRateB))



