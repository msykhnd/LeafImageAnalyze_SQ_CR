import tkinter
import tkinter.filedialog  as tkdialog
from tkinter import font
from PIL import Image, ImageTk
import os
import numpy as np
import cv2
import csv
from leaf import LeafImageProcessing


# cv2.imread が日本語ファイル，ディレクトリを読み込めないため
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


class AppForm(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master, height=1000, width=1000)
        self.pack()
        self.create_widgets()
        self.menubar_create()
        self.fname = ""
        self.log_fname = ""
        self.label = ""

    def create_widgets(self):
        self.canvas = tkinter.Canvas(
            root,
            width=900,
            height=900,
            relief=tkinter.RIDGE,
            bd=0
        )
        self.canvas.place(x=10, y=10)

    def menubar_create(self):
        self.menubar = tkinter.Menu(root)

        filemenu = tkinter.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.image_select)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="Image Select", menu=filemenu)

        filemenu = tkinter.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.log_file_select)
        self.menubar.add_cascade(label="Log File Select ", menu=filemenu)

        editmenu = tkinter.Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="SQ_Image", command=self.SQ_Imageprocess)
        editmenu.add_command(label="CR_Image", command=self.CR_Imageprocess)

        self.menubar.add_cascade(label="Processing", menu=editmenu)

        root.config(menu=self.menubar)
        root.config()

    def SQ_Imageprocess(self):
        leaf = LeafImageProcessing(self.fname)
        self.img = leaf.calc_leaf_SQ()
        with open(self.log_fname, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            relpath = os.path.relpath(self.fname, start=self.log_fname)
            label = os.path.split(relpath)[0].replace(".", " ").replace("\\", "_").replace("/", "_").lstrip()
            writer.writerow([label, leaf.area_size])

    def CR_Imageprocess(self):
        leaf = LeafImageProcessing(self.fname)
        self.img = leaf.calc_leaf_CR()
        with open(self.log_fname, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            relpath = os.path.relpath(self.fname, start=self.log_fname)
            label = os.path.split(relpath)[0].replace(".", " ").replace("\\", "_").replace("/", "_").lstrip()
            writer.writerow([label, leaf.area_size])

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
        self.log_fname = tkdialog.askopenfilename(filetypes=[("txt files", "*.txt")],
                                                  initialdir=os.getcwd())


root = tkinter.Tk()
root.title("Leaf Image")
root.option_add('*font', ('MS Sans Serif', 16))
app = AppForm(master=root)
app.mainloop()
