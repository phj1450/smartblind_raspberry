import spidev
import time
import RPi.GPIO as GPIO

ldr_channel = 0
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=100000

blind_state = 0
GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT)
p=GPIO.PWM(servo_pin,50)
p.start(0)

def readadc(adcnum):
    if adcnum > 7 or adcnum < 0 :
        return -1
    r = spi.xfer2([1,8+adcnum << 4,0])
    data = ((r[1]&3)<<8)+r[2]
    return data

try:
    while True:
        ldr = readadc(ldr_channel)
        print("LDR=%d"%(ldr))
        time.sleep(1) 
        if ldr < 30:
            p.ChangeDutyCycle(7.5)
            print("blinder up”)
            time.sleep(1)
blind_state = 0
else:
            p.ChangeDutyCycle(2.5)
print("blinder down")
time.sleep(1)
            blind_state = 1
except KeyboardInterrupt:
    GPIO.cleanup()
