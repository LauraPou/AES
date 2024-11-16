import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

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
    #labelArchivoEntrada.pack()
    img = Image.open(root.filename)

    img_tk = ImageTk.PhotoImage(img)  
    labelImg.config(image=img_tk, height=300, width=300)
    
    labelImg.image = img_tk
    archivoBMP = root.filename

def cifradoECB(ruta, llave, C0):
    messagebox.showinfo("info", "estás en modo ECB de cifrado")
    llave = llave.encode("utf-8")   # Convierte a bytes la llave

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    # Cifrado con AES en modo ECB 
    cifrado = AES.new(llave, AES.MODE_ECB)

    # Cifrar los datos de píxeles (rellenados para ser múltiplos de 16 bytes)
    encrypted_pixel_data = cifrado.encrypt(pad(pixel_data, AES.block_size))

    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_eECB{file_extension}"

    # Guardar la imagen cifrada con la misma cabecera
    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + encrypted_pixel_data)
        
    labelArchivoSalida = tk.Label(root, text="\n\nImagen cifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk, height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

def cifradoCBC(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo CBC de cifrado")
    llave = llave.encode("utf-8")   # Convierte a bytes la llave
    C0 = C0.encode("utf-8")    # Convierte a bytes el vector inicial

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]
    
    cifrado = AES.new(llave, AES.MODE_CBC, C0)
    # Cifrar los datos de píxeles (rellenados para ser múltiplos de 16 bytes)
    encrypted_pixel_data = cifrado.encrypt(pad(pixel_data, AES.block_size))

    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_eCBC{file_extension}"

    # Guardar la imagen cifrada con la misma cabecera y el C0 al final
    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + encrypted_pixel_data)
        
    labelArchivoSalida = tk.Label(root, text="\n\nImagen cifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk,height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk
   
def cifradoCFB(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo CFC de cifrado")
    llave = llave.encode("utf-8")   # Convierte a bytes la llave
    C0 = C0.encode("utf-8")    # Convierte a bytes el vector inicial

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]
    
    cifrado = AES.new(llave, AES.MODE_CFB, C0)

    # Cifrar los datos de píxeles (SIN RELLENO)
    encrypted_pixel_data = cifrado.encrypt(pixel_data)

    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_eCFB{file_extension}"

    # Guardar la imagen cifrada 
    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + encrypted_pixel_data)
        
    labelArchivoSalida = tk.Label(root, text="\n\nImagen cifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk,height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

def cifradoOFB(ruta, llave, C0):
    messagebox.showinfo("info", "estás en modo OFB de cifrado")
    
    llave = llave.encode("utf-8")   # Convierte a bytes la llave
    C0 = C0.encode("utf-8")    # Convierte a bytes el vector inicial

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]

    # Crear el cifrador AES en modo OFB
    cifrado = AES.new(llave, AES.MODE_OFB, iv=C0)

    # Cifrar los datos de píxeles
    encrypted_pixel_data = cifrado.encrypt(pixel_data)

    # Guardar la imagen cifrada
    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_eOFB{file_extension}"

    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + encrypted_pixel_data)

    labelArchivoSalida = tk.Label(root, text="\n\nImagen cifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk, height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

def descifradoECB(ruta, llave, C0):
    messagebox.showinfo("info", "estás en modo ECB de descifrado")
    llave = llave.encode("utf-8")   # Convierte a bytes la llave

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen cifrada
    header = bmp_data[:54]
    encrypted_pixel_data = bmp_data[54:]

    # Descifrar con AES en modo ECB
    cifrado = AES.new(llave, AES.MODE_ECB)

    # Descifrar los datos de píxeles (y quitar el relleno)
    decrypted_pixel_data = unpad(cifrado.decrypt(encrypted_pixel_data), AES.block_size)

    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_dECB{file_extension}"

    # Guardar la imagen descifrada con la misma cabecera
    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + decrypted_pixel_data)
        
    labelArchivoSalida = tk.Label(root, text="\n\nImagen descifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk, height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

def descifradoCBC(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo CBC de descifrado")
    llave = llave.encode("utf-8")   # Convierte a bytes la llave
    C0 = C0.encode("utf-8")    # Convierte a bytes el vector inicial

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]    

     # Crear el descifrador AES en modo CBC
    cipher = AES.new(llave, AES.MODE_CBC, C0)

    # Descifrar y quitar el relleno de los datos de píxeles
    decrypted_pixel_data = unpad(cipher.decrypt(pixel_data), AES.block_size)   

    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_dCBC{file_extension}"

    # Guardar la imagen descifrada
    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + decrypted_pixel_data)
        
    labelArchivoSalida = tk.Label(root, text="\n\nImagen cifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk,height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

def descifradoCFB(ruta, llave, C0):
    messagebox.showinfo("info", "estas en modo CFB de descifrado")
    llave = llave.encode("utf-8")   # Convierte a bytes la llave
    C0 = C0.encode("utf-8")    # Convierte a bytes el vector inicial

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen
    header = bmp_data[:54]
    pixel_data = bmp_data[54:]    

     # Crear el descifrador AES en modo CBC
    cipher = AES.new(llave, AES.MODE_CFB, C0)

    decrypted_pixel_data = cipher.decrypt(pixel_data)        

    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_dCFB{file_extension}"

    # Guardar la imagen descifrada 
    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + decrypted_pixel_data)
        
    labelArchivoSalida = tk.Label(root, text="\n\nImagen cifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk,height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

def descifradoOFB(ruta, llave, C0):
    messagebox.showinfo("info", "estás en modo OFB de descifrado")
    
    llave = llave.encode("utf-8")   # Convierte a bytes la llave
    C0 = C0.encode("utf-8")    # Convierte a bytes el vector inicial

    # Abrir la imagen BMP en modo binario
    with open(ruta, "rb") as f:
        bmp_data = f.read()

    # Separar la cabecera (primeros 54 bytes) y los datos de la imagen cifrada
    header = bmp_data[:54]
    encrypted_pixel_data = bmp_data[54:]

    # Crear el descifrador AES en modo OFB
    cifrado = AES.new(llave, AES.MODE_OFB, iv=C0)

    # Descifrar los datos de píxeles
    decrypted_pixel_data = cifrado.decrypt(encrypted_pixel_data)

    # Guardar la imagen descifrada
    file_name, file_extension = os.path.splitext(ruta)
    nuevoNombreArchivo = f"{file_name}_dOFB{file_extension}"

    with open(nuevoNombreArchivo, "wb") as f:
        f.write(header + decrypted_pixel_data)

    labelArchivoSalida = tk.Label(root, text="\n\nImagen descifrada guardada en " + nuevoNombreArchivo)
    labelArchivoSalida.pack()

    img = Image.open(nuevoNombreArchivo)
    img_tk = ImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=img_tk, height=300, width=300)
    labelImg.pack()  
    labelImg.image = img_tk

def algoritmoAES(proceso, modoOperacion, ruta, llave, C0):
    limpiarVentana()
    if proceso == "cifrado":
        # messagebox.showinfo("info", "estás en: cifrado")
        if modoOperacion == "ECB":
            cifradoECB(ruta, llave, C0)
        if modoOperacion == "CBC":
            cifradoCBC(ruta, llave, C0)
        if modoOperacion == "CFB":
            cifradoCFB(ruta, llave, C0)
        if modoOperacion == "OFB":
            cifradoOFB(ruta, llave, C0)            

    if proceso == "descifrado":
        # messagebox.showinfo("info2", "estas en descifrado")
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