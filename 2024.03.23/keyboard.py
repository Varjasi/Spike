'''
# Import required MicroPython libraries.
from usys import stdin
from uselect import poll
from uio import FileIO
import usys
a = FileIO(open('adatok.txt', '+rb'))
print(stdin)
'''
'''
# Import required MicroPython libraries.
from usys import stdin
from uselect import poll
from io import FileIO


with FileIO(open('2024.03.23/adatok.txt', 'w', encoding='utf-8')) as a:
    print('Ez kerül a fájlba', file=a)


'''

with open('2024.03.23/adatok.txt', 'w', encoding='utf-8') as celfajl:
    print('Ez kerül q afájlba', file=celfajl)