import io
import re
import pickle
import os
from collections import Counter
from itertools import repeat,chain
from docx import Document

#User defined objects
from tries import TrieNode , Trie
from stop_words import StopTrieNode , StopTrie

#GUI Package
import tkinter
from tkinter import *
from tkinter import filedialog

#Database
stop_words =StopTrie()
with open('stop_words.pickle', 'rb') as handle:
        stop_words = pickle.load(handle)
trie_db=Trie()
htable = []
hash_key = -1
file_supported=('.log','.txt','.c','.cpp','.html','.docx')

#Counter and globals
total_ind=0
total_err=0
to_walk=''

#Common buffers
file_q=[]


def hashfucn(filepath):
    global hash_key
    hash_key+=1
    htable.append(filepath)
    return hash_key

def remove_duplicates(values):
    set1 = set(values)
    return list(set1)

def keywords(fname):
    global total_err
    global total_ind
    keywrd_list=[]
    line='\t'
    if fname.endswith(".docx"):
        try:
            fullText = []
            document = Document(fname)
            for para in document.paragraphs:
                fullText.append(para.text)
            line='\n'.join(fullText)
        except:
            total_err+=1
            return keywrd_list
    else:
        file1 = open(fname)
        try:
            line = file1.read()
        except:
            total_err+=1
            return keywrd_list
    line=line.lower()
    line=re.sub("[^a-z]+"," ", line)
    words = line.split()
    total_ind+=1
    for tmp in words:
        if not stop_words.search(tmp):
            keywrd_list.append(tmp)
    return keywrd_list    
        
def fileLister():
    global to_walk
    global file_supported
    for path, subdirs, files in os.walk(to_walk):
        for filename in files:
            f = os.path.join(path, filename)
            if (filename.lower()).endswith(file_supported):
                file_q.append(str(f))
    return

def insert_into_trie(klist,i):
    for key in klist:
        trie_db.insert(key,i)
    return
def fileIndexer():
    global file_q
    for filename in file_q:
        klist=keywords(filename)
        klist=remove_duplicates(klist)
        i=hashfucn(str(filename))
        insert_into_trie(klist,i)
    write()
    return
    
def write():
    try:
        with open('database.pickle', 'wb') as handle:
                pickle.dump(trie_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('htable.pickle', 'wb') as handle:
                pickle.dump(htable, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('to_walk.pickle', 'wb') as handle:
                pickle.dump(to_walk, handle, protocol=pickle.HIGHEST_PROTOCOL)
        lbl.config(text="Done Indexing: "+str(total_ind)+" files")
    finally:
        B.config(state="active")
        b2.config(state="active")
        return
    
def idx():
    global to_walk
    B.config(state="disabled")
    to_walk =  filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory to index')
    lbl2.config(text=str(to_walk))
    fileLister()
    fileIndexer()

def search_files():
    for widget in frame.winfo_children():
        widget.destroy()
    line=T.get("1.0",END)
    trie_db=Trie()
    hash_db=[]
    with open('database.pickle', 'rb') as handle:
            trie_db = pickle.load(handle)
    with open('htable.pickle', 'rb') as handle:
            hash_db = pickle.load(handle)
    lst=[]
    line=line.lower()
    line=re.sub("[^a-z]+"," ", line)
    words = line.split()
    for r in words:
        tmp=trie_db.search(r)
        lst.extend(tmp)
    lst=list(chain.from_iterable(repeat(i,c) for i,c in Counter(lst).most_common()))
    lst=sorted(set(lst),key=lambda x:lst.index(x))
    i=int(0)
    for n in lst:
        tkinter.Label(frame, text =str(os.path.basename(hash_db[n])),font = "Helvetica 12 bold",bg='white',fg='green').grid(row=i,column=0,columnspan=3)
        tkinter.Button(frame, text ="Open",font = "Helvetica 10 bold",command=lambda n=n: os.startfile(os.path.normpath(hash_db[n]))).grid(row=i,column=1)
        tkinter.Label(frame, wraplength=300,text ="Location:  "+str(hash_db[n]),font = "Helvetica 9",bg='white').grid(row=i+1,column=0,columnspan=5)
        tkinter.Label(frame, text =".............................................................................................................",font = "Helvetica 13",bg='white').grid(row=i+2)
        i=i+3
def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


root = tkinter.Tk()
root.title('Tesla, SearchENGINE!')
try:
    with open('to_walk.pickle', 'rb') as handle:
        to_walk = pickle.load(handle)
except:
    to_walk=''
top=Frame(root)
top.pack(side=TOP,expand=TRUE,fill=Y)
mid=Frame(root)
mid.pack(side=TOP,expand=TRUE,fill=Y)
tkinter.Label(top,text="Choose the directory to Index",fg = "black",font = "Helvetica 14 bold").pack()
B = tkinter.Button(top, text ="INDEX", command =idx,font = "Helvetica 16 bold")
B.pack()
lbl=tkinter.Label(top,text="",fg = "green",font = "Helvetica 16 bold")
lbl.pack()
lbl2=Label(top)
lbl2.pack()
tkinter.Label(mid,text="Enter The Search Words",fg = "black",font = "Helvetica 14 bold").pack()
S = Scrollbar(mid)
T = Text(mid, height=2, width=40)
T.pack(side=LEFT, fill=Y)
S.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
b2=Button(mid,text="Search",font = "Helvetica 16 bold",command=search_files)
b2.pack(side=RIGHT)
bot=Frame(root,height=200,width=200)
bot.pack(expand=TRUE,fill=BOTH)

tkinter.Label(bot, text ="Search Results",font = "Helvetica 16").pack()
if to_walk == '':
    b2.config(state="disabled")
else:
    lbl2.config(text=str(to_walk))
    
canvas = Canvas(bot, borderwidth=0, background="#ffffff",width=450)
frame = Frame(canvas, background="#ffffff")
vsb = Scrollbar(bot, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

root.geometry('650x600')
root.mainloop()
