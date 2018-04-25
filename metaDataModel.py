class metaData(object):
    def __init__(self, fileName, hash, N_shares=1, K_required=1):
        self.__fileName = fileName
        self.__hash = hash
        self.__N_shares = N_shares
        self.__K_required = K_required
        self.__sharesHash = []
    
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

    def setN():
        pass
    

