import base64
path = 'text.txt'
f = open(path)
text = []
for line in f:
    line = base64.b64encode(bytes(line, 'utf-8'))
    text.append(line)
print(text)

for line in text:
    print(base64.b64decode(line).decode(), end='')
