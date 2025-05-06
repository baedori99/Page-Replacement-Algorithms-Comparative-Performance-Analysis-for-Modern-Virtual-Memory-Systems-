import random
with open('data.txt', 'w') as dataFile:
    for i in range(3000):
        dataFile.write(str(random.randint(0, 3000)) +"\n")