#!/usr/bin/env python3

import sys
from random import randint

args=sys.argv

### Generates random masks of cpu affinity for processes. Use it to [randomly] bind processes to cores.

def mask(total_cores,processes,rank):    
    """ Creates a bit mask for a given rank based on the number of threads per process on a P-cores machine"""
    try:
       process_mask=2**(int(total_cores/processes))-1
       shifter=total_cores-(len(bin(process_mask))-2)*(rank+1)
       return hex(process_mask<<shifter)
    except ValueError:
        print("Invalid values (rank too high?). Possible values are [cores] [processes] [rank]")
        exit()


# Hyper-crude command-line processing writen in a friday afternoon after not sleeping enough
cores=int(args[1])
processes=int(args[2])
if len(args) > 3:
   if args[3]=="-r":             # ./maskgenerator.py 48 24 -r
      randomize=True
   elif args[3].isdigit():       # ./maskgenerator.py 48 24 6
      print(mask(cores,processes,int(args[3])),end="")
      exit()

ranks=list(range(processes))
masks=[]
randomize=False

while(len(ranks)>0):
  if randomize==True:
    i=randint(0,len(ranks)-1)
  else:
    i=0
  #print("I'm here and i is",i," and len(ranks) is ",len(ranks)," and ranks is ",ranks)
  print(mask(cores,processes,ranks[i]),end="")
  if len(ranks)>1:
      print(",",end="")
  masks.append(mask(cores,processes,ranks[i]))
  del ranks[i]

