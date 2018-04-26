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
    # Calculate the Hash and name of the file
    # Param:
    #   filePath: path of file
    #   N_shares: List[byte] - file content
    #   K_required: number of shares required to reconstruce the original file
    #   chunkSize: Number of bytes read from file each time. CANNOT EXCEED LENGTH OF THE PRIME NUM!
    # Return: List[string] - All N generated shares. Each share is a string.

    content, meta = fileInOut.read_file_as_bytes(
        path=filePath, 
        chunkSize=chunkSize)

    totalBytes = len(content) * chunkSize
    progress = 0

    allShares = []
    print('Encrypting...')
    startTime = time.time()

    tick = time.time()
    for c in content:
        byteShare = betterAlgo.generate_polynomial(c, N, K)
        allShares.append(byteShare)

        # Progress report every 5 seconds
        progress += chunkSize
        percent = progress * 1.0 / totalBytes
        if time.time() - tick > 5.0:
            print("{0:.2f}% done.".format(percent * 100))
            tick = time.time()

    print("Encrypting Cost: {0} seconds".format(time.time() - startTime))
    return byteShare


