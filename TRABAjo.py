import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import colorchooser as colorchooser 
import tkinter as tk
import re
from aa import gauss
from tkinter import colorchooser as colorchooser
import pandas as pd





# creamos la ventana principal
ventana1 = tk.Tk()
ventana1.title('Ventana principal')
ventana1.geometry('500x150')
ventana1.configure(bg="pink")
sas=None

def limitar(entrada, limite):
    def limit(event):
        texto = entrada.get()
        if len(texto) >= limite and event.keysym != 'BackSpace':
            return "break"
    entrada.bind("<Key>", limit)

def limitar_letras(entrada, limite):
    def limit(event):
        texto = entrada.get()
        if len(texto) >= limite and event.keysym != 'BackSpace':
            return "break"
        if event.keysym == 'BackSpace':
            return
        if not event.char.isalpha():
            return "break"
    entrada.bind("<Key>", limit)

def limitar_numeros(entrada, limite):
    def limit(event):
        texto = entrada.get()
        if len(texto) >= limite and event.keysym != 'BackSpace':
            return "break"
        if event.keysym == 'BackSpace':
            return
        if not event.char.isdigit():
            return "break"
    entrada.bind("<Key>", limit)
# definimos las acciones asociadas a las opciones de los menús
def ADMINISTRADOR():
    texto.configure(text='Has elegido iniciar como administrador')
    ventana1.destroy()
    global sas
    sas="si"


def TRABAJADOR():
    texto.configure(text='Has elegido iniciar como trabajador')
    ventana1.destroy()
    global sas
    sas="no"
   

# creamos una barra de menús y la añadimos a la ventana principal
# cada ventana solo puede tener una barra de menús
barra_menus = tk.Menu(ventana1)
ventana1.config(menu=barra_menus)

# creamos un menú cuyo contenedor será la barra de menús
menu = tk.Menu(barra_menus, tearoff=False)

# añadimos opciones al menú indicando su nombre y acción asociado
menu.add_command(label='ADMINISTRADOR', command=ADMINISTRADOR)
menu.add_command(label='TRABAJADOR', command=TRABAJADOR)


# añadimos una línea separadora y la opción de salir
menu.add_separator()
menu.add_command(label='EXIT',  command=ventana1.destroy)
menu.configure(bg="yellow")

# finalmente añadimos el menú a la barra de menús
barra_menus.add_cascade(label="MENU PARA INICIAR SESION", menu=menu)

# añadimos una etiqueta para ver el efecto de los botones del menú
texto = tk.Label(ventana1, text='BIENVENIDO, ESCOJE TU CUENTA PARA INICIAR', bg="pink",font=("Comic Sans Ms",12,"bold"))
texto.place(x=50, y=50)
   
ventana1.mainloop()  
    
# Conectar a la base de datos
class asf():
    pass
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="alianza"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
    exit()


# Crear la tabla de trabajadores si no existe
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS trabajador (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255), edad INT, correo VARCHAR(255), folio INT(11), oficio VARCHAR(255))")
def validar_correo(correo):

    patron = r'^[a-zA-Z]+@gmail.com$'
    return re.match(patron, correo)

# Función para leer  los trabajadores de la base de datos
def leer_trabajadorDB():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM trabajador")
    return cursor.fetchall()
def mostrar():
    cursor=db.cursor()
    sentencia = "SELECT * FROM trabajador" 
    cursor.execute(sentencia)
    registro = cursor.fetchall()
    return registro

def mostrar_tabla():
    tabla_trabajador.delete(*tabla_trabajador.get_children())
    registro = mostrar()
    i = -1
    for dato in registro:
        i= i+1                       
        tabla_trabajador.insert('',i, text = registro[i][1:1], values=registro[i][0:6])
# Función para agregar un nuevo trabajador a la base de datos
def agregar_trabajadorDB(nombre, edad, correo, folio, oficio):
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO trabajador (nombre, edad, correo, folio, oficio ) VALUES (%s, %s, %s, %s, %s)", (nombre, edad, correo, folio, oficio))
        db.commit()
        datos=(nombre, edad, correo, folio, oficio)
        tabla_trabajador.insert('',0,text= nombre,values=datos)
        registro = mostrar()
        i = -1
        for dato in registro:
            i= i+1                       
            tabla_trabajador.insert('',i, text = registro[i][1:1], values=registro[i][0:5])
    except mysql.connector.Error as error:
        messagebox.showerror("Error al agregar el trabajador", f"No se pudo agregar el trabajador: {error}")
    finally:
        cursor.close()

# Función para actualizar un trabajador existente en la base de datos
def actualizar_trabajadorDB(id, nombre, edad, correo, folio, oficio):
    iid = int(id)
    cursor = db.cursor()
    cursor.execute("UPDATE `trabajador` SET `id`=%s,`nombre`=%s,`edad`=%s,`correo`=%s,`folio`=%s,`oficio`=%s WHERE id=%s", (iid, nombre, edad, correo, folio, oficio, iid))
    db.commit()
    
   
# Función para eliminar un alumno existente de la base de datos
def eliminar_trabajadorDB(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM trabajador WHERE id = %s", (id,))
    db.commit()

# Función para mostrar una lista de todos los alumnos
def mostrar_trabajador():
    # Limpiar la tabla
    for widget in tabla_trabajador.winfo_children():
        widget.destroy()

    # Obtener todos los alumnos
    trabajador = leer_trabajadorDB()

    # Mostrar los alumnos en la tabla
    for i, trabajador in enumerate(trabajador):
        id = trabajador[0]
        nombre = trabajador[1]
        edad = trabajador[2]
        correo = trabajador[3]
        folio = trabajador[4]
        oficio = trabajador[5]

# Función para agregar un nuevo alumno
def agregar_trabajador():

    # Obtener los datos del nuevo alumno
    try:
        correo = entrada_correo.get().lower()
        if validar_correo(correo):
            pass
        else:
            messagebox.showerror(message="El correo electronico no es valido")
            return
        
        edad = int(entrada_edad.get())
        if edad>=0 and edad<=99:
            pass
        else:
            messagebox.showerror(message="Ingresa una edad menor de o igual a '99'")
            return
        folio = int(entrada_folio.get())

        nombre = entrada_nombre.get()
        oficio = entrada_oficio.get()
        validar_nombre(nombre)
        validar_nombre(oficio)
        oficio = entrada_oficio.get()
        
    except Exception:
        pass
    
    def validar_nombre(nombre):
      return bool(re.match(r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z])$", nombre))
     
      
    # Validar que los campos no estén vacíos
    if not nombre or not edad or not correo or not folio or not oficio:
        messagebox.showerror("Error al agregar el trabajador", "Por favor ingrese todos los datos del trabajador")
        return

    # Agregar el nuevo alumno
    agregar_trabajadorDB(nombre, edad, correo, folio, oficio)

    # Limpiar los campos de entrada
    entrada_nombre.delete(0, END)
    entrada_edad.delete(0, END)
    entrada_correo.delete(0, END)
    entrada_folio.delete(0,END)
    entrada_oficio.delete(0,END)

    # Mostrar la lista actualizada de alumnos
    mostrar_trabajador()

# Función para actualizar un alumno existente

def actualizar_trabajador():
    # Obtener los datos del alumno a actualizar
    try:
        nombre = entrada_nombre.get()
        oficio = entrada_oficio.get()
        if nombre.isalpha() or oficio.isalpha():
            pass
        else:
            messagebox.showerror(message="La entrada nombre u oficio contiene carcteres no validos")
            return
        edad = int(entrada_edad.get())        
        if edad>=0 and edad<=99:
            pass
        else:
            messagebox.showerror(message="Ingresa una edad menor de o igual a '99'")
            return
        correo = entrada_correo.get().lower()
        if validar_correo(correo):
            pass
        else:
            messagebox.showerror(message="El correo electronico no es valido")
            return

        folio = int(entrada_folio.get())

        id = int(entrada_id.get())
    except Exception as e:
        messagebox.showerror(title="datos erroneos",message="datos erroneos{e}")
    
    # Validar que los campos no estén vacíos
    if not id or not nombre or not edad or not correo or not folio or not oficio:
        messagebox.showerror("Error al actualizar al trabajador", "Por favor ingrese todos los datos del trabajador")
        return

    # Actualizar el alumno
    actualizar_trabajadorDB(id=id,nombre=nombre,edad=edad,correo=correo,folio=folio,oficio=oficio)

    # Limpiar los campos de entrada
    entrada_id.delete(0, END)
    entrada_nombre.delete(0, END)
    entrada_edad.delete(0, END)
    entrada_correo.delete(0, END)
    entrada_folio.delete(0, END)
    entrada_oficio.delete(0, END)
    
    # Mostrar la lista actualizada de alumnos
    mostrar_trabajador()


# Función para eliminar un alumno existente
def eliminar_trabajador():
    # Obtener el ID del alumno a eliminar
    id = entrada_id.get()

    # Validar que se haya ingresado un ID
    if not id:
        messagebox.showerror("Error al eliminar el trabajador", "Por favor ingrese el ID del trabajdor")
        return

    # Preguntar al usuario si está seguro de eliminar el alumno
    confirmar = messagebox.askyesno("Confirmar eliminación", "¿Está seguro de eliminar este Trabajador?")

    if confirmar:
        # Eliminar el alumno
        eliminar_trabajadorDB(id)

        # Limpiar los campos de entrada
        entrada_id.delete(0, END)
        entrada_nombre.delete(0, END)
        entrada_edad.delete(0, END)
        entrada_correo.delete(0, END)
        entrada_folio.delete(0,END)
        entrada_oficio.delete(0,END)

        # Mostrar la lista actualizada de alumnos
        mostrar_trabajador()
def limpiar():
    entrada_id.delete(0,END)
    entrada_nombre.delete(0,END)
    entrada_edad.delete(0,END)
    entrada_correo.delete(0,END)
    entrada_folio.delete(0,END)
    entrada_oficio.delete(0,END)

   
    
    
def validar_decimal(self,valor):
      if valor.isdigit() or valor == "":
        return True
      else:
        return False
    
    
def validar_letras(valor):
        if valor.isalpha() or valor == "":
            return True
        else:
            return False    

def cerrar():

        global entrada_correo
        global entrada_edad
        global entrada_folio
        global entrada_id
        global entrada_nombre
        global entrada_oficio
        global tabla_trabajador
   
        ventana = Tk()
        ventana.title("LISTA DE TRABAJADORES")
        ventana.configure(padx=5)
        ventana.geometry("1230x800")
        ventana.configure(bg="#6DEAC2")
        

        # Crear los campos de entrada para los datos del alumno
        Label(ventana, text="Id:",bg="light goldenrod" ).grid(row=0, column=0, padx=40, pady=15)
        entrada_id = Entry(ventana)
        entrada_id.grid(row=0, column=1, padx=40, pady=15)
        entrada_id.configure(bg="lavender")
        
        Label(ventana, text="Buscar Nombre:",bg="light goldenrod" ).place(x=550,y=390)
        validacion_2=ventana1.register(validar_letras)
        buscar_nombre = Entry(ventana,validate="key", validatecommand=(validacion_2, '%P'))
        buscar_nombre.place(x=780,y=400)
        limitar_letras(buscar_nombre,12)
        buscar_nombre.configure(bg="lavender")
                
        def buscarRegistro():
            if len(buscar_nombre.get()) > 0:
                where = buscar_nombre.get()
                cursor = db.cursor()
                consulta = "SELECT * FROM trabajador WHERE nombre = %s"
                cursor.execute(consulta, (where,))
                resultados = cursor.fetchall()
                for resultado in resultados:
                    print(resultado)
                db.commit()
                cursor.close()
                tabla_trabajador.delete(*tabla_trabajador.get_children())
                i = -1
                for dato in resultados:
                    i= i+1                       
                    tabla_trabajador.insert('',i, text = resultados[i][1:1], values=resultados[i][0:6])
                    

        Label(ventana, text="Nombre:",bg="light goldenrod" ).grid(row=1, column=0, padx=40, pady=15)
        validacion_2=ventana1.register(validar_letras)
        entrada_nombre = Entry(ventana,validate="key", validatecommand=(validacion_2, '%P'))
        entrada_nombre.grid(row=1, column=1, padx=40, pady=15)
        limitar_letras(entrada_nombre,20)
        entrada_nombre.configure(bg="lavender")
        
        
        Label(ventana, text="Edad:",bg="light goldenrod" ).grid(row=2, column=0, padx=40, pady=15)
        validacion_3=ventana1.register(validar_decimal)
        entrada_edad = Entry(ventana,validate="key", validatecommand=(validacion_3, '%P'))
        entrada_edad.grid(row=2, column=1, padx=40, pady=15)
        entrada_edad.configure(bg="lavender")
        limitar_numeros(entrada_edad,3)
       
       
        Label(ventana, text="Correo:",bg="light goldenrod" ).grid(row=3, column=0, padx=40, pady=15)
        entrada_correo = Entry(ventana)
        limitar(entrada_correo,20)
        entrada_correo.grid(row=3, column=1, padx=40, pady=15)
        entrada_correo.configure(bg="lavender")

        Label(ventana, text="Folio:",bg="light goldenrod").grid(row=4, column=0, padx=40, pady=15)
        validacion_4=ventana1.register(validar_decimal)
        entrada_folio = Entry(ventana,validate="key", validatecommand=(validacion_4, '%P'))
        limitar_numeros(entrada_folio,10)
        entrada_folio.grid(row=4, column=1, padx=40, pady=15)
        entrada_folio.configure(bg="lavender")

        Label(ventana, text="Oficio:",bg="light goldenrod" ).grid(row=5, column=0, padx=40, pady=15)
        validacion_5=ventana1.register(validar_letras)
        entrada_oficio = Entry(ventana,validate="key", validatecommand=(validacion_5, '%P'))
        limitar_letras(entrada_oficio,10)
        entrada_oficio.grid(row=5, column=1, padx=40, pady=15)
        entrada_oficio.configure(bg="lavender")


        # Crear los botones para agregar, actualizar y eliminar alumnos
        Button(ventana, text="AGREGAR TRABAJADOR", command=agregar_trabajador, bg="AZURE",borderwidth=10).grid(row=0, column=2, padx=40, pady=15)
        Button(ventana, text="ACTUALIZAR TRABAJADOR", command=actualizar_trabajador, bg="AZURE",borderwidth=10).grid(row=1, column=2, padx=40, pady=15)
        Button(ventana, text="ELIMINAR TRABAJADOR", command=eliminar_trabajador, bg="AZURE",borderwidth=10).grid(row=2, column=2, padx=40, pady=15)
        Button(ventana, text="LIMPIAR CAMPOS", command=limpiar, bg="AZURE",borderwidth=10).grid(row=3, column=2, padx=40, pady=15)
        Button(ventana, text="MOSTRAR TABLA", command=mostrar_tabla, bg="AZURE",borderwidth=10).grid(row=4, column=2, padx=40, pady=15)
        Button(ventana, text="Buscar", command=buscarRegistro, bg="AZURE",borderwidth=10).grid(row=5, column=2, padx=40, pady=15)
        Button(ventana, text="Exporta exel", command=buscarRegistro, bg="AZURE",borderwidth=10).grid(row=5, column=2, padx=40, pady=15)


        # Crear la tabla para mostrar los alumnos
        def obtener_fila(event):
            current_item=tabla_trabajador.focus()
            if not current_item:
                return
            data=tabla_trabajador.item(current_item) 
            entrada_id.delete(0,END)   
            entrada_nombre.delete(0,END)  
            entrada_edad.delete(0, END)  
            entrada_correo.delete(0,END)  
            entrada_oficio.delete(0,END)  
            entrada_folio.delete(0, END)                
            entrada_id.insert(0,int(data['values'][0])) 
            entrada_nombre.insert(0,data['values'][1])  
            entrada_edad.insert(0,data['values'][2])  
            entrada_correo.insert(0,data['values'][3])  
            entrada_oficio.insert(0,data['values'][5])  
            entrada_folio.insert(0,data['values'][4])       
                 
                   

        
        
        tabla_trabajador =ttk.Treeview(ventana)
        tabla_trabajador.bind("<<TreeviewSelect>>",obtener_fila)
        tabla_trabajador.config(height=800)
        tabla_trabajador.grid(row=7, column=0, columnspan=6, padx=60, pady=50)
        
        tabla_trabajador['columns'] = ('Id','Nombre', 'Edad','Oficio','Folio','Correo')
        
        tabla_trabajador.column('#0', width=0, stretch=tk.NO)
        tabla_trabajador.column('Id', anchor=tk.CENTER, width=175)
        tabla_trabajador.column('Nombre', anchor=tk.CENTER, width=175)
        tabla_trabajador.column('Edad', anchor=tk.CENTER, width=75)
        tabla_trabajador.column('Oficio', anchor=tk.CENTER, width=220)
        tabla_trabajador.column('Folio', anchor=tk.CENTER, width=220)
        tabla_trabajador.column('Correo', anchor=tk.CENTER, width=220)
       
       
       
        tabla_trabajador.heading('#0', text='', anchor=tk.CENTER)
        tabla_trabajador.heading('Id', text='Id', anchor=tk.CENTER)
        tabla_trabajador.heading('Nombre', text='Nombre', anchor=tk.CENTER)
        tabla_trabajador.heading('Edad', text='Edad', anchor=tk.CENTER)
        tabla_trabajador.heading('Folio', text='folio', anchor=tk.CENTER)
        tabla_trabajador.heading('Oficio', text='oficio', anchor=tk.CENTER)
        tabla_trabajador.heading('Correo', text='correo', anchor=tk.CENTER)

        
        estilo = ttk.Style(ventana)
        estilo.theme_use('alt') 
              
        estilo.configure("Treeview", font= ('Helvetica', 10, 'bold'), foreground='green',  background='white')
        estilo.map('Treeview',background=[('selected', 'pink2')], foreground=[('selected','blue')] )
        
        

        # Mostrar la lista de alumnos en la tabla
        mostrar_trabajador()

        # Iniciar el loop de la ventana
        ventana.mainloop()
     

class Mexico(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.zora()
        self.usuarios = {'ppp': '123', 'ANGEL': '123', 'EDUARDO Creed': '123'}

        # Horarios preterminados
        self.horarios = {'ppp': {'Lunes': ['8:00', '9:30', '11:00'], 
                                 'Martes': ['9:00', '10:30', '12:00'],
                                 'Miércoles': ['10:00', '11:30', '1:00'],
                                 'Jueves': ['11:00', '12:30', '2:00'],
                                 'Viernes': ['12:00', '1:30', '3:00']}, 
                         'ANGEL': {'Lunes': ['9:00', '10:30', '12:00'], 
                                   'Martes': ['10:00', '11:30', '1:00'],
                                   'Miércoles': ['11:00', '12:30', '2:00'],
                                   'Jueves': ['12:00', '1:30', '3:00'],
                                   'Viernes': ['1:00', '2:30', '4:00']},
                         'EDUARDO Creed': {'Lunes': ['10:00', '11:30', '1:00'], 
                                           'Martes': ['11:00', '12:30', '2:00'],
                                           'Miércoles': ['12:00', '1:30', '3:00'],
                                           'Jueves': ['1:00', '2:30', '4:00'],
                                           'Viernes': ['2:00', '3:30', '5:00']}}

    def zora(self):
        self.fra = Frame()
        resultado = tk.Label(self.fra, text="BIENVENIDO",font=("Comic Sans Ms",12,"bold"),background="cornsilk4")
        resultado.pack(pady=30)
      
        # Crear los campos de usuario y contraseña
        etiqueta_usuario = ttk.Label(self.fra, text="Usuario:",font=("Comic Sans Ms",12,"bold"),background="cornsilk4")
        etiqueta_usuario.pack(pady=20)
        validacion = ventana1.register(self.validar_decimal)
        
        validacion_2=ventana1.register(self.validar_letras)
        
        self.campo_usuario = ttk.Entry(self.fra,validate="key", validatecommand=(validacion_2, '%P'))
        limitar(self.campo_usuario,14)
        self.campo_usuario.pack()
        
        vcmd = (self.register(self.validar_letras), "%P")
        self.campo_usuario.config(validate='key', validatecommand=vcmd)
       
        etiqueta_contraseña = ttk.Label(self.fra, text="Contraseña:",font=("Comic Sans Ms",12,"bold"),background="cornsilk4")
        etiqueta_contraseña.pack(pady=20)
        self.campo_contraseña = ttk.Entry(self.fra, show="*")
        limitar(self.campo_contraseña,14)
        self.campo_contraseña.pack()
        vcmd = (self.register(self.validar_decimal), "%P")
        self.campo_contraseña.config(validate="key", validatecommand=vcmd)  
    
        boton_inicio = tk.Button(self.fra, text="Iniciar sesión", command=self.iniciar_sesion,borderwidth=10,background="cornsilk4")
        boton_inicio.pack(pady=30)
        self.fra.config(width=600, height=880,background="cornsilk4")
        self.fra.place(x=190, y=100)

    def iniciar_sesion(self):
        self.usuario = self.campo_usuario.get()
        self.contraseña = self.campo_contraseña.get()

        if self.usuario in self.usuarios and self.usuarios[self.usuario] == self.contraseña:
            messagebox.showinfo(" ","Inicio de sesión exitoso")
            self.master.destroy()
            self.ventana_horarios(self.usuario)
        else:
            messagebox.showerror(" ","  Iniciar sesion fallida ")
   
       
    
    def validar_decimal(self,valor):
      if valor.isdigit() or valor == "":
        return True
      else:
        return False
    
    
    def validar_letras(self,valor):
        if valor.isalpha() or valor == "":
            return True
        else:
            return False

    validacion =ventana1.register(validar_decimal)
    validacion_2=ventana1.register(validar_letras)
  
    def limitar(entrada, limite):
        def limit(event):
            texto=entrada.get()
            if len(texto)>=limite and event.keysym!='BackSpace':
                return "break"
            entrada.bind("<key>",limite)
        


    def ventana_horarios(self, usuario):
        horario = self.horarios[usuario]

        ventana = tk.Tk()
        ventana.title("HORARIO DE " + usuario)

        tabla = ttk.Treeview(ventana, columns=("dia", "primerviaje", "segundoviaje", "tercerviaje"), show="headings")
        tabla.heading("dia", text="Día")
        tabla.heading("primerviaje", text="Primer Viaje")
        tabla.heading("segundoviaje", text="Segundo Viaje")
        tabla.heading("tercerviaje", text="Tercer Viaje")
      
        for dia, horas in horario.items():
            fila = (dia,) + tuple(horas)
            tabla.insert("", "end", values=fila)

        tabla.pack()
        ventana.mainloop()
        
             
    def limitar(entrada, limit):
        def limitar(event):
            texto=entrada.get()
            if len(texto)>=limit and not event.keysym=='BackSpace':
                return " break"
            entrada.bind("<Key>",limitar)
    
    def letra (char):
        return char in "qwertyuiopasdfghjklñzxcvbnmQWERTYUIOPASDFGHJKLÑZXCVBNM"
    
    
    def nuemro(char):
        return char in "0123456789/"
            
if sas=="si":
    root=tk.Tk()
    root.geometry("500x650")
    root.wm_resizable(False,False)
    root.title("......")
    van=gauss(root) 
    van.mainloop()
elif sas=="no":
    root=tk.Tk()
    root.geometry("500x650")
    root.wm_resizable(False,False)
    root.title("......")
    root.configure(background="cornsilk4")
    van=Mexico(root) 
    van.mainloop()
    
if van.destroy and sas=="si":
  
    
    cerrar()
