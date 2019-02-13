import math

FREQUENCY = 1.0/20.0
ReadingsPerSecond = 20.0
magReadings = []

LAG_MIN = 1
LAG_MAX = 2


def a(n):
    # return magReadings[n]
    return 30


def mean(m, lag):
    sum = 0
    for i in range(m, m+lag):
        sum += a(i)
    return sum / lag


def std(m, lag):
    mu = mean(m, lag)
    sum = 0
    for i in range(m, m+lag):
        sum += (a(i)-mu) ^ 2
    return sum / lag


def nac(m, lag):
    for k in range(0, lag):
        num = (a(m+k) - mean(m, lag)) * (a(m+k+lag) - mean(m+lag, lag))
    denom = lag * std(m, lag) * std(m+lag, lag)
    return num / denom


def maxnac(m):
    max = -100000000000000
    lag_opt = LAG_MIN
    for lag in range(LAG_MIN, LAG_MAX):
        curr = nac(m, lag)
        if (curr > max):
            max = curr
            lag_opt = lag

    return lag_opt


def calculateSquared(num):
    return num**2


def calculateMagnitude(x, y, z):
    tempMag = calculateSquared(x) + calculateSquared(y) + calculateSquared(z)
    return math.sqrt(tempMag)


def calculateSD(data, begin, end):
    sum = 0.0
    average = calculateAverage(data, begin, end)
    for k in range(begin, end+1):
        sum += calculateSquared(data[k] - average)
    return math.sqrt(sum/ReadingsPerSecond)


def calculateAverage(data, begin, end):
    sum = 0.0
    for k in range(begin, end+1):
        if (k >= len(data)):
            break
        sum += data[k]
    return sum/ReadingsPerSecond


def batshitCrazyThingHere(magReadings):
    status = []
    for second in range(0, len(magReadings)/20):
        sd = calculateSD(magReadings, second, second+20)
        if (sd < 0.0):
            status.append("Idle")
        else:
            nacs = []
            for sample in range(second*20, second*20+20):
                if (sample == 0):
                    nacs.append(0.5)
                nacs.append(maxnac(sample))
            avg = calculateAverage(nacs, second, second+20)
            if (avg > 0.7 or second == 0):
                status.append("Walking")
            else:
                status.append(status[second-1])

    return status


def main():
    file = open("movement.txt", "r")
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
    # print(len(magReadings))
    status = batshitCrazyThingHere(magReadings)
    for s in status:
        print(s)


if __name__ == '__main__':
    main()
