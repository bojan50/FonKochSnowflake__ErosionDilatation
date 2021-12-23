from __future__ import division
from matplotlib import pyplot as plt
import numpy as np
from tkinter import *
import tkinter
from PIL import Image
from PIL import ImageFilter, ImageTk
import sys
from tkinter import Tk, StringVar
from tkinter.ttk import *

class TkinterSaSlikomiDugmetom(Frame):
    def __init__(self, naslov, nazivslike):
        self.nazivslike = nazivslike
        super().__init__()
        try:
            img = Image.open(nazivslike)
            self.imgObj = img.resize((200,100))
        except IOError:
            print('Unable to load image', nazivslike)
            sys.exit(1)
        self.prikazislikuidugme(naslov)

    def prikazislikuidugme(self, naslov):
        self.master.title(naslov)
        slika = ImageTk.PhotoImage(self.imgObj)
        label = Label(self, image=slika)
        label.image = slika
        label.pack()
        self.pack()

        self.label1 = Label(self, image=slika)
        self.label1.image = slika
        self.label1.pack()
        self.pack()

        Label(self, text="Dilatacija").pack()
        self.dilatacija_var = StringVar()
        dilatacija = Spinbox(self, values=tuple(range(1, 31, 2)), command=self.dilate, textvariable=self.dilatacija_var)
        dilatacija.pack()
        self.pack()

        self.label2 = Label(self, image=slika)
        self.label2.image = slika
        self.label2.pack()
        self.pack()

        Label(self, text="Erozija").pack()
        self.erozija_var = StringVar()
        erozija = Spinbox(self, values=tuple(range(1, 31, 2)), command=self.erode, textvariable=self.erozija_var)
        erozija.pack(pady=20)
        self.pack()

    def setGeometry(self, width, height):
        # w, h = self.imgObj.size
        # if width>w:
        #    w = width
        # h *=3
        self.master.geometry("{}x{}".format(width, height))

        # dilatacija

    def dilate(self):
        dilateSlika = Image.open(self.nazivslike)
        var = int(self.dilatacija_var.get())
        dil = dilateSlika.filter(ImageFilter.MaxFilter(var)).resize((200, 100))
        slikaDilate = ImageTk.PhotoImage(dil)
        self.label1.configure(image=slikaDilate)
        self.label1.image = slikaDilate

        # erozija

    def erode(self):
        erodeSlika = Image.open(self.nazivslike)
        var = int(self.erozija_var.get())
        ero = erodeSlika.filter(ImageFilter.MinFilter(var)).resize((200, 100))
        slikaErode = ImageTk.PhotoImage(ero)
        self.label2.configure(image=slikaErode)
        self.label2.image = slikaErode


# def Nacrtaj():

class Segment:
    def __init__(self, x1=0,x2=1,y1=0,y2=0):  #pocetne koordinate linije
        self.setStartingCoordinates(x1,x2,y1,y2)

    def setStartingCoordinates(self, x1,x2,y1,y2):
        self.x1 = x1
        self.x2 = y1
        self.zabranjen1 = x1
        self.zabranjen2 = x2
        self.y1 = x2
        self.y2 = y2
        
    
    def display(self):  #iscrtavanje na matplot tabli
        x=[self.x1, self.x2]
        y=[self.y1, self.y2]
        if(self.x1 == self.zabranjen1 and self.y1 == self.zabranjen2):
            return
        plt.axis('equal')
        plt.plot(x,y,"-", lw=0.5, color='k')
        

    def breakSegment(self, n):  #lomi liniju na 5 jednakih delova
        x=np.zeros(n+1)
        y=np.zeros(n+1)
        dx=(self.x2-self.x1)/n
        dy=(self.y2-self.y1)/n
        for i in range(n+1):
            x[i]=self.x1+dx*i
            y[i]=self.y1+dy*i
        return x,y

        
    def rotation(x, y, phi):  # rotira polomljene linije po zadatoj N
        phi=phi*np.pi/180.
        dx=x[1]-x[0]
        dy=y[1]-y[0]
        xr=x[0]+dx*np.cos(phi)-dy*np.sin(phi)
        yr=y[0]+dx*np.sin(phi)+dy*np.cos(phi)
        return xr, yr

    def createSegmentList(x,y):
        list_seg=[]
        for i in range(len(x)-1):
            seg_new=Segment()
            seg_new.x1 = x[i]
            seg_new.y1 = y[i]
            seg_new.x2 = x[i+1]
            seg_new.y2 = y[i+1]
            list_seg.append(seg_new)
        return list_seg

    def create_shape(x,y,n):
        x1=np.zeros(len(x)+1)
        y1=np.zeros(len(x)+1)
        x1[:n+1]=x[:n+1]
        y1[:n+1]=y[:n+1]
        x1[n+2:]=x[n+1:]
        y1[n+2:]=y[n+1:]
        x1[n+1], y1[n+1]=Segment.rotation([x[n],x[n+1]],[y[n],y[n+1]], 60)
        return x1, y1

def ucitajPocetneKoord():
    lista =[int(x) for x in n3.get().split()]
    return len(lista), lista

def akcija(n):
    imaIh, pocetneKoord = ucitajPocetneKoord()

    A=Segment()
    if imaIh == 4:
        A.setStartingCoordinates(pocetneKoord[0],pocetneKoord[1],pocetneKoord[2],pocetneKoord[3] )
    list_seg=[A]
    for j in range(n):
        list_new = []
        if n > 5:
            print("Nije dozvoljeno iznad 5")
            break
        for i in list_seg:
            x,y=i.breakSegment(3)
            x,y=Segment.create_shape(x,y,1)
            list_sub_seg=Segment.createSegmentList(x,y)
            for k in list_sub_seg:
                list_new.append(k)
        list_seg=list_new
    for i in list_seg:        
        i.display()
    A.display()
    plt.show()

root = Tk()
tss = TkinterSaSlikomiDugmetom('Primer slike u tkinteru', 'bitcoin.jpg')
tss.setGeometry(600, 700)

L1 = Label(root, text="Nivo prikaza n:")
L1.pack(side=TOP, pady=10)


n = StringVar()
n3 = StringVar()

n1 = Entry(root,  textvariable=n)
n1.pack(side=TOP, pady=5)

L2 = Label(root, text="Proizvoljne A(xa,ya),B(xb,yb) koordinate:")
L2.pack(side=TOP, padx=10)
n2 = Entry(root,  textvariable=n3)
n2.pack(side=TOP, padx=15, pady=20)


B1 = Button(root, text="Crtaj",command= lambda: akcija(int(n.get())))
B1.pack(side = TOP, padx=15, pady=20)

root.mainloop()