class metaData(object):
    def __init__(self, fileName, hash, N_shares=1, K_required=1):
        self.__fileName = fileName
        self.__hash = hash
        self.__N_shares = N_shares
        self.__K_required = K_required
        self.__sharesHash = []
    
    def getHash(self):
        return self.__hash
    
    def getFileName(self):
        return self.__fileName

    def getTotalShares(self):
        return self.__N_shares
    
    def getRequiredShares(self):
        return self.__K_required
    

