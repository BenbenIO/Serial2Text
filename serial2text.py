import os
import subprocess
import serial
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
import webbrowser

#Global var:
Serial_en=False
serial_port=""
baud_rate=""
RUN=True
running=False
head_global=""
validation=False
ser = None        #add global ser in thread,... ?

def auto_scroll():
    content_serial.see("end")
    
class run_thread(threading.Thread):        
    def run(self):
        print("Start Run into the thread\n")
        global ser
        global Serial_en
        global serial_port
        global baud_rate
        global running
        
        ser=serial.Serial(serial_port,baud_rate)
        while (running==True):
            line=ser.readline()
            try:
                line = line.decode("utf-8")
                content_serial.insert(END,line)
            except:
                print("Cannot encode cararact: message dropped\n")
            
            if(autoVar.get()==1):
                auto_scroll()
        ser.close()
        self.stop()

    def stop(self):
        self._is_running = False
    
def start_run_thread():
    global Serial_en
    global running
    print(autoVar.get())
    if Serial_en==False:
        messagebox.showinfo("Error","Serial not found: Check your setting")
    else:
        running=True
        content_serial.delete(1.0,2.0)
        rt=run_thread()
        rt.start()
        
def send(event=None):
    print("Send function\n")
    global ser
    global running
    if(running!=True):
        messagebox.showinfo("Error","Serial not found: please connect before sending data")
    else:
        data=sendingE.get()
        ser.write(data)
         
def Stop():
    global running
    print("stop function\n")
    running=False

def get_setting():
    global serial_port
    global baud_rate
    global Serial_en
    global write_to_file_path
    serial_port=str(portNE.get())
    baud_rate=speedE.get()
    try:
        ser = serial.Serial(serial_port, baud_rate)
        Serial_en=True
        ser.close()
        content_serial.delete(1.0,END)
        content_serial.insert(END,"Waiting to RUN...\n")
    except:
        print("message alarm")
        messagebox.showinfo("Error", "Serial Port not found: Check port number")
        Serial_en=False
    print("Serial port="+serial_port+"\n")
    print("Speed = "+baud_rate+"\n")

def clear_content():
    print("Clear the serial content")
    content_serial.delete(1.0,END)
    
def valid_head(head_top_level,content):
    print("valid head call")
    global head_global
    head_global=content
    print(head_global)
    head_top_level.destroy()

def header(event=None):
    print("Header config\n")
    global head
    global validation
    dateV=BooleanVar()
    frameV=BooleanVar()
    full=datetime.now()
    date=str(full.year)+"/"+str(full.month)+"/"+str(full.day)
    hour=str(full.hour)+"h"+str(full.minute)

    if(writeVar.get()==True):
        print("Nope")
        return;

    #GUI
    head_top_level=Toplevel(root)
    head_top_level.iconbitmap('icon.ico')
    head_top_level.geometry("310x220+250+250")
    head_top_level.title('Header configuration')
    head_top_level.transient(root)
    title2=Label(head_top_level,text="HEADER:")
    title2.pack(side=TOP,fill='x')
    info=Label(head_top_level, text='The header information will be put on top of your serial\nGood programing start with good comment :)')
    info.pack(side=TOP,fill=X)
    content_head = Text(head_top_level)
    content_head.config(height=8)
    content_head.insert(END, "*****************\nCreated by:\nPurpose:\nComments:\nDate:"+date+"\nHour:"+hour+"\n*****************")
    content_head.pack()
    validBut=Button(head_top_level,text="OK",fg='blue',background="#b3b6b7",command = lambda: valid_head(head_top_level,content_head.get(1.0,END)))
    validBut.pack(side=RIGHT,padx=5,pady=5)
    
def save_content(event=None):
    print("Save function running\n")
    global head
    file_name=filedialog.asksaveasfilename(title='Saved serial content',
                                           filetypes=[('Text files','.txt'),('all files','.*')],
                                           defaultextension='.txt')
    if file_name:
        f = open(file_name,'a')
        content = content_serial.get(3.0,END) #modified for the measurment
        print(writeVar.get())
        if(writeVar.get()==True):
            f.write(head_global)
        f.write(content)
        f.close()
        
    return "break"

def go_github(event):
    webbrowser.open_new("https://github.com/BenbenIO")

def about():
    print("about\n")
    about_top_level=Toplevel(root)
    about_top_level.title('About')
    about_top_level.iconbitmap('icon.ico')
    about_top_level.transient(root)
    description = Label(about_top_level,text="Created by Benjamin IOLLER as an educatif project.\n The purpose of this program is to provide an easy serial to text interface.\n")
    description.pack(side=TOP,fill=BOTH)
    link = Label(about_top_level,text="more info HERE :)",fg="blue", cursor="hand2")
    link.pack(fill=BOTH)
    link.bind("<Button-1>",go_github)

def helpME():
    print("Help me")
    help_toplevel=Toplevel(root)
    help_toplevel.title('Help')
    help_toplevel.iconbitmap('icon.ico')
    help_toplevel.transient(root)
    shortcutframe=Frame(help_toplevel)
    shortcutframe.pack()
    shortcuttitle=Label(shortcutframe,text="Shortcut:",font=('',10,'bold'))
    shortcuttitle.pack(side=TOP,fill=BOTH)
    shortcutexp=Label(shortcutframe,text="Save= ctrl+S\nHeader config=ctrl+h\nSending: space",justify=LEFT)
    shortcutexp.pack(side=LEFT,fill=BOTH)
    how2comframe=Frame(help_toplevel)
    how2comframe.pack()
    comtitle=Label(how2comframe,text="How to find your COM number:",font=('',10,'bold'))
    comtitle.pack(side=TOP,fill=BOTH)
    explaination="On Windows:\no Open device manager (devmgmgt.msc)\no check out Ports (COM and LPT)\no That's it :)"
    windowsL=Label(how2comframe,text=explaination,justify=LEFT)
    windowsL.pack(side=LEFT,fill=NONE)  

#Start the main GUI
root = Tk()
root.title("Serial-2-Text")
root.iconbitmap('icon.ico')

#Default Value:
comVar = StringVar()
comVar.set("COM4")
speedVar = IntVar()
speedVar.set("9600")
nameVar = StringVar()
nameVar.set("measure_1")
writeVar = BooleanVar()
writeVar.set(False)
serialVar = StringVar()
serialVar.set("Waiting for config../n")
autoVar = IntVar()
autoVar.set(1)
data2send=StringVar()
data2send.set("")

#Setting bar creation:
setting_bar = Frame(root,height=35,background="#b3b6b7",highlightthickness=1)
setting_bar.pack(expand='no',fill='x')
SettingL = Label(setting_bar,text='[    SETTING    ]',background="#b3b6b7",font=('',10,'bold'))
SettingL.pack(side=TOP,fill=X)
portNL = Label(setting_bar, text='Serial Port: ',background="#b3b6b7")
portNL.pack(side=LEFT,padx=5,pady=5)
portNE = Entry(setting_bar,width=10,textvariable=comVar)
portNE.pack(side=LEFT)
speedL = Label(setting_bar,text='  Speed: ',background="#b3b6b7")
speedL.pack(side=LEFT,padx=5,pady=5)
speedE = Entry(setting_bar,width=10,textvariable=speedVar)
speedE.pack(side=LEFT)
SetBut = Button(setting_bar,text=' SET ',command = get_setting,background="#b3b6b7",font=('',10,'bold'))
SetBut.pack(side=RIGHT,padx=5,pady=5)

#Send via Serial:
sending_bar = Frame(root,height=30,background="#b3b6b7",highlightthickness=1)
sending_bar.pack(fill=X)
sendingL=Label(sending_bar,text='Send data:',background="#b3b6b7",highlightthickness=1)
sendingL.pack(side=LEFT,padx=5,pady=5)
sendingE=Entry(sending_bar,textvariable=data2send)
sendingE.pack(side=LEFT,fill=X,padx=15,pady=15)
sendingB=Button(sending_bar,text='SEND',command=send,background="#b3b6b7",font=('',10,'bold'))
sendingB.pack(side=RIGHT,padx=5,pady=5)
root.bind('<space>',send)

#Run-stop-clear-save bar creation:
run_bar=Frame(root,height=30,background="#b3b6b7",highlightthickness=1)
run_bar.pack(fill='x')
runBut = Button(run_bar,text="RUN",command = start_run_thread,background="#b3b6b7",fg='red',font=('',10,'bold'))
runBut.pack(side=LEFT, padx=10,pady=4)
stopBut = Button(run_bar,text='STOP',command = Stop,background="#b3b6b7",fg='red',font=('',10,'bold'))
stopBut.pack(side=LEFT, padx=10,pady=4)
headCheckBut = Checkbutton(run_bar, text='file header', variable=writeVar)
headCheckBut.pack(side=RIGHT,padx=10,pady=4)
clearBut = Button(run_bar,text='CLEAR',command = clear_content,background="#b3b6b7",fg='black',font=('',10,'bold'))
clearBut.pack(side=RIGHT,padx=10,pady=4)
saveBut = Button(run_bar,text='SAVE', command=save_content,background="#b3b6b7",fg='blue',font=('',10,'bold')) #filedialog
saveBut.pack(side=RIGHT,padx=10,pady=4)
root.bind('<Control-s>',save_content)
root.bind('<Control-h>',header)
headCheckBut.bind('<Button-1>',header)

#Serial Display creation:
content_serial = Text(root,background='black',fg='white')
content_serial.insert(END, "Hello, waiting for setting...\n")
content_serial.pack(expand='yes',fill=BOTH)
scroll_bar = Scrollbar(content_serial)
content_serial.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_serial.yview)
scroll_bar.pack(side='right',fill='y')
content_serial.see("end")
#Autoscroll:
autoSframe=Frame(root,background="#b3b6b7",highlightthickness=1)
autoSframe.pack(side=BOTTOM,anchor=SW,fill=BOTH)
autoscrollCheckBut = Checkbutton(autoSframe,text='autoscroll',variable=autoVar)
autoscrollCheckBut.pack(side=LEFT,anchor=SW,fill=NONE,padx=10,pady=4)

#Menu creation:
menu_bar=Menu(root)
menu_bar.add_command(label="About ",command=about)
menu_bar.add_command(label="Help",command=helpME)
root.config(menu=menu_bar)

#run
root.geometry("500x500")
root.pack_propagate(0)
root.mainloop()
