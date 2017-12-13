import glob
import os


def main():
    f1 = open('/home/icfoss/Desktop/asish1.txt', 'r')
    f2 = open('/home/icfoss/Desktop/asish2.txt', 'r')
    f3 = open('/home/icfoss/Desktop/asish3.txt', 'w')

    for line1 in f1:
        print line1,'------------------l1'
        for line2 in f2:
            print line2,'----------l2'
            if line1 == line2:
                print line1,'line------------------'
                f3.write(line1)


    f3.close()
    f1.close()
    f2.close()

if __name__== "__main__":
  main()
