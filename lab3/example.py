import numpy as np 
 
Sympthoms = np.zeros((7,5)) 

with open("db/Example.csv", "r") as f: 
    lines = f.readlines() 

diagnose_count = len(lines) - 1

for i in range(1, len(lines)): 
    print(lines[i]) 
    data = lines[i].split(';') 
 
    Age=int(data[0]) 
    if Age<20: 
        Sympthoms[1,1] += 1 
    elif (Age>=20) and (Age<40): 
        Sympthoms[1,2] += 1 
    elif (Age>=40) and (Age<60): 
        Sympthoms[1,3] += 1 
    else: 
        Sympthoms[1,4] += 1 
 
    if data[2]=='eye': 
        Sympthoms[3,1] += 1 
    elif data[2]=='skin': 
        Sympthoms[3,2] += 1 
    else: 
        Sympthoms[3,3] += 1
 
PrKD = Sympthoms/diagnose_count 
 
print(PrKD)