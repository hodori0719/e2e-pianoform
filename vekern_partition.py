import os
'''
Generate a duplicate partition identical to the bekrn partiion using the
vekrn conversions.
'''

pdir = 'Data/grandstaff_dataset/partitions'

ddir = 'Data/grandstaff_modified_dataset/partitions'

for filename in ['/train.txt', '/val.txt', '/test.txt']:
    with open(pdir + filename, 'r') as infile:
        with open(ddir + filename, 'w') as outfile:
            files = infile.read()
            lines = files.split("\n")
            for line in lines:
                outfile.write(os.path.splitext(line)[0] + '.vekrn' + '\n')