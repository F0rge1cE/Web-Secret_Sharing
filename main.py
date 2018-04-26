import sys
import time

from fileInOut import *
from betterAlgo import *
import bytesINT

if sys.version > '3':
    PY3 = True
else:
    PY3 = False

if __name__ == '__main__':
    # path = '/Users/xuxueyang/Pictures/1.pic.jpg'
    # path1 = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'
    path = '/Users/xuxueyang/Desktop/cracking-coding-interview-6th-programming.pdf'
    path1 = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'

    N = 10
    K = 6
    chunkSize = 255 # num of bytes read each time

    content, meta = read_file_as_bytes(path, chunkSize=chunkSize)

    totalBytes = len(content) * chunkSize
    progress = 0

    allShare = []
    print('encrypting..')
    startTime = time.time()

    tick = time.time()
    for c in content:
        byteShare = generate_polynomial(c, N, K)
        allShare.append(byteShare)

        # log
        progress += chunkSize
        percent = progress * 1.0 / totalBytes
        if time.time() - tick > 5.0:
            print(
                "{0}% done.".format(int(percent * 100))
            )
            tick = time.time()


    print("Encrypting Cost: {0} seconds".format(time.time() - startTime))

    ######
    re_content = []

    print('decrypting..')
    startTime = time.time()
    progress = 0
    tick = time.time()

    for i in range(len(allShare)):
        share_list = list(allShare[i])[1:7]
        recons_share = reconstruct(share_list, K)

        re_content.append(
            bytesINT.int_to_bytes(
                    recons_share, 
                    meta.lastChunkSize if i == len(allShare) - 1 else chunkSize)
            )

        progress += chunkSize
        percent = progress * 1.0 / totalBytes
        if time.time() - tick > 5.0:
            print(
                "{0}% done.".format(int(percent * 100))
            )
            tick = time.time()

    print("Decrypting Cost: {0} seconds".format(time.time() - startTime))


    reconstruct_file(re_content, path1, meta)

    for x in zip(re_content, content):
        if x[0] != x[1]:
            print(x)
    
