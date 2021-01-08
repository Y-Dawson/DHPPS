import subprocess
import json
import os


def SendParamsToCmd(popuList, transMatrix, infectedList):
    popuListStr = json.dumps(popuList)
    transMatrixStr = json.dumps(transMatrix)
    infectedListStr = json.dumps(infectedList)

    path = os.getcwd()+"/simulate/"+"model.py"
    print(path)

    result = subprocess.Popen(
        ['python3.7', path, popuListStr, transMatrixStr, infectedListStr],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    result.wait()
    resultStr = result.stdout.read()
    print(resultStr)
    resultList = eval(resultStr)
    print(resultList)
    if (isinstance(resultList, list)):
        return resultList
    else:
        return list("Return a non-list result!")


if __name__ == "__main__":
    SendParamsToCmd(
        popuList=[2000, 400],
        transMatrix=[[50, 60], [120, 40]],
        infectedList=[100, 256])
