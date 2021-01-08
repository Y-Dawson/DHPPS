import subprocess
import json
import os


def SendParamsToCmd(popuList, transMatrix, infectedList):
    popuListStr = json.dumps(popuList, separators=(',', ':'))
    transMatrixStr = json.dumps(transMatrix, separators=(',', ':'))
    infectedListStr = json.dumps(infectedList, separators=(',', ':'))

    path = os.path.abspath('.')+"/simulate/"+"model.py"
    # print(path)
    # print(popuListStr)
    # print(transMatrixStr)
    # print(infectedListStr)
    try:
        result = subprocess.check_output(
            ['python3.7', path, popuListStr, transMatrixStr, infectedListStr],
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        # print(result)
        # print(len(result))
        resultList = eval(result)
        # print(len(resultList))
        # print(len(resultList[0]))
        if (not isinstance(resultList, list)):
            resultList = list("Return a non-list result!")
        # print(resultList)
        return resultList
    except subprocess.CalledProcessError as exc:
        print('returncode:', exc.returncode)
        print('cmd:', exc.cmd)
        print('output:', exc.output)
        return list("Return a non-list result!")