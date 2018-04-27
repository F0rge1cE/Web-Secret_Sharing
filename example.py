import sys
import time

import fileInOut
import betterAlgo
import bytesINT
import sharesManipulation
import run
import getPrime

N = 10
K = 6
ChunkSize = 255

# Optional: use a new prime
# betterAlgo._PRIME = getPrime.generateLargePrime(2048)

# The original file's path
file_path = '/Users/xuxueyang/Pictures/1.pic.jpg'

# Where to put the reconstructed file in
decrypt_path = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'

# Where you want to put the shares in.
share_paths = [
    decrypt_path + '/shares/_' + str(x) + '.share' for x in range(N)]  # issue...

# Generate shares and meta data for the original file
allShares, meta = run.readAndEncrypt(file_path, N, K, ChunkSize)

# Save shares to *share_paths
run.distributeShares(allShares, meta, *share_paths)

# Read and deserialize all shares, then decrypt the file given enough shares.
run.fromSharesFilesReconstruct(decrypt_path, meta, *share_paths)



