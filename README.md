# OneStepAtATime
## Step counter using auto-correlation 

1. This project utilizes Contiki, a microcontroller's accelerometer to measure and record movements. 
2. Next, this data is then processed through the python file.
3. The core of the algorithm is the autoc-orrelation function, which can be used to find the periodicity in a noisy signaland determine if the user is on the bus, walking or stationary. 


### Running 

Dependencies:
-Python3
-Pip3
-Paho-MQTT
-PySerial

Compiling:
1. Install dependencies.
2. Enter the project directory.
3. To make the files: make TARGET=srf06-cc26xx BOARD=sensortag/cc2650 sensors_data_comm.bin CPU_FAMILY=cc26xx

Using MQTT:
1. Copy and paste your cacert.pem file into the project directory.
2. Open autocorrelation.py
2a. Inside, go to line 160 and change the email and password to your email and password
2b. Change the USING_SERIAL value to "False"

Using Serial Port:
1. Open autocorrelation.py
2. Change USING_SERIAL value to "True" 
