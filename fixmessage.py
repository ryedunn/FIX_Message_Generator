
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
import datetime
import random
import sys
import traceback
from time import strftime

# Get random int between to parameters
def FIXValues(start, finish):
    x = str(random.randint(start, finish))
    return x

# Verify input arguments are valid
try:
    #int_numberMessages = int(sys.argv[1])  # User Input
    int_numberMessages = 30                 # Testing purposes 
except Exception:
    if len(sys.argv) < 2:
        sys.exit('ERROR Missing Arguments. Usage: %s <number to generate>' % sys.argv[0], )
    elif not (sys.argv[1].isnumeric()):
        sys.exit('Please enter a positive integer. Usage: %s <number to generate>' % sys.argv[0], )
    else:
        print(traceback.print_exc())
        sys.exit('Unknown Error with input parameter (%s)', sys.argv[1])
        
# Set output text file name, then open and write file
filename = 'fixmsg.txt'
tio_file = open(filename, 'w')

# Some FIX tags will be limited to the most popular values. Any non-numeric values will be specified 
# in a dictionary (fixdict). Additional information on these tag/value pairs:
# https://www.onixs.biz/fix-dictionary/4.2/fields_by_tag.html
dic_fixValues = {'167': ['FUT', 'OPT', 'CS']}

for item in range(int_numberMessages):

    # Assignment of values to tags (e.g. t55 = 4 means assign value of 4 to tag 55)
    str_t167 = random.choice(dic_fixValues['167'])                  # get from fixdict
    str_t11 = datetime.date.today().strftime('%Y%m%d_' + str(item)) # Unique ID for the trading day
    str_t44 = round(random.uniform(0,100),2)                        # Price rounded to 2 decimal places,
    str_timeFields = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S.%f')[:-3] # Sending/Transact time w/milliseconds
    
    # Assemble FIX body using values obtained above.
    str_body = f'|1=TEST|11={str_t11}|21={FIXValues(1,3)}|55=SYMBOL_{FIXValues(1,30)}|54={FIXValues(1,2)}' \
        f'|38={FIXValues(1,10000)}|40={FIXValues(1,5)}|44={str(str_t44)}|60={str(str_timeFields)}|167={str_t167}|59={FIXValues(0,6)}'

    # Creation of header data
    str_header = f'8=FIX.4.2|9={str(len(str_body))}|35=D|34={str(item)}|49=SenderComp{FIXValues(1,10)}|50=USERINFO' \
        f'|52={str(str_timeFields)}|56=TargetComp_UAT'

    # Finish the message with Checksum - Not accurate
    str_trailer = f'|10={str(sys.getsizeof(str_header + str_body) % 256)}|'

    # Assemble the FIX message
    msg = f'{str_header}{str_body}{str_trailer}'

    print(msg)

# output message to file
    tio_file.write(msg + '\n')

# Housekeeping
tio_file.close()
