import lcd,sensor
import image
import gc, sys

img_bk = image.Image("/flash/bk.jpg")
img_who = image.Image("/flash/who.jpg")

img_sensor = image.Image(size=(320,240))
img_sensor_clip = image.Image(size=(100, 120))

labels = ['squirtle', 'bulbasaur', 'charmander', 'mewtwo', 'pikachu']

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

def ui_show():
    img_sensor = sensor.snapshot()
    img_sensor_clip = img_sensor.resize(100, 120)
    lcd.display(img_sensor_clip,oft=(30,28))

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
        ui_show()







