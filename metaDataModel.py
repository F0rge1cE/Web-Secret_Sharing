class metaData(object):
    def __init__(self, fileName, hash):
        self.fileName = fileName
        self.hash = hash
        self.N_shares = 0
        self.K_required = 0
        self.sharesHash = []
