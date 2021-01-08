import subprocess
import json
import os


def SendParamsToCmd(popuList, transMatrix, infectedList):
    popuListStr = json.dumps(popuList, separators=(',',':'))
    transMatrixStr = json.dumps(transMatrix, separators=(',',':'))
    infectedListStr = json.dumps(infectedList, separators=(',',':'))

    path = os.getcwd()+"/backend/simulate/"+"model.py"
    print(path)
    print(popuListStr)
    print(transMatrixStr)
    print(infectedListStr)
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
