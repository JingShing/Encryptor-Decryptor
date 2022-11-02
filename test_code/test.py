from encrypt_and_decrypt import *
from save_and_load import *
load_path = 'text.txt'
save_path = 'output.txt'
key = 'RRR'
data = list_encrypt(load_file(load_path), key)
# print(data)
save_file(save_path, data)
data2 = list_decrypt(load_file(save_path), key)
# print(data2)
save_file('out2.txt', data2)