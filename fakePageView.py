import urllib2
import json
import requests
import time
import threading

class FakePageView:
    def __init__(self):
        self.array = []
        self.url = ['FIRST_URL','SECOND_URL']
        self.yinTotal = 0
        self.alarmTotal = 0
        self.yinSuccess = 0
        self.alarmSuccess = 0
        self.loopTimes = 10
        self.threads = 5

    def alarmRequest(self, ipAddr, url):
        proxy = urllib2.ProxyHandler({'http': ipAddr})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        if url == self.url[0]:
            self.yinTotal += 1
        else:
            self.alarmTotal += 1
        try:
            data = urllib2.urlopen(request, timeout=1)
            if url == self.url[0]:
                self.yinSuccess += 1
            else:
                self.alarmSuccess += 1
            print "%s %s request success" %(url,ipAddr)
        except:
            print "%s %s request failed" %(url,ipAddr)

    def countSuccess(self,url):
        for i in self.array:
            count = 0
            while count < 5:
                count += 1
                self.alarmRequest(i, url)
        print 'yintianxia total requests: %s' %self.yinTotal
        print 'yintianxia success requests: %s' %self.yinSuccess
        print 'dinpan total requests: %s' %self.alarmTotal
        print 'dinpan success requests: %s' %self.alarmSuccess

    def refreshArray(self):
        data = requests.get('URL_TO_GET_PROXY_IP_ADDRESS')
        ipAddr = data.text.encode()
        ip = ipAddr.split('\r\n')
        self.array = ip
        print ip
        with open("ipAddress.txt", 'ab+') as f:
            f.write('\n===================================\n')
            f.write('new ip address:\n')
            f.write('===================================\n')
            f.write(ipAddr)

    def threadControl(self):
        self.refreshArray()
        count = 0
        length = len(self.array)
        while count < length:
            t1 = threading.Thread(target=self.countSuccess,args=(self.url[1],))
            t2 = threading.Thread(target=self.countSuccess,args=(self.url[0],))
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            print "%d  threading is finished" %count
            count += 1
            self.refreshArray()

    def multiThread(self):
        self.refreshArray()
        count = 0
        while count < self.loopTimes:
            threading_list = []
            for i in range(self.threads):
                threading_list.append(threading.Thread(target=self.countSuccess, args=(self.url[1],), name='alarm-thread-' + str(i)))
                threading_list.append(threading.Thread(target=self.countSuccess, args=(self.url[0],), name='yin-thread-' + str(i)))
            print threading_list
            for t in threading_list:
                t.start()
            for t in threading_list:
                t.join()
            print "%d  threading is finished" %count
            count += 1
            self.refreshArray()

if __name__ == "__main__":
    test = FakePageView()
    test.multiThread()
