from tkinter import *

ventana= Tk()
ventana.title("crud")
ventana.geometry("600x600")

marco= LabelFrame(ventana, text="Gestion de Facturas")
marco.place(x=50, y=50, width=500, height=400)

# labels inputs
rif= StringVar()

lab_rif=Label(marco, text="rif").grid(row=0, column=0)
inp_rif= Entry(marco, textvariable=rif)
inp_rif.grid(column=1)

ventana.mainloop()
