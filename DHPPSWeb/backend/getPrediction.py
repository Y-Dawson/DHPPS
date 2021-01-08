import subprocess
import json
import os


def SendParamsToCmd(popuList, transMatrix, infectedList):
    popuListStr = json.dumps(popuList)
    transMatrixStr = json.dumps(transMatrix)
    infectedListStr = json.dumps(infectedList)

    path = os.getcwd()+"/backend/simulate/"+"model.py"
    print(path)

    result = subprocess.Popen(
        ['python3.7', path, popuListStr, transMatrixStr, infectedListStr],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result.wait()
    resultStr = result.stdout.read()
    resultList = eval(resultStr)
    if (not isinstance(resultList, list)):
        resultList = list("Return a non-list result!")
    print(resultList)
    return resultList
