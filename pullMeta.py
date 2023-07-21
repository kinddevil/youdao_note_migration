#!/usr/bin/python

import requests
import sys
import time
import hashlib
import os
from requests.cookies import create_cookie
import json

def timestamp():
    return str(int(time.time() * 1000))

class YoudaoNoteSession(requests.Session):
    def __init__(self):
        requests.Session.__init__(self)
      
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8'
        }
        self.cookiesPath = 'cookies.json'
        self.configPath = 'config.json'
        self.metaPath = self.getConfig()["local_dir_meta"]
        self.cstk = None

    def login(self):
        '''
        self.get('https://note.youdao.com/web/')

        self.headers['Referer'] = 'https://note.youdao.com/web/'
        self.get('https://note.youdao.com/signIn/index.html?&callback=https%3A%2F%2Fnote.youdao.com%2Fweb%2F&from=web')

        self.headers['Referer'] = 'https://note.youdao.com/signIn/index.html?&callback=https%3A%2F%2Fnote.youdao.com%2Fweb%2F&from=web'
        self.get('https://note.youdao.com/login/acc/pe/getsess?product=YNOTE&_=' + timestamp())
        self.get('https://note.youdao.com/auth/cq.json?app=web&_=' + timestamp())
        self.get('https://note.youdao.com/auth/urs/login.json?app=web&_=' + timestamp())
        data = {
            "username": username,
            "password": hashlib.md5(password).hexdigest()
        }
        self.post('https://note.youdao.com/login/acc/urs/verify/check?app=web&product=YNOTE&tp=urstoken&cf=6&fr=1&systemName=&deviceType=&ru=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&er=https%3A%2F%2Fnote.youdao.com%2FsignIn%2F%2FloginCallback.html&vcode=&systemName=&deviceType=&timestamp=' + timestamp(), data=data, allow_redirects=True)
        self.get('https://note.youdao.com/yws/mapi/user?method=get&multilevelEnable=true&_=' + timestamp())
        print(self.cookies)
        self.cstk = self.cookies.get('YNOTE_CSTK')
        '''
        try:
            cookies = self.covertCookies()
        except Exception as err:
            return format(err)
        
        for cookie in cookies:
            self.cookies.set(name=cookie[0], value=cookie[1], domain=cookie[2], path=cookie[3])
        
        self.cstk = cookies[0][1]
        if not self.cstk:
            return 'YNOTE_CSTK empty'
        print('Use Cookies login')

    def getConfig(self):
        with open(self.configPath, "r") as f:
            config = json.loads(f.read())
        return config

    def covertCookies(self):
        with open(self.cookiesPath, 'rb') as f:
            json_str = f.read().decode('utf-8')
        try:
            cookies_dict = json.loads(json_str)
            cookies = cookies_dict['cookies']
        except Exception:
            raise Exception('转换「{}」为字典时出现错误'.format(self.cookies_path))
        return cookies

    def getRoot(self):
        data = {
            'path': '/',
            'entire': 'true',
            'purge': 'false',
            'cstk': self.cstk
        }
        response = self.post('https://note.youdao.com/yws/api/personal/file?method=getByPath&keyfrom=web&cstk=%s' % self.cstk, data = data)
        print('getRoot:' + response.text)
        jsonObj = response.json()
        return jsonObj['fileEntry']['id']

    def getNote(self, id, saveDir):
        data = {
            'fileId': id,
            'version': -1,
            'convert': 'true',
            'editorType': 1,
            'cstk': self.cstk
        }
        url = 'https://note.youdao.com/yws/api/personal/sync?method=download&keyfrom=web&cstk=%s' % self.cstk
        response = self.post(url, data = data)
        with open('%s/%s.xml' % (saveDir, id), 'w') as fp:
            fp.write(response.text)

    def getNoteDocx(self, id, saveDir):
        url = 'https://note.youdao.com/ydoc/api/personal/doc?method=download-docx&fileId=%s&cstk=%s&keyfrom=web' % (id, self.cstk)
        response = self.get(url)
        with open('%s/%s.docx' % (saveDir, id), 'w') as fp:
            fp.write(response.text)

    def getFileRecursively(self, id, saveDir, doc_type):
        data = {
            'path': '/',
            'dirOnly': 'false',
            'f': 'false',
            'cstk': self.cstk
        }
        url = 'https://note.youdao.com/yws/api/personal/file/%s?all=true&f=true&len=30&sort=1&isReverse=false&method=listPageByParentId&keyfrom=web&cstk=%s' % (id, self.cstk)
        lastId = None
        count = 0
        total = 1
        if not os.path.exists(saveDir):
            os.mkdir(saveDir)
        while count < total:
            if lastId == None:
                response = self.get(url)
            else:
                response = self.get(url + '&lastId=%s' % lastId)
            # print('getFileRecursively:' + response.text)
            print('\n-------')
            jsonObj = json.loads(response.text)
            total = jsonObj['count']
            for entry in jsonObj['entries']:
                fileEntry = entry['fileEntry']
                id = fileEntry['id']
                name = fileEntry['name']
                # print('%s %s' % (id, name))
                print('%s' %(id))
                if fileEntry['dir']:
                    subDir = saveDir + '/' + name
                    try:
                        os.lstat(subDir)
                    except OSError:
                        os.mkdir(subDir)
                    self.getFileRecursively(id, subDir, doc_type)
                else:
                    with open('%s/%s.json' % (saveDir, id), 'w') as fp:
                        fp.write(json.dumps(entry,ensure_ascii=False).encode('utf-8').decode())
                    if doc_type == 'xml':
                        self.getNote(id, saveDir)
                    else: # docx
                        self.getNoteDocx(id, saveDir)
                count = count + 1
                lastId = id

    def getAll(self, doc_type):
        rootId = self.getRoot()
        self.getFileRecursively(rootId, self.metaPath, doc_type)

if __name__ == '__main__':
    '''
    if len(sys.argv) < 2:
        print('args: [saveDir [doc_type]]' )
        print('doc_type: xml or docx')
        sys.exit(1)
    '''
    # if len(sys.argv) >= 2:
    #     saveDir = sys.argv[1]
    # else:
    #     saveDir = '.'
    if len(sys.argv) >= 2:
        doc_type = sys.argv[1]
    else:
        doc_type = 'xml'
    sess = YoudaoNoteSession()
    sess.login()
    sess.getAll(doc_type)
