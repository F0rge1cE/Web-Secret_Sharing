'''
Serialize & deserialize the combined shares. 
'''
import pickle
_CHUNK_SIZE_ = 1

# def combineShares(shares):
#     # Param: 
#     #   shares: List[bytes] - all small shares generated from the same file for 1 user.
#     # Return: bytes - super_share for this user to be serialized.
#     return b''.join(shares)

def encode(super_share_bytes, path):
    # Param:
    #   super_share_bytes: List[bytes]
    #   path: path to store the serialization
    # Return: None
    with open(path,'wb') as f:
        pickle.dump(super_share_bytes, f)

def decode(path):
    # Param:
    #   path: path to store the serialization
    # Return: bytes
    with open(path,'rb') as f:
        share_content = pickle.load(f)
    return share_content


def paddingAtTail():
    pass
