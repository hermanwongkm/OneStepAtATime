import math


def calculateSquared(num):
    return num**2


def calculateMagnitude(x, y, z):
    tempMag = calculateSquared(x) + calculateSquared(y) + calculateSquared(z)
    print(tempMag)
    return math.sqrt(tempMag)


def main():
    file = open("movement.txt", "r")
    readings = []
    for line in file:
        data = line.split()
        for reading in data:
            readings.append(float(reading))
    # Reading has all the data in the form of [x1,y1,z1,x2,y2,z2....]
    print(calculateMagnitude(2, 2, 2))


if __name__ == '__main__':
    main()
