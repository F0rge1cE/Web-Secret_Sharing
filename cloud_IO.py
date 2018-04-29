import run

import sys
import time

import fileInOut
import betterAlgo
import bytesINT
import sharesManipulation

class CombinedShare(object):
    def __init__(self):
        self.allShares = []
        self.meta = None
        self.shareCounter = 0
    

    def addNewShare(self, shareStr):
        # Read share from STRING objects in memory. PAY ATTENTION TO THE FORMAT AND ORDER!!!
        # Param:
        #   shareStr: the pickled share string.
        # Return: 
        #   allShares: List[byte] - shares given to the algorithm
        #   meta: meta data for the file
        share_content, meta = sharesManipulation.decodeShareInMemory(shareStr)
        self.shareCounter += 1

        if self.meta is None:
            # The first share to add
            self.allShares = [[] for _ in range(meta.totalSharesByBytes)]
        else:
            if self.meta.Hash != meta.Hash:
                print('Meta data does not match!')
                raise Exception('Meta data does not match!')

        for i in range(meta.totalSharesByBytes):
                self.allShares[i].append(share_content[i])


    def getAllSharesAndMeta(self):
        return self.allShares, self.meta


    def DirectEncrypt(self, Content_all, path, N_shares, K_required, chunkSize=1):
        # Directly encrypt the content (in list[bytes]) it into N shares.
        # Param:
        #   Content: A very large STRING (usually read by the web browser.)
        #   path: the path of the file, only use for calculate the meta data here, not for reading!
        #   N_shares: number of total shares to be generated
        #   K_required: number of shares required to reconstruce the original file
        #   chunkSize: Number of bytes read from file each time. CANNOT EXCEED LENGTH OF THE PRIME NUM!
        # Return: List[string] - All N generated shares. Each share is a string.

        totalBytes = len(Content_all)
        # split the whole data into chunks
        content = [Content_all[x:x + chunkSize]
                for x in totalBytes if x % chunkSize == 0]
        meta = fileInOut.record_meta_data(
            path, content, lastChunkSize=len(content[-1]))

        allShares = []
        totalBytes = len(content) * chunkSize - chunkSize + meta.lastChunkSize
        progress = 0
        print('Encrypting...')
        startTime = time.time()

        tick = time.time()
        for c in content:
            byteShares = betterAlgo.generate_polynomial(c, N_shares, K_required)
            allShares.append(byteShares)

            # Progress report every 5 seconds
            progress += chunkSize
            percent = progress * 1.0 / totalBytes
            if time.time() - tick > 5.0:
                print("{0:.2f}% done.".format(percent * 100))
                tick = time.time()

        # set some meta properties..
        meta.totalBytes = totalBytes
        meta.K_required = K_required
        meta.N_shares = N_shares
        meta.normalChunkSize = chunkSize
        meta.totalSharesByBytes = len(content)

        print("Encrypting Cost: {0} seconds".format(time.time() - startTime))
        return allShares, meta


    def decryptAndReconstruct(self):
        # From the share(path), give back the original file.
        # Param:
        # Return: 
        #   re_content: List[string] - All N generated shares. Each share is a string.
        #   meta: meta data of the file

        if self.shareCounter < self.meta.K_required:
            raise Exception('Not enough shares are given!!!!')

        # logging
        print('Decrypting..')
        startTime = time.time()
        progress = 0
        tick = time.time()

        re_content = []
        for i in range(len(self.allShares)):
            # Use the first K_required shares to reconstruct.
            share_list = list(self.allShares[i])[:self.meta.K_required]
            recons_share = betterAlgo.reconstruct(share_list, self.meta.K_required)
            re_content.append(
                bytesINT.int_to_bytes(
                    recons_share,
                    self.meta.lastChunkSize if i == len(self.allShares) - 1 else self.meta.normalChunkSize)
            )
        # log
            progress += self.meta.normalChunkSize
            percent = progress * 1.0 / self.meta.totalBytes
            if time.time() - tick > 5.0:
                print(
                    "{0}% done.".format(int(percent * 100))
                )
                tick = time.time()

        print("Decrypting Cost: {0} seconds".format(time.time() - startTime))

        # fileInOut.reconstruct_file(re_content, filePath, self.meta)
        return re_content, self.meta


# Example of how to use it...
if __name__ == '__main__':
    shares = CombinedShare()

    # Encrypt given data..
    allShares, meta = shares.DirectEncrypt(content_original, fileName, N_shares, K_required)

    # For decryption, add each share
    for shareString in share_list:
        shares.addNewShare(shareString)
    
    # After add all shares
    original_data, meta = shares.decryptAndReconstruct()
    
    







