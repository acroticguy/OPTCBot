import os, numpy, base64, subprocess, random, threading, time

'''
LDPlayer has a CLI, so we will be using subprocess to throw queries to the client.
'''

class LDPlayer:

    pathLD = "C:\LDPlayer\LDPlayer9"
    index = -1
    w = 0
    h = 0
    def __init__(self, index = 0, w=1080, h=1920):
        self.index = index
        self.w = w
        self.h = h
    
    def exec_query(self, query):
        return str(subprocess.Popen(f"ldconsole {query}", creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, shell=True, cwd=self.pathLD).stdout.read())

    # LDPlayer Functionality

    def init_adb(self):
        return str(subprocess.Popen(f"adb start-server", creationflags=subprocess.CREATE_NO_WINDOW, stdout=subprocess.PIPE, shell=True, cwd=self.pathLD).stdout.read())

    def Start(self):
        self.exec_query(f"launch --index {self.index}")

    def Close(self):
        self.exec_query(f"quit --index {self.index}")

    def RunApp(self, Package_Name: str):
        self.exec_query(f"runapp --index {self.index} --packagename {Package_Name}")
    
    def StopApp(self, Package_Name):
       self.exec_query(f"killapp --index {self.index} --packagename {Package_Name}")

    def Reboot(self):
        self.exec_query(f"reboot --index {self.index}")

    # Controls

    def Click(self, pos: tuple):
        print(f"Trying to click coordinates {pos[0]}, {pos[1]}")
        return self.exec_query(f'adb --index {self.index} --command "shell input tap {pos[0]} {pos[1]}"')
    
    def SendText(self, text, VN=True):
        if VN:
            text =  str(base64.b64encode(text.encode('utf-8')))[1:]
            self.exec_query(f'adb --index {self.index} --command "shell ime set com.android.adbkeyboard/.AdbIME"')
            self.exec_query(f'adb --index {self.index} --command "shell am broadcast -a ADB_INPUT_B64 --es msg {text}"')
            return
            
        self.exec_query(f'adb --index {self.index} --command "shell input text \'{text}\'"')

    def Swipe(self, x1, y1, x2, y2, delay=0):
        if delay == 0: delay = ""
        self.exec_query(f'adb --index {self.index} --command "shell input touchscreen swipe {x1} {y1} {x2} {y2} {delay}"')
    