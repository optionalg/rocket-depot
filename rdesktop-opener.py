#!/usr/bin/python2

# Originally written by Cory Wright
# http://projects.standblue.net/software/#rdesktop-open

from Tkinter import *
import os, string

if os.environ.has_key('USER'):
    user = os.environ['USER']
else:
    user = "username"

options = { "host"       : "host.example.com",
            "user"       : user,
            "resolution" : "85",
            "pass"       : "",
            "domain"     : "",
            "fullscreen" : 0,
            "grabkeyboard"    : 0 }

optlist = ("host","user","resolution","domain","fullscreen","grabkeyboard")

configfile = "%s/.rdesktop-open" % os.environ['HOME']

def popup_alert(title,textmsg):
    alert = Tk(className='rdesktop-opener')
    alert.title("Notice: "+title)
    Label(alert,text="Notice: "+textmsg).pack()
    alert.mainloop()

def save_conf():
    # host, user name, resolution, domain, fullscreen (0,1), grab keyboard (0,1)
    conf = open(configfile,"w")
    geometry = string.strip(textGeometry.get())
    ofline = "%s,%s,%s,," % (textHost.get(),textUsername.get(),geometry)
    ofline = ofline + "%s,%s\n" % (varFs.get(),varGrabKeyboard.get())
    conf.write(ofline)
    conf.close()

def open_url(url):
    os.spawnvp("P_NOWAIT","x-www-browser",('x-www-browser',url))
    return

def open_rdesktop_site():
    open_url("http://www.rdesktop.org/")
    return

def open_rdo_site():
    open_url("http://projects.standblue.net/software/")
    return

def open_rdoer_site():
    open_url("https://github.com/robled/rdesktop-opener/")
    return

def run_rdesktop():
    params = ['rdesktop']

    if(textHost.get() == ""):
        popup_alert("No Host","No Host or IP Address Given")
        return
    if(textUsername.get() != ""):
        params.append("-u")
        params.append("%s" % string.strip(textUsername.get()))
    if(textPassword.get() != ""):
        params.append("-p")
        params.append("%s" % string.strip(textPassword.get()))
    if(textGeometry.get() != ""):
        params.append("-g")
        params.append("%s" % string.strip(textGeometry.get()) + '%')
    if(varFs.get() == 1):
        params.append("-f")
    if(varGrabKeyboard.get() == 0):
        params.append("-K")
    if(textHost.get() != ""):
        params.append("%s" % string.strip(textHost.get()))

    print params
    os.spawnvp(os.P_NOWAIT, params[0], params)
    return

def print_options():
    print "-- default options --"
    for i in options.keys():
        print i, " => ", options[i]
    print "-- currently selected options --"
    print "host => " + textHost.get()
    print "user => " + textUsername.get()
    print "resolution => " + textGeometry.get()
    print "pass => " + textPassword.get()
    print "domain => "
    print "fullscreen => " + str(varFs.get())
    print "grabkeyboard => " + str(varGrabKeyboard.get())

try:
    conf = open(configfile,"r")
except IOError:
    popup_alert("No ~/.rdesktop-open found",
                "No ~/.rdesktop-open file was found.\nChoose 'Save' from the 'File' menu to create one")
else:
    if(conf):
        readconf = string.strip(conf.readline())
        # host, user name, resolution, domain, fullscreen (0,1), grab keyboard (0,1)
        optindex = 0
        for opt in string.split(readconf,","):
            options[optlist[optindex]] = opt
            optindex = optindex + 1

if __name__ == "__main__":

    root = Tk(className='rdesktop-opener')
    root.title("rdesktop-opener")

    menuFrameTop = Frame(root,relief=RIDGE,bd=2)
    menuFrameTop.pack(side=TOP,fill=X)

    menuFileButton = Menubutton(menuFrameTop,text='File',underline=0)
    menuFileButton.pack(side=LEFT)
    menuFileDropdown = Menu(menuFileButton,relief=RIDGE)
    menuFileDropdown.add_command(label="Save Current Configuration",underline=0,command=save_conf)
    menuFileDropdown.add_command(label="Exit",underline=0,command=root.destroy)
    menuFileButton.config(menu=menuFileDropdown)

    menuOptsButton = Menubutton(menuFrameTop,text='Options',underline=0)
    menuOptsButton.pack(side=LEFT)
    menuOptsDropdown = Menu(menuOptsButton,relief=RIDGE)
    menuOptsDropdown.add_command(label="Print Debugging Info To Console",underline=0,command=print_options)
    menuOptsButton.config(menu=menuOptsDropdown)

    menuHelpButton = Menubutton(menuFrameTop,text='Help',underline=0)
    menuHelpButton.pack(side=RIGHT)
    menuHelpDropdown = Menu(menuHelpButton,relief=RIDGE)
    menuHelpDropdown.add_command(label="RDesktop Homepage",underline=0,command=open_rdesktop_site)
    menuHelpDropdown.add_command(label="rdesktop-open Homepage",underline=9,command=open_rdo_site)
    menuHelpDropdown.add_command(label="rdesktop-opener GitHub",underline=9,command=open_rdoer_site)
    menuHelpButton.config(menu=menuHelpDropdown)

    # Create the area for hosts
    frameHost = Frame(root)
    labelHost = Label(frameHost,width=9,text='Host')
    textHost = Entry(frameHost)
    textHost.insert(0,options['host'])
    frameHost.pack(side=TOP, fill=X)
    labelHost.pack(side=LEFT)
    textHost.pack(side=RIGHT, expand=YES, fill=X)
    textHost.focus()
    textHost.bind('<Return>', (lambda event: run_rdesktop()))

    # Create the area for user name
    frameUsername = Frame(root)
    labelUsername = Label(frameUsername,width=9,text='Username')
    textUsername = Entry(frameUsername)
    textUsername.insert(0,options['user'])
    frameUsername.pack(side=TOP, fill=X)
    labelUsername.pack(side=LEFT)
    textUsername.pack(side=RIGHT, expand=YES, fill=X)

    # Create the area for the password
    framePassword = Frame(root)
    labelPassword = Label(framePassword,width=9,text='Password')
    textPassword = Entry(framePassword, show='**')
    textPassword.insert(0,options['pass'])
    framePassword.pack(side=TOP, fill=X)
    labelPassword.pack(side=LEFT)
    textPassword.pack(side=RIGHT, expand=YES, fill=X)

    # Create the area for the full screen
    rightFrame = Frame(root)
    varFs = IntVar()
    varFs.set(options['fullscreen'])
    Checkbutton(rightFrame, text='Fullscreen', variable=varFs).pack(side=RIGHT, expand=YES, fill=X)
    varGrabKeyboard = IntVar()
    varGrabKeyboard.set(options['grabkeyboard'])
    Checkbutton(rightFrame, text='Grab keyboard', variable=varGrabKeyboard).pack(side=RIGHT, expand=YES, fill=X)
    rightFrame.pack(side=TOP)

    # Create the area and the scrolldown for resolution
    frameGeometry = Frame(root)
    labelGeometry = Label(frameGeometry,width=9,text='Geometry %')
    textGeometry = Entry(frameGeometry, width=3)
    textGeometry.insert(0,options['resolution'])
    frameGeometry.pack(side=TOP, fill=X)
    labelGeometry.pack(side=LEFT)
    textGeometry.pack(side=LEFT, expand=NO)

    frameButtons = Frame(root)
    frameButtons.pack(side=BOTTOM)
    Button(frameButtons,text="Quit",command=root.destroy).pack(side=LEFT, fill=X)
    Button(frameButtons,text='Connect',command=run_rdesktop).pack(side=RIGHT, fill=X)

    root.mainloop()

print "rdesktop-opener.py -- https://github.com/robled/rdesktop-opener"