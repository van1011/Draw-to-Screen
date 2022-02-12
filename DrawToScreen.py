import tkinter as tk
from tkinter import messagebox
import sys
import subprocess
import os
from os import path
from datetime import datetime
from PIL import ImageTk, Image, ImageDraw
import PIL

class draw_screen:

    def __init__(self):
        
        self.image_path = os.path.expanduser('~') + "/DrawToScreen"
        if not os.path.exists(self.image_path):
            os.mkdir(self.image_path)
            
        self.root = tk.Tk()
        self.root.title("Draw")
        self.root.config(bg = "blue")
        self.root.geometry("700x400")

        self.root.rowconfigure(0, weight = 1)
        self.root.columnconfigure(0, weight = 0)
        self.root.columnconfigure(1, weight = 8)
        self.root.columnconfigure(2, weight = 8)
        
        self.pallete = tk.Canvas(self.root, bg = "#D3D3D3", width = 60, height = 400)
        self.pallete.pack(side = tk.LEFT)
    
        self.canvas = tk.Canvas(self.root, width = 640, height = 400)
        self.canvas.pack(side = tk.RIGHT)
        self.canvas.bind("<Button-1>", self.get_coord)
        self.canvas.bind("<B1-Motion>", self.draw_line)

        self.image = PIL.Image.new("RGB", (640, 400), color = "white")
        self.draw = ImageDraw.Draw(self.image)

        self.currX, self.currY = 0,0
        self.color = "black"
        self.width = 1
        self.maxWidth = 5
        self.minWidth = 1

        self.button = tk.Button(self.pallete, width = 3, text='Save', command= self.changeBackground).place(x = 0, y = 310)
        self.clearButton = tk.Button(self.pallete, width = 3, text='Clear', command= self.clear).place(x = 0, y = 350)

        self.display_pallete()
        self.root.mainloop()

    def changeBackground(self):
        now = datetime.now().isoformat()
        filename = now[:-1] + ".png"
        fullpath = self.image_path + "/" + filename
        self.image.save(fullpath)
        print("Openning %s" %fullpath)

        SCRIPT = """/usr/bin/osascript<<END
            tell application "Finder"
            set desktop picture to POSIX file "%s"
            end tell
            END"""
       
        subprocess.Popen(SCRIPT%fullpath, shell = True)

    #https://www.youtube.com/watch?v=WfUC4l09TX0
    def get_coord(self, event):
        self.currX, self.currY = event.x, event.y

    def set_color(self, color):
        self.color = color

    def set_width(self, width):
        
        self.width = self.width if (width > self.maxWidth or width < self.minWidth) else width

    def draw_line(self,event):
        self.draw.line([self.currX, self.currY, event.x, event.y], fill = self.color, width = self.width)
        self.canvas.create_line(self.currX, self.currY, event.x, event.y, fill = self.color, width = self.width)
        self.currX, self.currY = event.x, event.y
        
    def clear(self):
        self.canvas.delete(tk.ALL)
        self.image = PIL.Image.new("RGB", (640, 400), color = "white")
        self.draw = ImageDraw.Draw(self.image)
        
    def display_pallete(self):
        id = self.pallete.create_rectangle((20,20,40,40),fill='#D998BA')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_color('#D998BA'))

        id = self.pallete.create_rectangle((20,55,40,75),fill='#E3BCD6')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_color('#E3BCD6'))

        id = self.pallete.create_rectangle((20,90,40,110),fill='#D8769A')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_color('#D8769A'))
        
        id = self.pallete.create_rectangle((20,125,40,145),fill='#C2465C')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_color('#C2465C'))

        id = self.pallete.create_rectangle((20,160,40,180),fill='#9B283C')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_color('#9B283C'))

        id = self.pallete.create_rectangle((20,195,40,215),fill='black')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_color('black'))

        id = self.pallete.create_oval((20,230,40,250),fill='gray')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_width(self.width + 1))

        id = self.pallete.create_oval((22,267,38,283),fill='gray')
        self.pallete.tag_bind(id, '<Button-1>', lambda x: self.set_width(self.width - 1))

draw_screen()


    #give executable permissions to write to desktop and create folder somewhere in computer
