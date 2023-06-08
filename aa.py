import tkinter as tk
from tkinter import Frame,messagebox
import cv2
from PIL import ImageTk, Image


def limitar(entrada, limite):
     def limit(event):
        texto = entrada.get()
        if len(texto) >= limite and event.keysym != 'BackSpace':
            return "break"
     entrada.bind("<Key>", limit)

def validar_letras(valor):
        if valor.isalpha() or valor == "":
            return True
        else:
            return False    


     
def validar_decimal(valor):
      if valor.isdigit() or valor == "":
        return True
      else:
         return False

 
    

class gauss(tk.Frame):
    def __init__(self,master):
       super().__init__(master)
       self.wigets()      
    def wigets(self):
        self.fra=Frame()
        global photo
        
        image = Image.open("usuario.png")
        var= (500,650)
        resized = image.resize(var)
        photo = ImageTk.PhotoImage(resized)
        label = tk.Label(self.fra, image=photo)
        label.pack()
        self.usuario=tk.StringVar()
        self.contraseña=tk.StringVar()
        #Entradas
        entrada3=self.fra.register(validar_letras)
        entrada=tk.Entry(self.fra,validate="key",validatecommand=(entrada3,'%P'),textvar=self.usuario,width=26,relief="flat",bg="#e7e7e7")
        limitar(entrada,6)
        entrada4=self.fra.register(validar_decimal)
        entrada1=tk.Entry(self.fra,validate="key",validatecommand=(entrada4,'%P'),textvar=self.contraseña,show="*",width=26,relief="flat",bg="#e7e7e7")
        limitar(entrada1,6)  
        boton=tk.Button(self.fra,text="Entrar",command=self.login,cursor="hand2",bg="#f81c99",height=0,width=16,relief="flat",font=("Comic Sans Ms",12,"bold"))
        boton1=tk.Button(self.fra,text="Salir",command=self.salir,cursor="hand2",bg="#FF007F",width=12,relief="flat",font=("Comic Sans Ms",12,"bold"))
        
        self.fra.config(width=500,height=650)
        
        
        entrada.place(x=200,y=400,height=45)
        entrada1.place(x=200,y=480,height=45)
        boton.place(x=160,y=575)
        boton1.place(x=0,y=0)
        self.fra.place(x=0,y=0)
        
    def login(self):
        nombre=self.usuario.get()
        password=self.contraseña.get()
        if nombre=="bobo" and password=="1234":
            self.correcta()
        else:
            self.incorrecta()
            
    def correcta(self):
        fondo=cv2.imread("bien.png")
        fondo3=cv2.resize(fondo,None,fx=0.2,fy=0.2)
        cv2.imshow('Window',fondo3)
        cv2.setMouseCallback('Window', self.on_button_click)
        self.var=True
     
        
        
    def incorrecta(self):
        fondo=cv2.imread("mal.png")
        fondo3=cv2.resize(fondo,None,fx=0.2,fy=0.2)
        cv2.imshow('Window',fondo3)
        cv2.setMouseCallback('Window', self.on_button_click)
        self.var=False
    
   
    def on_button_click(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Acciones que quieres realizar cuando se hace clic en el botón
            cv2.destroyAllWindows()
            if self.var==True:
                self.salir()
            global sasaa
            sasaa=True
                
            
    
    def salir(self):
        self.master.destroy()




