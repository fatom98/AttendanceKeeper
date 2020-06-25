#Disable empty row selection

from tkinter import *
from tkinter import ttk
import os

class Classes:
    data = dict()
    def __init__(self):
        with open("class.txt", "r") as doc:
            for line in doc:
                lecture = line.split(",")[0]
                hour = int(line.split(",")[1].strip())
                missing = int(line.split(",")[2].strip())
                self.data[lecture] = [hour, missing]

class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.classes = Classes()
        self.initUI()

    def initUI(self):
        self.pack(fill = BOTH, expand = True)

        x = "#25d102"
        y  = "#015578"

        f1 = Frame(self)
        f1.pack(side = TOP, fill = X)

        self.f2 = Frame(self, bg = "#630611")
        self.f2.pack(side=TOP, fill = X, pady = (50,0), padx= 20)

        f3 = Frame(self, bg = "#630611")
        f3.pack(side=BOTTOM, fill = X, pady = (0,20), padx= 150)

        mainLabel = Label(f1, text = "Attendance Keeper", font = "ComicSans 16", bg = y, fg = "white").pack(fill = X)

        self.listItems = Listbox(self.f2, selectmode = "single", height = 24, width = 50, selectbackground = "green", activestyle = "none")
        self.listItems.bind("<ButtonRelease>", self.show)
        self.listItems.grid(row = 0, column = 0, rowspan = 5)

        button1 = Button(self.f2,font=("Verdana",10,'bold'), text="1 Hour", width="7", bd=0, bg=x, activebackground="#3c9d9b",fg='#ffffff', command = self.onehour)
        button1.grid(row = 1, column = 1, padx = 50)

        button2 = Button(self.f2,font=("Verdana",10,'bold'), text="2 Hours", width="7", bd=0, bg=x, activebackground="#3c9d9b",fg='#ffffff', command = self.twohours)
        button2.grid(row=2, column=1, padx = 50)

        button3 = Button(self.f2,font=("Verdana",10,'bold'), text="3 Hours", width="7", bd=0, bg=x, activebackground="#3c9d9b",fg='#ffffff', command = self.threehours)
        button3.grid(row=3, column=1, padx = 50)

        self.showItems = Listbox(self.f2, height=24, width=50)
        self.showItems.grid(row=0, column=2, rowspan=5)

        Grid.columnconfigure(self.f2, 0, weight = 1)
        Grid.columnconfigure(self.f2, 1, weight = 1)
        Grid.columnconfigure(self.f2, 2, weight = 1)

        showFile = Button(f3,font=("Verdana",10,'bold'), text="Show File", width="8", bd=0, bg=x, activebackground="#3c9d9b",fg='#ffffff', command = self.show_file)
        showFile.grid(row = 0, column = 0)

        save = Button(f3,font=("Verdana",10,'bold'), text="Save", width="7", bd=0, bg=x, activebackground="#3c9d9b",fg='#ffffff', command = self.save)
        save.grid(row = 0, column = 1)

        exit =  Button(f3,font=("Verdana",10,'bold'), text="Exit", width="7", bd=0, bg=x, activebackground="#3c9d9b",fg='#ffffff', command = self.exit)
        exit.grid(row = 0, column = 2)

        Grid.columnconfigure(f3, 0, weight = 1)
        Grid.columnconfigure(f3, 1, weight = 1)
        Grid.columnconfigure(f3, 2, weight = 1)
        self.fetch()

    def fetch(self):
        self.data = self.classes.data
        for line in self.data:
            self.listItems.insert("end", line)
            self.listItems.insert("end", "")

    def show(self, event):
        self.selected = self.listItems.get(self.listItems.curselection())
        if self.selected != "": self.calculate()

    def calculate(self):
        self.showItems.bindtags((self.showItems, self.f2, "all"))
        self.showItems.delete(0, "end")
        lecture = self.selected
        hour = self.data[self.selected][0]
        missing = self.data[self.selected][1]
        self.totalHoursInSemester = 14 * hour
        percentage = (self.totalHoursInSemester - missing) / (self.totalHoursInSemester) * 100
        percentage = float("{:.2f}".format(percentage))
        if percentage <= 100 and percentage > 90: state = "Fine"
        elif percentage <= 90 and percentage > 80: state = "OK"
        elif percentage <=80 and percentage > 50: state = "Critic"
        elif percentage <= 50 and percentage > 0: state = "Failed"
        else:
            percentage = 0
            state = "Failed"

        self.showItems.insert("end", "Your Lecture information will appear below")
        self.showItems.insert("end", "")
        self.showItems.insert("end", f"Lecture Name: {lecture}")
        self.showItems.insert("end", "")
        self.showItems.insert("end", f"Lecture hours in one week: {hour}")
        self.showItems.insert("end", "")
        self.showItems.insert("end", f"Missing hours: {missing}")
        self.showItems.insert("end", "")
        self.showItems.insert("end", f"percentage: %{percentage}")
        self.showItems.insert("end", "")
        self.showItems.insert("end", f"State: {state}")

        if state == "Fine" or state == "OK": self.showItems.itemconfig(10, fg = "green" )
        if state == "Critic": self.showItems.itemconfig(10, fg = "orange" )
        if state == "Failed": self.showItems.itemconfig(10, fg = "red" )

    def onehour(self):
        try:
            if self.data[self.selected][1] < self.totalHoursInSemester:
                self.data[self.selected][1] += 1
                self.calculate()
        except AttributeError as hata1:
            pass
        except KeyError as hata2:
            pass

    def twohours(self):
        try:
            if self.data[self.selected][1] < self.totalHoursInSemester:
                self.data[self.selected][1] += 2
                self.calculate()
        except AttributeError:
            pass
        except KeyError:
            pass

    def threehours(self):
        try:
            if self.data[self.selected][1] < self.totalHoursInSemester:
                self.data[self.selected][1] += 3
                self.calculate()
        except AttributeError:
            pass
        except KeyError:
            pass

    def save(self):
        with open("class.txt", "w") as doc:
            for line in self.data:
                doc.write(f"{line}, {self.data[line][0]}, {self.data[line][1]}\n")

    def exit(self):
        exit()

    def show_file(self):
        os.system("start" + "./class.txt")

if __name__ == '__main__':
    root = Tk()
    app = GUI(root)
    root.title("Attendance Keeper V2.0")
    app.config(bg = "#630611")
    root.geometry("900x600+250+25")
    root.mainloop()
