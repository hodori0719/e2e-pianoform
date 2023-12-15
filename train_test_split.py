import os
import random

directory = 'Data/grandstaff'

train = []
val = []
test = []

for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.bekrn'):
            split = random.randint(1, 10)
            point = os.path.join(subdir, file)
            if split == 9:
                val.append(point)
            elif split == 10:
                test.append(point)
            else:
                train.append(point)

pdir = 'Data/grandstaff_dataset/partitions'

for filename, source in [('/train.txt', train), ('/val.txt', val), ('/test.txt', test)]:
    with open(pdir + filename, 'w') as outfile:
        for point in source:
            outfile.write(point + '\n')
