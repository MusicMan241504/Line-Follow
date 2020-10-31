import RPi.GPIO as GPIO

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

def setup():
    global Lp, LP1, LP2, Rp, RP1, RP2, LS, RS, EP, TP, TO
    
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

    GPIO.output(LP1,GPIO.LOW)   #turn motor pins off
    GPIO.output(LP2,GPIO.LOW)
    GPIO.output(LEn,GPIO.LOW)
    GPIO.output(RP1,GPIO.LOW)
    GPIO.output(RP2,GPIO.LOW)
    GPIO.output(REn,GPIO.LOW)

    Lp = GPIO.PWM(LEn,1000)   #create pwms
    Rp = GPIO.PWM(REn,1000)
    Lp.start(0)
    Rp.start(0)
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
