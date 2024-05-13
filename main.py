from tkinter import *
from views.form_fact1 import form_fact
from views.form_fact import f2

from utils.table_utils import utils_table

ventana= Tk()
ventana.title("crud")
ventana.geometry("1000x700")


marco= LabelFrame(ventana, text="Gestion de Facturas")
marco.place(x=5, y=5, width=1200, height=700)

form_fact()

utils_table(marco)
# f2()


ventana.mainloop()
