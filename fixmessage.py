
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

# check if input argument is given when calling the script on terminal
# if no input argument is given, raise index error and print error message
try:
    #nummsg = int(sys.argv[1])
    nummsg = 30
except:
    if len(sys.argv) < 2:
        sys.exit('ERROR Missing Arguments. Usage: %s <number to generate>' % sys.argv[0], )
    elif not (sys.argv[1].isnumeric()):
        sys.exit('Please enter a positive integer. Usage: %s <number to generate>' % sys.argv[0], )

# set output text file name, then open and write file
filename = 'fixmsg.txt'
f = open(filename, 'w')

# From the simplified rules on FIX message, some of the tags have restricted values,
# define dictionary fixdict to store tags and their corresponding values
# for detailed information on what these values represent
# refer to https://www.onixs.biz/fix-dictionary/4.2/fields_by_tag.html
fixdict = {'167': ['FUT', 'OPT', 'CS']}

for item in range(nummsg):

    # assign values to tags,
    # e.g. t55 = 4 means assign value of 4 to tag 55
    t167 = random.choice(fixdict['167'])    # security type, 'FUT'=future, 'OPT'=option, ...
    t11 = datetime.date.today().strftime('%Y%m%d_' + str(item)) #Unique ID for the trading day
    t44 = round(random.uniform(0,100),2)    # price to sell or buy, round to 2 decimal places,
    timefields = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S.%f')[:-3] # Sending/Transact time w/milliseconds
    
    # Assemble body using values obtained above, with order of tags arranged
    body = ('|1=TEST' + '|11=' + t11 + '|21=' + FIXValues(1,3) + '|55=SYMBOL_' + FIXValues(1,30) + 
           '|54=' + FIXValues(1,2) + '|38=' + FIXValues(1,10000) + '|40=' + FIXValues(1,5) + '|44=' + str(t44) +
           '|60=' + str(timefields) + '|167=' + t167 + '|59=' + FIXValues(0,6))

    #ERROR Field 9 Message length, in bytes, is verified by counting the number of characters in the message 
    # following the BodyLength (9) field up to, and including, the delimiter immediately preceding the CheckSum (10)
    # field. ALWAYS SECOND FIELD IN MESSAGE. (Always unencrypted) For example, for message 8=FIX 4.4^9=5^35=0^10=10^,
    # the BodyLength is 5 for 35=0^
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