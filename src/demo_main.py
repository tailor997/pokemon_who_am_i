import lcd,sensor
import image
import gc, sys

img_bk = image.Image("/flash/bk.jpg")
img_who = image.Image("/flash/who.jpg")

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
    img = sensor.snapshot()
    img2 = img.resize(100, 100)
    lcd.display(img2,oft=(30,30))

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
    ui_show()







