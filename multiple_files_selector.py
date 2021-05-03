from itertools import izip

with open("textfile1") as textfile1, open("textfile2") as textfile2:
    for x, y in izip(textfile1, textfile2):
        x = x.strip()
        y = y.strip()
        print("{0}\t{1}".format(x, y))
