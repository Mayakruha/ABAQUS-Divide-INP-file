# ABAQUS-Divide-INP-file

# command line:
# python Divide_INPfile.py [Inp-file name]

The script divides Abaqus inp-file into several files:
 - a text file of nodes coordinates
 - a text file of elements (just numbers of elements and nodes - without command '*element')
 - a text file of sets
 
It's a useful tool if there are several similar models where it's necessary to change just element type or mesh. 
