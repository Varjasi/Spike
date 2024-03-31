'''
# Import required MicroPython libraries.
from usys import stdin
from uselect import poll
from uio import FileIO
import usys
a = FileIO(open('adatok.txt', '+rb'))
print(stdin)
'''

from uio import FileIO as bemenet

file = bemenet(open('adatok.txt', 'rb'))

tartalom = file.read()
print(tartalom)
file.close()
