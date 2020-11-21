cityPopulationList = [100000, 200000, 12512512, 124125]、


def predictSimulator(cityPopulationList, generateDays):
    returnList = []
    loopList = []
    for i in cityPopulationList:
        loopList.append(i*0.02)

    for i in range(generateDays):
        tempList = []
        for i in loopList:
            tempList.append(int(i*1.05))
        returnList.append(tempList)
        loopList = tempList
        tempList = []
    return returnList


print(predictSimulator(cityPopulationList, 6))
