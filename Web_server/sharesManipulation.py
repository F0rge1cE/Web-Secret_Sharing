'''
Serialize & deserialize the shares. 
In memory OR to File.
'''
# import cPickle as pickle
import pickle
import StringIO
import metaDataModel


def encodeShareInMemory(super_share_bytes, meta, serialMode=0):
    # Param:
    #   super_share_bytes: List[bytes]
    #   meta: meta of the original file
    #   serialMode: serialization mode for Pickle
    # Return: Pickled STRING

    super_share_bytes = addKeyToShare(super_share_bytes, meta)

    f = StringIO.StringIO()
    pickle.dump(super_share_bytes, f, serialMode)
    f.seek(0)   # reset the position
    return f.buf


def decodeShareInMemory(f):
    # Unpickle the serialized string in memory.
    # Param:
    #   path: String or StringIO object.
    # Return: KEY of the target file[0], Shares[1:]
    if isinstance(f, str):
        f = StringIO.StringIO(f)
    f.seek(0)
    share_content = pickle.load(f)
    newMeta = metaDataModel.metaData(0, 0)
    newMeta.initFromDict(share_content[0])

    return share_content[1:], newMeta



def encodeShareToFile(super_share_bytes, path, meta, serialMode=0):
    # Param:
    #   super_share_bytes: List[bytes]
    #   path: path to store the serialization
    #   meta: meta of the original file
    #   serialMode: serialization mode for Pickle
    # Return: None

    super_share_bytes = addKeyToShare(super_share_bytes, meta)

    with open(path,'wb') as f:
        pickle.dump(super_share_bytes, f, serialMode)
    # print('encrypt: ', path,super_share_bytes)


def decodeShareToFile(path):
    # Param:
    #   path: path to store the serialization
    # Return: KEY of the target file[0], Shares[1:]
    with open(path,'rb') as f:
        share_content = pickle.load(f)
    # print('decrypt: ', path, share_content)

    # initialize a meta data model fron the dictionary
    newMeta = metaDataModel.metaData(0, 0 )
    newMeta.initFromDict(share_content[0])

    return share_content[1:], newMeta


def addKeyToShare(share, fileMeta):
    # Param:
    #   path: original shares
    #   fileMeta: meta data of the file
    # Return: List[bytes]

    return [fileMeta.toDict()] + share




if __name__ == '__main__':
    class test(object):
        KEY = '123'

    path = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing/ctest'
    path1 = '/Users/xuxueyang/Desktop/111_share_0.share'

    # encodeShareInMemory(bytes, path, test())
    # print(bytes)
    data, meta = decodeShareInMemory(path)
    print(data)
    print(meta)

