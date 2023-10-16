# generated by maixhub, tested on maixpy v0.6.0_2_g9720594
# copy files to TF card and plug into board and power on

import sensor, image, lcd, time
import KPU as kpu
import gc, sys
from machine import UART
from fpioa_manager import fm

input_size = (224, 224)
labels = ['squirtle', 'bulbasaur', 'charmander', 'mewtwo', 'pikachu']

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=input_size)
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

class Comm:
    def __init__(self, uart):
        self.uart = uart

    def send_classify_result(self, pmax, idx, label):
        msg = "{}:{:.2f}:{}\n".format(idx, pmax, label)
        self.uart.write(msg.encode())

def init_uart():
    fm.register(10, fm.fpioa.UART1_TX, force=True)
    fm.register(11, fm.fpioa.UART1_RX, force=True)

    uart = UART(UART.UART1, 115200, 8, 0, 0, timeout=1000, read_buf_len=256)
    return uart

def main(labels = None, model_addr="/sd/m.kmodel", sensor_window=input_size, lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    if not labels:
        with open('pokemon_cls5_labels.txt','r') as f:
            exec(f.read())
    if not labels:
        print("no pokemon_cls5_labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no pokemon_cls5_labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("Pikachu.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

    uart = init_uart()
    comm = Comm(uart)

    try:
        task = None
        task = kpu.load(model_addr)
        while(True):
            img = sensor.snapshot()
            t = time.ticks_ms()

            t = time.ticks_ms() - t
            plist=fmap[:]
            pmax=max(plist)
            max_index=plist.index(pmax)
            img.draw_string(0,0, "%.2f : %s" %(pmax, labels[max_index].strip()), scale=2, color=(255, 0, 0))
            img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
            comm.send_classify_result(pmax, max_index, labels[max_index].strip())
            lcd.display(img)
    except Exception as e:
        raise e
    finally:
        if not task is None:
            kpu.deinit(task)


if __name__ == "__main__":
    try:
        main(labels=labels, model_addr=0x300000)
        #main(labels=labels, model_addr="/sd/model-90631.kmodel")
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
