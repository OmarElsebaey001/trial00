import glob
import time
import os 
import shutil
import traceback
from contextlib import redirect_stdout
from janim_2 import extract_transactions_from_single_contract
files = glob.glob('V0/*.pdf')
dir = os.path.join("output_dir")
if  os.path.exists(dir):
    shutil.rmtree(dir)
    os.mkdir(dir)
else :
    os.mkdir(dir)
dir_error = os.path.join("errors")
if  os.path.exists(dir_error):
    shutil.rmtree(dir_error)
    os.mkdir(dir_error)
else :
    os.mkdir(dir_error)
passed = 0 
failed = 0 
for file in files : 
    try:
        print("Processing: ", file)
        start = time.time()
        name = file.replace("V0\\","")
        name = name.replace(".PDF",".csv")
        df =  extract_transactions_from_single_contract(file)  
        df.to_csv('output_dir/'+name) 
        end = time.time()
        print("the time of excecution",(end- start),"seconds")
        passed +=1
    except ValueError  :
        tb = traceback.format_exc()
        name = file.replace("V0\\","")
        name = name.replace(".PDF",".log") 
        print ("excption ocuured for file :",name)
        with open ("errors\\" + name ,"w") as f:
            f.write(tb)
        failed += 1
    print ("passed :",passed)
    print ("failed :",failed)


                

    