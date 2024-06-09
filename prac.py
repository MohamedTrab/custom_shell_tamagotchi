import os
import cmd
import tkinter as tk
from tkinter import messagebox
import random
import datetime

class Tamagotchi:
    def __init__(self):
        self.hambre = 50
        self.energia = 50
        self.felicidad = 50

    def alimentar(self):
        self.hambre = max(0, self.hambre - 10)
        self.energia = min(100, self.energia + 5)
        return "Has alimentado a tu Tamagotchi."

    def jugar(self):
        if self.energia > 10:
            self.felicidad = min(100, self.felicidad + 10)
            self.energia = max(0, self.energia - 10)
            return "Has jugado con tu Tamagotchi."
        else:
            return "Tu Tamagotchi está demasiado cansado para jugar."

    def dormir(self):
        self.energia = min(100, self.energia + 20)
        self.hambre = min(100, self.hambre + 5)
        return "Tu Tamagotchi ha dormido."

    def estado(self):
        return (f"Hambre: {self.hambre}\n"
                f"Energía: {self.energia}\n"
                f"Felicidad: {self.felicidad}")

class CustomShell(cmd.Cmd):
    intro = "Bienvenido a tu Shell personalizado. Escribe ? para la lista de comandos."
    prompt = f"({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) (myshell) "

    def __init__(self, output_func):
        super().__init__()
        self.tamagotchi = Tamagotchi()
        self.output_func = output_func

        # Cambiar el directorio de trabajo al directorio del script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_dir)

    def preloop(self):
        """Actualizar prompt con fecha y hora dinámica"""
        self.update_prompt()

    def update_prompt(self):
        self.prompt = f"({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) (myshell) "

    def onecmd(self, line):
        """Sobrescribir onecmd para actualizar el prompt cada vez que se ejecuta un comando"""
        self.update_prompt()
        return super().onecmd(line)

    def do_cd(self, path):
        """Cambiar el directorio actual al path especificado"""
        try:
            os.chdir(path)
            self.output_func(f"Directorio cambiado a: {os.getcwd()}")
        except FileNotFoundError:
            self.output_func(f"Directorio no encontrado: {path}")

    def do_mkdir(self, path):
        """Crear un nuevo directorio"""
        try:
            os.mkdir(path)
            self.output_func(f"Directorio creado: {path}")
        except FileExistsError:
            self.output_func(f"El directorio ya existe: {path}")

    def do_touch(self, filename):
        """Crear un nuevo archivo"""
        with open(filename, 'a'):
            os.utime(filename, None)
        self.output_func(f"Archivo creado: {filename}")

    def do_rm(self, filename):
        """Eliminar un archivo"""
        try:
            os.remove(filename)
            self.output_func(f"Archivo eliminado: {filename}")
        except FileNotFoundError:
            self.output_func(f"Archivo no encontrado: {filename}")

    def do_rmdir(self, path):
        """Eliminar un directorio"""
        try:
            os.rmdir(path)
            self.output_func(f"Directorio eliminado: {path}")
        except FileNotFoundError:
            self.output_func(f"Directorio no encontrado: {path}")

    def do_pwd(self, _):
        """Imprimir el directorio de trabajo actual"""
        self.output_func(os.getcwd())

    def do_quit(self, _):
        """Salir del shell"""
        self.output_func("¡Adiós!")
        return True

    def do_custom1(self, _):
        """Mostrar la fecha actual"""
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
        self.output_func(f"Fecha actual: {fecha_actual}")

    def do_custom2(self, _):
        """Mostrar la hora actual"""
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        self.output_func(f"Hora actual: {hora_actual}")

    def do_custom3(self, _):
        """Imprimir un mensaje de agradecimiento"""
        self.output_func("¡Gracias por usar este shell personalizado!")

    def do_art(self, _):
        """Generar arte ASCII"""
        art = r"""
        (\_/)
        (='.'=)
        (")_(")
        """
        self.output_func(art)
    
    def do_phrase(self, _):
        """Generar una frase aleatoria"""
        frases = [
            "La vida es bella.",
            "Carpe diem.",
            "A cada día le basta su propio afán.",
            "La imaginación es más importante que el conocimiento."
        ]
        self.output_func(random.choice(frases))

    def do_guess(self, _):
        """Iniciar un juego de adivinanzas"""
        self.output_func("¡Bienvenido al juego de adivinanzas!")
        self.output_func("Adivina un número entre 1 y 100:")
        self.output_func("Escribe tu adivinanza y presiona Enter.")

    # Comandos Tamagotchi
    def do_alimentar(self, _):
        """Alimentar a tu Tamagotchi"""
        self.output_func(self.tamagotchi.alimentar())
    
    def do_jugar(self, _):
        """Jugar con tu Tamagotchi"""
        self.output_func(self.tamagotchi.jugar())

    def do_dormir(self, _):
        """Poner a dormir a tu Tamagotchi"""
        self.output_func(self.tamagotchi.dormir())

    def do_estado(self, _):
        """Comprobar el estado de tu Tamagotchi"""
        self.output_func(self.tamagotchi.estado())

class ShellGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Custom Shell")
        
        self.text_area = tk.Text(self.root, wrap='word', height=20, width=80, bg='black', fg= 'white', insertbackground='white')
        self.text_area.pack(expand=True, fill='both')
        
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.input_var, width=80, bg='black', fg='white', insertbackground='white')
        self.entry.pack()
        self.entry.bind("<Return>", self.execute_command)
        
        self.create_menu()
        
        self.shell = CustomShell(self.output)
        self.guess_game_active = False
        self.guess_number = 0
        self.guess_attempts = 0
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Acerca de", command=self.show_about)
        file_menu.add_command(label="Versión", command=self.show_version)
        menubar.add_cascade(label="Ayuda", menu=file_menu)
        
        self.root.config(menu=menubar)
    
    def show_about(self):
        messagebox.showinfo("Acerca de", "Creado por Mohamed Trabelsi\nContacto: Mohamed.trabelsi@alumno.ucjc.edu")
    
    def show_version(self):
        messagebox.showinfo("Versión", "Versión 1.0")
    
    def output(self, text):
        """Función para mostrar texto en el área de texto"""
        self.text_area.insert(tk.END, text + '\n')
        self.text_area.see(tk.END)
    
    def execute_command(self, event):
        command = self.input_var.get()
        self.text_area.insert(tk.END, f"{self.shell.prompt}{command}\n")
        self.process_command(command)
        self.input_var.set('')
    
    def process_command(self, command):
        if self.guess_game_active:
            self.process_guess(command)
        else:
            self.shell.onecmd(command)
            if command.strip() == "guess":
                self.start_guess_game()
    
    def start_guess_game(self):
        self.guess_game_active = True
        self.guess_number = random.randint(1, 100)
        self.guess_attempts = 0
        
    
    def process_guess(self, guess):
        try:
            guess = int(guess)
        except ValueError:
            self.output("Por favor, introduce un número válido.")
            return

        self.guess_attempts += 1

        if guess < self.guess_number:
            self.output("Más alto!")
        elif guess > self.guess_number:
            self.output("Más bajo!")
        else:
            self.output(f"¡Felicidades! Has adivinado el número {self.guess_number} en {self.guess_attempts} intentos.")
            self.guess_game_active = False

if __name__ == '__main__':
    app = ShellGUI()
    app.root.mainloop()


