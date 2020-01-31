# OneStepAtATime - Step counter using auto-correlation 
This project's auto-correlation algorithm is based on the paper:

`A. Rai, K. K. Chintalapudi, V. N. Padmanabhan, and R. Sen. Zee -
zero-effort crowdsourcing for indoor localization. In Mobicom ’12,
page 293, 2012` 

## What is this project about?
1. This project utilizes Contiki, using the microcontroller's  X,Y,Z accelerometer data to measure and record movements. 
2. The objective is to determine if the user is walking, in a bus or is stationery (small movements are allowed).
3. The core of the algorithm is the auto-correlation function, which can be used to find the periodicity in a noisy signaland determine if the user is on the bus, walking or stationary.

### Why use auto correlation?

While there exists many methods for step counting, the simplest one are using some threshold to determine the state. However, as with any threshold techique, the major drawback is determining the optimal level of threshold as this would defer from individual to individual.  

Instead of using threshold methodology, based on the various paper, we decided that a periodic method would inherently be better due to the cyclical nature of walking. 

### Overview of algorithm

**Idle**
When a user is idle, it is expected that acceleration would be low. Thus the standard deviation in the magnitude of accleration would be low and be a good indicator of this state. However, sudden movement will lead to a higher SD, thus, we utlized auto-correlation to detect for cyclical movement.

**Walking**
If we were to plot a graph based on the 3 axis, we could observe that walking exhibits a very periodical and repetitive pattern. We can then make use of this repeititve pattern as a way to determine the user's state. 

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
