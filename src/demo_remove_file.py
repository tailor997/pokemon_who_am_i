import uos

print("flash files:", uos.listdir("/flash"))
print("sd files:", uos.listdir("/sd"))
print("sd files:", uos.listdir("/sd/1000_class_object_classification_model"))
# bk.png
try:
    uos.remove("/flash/bk.jpg")
except:
    print("There is no such file here.")
finally:
    print("files:", uos.listdir("/flash"))
