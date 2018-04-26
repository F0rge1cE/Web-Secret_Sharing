import sys
import time

import fileInOut 
import betterAlgo
import bytesINT


if sys.version > '3':
    PY3 = True
else:
    PY3 = False


def readAndEncrypt(filePath, N_shares, K_required, chunkSize=1):
    # Read the uploaded file and encrypt it into N shares.
    # Param:
    #   filePath: path of file
    #   N_shares: number of total shares to be generated
    #   K_required: number of shares required to reconstruce the original file
    #   chunkSize: Number of bytes read from file each time. CANNOT EXCEED LENGTH OF THE PRIME NUM!
    # Return: List[string] - All N generated shares. Each share is a string.

    content, meta = fileInOut.read_file_as_bytes(
        path=filePath, 
        chunkSize=chunkSize)

    meta.setK(K_required)
    meta.setN(N_shares)
    #####
    # TODO: Save meta data. 
    #####


    allShares = []

    totalBytes = len(content) * chunkSize
    progress = 0   
    print('Encrypting...')
    startTime = time.time()

    tick = time.time()
    for c in content:
        byteShare = betterAlgo.generate_polynomial(c, N_shares, K_required)
        allShares.append(byteShare)

        # Progress report every 5 seconds
        progress += chunkSize
        percent = progress * 1.0 / totalBytes
        if time.time() - tick > 5.0:
            print("{0:.2f}% done.".format(percent * 100))
            tick = time.time()

    print("Encrypting Cost: {0} seconds".format(time.time() - startTime))
    return byteShare


def fromSharesReconstruct(filePath, allShares, meta):
    # From the share, give back the original file.
    # Param:
    #   filePath: the path for the file to be save. DO NOT INCLUDE THE FILE NAME.
    #   allShares: List[byte] - shares given to the algorithm
    #   meta: meta data for the file to be reconstruct
    # Return: List[string] - All N generated shares. Each share is a string.
    re_content = []

    print('Decrypting..')
    startTime = time.time()
    progress = 0
    tick = time.time()

    for i in range(len(allShares)):
        share_list = list(allShares[i])[:meta.K_required]
        recons_share = betterAlgo.reconstruct(share_list, meta.K_required)
        re_content.append(
            bytesINT.int_to_bytes(
                recons_share, 
                meta.lastChunkSize if i == len(allShares) - 1 else chunkSize)
            )
    # log
        progress += chunkSize
        percent = progress * 1.0 / totalBytes
        if time.time() - tick > 5.0:
            print(
                "{0}% done.".format(int(percent * 100))
            )
            tick = time.time()

    print("Decrypting Cost: {0} seconds".format(time.time() - startTime))


    fileInOut.reconstruct_file(re_content, filePath, meta)

