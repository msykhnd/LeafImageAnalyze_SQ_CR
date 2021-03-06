import tkinter
import tkinter.filedialog  as tkdialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import cv2
import csv
import sys
from ImageProcessing.leaf import LeafImageProcessing
from utils.utils import imread

'''GUI Size & Scale'''
app_height = 1000
app_width = 1200
image_scale = 0.8

'''Application GUI'''
class AppForm(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=app_height, width=app_width)
        self.master = master
        self.pack()
        self.create_widgets()
        self.menubar_create()
        self.fname = ""
        self.log_fname = ""
        self.label = ""

    '''GUI widgets'''
    def create_widgets(self):
        self.canvas = tkinter.Canvas(
            self.master,
            width=app_width * image_scale,
            height=app_height,
            relief=tkinter.RIDGE,
            bd=1
        )
        self.canvas.place(x=0, y=0)
        # self.canvas.grid()

        self.textframe = Outputview()
        self.textframe.place(relx=image_scale + 0.01, rely=0, width=app_width * (1 - image_scale) - 10,
                             height=app_height)

    def menubar_create(self):
        self.menubar = tkinter.Menu(self.master)

        filemenu = tkinter.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.image_select)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="Image Select", menu=filemenu)

        filemenu = tkinter.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.log_file_select)
        self.menubar.add_cascade(label="Log File Select ", menu=filemenu)

        editmenu = tkinter.Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="SQ_Image", command=self.SQ_Imageprocess)
        editmenu.add_command(label="CR_Image", command=self.CR_Imageprocess)

        self.menubar.add_cascade(label="Processing", menu=editmenu)

        self.master.config(menu=self.menubar)
        self.master.config()

    def SQ_Imageprocess(self):
        try:
            leaf = LeafImageProcessing(self.fname)
            self.img = leaf.calc_leaf_SQ()
        except:
            pass
        else:
            try:
                with open(self.log_fname, 'a') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    relpath = os.path.relpath(self.fname, start=self.log_fname)
                    label = os.path.split(relpath)[0].replace(".", " ").replace("\\", "_").replace("/", "_").lstrip()
                    writer.writerow([label, leaf.area_size])
                    # self.textframe.text.set(os.path.basename(self.fname) + "  " + str(leaf.area_size))
                    self.textframe.insert_result(os.path.basename(self.fname) + "  " + str(leaf.area_size))
            except FileNotFoundError as e:
                messagebox.showerror("Error", e)


    def CR_Imageprocess(self):
        try:
            leaf = LeafImageProcessing(self.fname)
            self.img = leaf.calc_leaf_CR()
        except:
            pass
        else:
            try:
                with open(self.log_fname, 'a') as f:
                    writer = csv.writer(f, lineterminator='\n')
                    relpath = os.path.relpath(self.fname, start=self.log_fname)
                    label = os.path.split(relpath)[0].replace(".", " ").replace("\\", "_").replace("/", "_").lstrip()
                    writer.writerow([label, leaf.area_size])
                    # self.textframe.text.set(os.path.basename(self.fname) + "  " + str(leaf.area_size))
                    self.textframe.insert_result(os.path.basename(self.fname) + "  " + str(leaf.area_size))

            except FileNotFoundError as e:
                messagebox.showerror("Error", e)

    def disp_image(self, img_temp):
        self.img_temp = cv2.resize(img_temp, dsize=None, fx=0.2, fy=0.2)
        self.img_temp = ImageTk.PhotoImage(Image.fromarray(self.img_temp))
        self.canvas.create_image(
            0,
            0,
            image=self.img_temp,
            anchor=tkinter.NW
        )

    def image_select(self):
        self.fname = tkdialog.askopenfilename(filetypes=[("jpg files", "*.jpg"), ("png files", "*.png")],
                                              initialdir=os.getcwd())
        print(self.fname)
        self.img = imread(self.fname)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        self.disp_image(self.img)

    def log_file_select(self):
        self.log_fname = tkdialog.askopenfilename(filetypes=[("txt files", "*.txt"), ("csv files", "*.csv")],
                                                  initialdir=os.getcwd())


class Outputview(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(padx=5, pady=5, anchor=tkinter.W)
        self.text = tkinter.StringVar()
        self.text.set("None")
        self.create_widgets()

    def create_widgets(self):
        # self.label = tkinter.Label(self, textvariable=self.text)
        self.label = tkinter.Label(self, text="Result Log", relief=tkinter.RIDGE)
        self.label.pack(padx=5, pady=5, fill=tkinter.X)
        self.txt = tkinter.Text(self, height=int(app_height * 0.9), width=int(app_width * (1 - image_scale)) - 100)
        # self.textframe.insert(1.0,self.text)
        self.txt.pack(padx=5, pady=5, anchor=tkinter.W)

    def insert_result(self, str):
        self.txt.insert("1.0", str + "\n")