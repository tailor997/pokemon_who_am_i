import sensor, lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames()

lcd.init(freq=15000000)

while(True):
    img = sensor.snapshot()
    img2 = img.resize(50, 50)
    #print(img)
    lcd.display(img2)
    #lcd.display(sensor.snapshot())

