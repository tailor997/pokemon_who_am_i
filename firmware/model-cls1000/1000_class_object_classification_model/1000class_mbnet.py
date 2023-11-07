import sensor, image, lcd, time
import KPU as kpu
lcd.init(type=2)
lcd.rotation(2)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_hmirror(1)
sensor.set_vflip(1) #flip camera; maix go use sensor.set_hmirror(0)
sensor.run(1)
lcd.clear()
lcd.draw_string(100,96,"MobileNet Demo")
lcd.draw_string(100,112,"Loading labels...")

f=open('labels.txt','r')
labels=f.readlines()
f.close()

task = kpu.load(0x300000)
clock = time.clock()

while(True):
    img = sensor.snapshot()
    clock.tick()
    fmap = kpu.forward(task, img)
    fps=clock.fps()

    plist=fmap[:]
    pmax=max(plist)
    max_index=plist.index(pmax)
    a = lcd.display(img, oft=(0,0))
    lcd.draw_string(0, lcd.height()-20, "%.2f:%s"%(pmax, labels[max_index].strip()))
    a=img.draw_rectangle(pmax.rect())
    print(fps)
a = kpu.deinit(task)
