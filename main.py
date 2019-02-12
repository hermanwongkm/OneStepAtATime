import math

FREQUENCY = 1.0/20.0
ReadingsPerSecond = 20.0
defaultMinτ = 40
defaultMaxτ = 100


def calculateSquared(num):
    return num**2


def calculateMagnitude(x, y, z):
    tempMag = calculateSquared(x) + calculateSquared(y) + calculateSquared(z)
    return math.sqrt(tempMag)

def calculateSD(data,begin,end):
    sum = 0.0
    average = calculateAverage(data,begin,end)
    for k in range(begin,end+1):
        sum += calculateSquared(data[k] - average)
    return math.sqrt(sum/ReadingsPerSecond)


def calculateAverage(data,begin,end):
    sum = 0.0
    for k in range(begin,end+1):
        sum += data[k]
    return sum/ReadingsPerSecond
    

def batshitCrazyThingHere(magReadings):
    sd = calculateSD(magReadings,60,80)
    print(sd)
    if(sd < 0.01):
        print("Idle")

def main():
    file = open("stationery.txt", "r")
    readings = []
    for line in file:
        data = line.split()
        for reading in data:
            readings.append(float(reading))
    # Reading has all the data in the form of [x1,y1,z1,x2,y2,z2....]
    magReadings = []
    for x in range (0,len(readings),3):
        temp = calculateMagnitude(readings[x],readings[x+1],readings[x+2])
        magReadings.append(temp) #Converts all into their magnitude
    # print(len(magReadings))
    batshitCrazyThingHere(magReadings)


if __name__ == '__main__':
    main()
