import math

FREQUENCY = 1.0/20.0
ReadingsPerSecond = 20.0
magReadings = []
STATUS = "IDLE"

LAG_MIN = 16
LAG_MAX = 40

def calculateSquared(num):
    return num**2


def calculateMagnitude(x, y, z):
    tempMag = calculateSquared(x) + calculateSquared(y) + calculateSquared(z)
    return math.sqrt(tempMag)


def calculateSD(data, begin, end):
    # e.g I have 170 values, 169 will be my last index. But since im always adding +20 for 1 second i have to check if it exists or not
    if(end > len(data)):
        end = len(data)
    sum = 0.0
    average = calculateAverage(data, begin, end) #average of 1 second from begin + 20
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

def maxNASC(index, magReadings):
    maxNacReading = 0.00 #correlation is from 0 to 1
    for lag in range(LAG_MIN, LAG_MAX):
        tempNac = calculateNASC(index, magReadings, lag)
        if(tempNac > maxNacReading):
            maxNacReading =  tempNac
    
    return maxNacReading
        

def calculateNASC(index,magReadings, lag):
    end = index + lag
    avgForReading = calculateAverage(magReadings,index,end)
    sdForReading = calculateSD(magReadings,index,end)

    avgForLag = calculateAverage(magReadings,end,end + lag)
    sdForLag = calculateSD(magReadings,end,end + lag)

    sum = 0.0
    for x in range(index, index + lag):
        top = magReadings[x] - avgForReading
        bottom = magReadings[x + lag] - avgForLag
        sum += top * bottom

    normalization = lag * sdForReading * sdForLag
    if(normalization  == 0):
        return 0

    return sum/normalization


def processDataReadings(index,magReadings):
    # print("Index:" + str(index) + " With magnitude: " + str(magReadings[index]))
    # Calculate SD for 1 second to detect if there is any large variation
    autoCorrelations = []

    global STATUS
    
    sd = calculateSD(magReadings,index,index + int(ReadingsPerSecond))
    
    print("Index:" + str(index) + " With SD: " + str(sd))

    if(sd < 0.02):
        STATUS = "IDLE"
        print(STATUS)
    else:
        for i in range(index, min(len(magReadings) - 2*LAG_MAX, index+20)):
            autoCorrelationValue = maxNASC(i,magReadings)
            autoCorrelations.append(autoCorrelationValue)

            #acChosen = max(autoCorrelations)
            acChosen = calculateAverage(autoCorrelations, 0, 20)
            #Since im not idle, i want to loop through all the lag range to find the lag with the highest correlation
        
        print(acChosen)
        if (acChosen > 0.6 and sd > 0.17):
            STATUS ="WALKING"
        elif (acChosen > 0.4 and sd < 0.05):     
            STATUS = "DRIVING"
        elif (acChosen > 0.4 and sd > 0.2):
            STATUS = "WALKING"
        
        print(STATUS)

def main():
    file = open("Idle2", "r")
    readings = []
    for line in file:
        data = line.split()
        for reading in data:
            readings.append(float(reading))
    # Reading has all the data in the form of [x1,y1,z1,x2,y2,z2....]
    magReadings = []
    for x in range(0, len(readings), 3):
        temp = calculateMagnitude(readings[x], readings[x+1], readings[x+2])
        magReadings.append(temp)  # Converts all into their magnitude
    # print(magReadings)
    for index in range(0, len(magReadings) - LAG_MAX*2, 20):
        processDataReadings(index, magReadings)
    print("magReadingAvg:" + str(calculateAverage(magReadings, 0, len(magReadings))))
    print("magReadingMax:" + str(max(magReadings)))
    # status = processDataReadings(magReadings)
    # for s in status:
    #     print(s)
    
if __name__ == '__main__':
    main()
