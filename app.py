from json import loads
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import sys

def readJSON():
    setting = loads( open("E:\\0 quang\\fun\\tkinter\\text-editor\\setting.json","r").read())
    return [setting["first_width"], setting["first_height"], setting["icon"], setting["workspace"], 
    setting["font"], setting["color_char"], setting["background_color"], setting["select_background"]]

try:
    data = readJSON()
    if len(sys.argv) == 0:
        inFile = "Untitled"
    elif len(sys.argv) > 0:
        inFile = sys.argv[-1]
    root = Tk()
    root.title(inFile)
    root.iconbitmap(f"{data[2]}")
    root.geometry(f"{data[0]}x{data[1]}")
    workspace = data[3]

    global selected
    selected = False

    # root.configure(background="#404254")
    def newFile(e):
        global inFile
        text.delete("1.0",END)
        root.title(inFile)
        statusBar.config(text=inFile)


    def openFile(e):
        global inFile
        text.delete("1.0",END)
        text_file = filedialog.askopenfilename(initialdir=workspace,title="open",filetypes=(("All Files","*.*"),
        ("do script Files","*.do")))
        inFile = text_file
        root.title(inFile)

        statusBar.config(text=inFile)
        ftxt = open(text_file,"r")
        fileContent = ftxt.read()
        text.insert(END,fileContent)
        ftxt.close()

    def saveAs(e):
        global inFile
        text_file=filedialog.asksaveasfilename(defaultextension="Untitled.txt",initialdir=workspace,title="save as",
        filetypes=(("All Files","*.*"),("do script Files","*.do")))
        if text_file:
            inFile = text_file
            root.title(inFile)
        f = open(text_file,"w")
        f.write(text.get(1.0,END))
        f.close()
        statusBar.config(text=f"saved {inFile}")

    def save(e):
        global inFile
        if inFile != "Untitled":
            text_file = open(inFile,"w")
            text_file.write(text.get(1.0,END))
            text_file.close()
        else:
            saveAs(1)
        statusBar.config(text=f"saved {inFile}")

    def cut_T(e):
        global selected
        if text.selection_get():
            selected = text.selection_get()
            text.delete("sel.first","sel.last")
            text.pack()

    def copy_T(e):
        global selected
        if text.selection_get():
            selected = text.selection_get()
            text.pack()

    def paste_T(e):
        if selected:
            position = text.index(INSERT)
            text.insert(position,selected)
            text.pack()
        else:pass


    frame = Frame(root)
    frame.pack(pady=5)
    #selectforeground="black"
    text_scroll = Scrollbar(frame)
    text_scroll.pack(side=RIGHT,fill=Y)

    hor_scroll = Scrollbar(frame,orient="horizontal")
    hor_scroll.pack(side=BOTTOM,fill=X)

    text = Text(frame, width=89,height=18,font=(data[4], 16), selectbackground=data[-1],
    fg=data[5], undo=True, yscrollcommand=text_scroll.set,wrap="none",xscrollcommand=hor_scroll.set )
    text.pack()
    text.configure(background=data[6])
    text_scroll.config(command=text.yview)
    hor_scroll.config(command=text.xview)

    text_scroll.config(command=text.yview )
    backgroundD = data[6]
    menu = Menu(root,background=backgroundD,fg=data[5])
    root.config(menu=menu)
    fileMenu = Menu(menu,tearoff=False,background=backgroundD,fg=data[5])
    menu.add_cascade(label="File",menu=fileMenu)
    fileMenu.add_command(label="New",command=lambda: newFile(1),accelerator="(Ctr+n)")
    fileMenu.add_command(label="Open",command=lambda: openFile(1),accelerator="(Ctr+o)")
    fileMenu.add_command(label="Save",command=lambda: save(1),accelerator="(Ctr+s)")
    fileMenu.add_command(label="Save As",command=lambda: saveAs(1),accelerator="(Ctr+Shift+s)")
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit",command=root.quit)

    editMenu = Menu(menu, tearoff=False,background=backgroundD,fg=data[5])
    menu.add_cascade(label="Edit",menu=editMenu)
    editMenu.add_command(label="Cut", command=lambda: cut_T(1),accelerator="(Ctr+x)")
    editMenu.add_command(label="Copy", command=lambda: copy_T(1),accelerator="(Ctr+c)")
    editMenu.add_command(label="Paste", command=lambda: paste_T(1),accelerator="(Ctr+v)")
    editMenu.add_command(label="Undo", command=text.edit_undo,accelerator="(Ctr+z)")
    editMenu.add_command(label="Redo", command=text.edit_redo,accelerator="(Ctr+y)")


    if inFile != "Untitled":
        
        ftxt = open(inFile,"r")
        fileContent = ftxt.read()
        text.insert(END,fileContent)
        ftxt.close()

    statusBar = Label(root,text=f"Untitled",anchor=E)
    statusBar.pack(fill=X,side=LEFT,ipady=30.0)

    # def a(e):print(123)

    root.bind("<Control-n>",newFile)
    root.bind("<Control-o>", openFile)
    root.bind("<Control-s>", save)
    root.bind("<Control-S>", saveAs)


    root.bind("<Control-x>",cut_T)
    root.bind("<Control-c>",copy_T)
    root.bind("<Control-v>",paste_T)
    root.bind("<Control-z>",text.edit_undo)
    root.bind("<Control-y>",text.edit_redo)

    print(sys.argv[1])
    root.mainloop()
except Exception as bug:
    print(bug)
finally:
    print("exited")
    sys.exit()

