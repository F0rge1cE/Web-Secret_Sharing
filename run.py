import sys
import time

import fileInOut 
import betterAlgo
import bytesINT
import sharesManipulation


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
    #####
    # TODO: Save meta data.
    #####

    print("Encrypting Cost: {0} seconds".format(time.time() - startTime))
    return allShares, meta


def distributeShares(allShares, meta, *paths):
    # Generate share files and distribute them
    # Param:
    #   allShares: List[string] - shares given to the algorithm
    #   meta: meta data for the file to be reconstruct
    #   *path: paths that shares are going to..
    # Return: List[string] - All N generated shares. Each share is a string.

    N_shares = meta.N_shares
    num_paths = len(paths)
    if num_paths > N_shares:
        print('Number of share is {0}, given {1} paths!'.format(
            N_shares, num_paths))
        print('Additional shares will be give to the first path!')

    # print(allShares)

    for i in range(N_shares):
        data_per_share = [x[i] for x in allShares]
        # for s in allShares:
        #     data_per_share.append(s[i])

        # print(data_per_share)

        sharesManipulation.encodeShare(
            data_per_share, paths[i % num_paths], meta)
            # allShares[i], paths[i % num_paths], meta)


def collectShares(meta, *sharePaths):
    # Read share files into the memory. PAY ATTENTION TO THE FORMAT AND ORDER!!!
    # Param:
    #   meta: meta data for the file to be reconstruct
    # Return: allShares: List[byte] - shares given to the algorithm

    #####
    #   Format of allShares: [[(), (), ...., ()], [(), (), ...., ()], ..., []] 
    #####
    allShares = [[] for _ in range(meta.totalSharesByBytes)]
    for path in sharePaths:
        content, key = sharesManipulation.decodeShare(path)
        # print(content)
        for i in range(meta.totalSharesByBytes):
            allShares[i].append(content[i])

    # print(allShares)

    return allShares, key


def fromSharesFilesReconstruct(filePath, meta, *sharePaths):
    # From the share(path), give back the original file.
    # Param:
    #   filePath: the path for the file to be save. DO NOT INCLUDE THE FILE NAME.
    #   allShares: List[byte] - shares given to the algorithm
    #   meta: meta data for the file to be reconstruct
    # Return: List[string] - All N generated shares. Each share is a string.

    if sharePaths is None or len(sharePaths) < meta.K_required:
        raise Exception('Not enough shares are given!!!!')

    allShares = []
    # for path in sharePaths:
    #     content, key = sharesManipulation.decodeShare(path)
    #     allShares.append(content)
    allShares, key = collectShares(meta, *sharePaths)

    # logging
    print('Decrypting..')
    startTime = time.time()
    progress = 0
    tick = time.time()

    re_content = []
    for i in range(len(allShares)):
        # Use the first K_required shares to reconstruct.
        share_list = list(allShares[i])[:meta.K_required]
        recons_share = betterAlgo.reconstruct(share_list, meta.K_required)
        re_content.append(
            bytesINT.int_to_bytes(
                recons_share, 
                meta.lastChunkSize if i == len(allShares) - 1 else meta.normalChunkSize)
            )
    # log
        progress += meta.normalChunkSize
        percent = progress * 1.0 / meta.totalBytes
        if time.time() - tick > 5.0:
            print(
                "{0}% done.".format(int(percent * 100))
            )
            tick = time.time()

    print("Decrypting Cost: {0} seconds".format(time.time() - startTime))


    fileInOut.reconstruct_file(re_content, filePath, meta)

