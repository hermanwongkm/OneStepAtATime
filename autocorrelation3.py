USING_SERIAL = False

import time
import math
from threading import Thread
from threading import Timer
from queue import Queue
from functools import partial
import re
import sys

# Handle Serial vs MQTT
# -------------------------------------
if USING_SERIAL:
    import serial
else:
    import paho.mqtt.client as mqtt

ser = None
client = None
if USING_SERIAL:
    try:
        ser = serial.Serial(
        port='/dev/ttyACM0',\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0)
    except serial.serialutil.SerialException as a:
        print("Failure on connecting to the Serial Port")
        sys.exit(1)
    except:
        print("Serial Port Exception")
    #     # print(error)
else:
    client = mqtt.Client()
# ------------------------------------
# Global Variables
# ------------------------------------
SENDING_RATE = 50

magReadings = []

lagMin = 40
lagMax = 100
timestamp = "Timestamp: 0.00"
# ------------------------------------
# REGEX PATTERNS
# ------------------------------------
DECIMAL_PATTERN = "[0-9]+\.[0-9]+"
ACC_PATTERN = "{}\s{}\s{}".format(DECIMAL_PATTERN, DECIMAL_PATTERN, DECIMAL_PATTERN)
LIGHT_PATTERN = "{}".format(DECIMAL_PATTERN)
DATALINE_PATTERN = "{},\s{}".format(ACC_PATTERN, LIGHT_PATTERN)

def calculateSquared(num):
    return num**2

def calculateMagnitude(x, y, z):
    tempMag = calculateSquared(x) + calculateSquared(y) + calculateSquared(z)
    return math.sqrt(tempMag)

def calculateSD(data, begin, end):
    if(end > len(data)):
        end = len(data)
    sum = 0.0
    average = calculateAverage(data, begin, end) 
    for k in range(begin, end): 
        sum += calculateSquared(data[k] - average)
    return math.sqrt(sum/(end-begin))

def calculateAverage(data, begin, end):
    sum = 0.0
    if(end > len(data)):
        end = len(data)
    count = end - begin 
    for k in range(begin, end):
        if (k >= len(data)):
            break
        sum += data[k]

    return sum/count

def getMagnitudeAndLight(rawDataLine):

    reObject = re.search(DATALINE_PATTERN, rawDataLine)
    if reObject == None:
        return None

    rawDataLine = reObject.group()

    rawDataLineArray = rawDataLine.split(",")
    rawAccData = rawDataLineArray[0]
    rawLightData = rawDataLineArray[1]
    # rawAccData = rawDataLine
    accValues = rawAccData.split(" ")
    lightValue = rawLightData.strip()
    # return calculateMagnitude(float(accValues[1]), float(accValues[2]), float(accValues[3]))
    return calculateMagnitude(float(accValues[0]), float(accValues[1]), float(accValues[2])), float(lightValue)

def maxNASC(index, magReadings):
    maxNacReading = 0.00 #correlation is from 0 to 1
    for lag in range(lagMin, lagMax):
        tempNac = calculateNASC(index, magReadings, lag)
        if tempNac > 0.6:
            return tempNac
        if(tempNac > maxNacReading):
            maxNacReading =  tempNac
    
    return maxNacReading

def calculateNASC(index, magReadings, lag):
    middle = index - lag
    begin = middle - lag
    avgForLag = calculateAverage(magReadings,begin,middle)
    sdForLag = calculateSD(magReadings,begin,middle)

    avgForReading = calculateAverage(magReadings,middle,index)
    sdForReading = calculateSD(magReadings,middle,index)

    sum = 0.0
    for x in range(index - lag, index):
        top = magReadings[x - lag] - avgForLag
        bottom = magReadings[x] - avgForReading
        sum += top * bottom

    normalization = lag * sdForReading * sdForLag
    if(normalization  == 0):
        return 0

    return sum/normalization 

def on_message(packetMsgsQ, client, userdata, msg):
    packetMsgsQ.put(msg.payload.decode("utf-8"))

def on_connect(client, userdata, flags, rc):
    print("Trying to connect...")
    
    if(rc == 0):
        print("Connected to MQTT server successfully")
        client.subscribe("#")

    elif(rc == 1):
        print("Connection refused - Incorrect protocol version")
    elif(rc == 2):
        print("Connection refused - Invalid client identifier")
    elif(rc == 3):
        print("Connection refused - Server unavailable")
    elif(rc == 4):
        print("Connection refused - Bad username/ password")
    elif(rc == 5):
        print("Connection refused - Not authorised")
    

def connectToMQTT(packetMsgsQ):
    client.on_message = partial(on_message, packetMsgsQ)
    client.on_connect = on_connect

    client.username_pw_set("cherrycecegoh@gmail.com", "21Flna3QhGMt3kGc")
    client.tls_set("cacert.pem", tls_version=2)
    try:
        client.connect("indriya.comp.nus.edu.sg", port=8080)

        client.loop_start()
        time.sleep(4)
    except:
        print("Failure on connecting to the MQTT_server")
        sys.exit(1)
    
def connectToSerial(packetMsgsQ):
    print("Connected to Serial Port successfully")
    time.sleep(3)
    counter = 0

    # Handles data collected during sleep
    t_end = time.time() + 1
    while time.time() < t_end:
        ser.read()

    while(1):
        buffer = ""
        while (1):
            x = ser.read().decode("utf-8")
            if x == "\n":
                break
            buffer += x

        if(len(buffer) > 0):
            packetMsgsQ.put(buffer)
            if counter < 10:
                print(buffer)
                counter += 1

def main():
    global timestamp

    packetMsgsQ = Queue()

    dataThread = None
    if USING_SERIAL:
        dataThread = Thread(target=connectToSerial, args = (packetMsgsQ,))
    else:
        dataThread = Thread(target=connectToMQTT, args = (packetMsgsQ,))

    dataThread.setDaemon(True)
    dataThread.start()
    
    counter = 0
    index = 0
    STATUS = "STATIONARY"
    PREVIOUS_STATUS = ""
    LIGHT_STATUS = "LIGHT"
    PREVIOUS_LIGHT_STATUS = ""
    
    while 1:
        dataline = packetMsgsQ.get(block=True)
        magnitudeAndLight = getMagnitudeAndLight(dataline)
        if magnitudeAndLight == None:
            continue
        magnitude = magnitudeAndLight[0]
        light = magnitudeAndLight[1]
        magReadings.append(magnitude)

        if len(magReadings) > 20:
            sd = calculateSD(magReadings, index - 20, index)
            # print("SD" + str(sd))

            if (sd < 0.02):
                STATUS = "STATIONARY"

            elif(counter >= lagMax*2): 
                autoCorrelationValue = maxNASC(counter, magReadings)
                # print("Autocorr: " + str(autoCorrelationValue))
                if (autoCorrelationValue > 0.6 and sd > 0.17):
                    STATUS ="WALKING"
                elif (autoCorrelationValue > 0.4 and sd < 0.08):     
                    STATUS = "STATIONARY"
                elif (autoCorrelationValue > 0.4 and sd > 0.2):
                    STATUS = "WALKING"

        if light > 10:
            LIGHT_STATUS = "LIGHT"
        else:
            LIGHT_STATUS = "DARK"

        if STATUS != PREVIOUS_STATUS or LIGHT_STATUS != PREVIOUS_LIGHT_STATUS:
            print(str(time.time()) + ", " + STATUS + "/" + LIGHT_STATUS + "-------------------------")

        PREVIOUS_STATUS = STATUS
        PREVIOUS_LIGHT_STATUS = LIGHT_STATUS
        counter += 1    

if __name__ == "__main__":
    main()
