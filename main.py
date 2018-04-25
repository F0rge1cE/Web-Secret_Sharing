from fileInOut import *
from testalgo import *

if __name__ == '__main__':
    path = '/Users/xuxueyang/Pictures/1.pic.jpg'
    path1 = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'

    N = 10
    K = 6

    content, meta = read_file_as_bytes(path, chunkSize=1)
    # meta = record_meta_data(path, content, N, K)

    allShare = []
    print('encryp..')
    for c in content:
        byteShare = generate_polynomial(c, N, K)
        allShare.append(byteShare)
    
    re_content = []
    print('decrypt..')
    for s in allShare:
        share_list = list(s)[1:7]
        recons_share = reconstruct(share_list, K)

        re_content.append(
            str(
                bytearray([recons_share]))
                )  # works on python 2.7

        # re_content.append(bytes([recons_share]))    # works on python 3.6

    print(meta.getHash())

    reconstruct_file(re_content, path1, meta)
    
