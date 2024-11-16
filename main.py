import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

# llave: 4578123547854458
# C0:    5877961021354763

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

    buttonEnviar = tk.Button(root, text="Siguiente", command=enviar, font=("Arial", 14))
    buttonEnviar.pack()

def limpiarVentana():
    for widget in root.winfo_children():
        widget.destroy()

def buscarArchivo(labelArchivoEntrada,labelImg):
    global archivoBMP
    root.filename = filedialog.askopenfilename(title="Buscar imagen", filetypes=([("archivos bmp", "*.bmp")]))
    labelArchivoEntrada.config(text= "Ruta del archivo seleccionado:\n"+root.filename, font=("Arial", 14))
    img = Image.open(root.filename)

    img_tk = ImageTk.PhotoImage(img)  
    labelImg.config(image=img_tk, height=300, width=300)
    
    labelImg.image = img_tk
    archivoBMP = root.filename

def algoritmoAES(proceso, modoOperacion, ruta, llave, C0):
    limpiarVentana()
    llave = llave.encode("utf-8")
    llave = hashlib.md5(llave).hexdigest().encode("utf-8")
    C0 = C0.encode("utf-8")    # Convierte a bytes el vector inicial

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    if modoOperacion == "ECB":
            cifrado = AES.new(llave, AES.MODE_ECB)
    if modoOperacion == "CBC":
            cifrado = AES.new(llave, AES.MODE_CBC, C0)
    if modoOperacion == "CFB":
            cifrado = AES.new(llave, AES.MODE_CFB, C0)
    if modoOperacion == "OFB":
            cifrado = AES.new(llave, AES.MODE_OFB, C0)

    if proceso == "cifrado":
        if(modoOperacion == "ECB" or modoOperacion == "CBC"):
            encrypted_pixel_data = cifrado.encrypt(pad(pixel_data, AES.block_size))
        else:
             encrypted_pixel_data = cifrado.encrypt(pixel_data)

        file_name, file_extension = os.path.splitext(ruta)
        nuevoNombreArchivo = f"{file_name}_e{modoOperacion}{file_extension}"
        with open(nuevoNombreArchivo, "wb") as f:
            f.write(header + encrypted_pixel_data)
        labelArchivoSalida = tk.Label(root, text="\n\nImagen cifrada guardada en " + nuevoNombreArchivo)
        labelArchivoSalida.pack()
        
    if proceso == "descifrado":
        if(modoOperacion == "ECB" or modoOperacion == "CBC"):
            decrypted_pixel_data = unpad(cifrado.decrypt(pixel_data), AES.block_size)
        else:
            decrypted_pixel_data = cifrado.decrypt(pixel_data)

        decrypted_pixel_data = cifrado.decrypt(pixel_data)
        file_name, file_extension = os.path.splitext(ruta)
        nuevoNombreArchivo = f"{file_name}_d{modoOperacion}{file_extension}"
        with open(nuevoNombreArchivo, "wb") as f:
            f.write(header + decrypted_pixel_data)
        labelArchivoSalida = tk.Label(root, text="\n\nImagen descifrada guardada en " + nuevoNombreArchivo)
        labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk, height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

    buttonRegresarInicio = tk.Button(root, text="Volver al inicio", command=inicio, font=("Arial", 14))
    buttonRegresarInicio.pack(side="bottom")

def enviar():
    proceso = valueProceso.get()
    modoOperacion = valueModoOperacion.get()
    limpiarVentana()

    texto = "Has elegido " + proceso + " con " + modoOperacion
    labelTitulo = tk.Label(root, text=texto , font=("Arial", 14))
    labelTitulo.pack()

    labelLlave = tk.Label(root, text="Llave: ", font=("Arial", 14))
    labelLlave.pack()
    entryLlave = tk.Entry(root)
    entryLlave.pack()
    
    if(modoOperacion != 'ECB'):
        labelC0 = tk.Label(root, text="Vector de inicialización (C0): ", font=("Arial", 14))
        labelC0.pack()
        entryC0 = tk.Entry(root)
        entryC0.pack()
    else:
        entryC0 = tk.Entry(root, textvariable="0")

    labelArchivoEntrada = tk.Label(root, text="No se ha seleccionado ningún archivo", font=("Arial", 14))
    labelArchivoEntrada.pack()
    
    labelImg = tk.Label(root)
    labelImg.pack()

    buttonBuscarArchivo = tk.Button(root, text="Buscar archivo", command=lambda: buscarArchivo(labelArchivoEntrada,labelImg), font=("Arial", 14))
    buttonBuscarArchivo.pack()
    
    buttonRegresarInicio = tk.Button(root, text="Volver al inicio", command=inicio, font=("Arial", 14))
    buttonRegresarInicio.pack(side="bottom")
    buttonEnviarCampos = tk.Button(root, text="Enviar", command=lambda: algoritmoAES(proceso, modoOperacion,archivoBMP, entryLlave.get(), entryC0.get()), font=("Arial", 14))
    buttonEnviarCampos.pack(side="bottom")

inicio()
root.mainloop()