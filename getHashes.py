
import hashlib
import xxhash


def getHashSum(file_path):
    hashsums = {}
    result = {}
    hashsums['xxh32'] = xxhash.xxh32()
    hashsums['xxh64'] = xxhash.xxh64()
    hashsums['md5'] = hashlib.md5()

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(64 * 1024)
            if len(chunk):
                for key in hashsums.keys():
                    hashsums[key].update(chunk)
            else:
                break

    for key, value in hashsums.items():
        result[key] = value.hexdigest()

    return result
