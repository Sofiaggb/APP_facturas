from tkinter import *
from views.form_fact import form_fact
from utils.table_utils import utils_table

ventana= Tk()
ventana.title("crud")
ventana.geometry("1000x700")


marco= LabelFrame(ventana, text="Gestion de Facturas")
marco.place(x=5, y=5, width=1200, height=700)

form_fact(marco)
utils_table(marco)


ventana.mainloop()
