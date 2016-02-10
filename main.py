#this program runs from Linux terminal using the following syntax:
#python main.py inputfile
#inputfile is the filename of the initial configuration of the ecosystem
from Ecosystem import Ecosystem
from River import River

import sys
def main():
    if len( sys.argv ) != 2:
        inputfile = input("Name of input file: ")
    else:
        # Pick up the command line argument
        inputfile = sys.argv[1]
    print(inputfile)

    ecosystem = Ecosystem(inputfile)
    river = River(ecosystem, 11)
    river.run()

main()
