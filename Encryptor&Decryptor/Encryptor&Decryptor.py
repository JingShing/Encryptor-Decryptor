from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from ttkthemes import ThemedStyle

# save and load
def save_file(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        for line in data:
            if isinstance(line, bytes):
               line = line.decode("utf-8") + '\n'
            f.write(line)
    f.close()

def load_file(path):
    data = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            data.append(line)
    return data

# encrypt and decrypt
import base64
def key_line_len(line, key):
    if len(key)>0:
        while len(key)<len(line):
            key += key
    else:
        key = key_line_len(line, 'RRR')# default key
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

# window
class Gui_helper_main:# I don't like to stuff all widget in main root so I use class to manage class and root.
    def __init__(self):
        self.root = Tk()
        self.style = ThemedStyle(self.root)
        self.style.set_theme('adapta')
        self.root.config(bg='#FAFBFC')
        self.frame = None
        self.frame_index = 0
        self.root.geometry('350x220')# main window size
        self.root.resizable(width=False, height=False)
        self.root.title('Encryptor&Decryptor加解密工具')
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        # maker info
        self.maker_name = Label(self.root, text="Maker : JingShing")
        self.maker_name.grid(column=0, row=3, sticky=N+W, padx=(5, 0))
        
        self.frames = [page_module(self)]
        self.switch_frame(0)
        
    def switch_frame(self, index):# switch different page and init
        if self.frame is not None:
            self.frame.grid_forget()
        self.frame_index = index
        self.frame = self.frames[self.frame_index]
        self.frame.grid(column=0, row=0, sticky=N+W, padx=(5, 0))

    def run(self):# run the mainloop
        self.root.mainloop()

    def quit(self):# if quit will pop a window to confirm
        self.root.quit()

class page_module(Frame):# I use page class to manage tkinter widget
    def __init__(self, master):
        Frame.__init__(self, master = master.root)
        self.main = master
        self.master = master.root
        self.data = []
        self.file_name = 'None'
        self.status = 'None'
        self.now_file_str = 'Now file : '
        self.now_status_str = 'Now status : '

        self.key_label = Label(self, text='Key密鑰')
        self.key_label.grid(column=0, row=0, sticky=N+W)
        self.key_text = Text(self, width=40, height=5)# result text box
        self.key_text.grid(column=0, row=1, sticky=N+W, rowspan=7, columnspan=5)
        self.import_button = Button(self, text='import導入', command=self.import_set)
        self.import_button.grid(column=0, row=9, sticky=N+W, pady=5)
        self.decrycpt_button = Button(self, text='decrycpt解密', command=self.decrypt_file)
        self.decrycpt_button.grid(column=1, row=9, sticky=N+W, pady=5)
        self.encrycpt_button = Button(self, text='encrycpt加密', command=self.encrypt_file)
        self.encrycpt_button.grid(column=2, row=9, sticky=N+W, pady=5)

        self.now_file_name = StringVar()
        self.now_file = Label(self, textvariable=self.now_file_name)
        self.now_file.grid(column=0, row=10, sticky=N+W)
        self.status_name = StringVar()
        self.now_status = Label(self, textvariable=self.status_name)
        self.now_status.grid(column=0, row=11, sticky=N+W)
        self.set_label_text()

    def set_label_text(self):
        self.now_file_name.set(self.now_file_str + self.file_name)
        self.status_name.set(self.now_status_str + self.status)


    def import_set(self):# import spell book
        set_path = filedialog.askopenfilename()
        if set_path:
            self.status = 'File'
            self.file_name = set_path.split('/')[-1]
            self.now_file_name.set(self.now_file_str + self.file_name)
            self.data = load_file(set_path)
        self.set_label_text()

    def encrypt_file(self):
        if self.file_name != 'None' and len(self.data)>0:
            key = self.key_text.get("1.0",END)
            file_name = self.file_name.split('.')
            save_path = file_name[0] + '_en.' + file_name[-1]
            save_file(save_path, list_encrypt(self.data, key))
            self.status = 'Done enc'
        self.set_label_text()

    def decrypt_file(self):
        if self.file_name != 'None' and len(self.data)>0:
            key = self.key_text.get("1.0",END)
            file_name = self.file_name.split('.')
            save_path = file_name[0] + '_de.' + file_name[-1]
            save_file(save_path, list_decrypt(self.data, key))
            self.status = 'Done dect'
        self.set_label_text()

main = Gui_helper_main()
main.run()