import uos

print("files:", uos.listdir("/flash"))

with open("/flash/pokemon_cls5_labels.txt", "r") as f:
    content = f.read()

print("read:", content)