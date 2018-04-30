import time
class metaData(object):
    def __init__(self, fileName, hash, N_shares=1, K_required=1, lastChunkSize = 0):
        self.__fileName = fileName
        self.__hash = hash
        self.__N_shares = N_shares
        self.__K_required = K_required

        self.lastChunkSize = lastChunkSize
        self.normalChunkSize = 1
        self.totalBytes = 0

        self.totalSharesByBytes = 0

    
    def toDict(self):
        dic = {
            'fileName': self.__fileName,
            'Hash': self.__hash,
            'N_shares': self.__N_shares,
            'K_reqired': self.__K_required,
            'lastChunkSize': self.lastChunkSize,
            'normalChunkSize': self.normalChunkSize,
            'totalBytes': self.totalBytes,
            'totalSharesByBytes': self.totalSharesByBytes
        }
        return dic

    def initFromDict(self, dic):
        self.__fileName = dic['fileName']
        self.__hash = dic['Hash']
        self.__N_shares = dic['N_shares']
        self.__K_required = dic['K_reqired']
        self.lastChunkSize = dic['lastChunkSize']
        self.normalChunkSize = dic['normalChunkSize']
        self.totalBytes = dic['totalBytes']
        self.totalSharesByBytes = dic['totalSharesByBytes']


    @property
    def Hash(self):
        return self.__hash
    
    @property
    def FileName(self):
        return self.__fileName

    @property
    def N_shares(self):
        return self.__N_shares
    
    @property
    def K_required(self):
        return self.__K_required

    @N_shares.setter
    def N_shares(self, n):
        if isinstance(n, int):
             self.__N_shares = n
        else:
            print("N must be an interger, now is {0}".format(n))
       
    @K_required.setter
    def K_required(self, k):
        if isinstance(k, int):
            self.__K_required = k
        else:
            print("K must be an interger, now is {0}".format(k))
    
