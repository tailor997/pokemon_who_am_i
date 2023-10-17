import lcd
import image

lcd.init()

# img = image.Image("/flash/Pikachu.jpg")
img = image.Image("/flash/bk_320240.jpg")
img.resize(50, 50)
lcd.display(img)


#lcd.draw_string(100, 100, "hello maixpy", lcd.RED, lcd.BLACK)


