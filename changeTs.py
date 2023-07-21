import os
import time
import json

def getAllFiles(root):
    ret = dict()
    for path, dirs, files in os.walk(root):
        for filename in files:
            # print("file", os.path.splitext(filename)[0])
            key = os.path.splitext(filename)[0]
            # ret[key] = os.path.join('"' + path + '"', '"' + filename + '"')
            ret[key] = os.path.join(path, filename)
        for dirname in dirs:
            pass
    return ret 

def changeTs(root, fileDict):
   for root, dirs, files in os.walk(root):
        for filename in files:
            if not filename.endswith(".json"):
                continue
            path = os.path.join(root, filename)
            with open(path, "r") as f:
                content = f.read()
            meta = json.loads(content)["fileMeta"]
            # remove .note extention
            title = meta["title"][:-5]
            createdBy = meta["createTimeForSort"]
            updatedBy = meta["modifyTimeForSort"]
            # print(title, createdBy, updatedBy)
            if title not in fileDict:
                print("Cannot find file by key --- %s --- %d --- %d" % (title, createdBy, updatedBy))
                continue
            file = fileDict[title]
            # print(file)
            try:
                os.utime(file, (createdBy, updatedBy))
            except:
                print("Cannot open file %s..." % (file))

def getErrorLogs(path):
    '''
    Get error logs from console output or same formatted logs
    '''
    ret = []
    cnt = 0
    with open(path) as f:
        for l in f.readlines():
            (_, title, createdBy, updatedBy) = l[:-1].split(" --- ")
            title = title.replace(":", "_").replace("/", "_")
            title = title.replace("?", "_").replace(":", "_")
            title = title.replace("|", "_")
            cnt += 1
            # print(title, createdBy, updatedBy)
            ret.append((title, int(createdBy), int(updatedBy)))
    print("There are total %d files cannot change time..." % (cnt))
    return ret

if __name__ == "__main__":
    with open("config.json") as f:
        config = json.loads(f.read())
    mdPath = config['local_dir']
    metaPath = config['local_dir_meta']

    files = getAllFiles(mdPath)
    changeTs(metaPath, files)

    # handle error files
    errFiles = getErrorLogs("<path_of_error_log>")
    for f in errFiles:
        title, createdBy, updatedBy = f
        if title not in files:
            print("%s---%d---%d--- still not in the list..." % (title, createdBy, updatedBy))
        path = files[title]
        try:
            os.utime(path, (createdBy, updatedBy))
            # print("ok for %s" % (title))
        except Exception as e:
            print("Cannot open file during error handling %s..." % (path)) 
            print(e)
