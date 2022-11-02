import base64
def key_line_len(line, key):
    if len(key)>0:
        while len(key)<len(line):
            key += key
    return key

# encryption
def encrypt(line, key):
    key = key_line_len(line, key)
    en_str = ""
    for i,j in zip(line,key): # i is data, j is key
        temp = str(ord(i)+ord(j))+'_' # encryption character = character Unicode + key Unicode
        en_str = en_str + temp
    s1 = base64.b64encode(en_str.encode("utf-8"))
    return s1

# decryption
def decrypt(line, key):
    key = key_line_len(line, key)
    p = base64.b64decode(line).decode("utf-8")
    de_str = ""
    for i,j in zip(p.split("_")[:-1],key): # i is data, j is key
        temp = chr(int(i) - ord(j)) # decryption = (encryption Unicode碼字符 - key Unicode) character
        de_str = de_str+temp
    return de_str

def list_encrypt(data, key):
    en_list = []
    for line in data:
        en_list.append(encrypt(line, key))
    return en_list

def list_decrypt(data, key):
    de_list = []
    for line in data:
        de_list.append(decrypt(line, key))
    return de_list

def test():
    line = 'hello'
    key = 'RRR'
    en = encrypt(line, key)
    print(en)
    print(decrypt(en, key))