import glob
from re import T
import time
import os 
import shutil
import traceback
from contextlib import redirect_stdout
import filecmp
import sys
from janim_2 import extract_transactions_from_single_contract
def diff_golden_to_output( x ):
    try:
        output_file = "output_dir\\"+ x 
        golden_file = "golden_dir\\"+ x 
        result = filecmp.cmp(output_file,golden_file,shallow=False)
        if result == True :
            return  "YES"
        else :
            return "NO"
    except:
        return "NA"
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
test_t= sys.argv[1]
passed = 0
fail_diff = 0 
fail_sanity = 0 
fail_compare=0

for file in files : 
    try:
        print("Processing: ", file)
        start = time.time()
        name = file.replace("V0\\","")
        name = name.replace(".PDF",".csv")
        df =  extract_transactions_from_single_contract(file)  
        df.to_csv('output_dir/'+name) 
        end = time.time()
        print("Time:",round((end- start),2),"seconds")
        if test_t != "s" : 
            dt_comprison  = diff_golden_to_output(name)
            if dt_comprison == "YES" : 
                print ("passed")
                passed +=1 
            elif dt_comprison == "NO" : 
                print ("matching fault")
                fail_diff += 1
            else  :
                print ("error in matching files ")
                fail_compare+=1
        else:
            print("Skipping comparison")
            passed+=1
    except ValueError  :
        tb = traceback.format_exc()
        name = file.replace("V0\\","")
        name = name.replace(".PDF",".log") 
        print ("excption ocuured for file :",name)
        with open ("errors\\" + name ,"w") as f:
            f.write(tb)
            fail_sanity += 1
    if test_t != "s":
        print(f"Current: PASS={passed} FAIL_S={fail_sanity} FAIL_C={fail_compare} FAIL_D={fail_diff}") 
    else:
        print(f"Current: PASS={passed} FAIL_S={fail_sanity}")