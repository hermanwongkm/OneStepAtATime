import math

FREQUENCY = 1.0/20.0
ReadingsPerSecond = 20.0
defaultMinτ = 40
defaultMaxτ = 100

LAG_MIN = 40
LAG_MAX = 100

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
    for second in range(0, magReadings/20):
        sd = calculateSD(magReadings, second, second+20)
        if (sd < 0.01):
            print("Idle")
        else:
            print("Unknown")

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

# NASC stuff below
def a(n):
    return magReadings[n]
    
def mean(m, t):
    sum = 0
    for i in range(m, m+lag):
        sum += a(i)
    return sum / lag

def std(m, t):
    mu = mean(m, t)
    sum = 0
    for i in range(m, m+lag):
        sum+= (a(i)-mu)^2
    return sum / lag

def nac(m, lag):
    for k  in range(0, lag):
        num = (a(m+k) - mean(m, lag)) * (a(m+k+lag) - mean(m+lag, lag))
    denom = lag * std(m, lag) * std(m+lag, lag)
    return num / denom

def maxnac(m):
    max = -math.inf
    lag_opt = LAG_MIN
    for lag in range(LAG_MIN, LAG_MAX):
        curr = nac(m,lag)
        if (curr > max):
            max = curr
            lag_opt = lag

    return lag_opt
