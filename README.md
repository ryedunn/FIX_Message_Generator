# FIX_Message_Generator
This script generates FIX messages for testing purposes and is based on simplified_FIX_messages by Michael Tang https://github.com/michaeltang235/simplfied_FIX_messages

## Usage: 
Enter number of messages needed when executing the script (ie. python fixmessage.py 500) output messages are written in file named 'fixmsg.txt'
  

## Known problems: 
### FIX tag 10 (CheckSum) is not accurate
  - The checksum of a FIX message is always the last field in the message. It is composed of three characters and has tag 10.[5] It is given by summing the ASCII value of all 
characters in the message, except for those of the checksum field itself, and performing modulo 256 over the resulting summation.[6] For example, in the message below, the 
summation of all ASCII values (including the SOH character, which has a value of 1 in the ASCII table) results in 4158. Performing the modulo operation gives the value 62. 
Since the checksum is composed of three characters, 062 is used.  
<pre>
8=FIX.4.2|9=65|35=A|49=SERVER|56=CLIENT|34=177|52=20090107-18:15:16|98=0|108=30|10=062|
     0   + 0  + 5  +   10    +   10    +  7   +        21          + 5  +  7   +   0    = 65
</pre>
