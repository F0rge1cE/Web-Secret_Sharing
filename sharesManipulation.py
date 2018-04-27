'''
Serialize & deserialize the shares. 
'''
import pickle

def encodeShare(super_share_bytes, path, meta, serialMode=1):
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


def decodeShare(path):
    # Param:
    #   path: path to store the serialization
    # Return: KEY of the target file[0], Shares[1:]
    with open(path,'rb') as f:
        share_content = pickle.load(f)
    # print('decrypt: ', path, share_content)
    return share_content[1:], share_content[0]


def addKeyToShare(share, fileMeta):
    # Param:
    #   path: original shares
    #   fileMeta: meta data of the file
    # Return: List[bytes]
    return [fileMeta.KEY] + share




# if __name__ == '__main__':
#     class test(object):
#         KEY = '123'

#     path = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing/ctest'
#     path1 = '/Users/xuxueyang/Desktop/ECE6102-Dependable-Distributed-System/Web-Secret_Sharing'
#     bytes = [(10,5777039903557844430036768186527487503110851800863090253527529362178407617274811626709570375169278262602087426174628508253092305817025479280549021333914750298434758008056122618084203732925598908944931456394245382144416758048020560009509368717104753153901361844865164494237072747660406518699694898423077055039705248168295378683605452087390395125582369472705736773986503154779745669773582651394503442439995078929380813494082515008944150899856292907735976225426420324017446501955694648186357007416445884916963748772602955127689106962047670315875312389286598779551827194598664574502346764321225890515403549212296395866145L)]
#     encodeShare(bytes, path, test())
#     print(bytes)
#     a = decodeShare(path)
#     print(a)

