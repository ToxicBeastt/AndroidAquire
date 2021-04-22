import sys
import tkinter as tk
from tkinter import ttk
from io import StringIO
import os
from ppadb.client import Client as AdbClient
import subprocess as sp

root = tk.Tk()
root.title("Detektive")
root.geometry("612x417")

mytext = tk.StringVar(value='test \n' * 30)

myframe = ttk.Frame(root)
my_scrollbar = tk.Scrollbar(myframe, orient = tk.VERTICAL)

my_listbox = tk.Listbox(myframe, width=50, yscrollcommand=my_scrollbar.set)

my_scrollbar.config(command = my_listbox.yview)
my_scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

def myCmd():
    my_listbox.delete(0,'end')
    output = sp.getoutput('adb get-serialno')
    output2 = sp.getoutput('adb -s '+ output +' shell getprop')
    #adb -s RR8M6064F0B shell getprop
    output2 = output2.replace('[','') 
    output2 = output2.replace(']','')
    my_listbox.delete(0,'end')
    split = output2.split('\n')
    serialNumber = [s for s in split if "ro.serialno" in s]
    if not serialNumber:
        my_listbox.insert(tk.END,"Tolong Sambungkan HP Anda")
    else :
        serialNumber = str(serialNumber)
        x,y = serialNumber.split(':')
        my_listbox.insert(tk.END,"Serial Number :" + y)
        model = [s for s in split if "product.model" in s]
        model[0] = str(model[0])
        x,y = model[0].split(':')
        my_listbox.insert(tk.END,"Model :" + y)
        sim = [s for s in split if "sim.operator.alpha" in s]
        sim = str(sim)
        x,y = sim.split(':')
        my_listbox.insert(tk.END,"SIM :" + y)
        product = [s for s in split if "product.brand" in s]
        product = str(product)
        x,y = product.split(':')
        my_listbox.insert(tk.END,"Brand :" + y)
        androidversion = [s for s in split if "ro.build.version.release" in s]
        androidversion = str(androidversion[0])
        print(androidversion.split(':'))
        x,y = androidversion.split(':')
        my_listbox.insert(tk.END,"Android Version :" + y)
        GetLog['state'] = 'normal'
        Backup['state'] = 'normal'
    
def exit():
    sp.getoutput('adb kill-server')
    sys.exit()

def getLogDevice():
    output = sp.getoutput('adb get-serialno')
    my_listbox.delete(0,'end')
    with open('out-file.txt', 'w') as f:
        sp.call(['adb','logcat', '-d'], stdout=f)
    my_listbox.insert(tk.END,'Log Scan Complete')
    my_listbox.insert(tk.END,'Log File Name out-file.txt in this program folder')

def getBackupDevice():
    my_listbox.delete(0,'end')
    my_listbox.insert(tk.END,'Starting Backup.....')
    os.system("adb backup -all -f backup_apk.ab")
    my_listbox.delete(0,'end')
    my_listbox.insert(tk.END,'Backup Complete')
    my_listbox.insert(tk.END,'Backup File Name backup_apk.ab in this program folder')

my_button = tk.Button(root,
                   text = "Get Device Information",
                   command = myCmd)

GetLog = tk.Button(root,
                   text = "Get Device Log",
                   command = getLogDevice,
                   state = 'disable')

Backup = tk.Button(root,
                   text = "Full Backup",
                   command = getBackupDevice,
                   state = 'disable')

exit_button = tk.Button(root,
                   text = "Exit",
                   command = exit)

output = " "
my_button.pack(pady = 15)
my_listbox.pack(pady = 15)
GetLog.pack(pady = 15)
Backup.pack(pady = 15)
myframe.pack()
exit_button.pack(pady = 15)

root.mainloop()