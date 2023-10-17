import uos

print("files:", uos.listdir("/flash"))

# bk.png
try:
    uos.remove("/flash/bk.png")
except:
    print("There is no such file here.")
finally:
    print("files:", uos.listdir("/flash"))
