import os
import ctypes
import customtkinter as ctk
from reportlab.pdfgen import canvas
from ctypes.wintypes import DWORD
from reportlab.lib.pagesizes import letter
import threading
import re
# Define la estructura GUID (Globally Unique Identifier) que se utiliza para 
# identificar las carpetas conocidas en Windows
class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", DWORD),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8)
    ]

# Define el GUID para la carpeta de descargas
FOLDERID_Downloads = GUID(0x374DE290, 0x123F, 0x4565, (0x91, 0x64, 0x39, 0xC4, 0x92, 0x5E, 0x46, 0x7B))

def get_known_folder_path(folderid):
    buf = ctypes.c_wchar_p()
    ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(folderid), 0, None, ctypes.byref(buf))
    path = buf.value
    ctypes.windll.ole32.CoTaskMemFree(buf)
    return path

def clean_text(text):
    # Eliminar caracteres no imprimibles
    return re.sub(r'[^\x20-\x7E]', '', text)

def draw_wrapped_text(c, text, x, y, max_width):
    # Divide el texto en palabras
    words = text.split()
    line = ""
    for word in words:
        # Si agregar la palabra a la línea actual excede el ancho máximo, dibuja la línea actual y comienza una nueva línea
        if c.stringWidth(line + " " + word) > max_width:
            c.drawString(x, y, line)
            y -= 14  # Ajusta la altura de línea según sea necesario
            line = word
        else:
            if line:
                line += " " + word
            else:
                line = word
    # Dibuja cualquier línea restante
    if line:
        c.drawString(x, y, line)
    return y

def draw_invoice(c, data):
    # Dibujar encabezado de la empresa
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "FACTURA")
    c.setFont("Helvetica", 12)
    c.drawString(50, 735, "Avenida, calle, Ciudad")
    c.drawString(50, 720, "Estado, Pais")
    c.drawString(50, 705, "Teléfono: 0111-1111111")

    # Dibujar detalles de la factura
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, 750, "Factura")
    c.setFont("Helvetica", 12)
    c.drawString(400, 735, f"Fecha: {str(data['fecha_emision_fact'])}")
    c.drawString(400, 720, f"Nro de la Factura: {data['nro_fact']}")

    # Dibujar detalles del cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 680, "Datos:")
    c.setFont("Helvetica", 12)
    c.drawString(50, 665, f"Nombre: {data['cliente']['nombre']}")
    c.drawString(50, 650, f"RIF/CI:{data['cliente']['rif']}")
    c.drawString(50, 635, f"Teléfono: {data['cliente']['telefono']}")
    c.drawString(50, 620, f"Dirección:{clean_text(data['cliente']['dirección'])}")


 # Dibujar tabla de elementos facturados
    if data["tipo_fact"] in ["Servicios Públicos",  "Impuestos"]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 580, "Descripción")
        c.drawString(300, 580, "Monto")
        c.drawString(380, 580, "Mes")

        c.setFont("Helvetica", 12)
        y = 560
        for item in data["servicios_impuestos"]:
            y = draw_wrapped_text(c, clean_text(item['descripcion_serv_impto']), 50, y, 250)
            # c.drawString(50, y, clean_text(item['descripcion_serv_impto']))
            c.drawString(300, y, f"{str(item['monto_serv_impto'])} Bs.")
            c.drawString(380, y, item['meses_serv_impto'])
            y -= 20

    else:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 580, "Descripción")
        c.drawString(300, 580, "Cantidad")
        c.drawString(370, 580, "Precio c/u")
        c.drawString(460, 580, "Total")

        c.setFont("Helvetica", 12)
        y = 560
        for producto in data['productos']:
            y = draw_wrapped_text(c, clean_text(producto['descripción_pdt']), 50, y, 250)
            # c.drawString(50, y, clean_text(producto['descripción_pdt']))
            c.drawString(300, y, str(producto['cantidad_pdt']))
            c.drawString(370, y, f"{str(producto['precio_pdt'])} Bs.")
            total_producto = float(producto['cantidad_pdt']) * float(producto['precio_pdt'])
            c.drawString(460, y, f"{total_producto:.2f} Bs.")
            y -= 20

    # Dibujar totales
        # Dibujar totales
    if data["tipo_fact"] in ["Servicios Públicos",  "Impuestos"]:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y - 20, "Total:")

        c.setFont("Helvetica", 12)
        c.drawString(450, y - 20, f"{str(data['monto_neto'])} Bs.")
    else:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(400, y - 20, "Subtotal:")
        c.drawString(400, y - 35, "IVA:")
        c.drawString(400, y - 50, "Total:")

        c.setFont("Helvetica", 12)
        c.drawString(460, y - 20, f"{str(data['monto_neto'])} Bs.")
        c.drawString(460, y - 35, f"{str(data['IVA'])} Bs.")
        c.drawString(460, y - 50, f"{str(data['monto_total'])} Bs.")

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1
    while os.path.exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1
    return path


def generate_pdf(data, progress_callback):
    downloads_folder = get_known_folder_path(FOLDERID_Downloads)
    # Uso:
    pdf_path = os.path.join(downloads_folder, "factura.pdf")
    unique_pdf_path = uniquify(pdf_path)
    c = canvas.Canvas(unique_pdf_path, pagesize=letter)
    # pdf_path = os.path.join(downloads_folder, "factura.pdf")
    # c = canvas.Canvas(pdf_path, pagesize=letter)
     # Inicializar progreso
    total_steps = 3
    step = 0
    
    # Actualizar progreso
    def update_progress():
        nonlocal step
        step += 1
        progress_callback(step / total_steps)
    draw_invoice(c, data)
    c.showPage()
    update_progress()
    c.save()
    update_progress()
    c = None  # Cierra el archivo PDF explícitamente
    update_progress()

class PDFGenerator:
    def __init__(self, data, progress_callback):
        self.data = data
        self.progress_callback = progress_callback

    def start_pdf_generation(self):
        thread = threading.Thread(target=generate_pdf, args=(self.data, self.progress_callback))
        thread.start()


