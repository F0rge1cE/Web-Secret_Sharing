import sys
import time

# Own package
from fileInOut import *
# from testalgo import *
from betterAlgo import *
import bytesINT

if sys.version > '3':
    PY3 = True
else:
    PY3 = False

if __name__ == '__main__':
    # path = '/Users/xuxueyang/Pictures/1.pic.jpg'
    # path1 = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'
    path = '/Users/xuxueyang/Desktop/04-dynamic-programming.pdf'
    path1 = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'

    N = 10
    K = 6
    chunkSize = 4

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

    for s in allShare:
        share_list = list(s)[1:7]
        # print(share_list)
        recons_share = reconstruct(share_list, K)

        if not PY3:
            re_content.append(
                # Formalize int to bytes here!!
                bytesINT.int_to_bytes(recons_share, chunkSize)
            )  # works on python 2.7


        else:
            re_content.append(bytes([recons_share]))    # works on python 3.6

    print("Eecrypting Cost: {0} secdong", [time.time() - startTime])

    # print(meta.Hash)

    reconstruct_file(re_content, path1, meta)


    for x in zip(re_content, content):
        if x[0] != x[1]:
            print(x)
    
