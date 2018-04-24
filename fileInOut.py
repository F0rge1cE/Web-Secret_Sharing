import hashlib
import os
_HASH_FUNC_ = hashlib.sha256

class metaData():
    def __init__(self, fileName, hash):
        self.fileName = fileName
        self.hash = hash
        self.N = 0
        self.K = 0


def record_meta_data(path, fileContent):
    # Calculate the Hash and name of the file
    # Param: 
    #   path: path of file
    #   fileContent: List[byte] - file content
    # Return: Metadata of file in dictionary
    fullName = os.path.split(path)[-1]
    hash = _HASH_FUNC_(''.join(fileContent)).hexdigest()
    meta = metaData(fullName, hash)
    return meta


def read_file_as_bytes(path, chunkSize=1):
    # Read given file as a stream of bytes.
    # Param: 
    #   path: path of file
    #   chunkSize: combine n bytes into one element
    # Return: List[nByte], metaData
    content = []
    try:
        with open(path, 'rb') as f:
            chunk = f.read(chunkSize)
            while chunk:
                content.append(chunk)
                chunk = f.read(chunkSize)
    except:
        raise Exception('Error in reading file!')
    finally:
        meta = record_meta_data(path, content)
        return content, meta
    

def reconstruct_file(fileContent, path, metaData=None):
    # Reconstruct the original file
    # Param:
    #   metaData: the meta data of the file
    #   fileContent: List[bytes] content of file
    #   path: the path to be written to. The filename is not given
    # Return: None
    if metaData:
        fileName = metaData.fileName
        hash = metaData.hash
    else:
        fileName = 'Not-Given'
        hash = ''
    # reset the file name.
    path = os.path.join(path, fileName)

    # reconstruct the file.
    try:
        with open(path, 'wb') as f:
            for chunk in fileContent:
                f.write(chunk)
    except:
        raise Exception('Error in writting file!')

    # check hash
    recover_hash = _HASH_FUNC_(''.join(fileContent)).hexdigest()
    if hash != recover_hash:
        print('Warning: Hash does not match!')
    

    
if __name__ =='__main__':
    path = '/Users/xuxueyang/Desktop/04-dynamic-programming.pdf'
    content, meta = read_file_as_bytes(path, chunkSize=10)
    path1 = '/Users/xuxueyang/Downloads'
    reconstruct_file(content, path1, meta)
