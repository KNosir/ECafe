import hashlib


def convert_to_hash(var):
    var_byte = var.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(var_byte)
    var_hashed = sha256_hash.hexdigest()
    return var_hashed
