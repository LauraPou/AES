import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("600x600")
root.title("AES")

valueProceso = tk.StringVar(value="-")
valueModoOperacion = tk.StringVar(value="-")

def inicio():
    limpiarVentana()
    label = tk.Label(root, text="Práctica Cifrador por bloques (AES)", font=("Arial", 16, "bold"))
    label.pack()

    pregunta = tk.Label(root, text="\n¿Qué quieres realizar?", font=("Arial", 14))
    pregunta.pack()

    radioC = tk.Radiobutton(root, text="Cifrado", variable=valueProceso, value="cifrado", font=("Arial", 14))
    radioC.pack()

    radioD = tk.Radiobutton(root, text="Descifrado", variable=valueProceso, value="descifrado", font=("Arial", 14))
    radioD.pack()

    labelModoOperacion = tk.Label(root, text="\nElige el modo de operación:", font=("Arial", 14))
    labelModoOperacion.pack()

    radioECB = tk.Radiobutton(root, text="ECB", variable=valueModoOperacion, value="ECB", font=("Arial", 14))
    radioECB.pack()

    radioCBC = tk.Radiobutton(root, text="CBC", variable=valueModoOperacion, value="CBC", font=("Arial", 14))
    radioCBC.pack()

    radioCFB = tk.Radiobutton(root, text="CFB", variable=valueModoOperacion, value="CFB", font=("Arial", 14))
    radioCFB.pack()

    radioOFB = tk.Radiobutton(root, text="OFB", variable=valueModoOperacion, value="OFB", font=("Arial", 14))
    radioOFB.pack()

    buttonEnviar = tk.Button(root, text="Enviar", command=enviar, font=("Arial", 14))
    buttonEnviar.pack()

def limpiarVentana():
    for widget in root.winfo_children():
        widget.destroy()

def buscarArchivo(labelArchivoEntrada,labelImg):
    global archivoBMP
    root.filename = filedialog.askopenfilename(title="Buscar imagen", filetypes=([("archivos bmp", "*.bmp")]), font=("Arial", 14))
    labelArchivoEntrada.config(text= "Ruta del archivo seleccionado:\n"+root.filename, font=("Arial", 14))
    #labelArchivoEntrada.pack()
    img = Image.open(root.filename)

    img_tk = ImageTk.PhotoImage(img)  
    labelImg.config(image=img_tk, height=300, width=300)
    
    labelImg.image = img_tk
    archivoBMP = root.filename

def cifradoECB(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo ECB de cifrado")

def cifradoCBC(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo CBC de cifrado")

def cifradoCFB(ruta, llave, C0):
    # Los messagebox solo son para confirmar que entran a la funcipon correcta
    messagebox.showinfo("info", "estas en modo CFB de cifrado")
    # los label son para ver si sí se reciben bien los parámetros 
    labelRuta = tk.Label(root, text=ruta)
    labelRuta.pack()

    labelLlave = tk.Label(root, text=llave)
    labelLlave.pack()

    labelC0 = tk.Label(root, text=C0)
    labelC0.pack()

def cifradoOFB(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo OFB de cifrado")
    labelRuta = tk.Label(root, text=ruta)
    labelRuta.pack()

    labelLlave = tk.Label(root, text=llave)
    labelLlave.pack()

    labelC0 = tk.Label(root, text=C0)
    labelC0.pack()

def descifradoECB(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo ECB de descifrado")
    
def descifradoCBC(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo CBC de descifrado")

def descifradoCFB(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo CFB de descifrado")

def descifradoOFB(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo OFB de descifrado")

def AES(proceso, modoOperacion, ruta, llave, C0):
    limpiarVentana()
    if proceso == "cifrado":
        messagebox.showinfo("info", "estás en: cifrado")
        if modoOperacion == "ECB":
            cifradoECB(ruta, llave, C0)
        if modoOperacion == "CBC":
            cifradoCBC(ruta, llave, C0)
        if modoOperacion == "CFB":
            cifradoCFB(ruta, llave, C0)
        if modoOperacion == "OFB":
            cifradoOFB(ruta, llave, C0)            

    if proceso == "descifrado":
        messagebox.showinfo("info2", "estas en descifrado")
        if modoOperacion == "ECB":
            descifradoECB(ruta, llave, C0)
        if modoOperacion == "CBC":
            descifradoCBC(ruta, llave, C0)
        if modoOperacion == "CFB":
            descifradoCFB(ruta, llave, C0)
        if modoOperacion == "OFB":
            descifradoOFB(ruta, llave, C0)
    buttonRegresarInicio = tk.Button(root, text="Volver al inicio", command=inicio, font=("Arial", 14))
    buttonRegresarInicio.pack(side="bottom")

def enviar():
    proceso = valueProceso.get()
    modoOperacion = valueModoOperacion.get()
    messagebox.showinfo("Elección",  "Has elegido:\n" + proceso + "\n"+ modoOperacion)
    limpiarVentana()

    labelLlave = tk.Label(root, text="Llave: ", font=("Arial", 14))
    labelLlave.pack()
    entryLlave = tk.Entry(root)
    entryLlave.pack()
    
    labelC0 = tk.Label(root, text="Vector de inicialización (C0): ", font=("Arial", 14))
    labelC0.pack()
    entryC0 = tk.Entry(root)
    entryC0.pack()
   
    labelArchivoEntrada = tk.Label(root, text="No se ha seleccionado ningún archivo", font=("Arial", 14))
    labelArchivoEntrada.pack()
    
    labelImg = tk.Label(root)
    labelImg.pack()

    buttonBuscarArchivo = tk.Button(root, text="Buscar archivo", command=lambda: buscarArchivo(labelArchivoEntrada,labelImg), font=("Arial", 14))
    buttonBuscarArchivo.pack()
    
    buttonRegresarInicio = tk.Button(root, text="Volver al inicio", command=inicio, font=("Arial", 14))
    buttonRegresarInicio.pack(side="bottom")
    buttonEnviarCampos = tk.Button(root, text="Enviar", command=lambda: AES(proceso, modoOperacion,archivoBMP, entryLlave.get(), entryC0.get()), font=("Arial", 14))
    buttonEnviarCampos.pack(side="bottom")

inicio()

root.mainloop()