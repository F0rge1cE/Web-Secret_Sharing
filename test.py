from fileInOut import *
from testalgo import *

if __name__ == '__main__':
    path = '/Users/xuxueyang/Desktop/04-dynamic-programming.pdf'
    path1 = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'

    content, meta = read_file_as_bytes(path, chunkSize=1)
    allShare = []
    
    print('encryp..')
    for c in content:
        byteShare = generate_polynomial(c, 10, 6)
        allShare.append(byteShare)
    
    meta.K = 6
    meta.N = 10
    re_content = []
    print('decrypt..')
    for s in allShare:
        share_list = list(s)[1:7]
        recons_share = reconstruct(share_list, 6)
        re_content.append(bytes([recons_share]))

    reconstruct_file(re_content, path1, meta)
