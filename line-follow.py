import RPi.GPIO as GPIO
import time
def pulseIn(pin,level,timeOut):   #wait for response
    t0 = time.time()
    while(GPIO.input(pin) != level):
          if((time.time() - t0) > timeOut*0.000001):
             return 200;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 200;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar(): #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(TP,GPIO.HIGH) #make trigPin send 10us high level
    time.sleep(0.00001) #10us
    GPIO.output(TP,GPIO.LOW)
    pingTime = pulseIn(EP,GPIO.HIGH,TO) #read plus time of echo pin
    distance = pingTime * 340.0 / 2.0 / 10000.0 # the sound speed is 340m/s, and calculate distance (cm)
    return round(distance)

def sense():
    Od = getSonar()   #Object distance
    Ol = GPIO.input(LS)   #left object
    Or = GPIO.input(RS)   #right object
    Ll = GPIO.input(Llp)   #left line
    Lm = GPIO.input(Lmp)   #middle line
    Lr = GPIO.input(Lrp)   #right line
    #if sensing black lines comment this out
    Ll = int(not(Ll))
    Lm = int(not(Lm))
    Lr = int(not(Lr))
    return Od, Ol, Or, (Ll, Lm, Lr)
def setup():
    global Lp, LP1, LP2, Rp, RP1, RP2, LS, RS, EP, TP, TO, Llp, Lmp, Lrp
    
    GPIO.setmode(GPIO.BOARD)
    LP1 = 11   #left motor pins
    LP2 = 13
    LEn = 15
    RP1 = 33   #right motor pins
    RP2 = 35
    REn = 37
    LS = 12   #left sensor
    RS = 16   #right sensor
    EP = 18   #ultrasonic sensor echo
    TP = 22   #trigger pin
    MD = 220
    TO = MD*60   #timeout
    #line sensing pins
    Llp = 36
    Lmp = 38
    Lrp = 40

    GPIO.setup(TP, GPIO.OUT)   # set trigger to output mode
    GPIO.setup(EP, GPIO.IN)   #echo pin to input

    GPIO.setup(LP1,GPIO.OUT)   #set motor pins to output
    GPIO.setup(LP2,GPIO.OUT)
    GPIO.setup(LEn,GPIO.OUT)
    GPIO.setup(RP1,GPIO.OUT)
    GPIO.setup(RP2,GPIO.OUT)
    GPIO.setup(REn,GPIO.OUT)
    
    GPIO.setup(LS,GPIO.IN)   #set sensor pins to input
    GPIO.setup(RS,GPIO.IN)
    
    GPIO.setup(Llp,GPIO.IN)
    GPIO.setup(Lmp,GPIO.IN)
    GPIO.setup(Lrp,GPIO.IN)

    GPIO.output(LP1,GPIO.LOW)   #turn motor pins off
    GPIO.output(LP2,GPIO.LOW)
    GPIO.output(LEn,GPIO.LOW)
    GPIO.output(RP1,GPIO.LOW)
    GPIO.output(RP2,GPIO.LOW)
    GPIO.output(REn,GPIO.LOW)

    Lp = GPIO.PWM(LEn,1000)   #create pwms
    Rp = GPIO.PWM(REn,1000)
    Lp.start(100)
    Rp.start(100)
    Lp.ChangeDutyCycle(100)
    Rp.ChangeDutyCycle(100)
def loop():
    # lmr is the status of line sesnors and is 1 if there is a line and 0 if no line
    while True:
        #get values
        Od, Ol, Or, line = sense()
        #if 010 straight
        if line == (0,1,0):
            print('forwards')
            GPIO.output(LP1,GPIO.HIGH)
            GPIO.output(LP2,GPIO.LOW)
            GPIO.output(RP1,GPIO.HIGH)
            GPIO.output(RP2,GPIO.LOW)
        #if 000 straight
        if line == (0,0,0):
            print('forwards')
            GPIO.output(LP1,GPIO.HIGH)
            GPIO.output(LP2,GPIO.LOW)
            GPIO.output(RP1,GPIO.HIGH)
            GPIO.output(RP2,GPIO.LOW)
        #if 100 left
        if line == (1,0,0):
            print('left')
            GPIO.output(LP1,GPIO.LOW)
            GPIO.output(LP2,GPIO.HIGH)
            GPIO.output(RP1,GPIO.HIGH)
            GPIO.output(RP2,GPIO.LOW)
        #if 001 right
        if line == (0,0,1):
            print('right')
            GPIO.output(LP1,GPIO.HIGH)
            GPIO.output(LP2,GPIO.LOW)
            GPIO.output(RP1,GPIO.LOW)
            GPIO.output(RP2,GPIO.HIGH)
        #if 111 stop
        if line == (1,1,1):
            print('stop')
            GPIO.output(LP1,GPIO.LOW)
            GPIO.output(LP2,GPIO.LOW)
            GPIO.output(RP1,GPIO.LOW)
            GPIO.output(RP2,GPIO.LOW)
        #if 110 left
        if line == (1,1,0):
            print('left')
            GPIO.output(LP1,GPIO.LOW)
            GPIO.output(LP2,GPIO.HIGH)
            GPIO.output(RP1,GPIO.HIGH)
            GPIO.output(RP2,GPIO.LOW)
        #if 011 right
        if line == (0,1,1):
            print('right')
            GPIO.output(LP1,GPIO.HIGH)
            GPIO.output(LP2,GPIO.LOW)
            GPIO.output(RP1,GPIO.LOW)
            GPIO.output(RP2,GPIO.HIGH)
        #wait
    time.sleep(0.1)
def destroy():
    Lp.stop()
    Rp.stop()
    GPIO.cleanup()
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
