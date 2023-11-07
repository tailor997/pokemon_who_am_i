import lcd,sensor
import image
import gc, sys
import utime
import gc
import Maix
from Maix import utils
import KPU as kpu
import time
from machine import Timer

print(gc.mem_free() / 1024) # stack mem
print(Maix.utils.heap_free() / 1024) # heap mem
utils.gc_heap_size(1024*1024) # 1MiB
print(Maix.utils.heap_free() / 1024) # heap mem

img_bk = image.Image("/flash/bk.jpg")
img_who = image.Image("/flash/who.jpg")
input_size = (224, 224)
labels = ['squirtle', 'bulbasaur', 'charmander', 'mewtwo', 'pikachu']
model_addr=0x300000


#img_sensor = image.Image(size=(320,240))
#img_sensor_show = image.Image(size=(100, 120))
#img_sensor_cls = image.Image(size=input_size)
img_sensor_cls = image.Image(size=(320,240))
def init_dev():
    lcd.init(freq=15000000)

    lcd.display(img_bk)
    lcd.display(img_who,oft=(180,45))

    #lcd.clear((21, 70, 35))

def init_sensor():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)
    sensor.skip_frames()

def sensor_show():
    img_sensor_cls = sensor.snapshot()
    #img_sensor_cls = sensor.snapshot().resize(224, 224)
    img_sensor_show = img_sensor_cls.resize(100, 120)
    print(gc.mem_free() / 1024) # stack mem
    print(Maix.utils.heap_free() / 1024) # heap mem
    lcd.display(img_sensor_show,oft=(30,28))


def init_model():
    img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)

def task_cls():
    try:
        task = None
        task = kpu.load(model_addr)
        while(True):
            t = time.ticks_ms()
            t = time.ticks_ms() - t
            fmap = kpu.forward(task, img_sensor_cls)
            plist = fmap[:]
            pmax = max(plist)
            max_index = plist.index(pmax)
            img.draw_string(0,0, "%.2f : %s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 0, 0))
            img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
    except Exception as e:
        raise e
    finally:
        if not task is None:
            kpu.deinit(task)


#init_dev()
if __name__ == "__main__":
    #try:
        #init()
    #except :
        #sys.print_exception(e)
    #finally:
        #gc.collect()
    init_dev()
    init_sensor()
    while(True):
        # utime.sleep_ms(1000)
        sensor_show()
        task_cls()
        # utime.sleep_ms(1000)
        # lcd.draw_string(180, 45, "Who am i", lcd.YELLOW, 5317)
        # utime.sleep_ms(1000)
        # lcd.fill_rectangle(180, 45, 100, 50, (21,35,70))










