
# ----------------------------------------------------------------------
# This script generates FIX messages for testing purposes
# and # is based on simplified_FIX_messages by Michael Tang
# https://github.com/michaeltang235/simplfied_FIX_messages
# 
# Usage: 
# Enter number of messages needed when executing the script 
# (ie. python fixmessage.py 500)
# output messages are written in file named 'fixmsg.txt'
#
# Known problems - FIX tag 10 (CheckSum) is not accurate.
#
# Created on July 5, 2021
# ----------------------------------------------------------------------

# import modules required:
import sys
import random
from time import strftime
import datetime

def FIXValues(start, finish):
    x = str(random.randint(start, finish))
    return x

# Verify input arguments are valid
try:
    #nummsg = int(sys.argv[1])
    nummsg = 30
except:
    if len(sys.argv) < 2:
        sys.exit('ERROR Missing Arguments. Usage: %s <number to generate>' % sys.argv[0], )
    elif not (sys.argv[1].isnumeric()):
        sys.exit('Please enter a positive integer. Usage: %s <number to generate>' % sys.argv[0], )
    else:
        sys.exit('Unknown Error with input parameter (%s)', sys.argv[1])

# Set output text file name, then open and write file
filename = 'fixmsg.txt'
f = open(filename, 'w')

# Some FIX tags will be limited to the most popular values. Any non-numeric values will be specified 
# in a dictionary (fixdict). Additional information on these tag/value pairs:
# https://www.onixs.biz/fix-dictionary/4.2/fields_by_tag.html
fixdict = {'167': ['FUT', 'OPT', 'CS']}

for item in range(nummsg):

    # Assignment of values to tags (e.g. t55 = 4 means assign value of 4 to tag 55)
    t167 = random.choice(fixdict['167'])                        # get from fixdict
    t11 = datetime.date.today().strftime('%Y%m%d_' + str(item)) # Unique ID for the trading day
    t44 = round(random.uniform(0,100),2)                        # Price rounded to 2 decimal places,
    timefields = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S.%f')[:-3] # Sending/Transact time w/milliseconds
    
    # Assemble FIX body using values obtained above.
    body = ('|1=TEST' + '|11=' + t11 + '|21=' + FIXValues(1,3) + '|55=SYMBOL_' + FIXValues(1,30) + 
           '|54=' + FIXValues(1,2) + '|38=' + FIXValues(1,10000) + '|40=' + FIXValues(1,5) + '|44=' + str(t44) +
           '|60=' + str(timefields) + '|167=' + t167 + '|59=' + FIXValues(0,6))

    # Creation of header data
    header = ('8=FIX.4.2|9=' + str(len(body)) + '|35=D' + '|34=' + str(item) + '|49=SenderComp' + FIXValues(1,10) + 
              '|50=USERINFO' + '|52=' + str(timefields) + '|56=TargetComp_UAT')

    # Finish the message with Checksum - Not accurate
    trailer = ('|10=' + str(sys.getsizeof(header + body) % 256))

    # Assemble the FIX message
    msg = header + body + trailer
    print(msg)

# output message to file
    f.write(msg + '\n')

# close and save output file after the loop
f.close()

