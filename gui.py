import tkinter as tk
from main import *

def read_and_write(ai_name):

    a = read_ai(ai_name)
    write_ai(a,"best")

root = tk.Tk()

inputtxt = tk.Text(root, height = 1, width = 15)
inputtxt.pack()

inputtxt2 = tk.Text(root, height = 1, width = 15)
inputtxt2.pack()

button1 = tk.Button(root, text = "Self train infinite", command = lambda: run_vs_self(0,True,int(inputtxt2.get(1.0, "end-1c")),True))
button1.pack()

button1 = tk.Button(root, text = "Self train one round", command = lambda: run_vs_self(0,True,int(inputtxt2.get(1.0, "end-1c")),False))
button1.pack()

button1 = tk.Button(root, text = "Other train infinite", command = lambda: run_vs_other(0,True,inputtxt.get(1.0, "end-1c"),['huns','huns'],int(inputtxt2.get(1.0, "end-1c")),True))
button1.pack()

button1 = tk.Button(root, text = "Other train one round", command = lambda: run_vs_other(0,True,inputtxt.get(1.0, "end-1c"),['huns','huns'],int(inputtxt2.get(1.0, "end-1c")),False))
button1.pack()

button1 = tk.Button(root, text = "FFA new start", command = lambda: run_ffa(0,False))
button1.pack()

button1 = tk.Button(root, text = "FFA load", command = lambda: run_ffa(0,True))
button1.pack()

button1 = tk.Button(root, text = "Save AI", command = backup)
button1.pack()

button1 = tk.Button(root, text = "Benchmark", command = lambda: benchmarker("best",inputtxt.get(1.0, "end-1c"),100,['huns','huns']))
button1.pack()

button1 = tk.Button(root, text = "Ladder", command = lambda: group_train(ai_ladder,True,int(inputtxt2.get(1.0, "end-1c"))))
button1.pack()

inputtxt3 = tk.Text(root, height = 1, width = 15)
inputtxt3.pack()

button1 = tk.Button(root, text = "Write AI", command = lambda: read_and_write(inputtxt3.get(1.0, "end-1c")))
button1.pack()

button1 = tk.Button(root, text = "Speed score", command = lambda: speed_train(inputtxt.get(1.0, "end-1c")))
button1.pack()

button1 = tk.Button(root, text = "ELO Train", command = lambda: elo_train())
button1.pack()

button1 = tk.Button(root, text = "Other train slow", command = lambda: run_vs_other_slow(0,True,inputtxt.get(1.0, "end-1c"),['huns','huns'],40,True))
button1.pack()

button1 = tk.Button(root, text = "Self train slow", command = lambda: run_vs_self_slow(0,True,40))
button1.pack()

root.mainloop()
