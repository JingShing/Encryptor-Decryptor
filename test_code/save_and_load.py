def save_file(path, data):
    with open(path, 'w', encoding="utf-8") as f:
        for line in data:
            if isinstance(line, bytes):
               line = line.decode("utf-8") + '\n'
            f.write(line)
    # f.writelines(data)
    f.close()

def load_file(path):
    data = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            data.append(line)
    return data