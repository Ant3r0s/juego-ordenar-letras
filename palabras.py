import tkinter as tk
import tkinter.messagebox as messagebox
import random
import time

# --- Funciones ---

def desordenar_palabra(palabra):
    """Desordena las letras de una palabra."""
    lista_letras = list(palabra)
    random.shuffle(lista_letras)
    return "".join(lista_letras)

def validar_palabra(palabra_original, palabra_ordenada):
    """Valida si la palabra ordenada es correcta."""
    return palabra_original.lower() == palabra_ordenada.lower()

def crear_interfaz_entrada():
    """Crea la interfaz para la entrada de palabras."""
    global entry_palabras, boton_siguiente, boton_borrar  # Para poder modificarlas dentro de la función
    
    instrucciones_label = tk.Label(root, text="Introduce palabras en inglés separadas por comas (o una sola palabra):")
    instrucciones_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

    entry_palabras = tk.Entry(root, width=50)
    entry_palabras.grid(row=1, column=0, columnspan=2, padx=10)
    entry_palabras.focus_set() # Pone el foco en el entry al iniciar

    boton_siguiente = tk.Button(root, text="Siguiente", command=lambda: iniciar_juego(entry_palabras.get()))
    boton_siguiente.grid(row=2, column=0, pady=10)

    boton_borrar = tk.Button(root, text="Borrar", command=borrar_entrada)
    boton_borrar.grid(row=2, column=1, pady=10)

    # Configurar la tecla Enter para que funcione como el botón "Siguiente"
    root.bind('<Return>', lambda event: iniciar_juego(entry_palabras.get()))
    


def borrar_entrada():
    """Borra el contenido del Entry de palabras."""
    entry_palabras.delete(0, tk.END)

def iniciar_juego(entrada_palabras):
    """Inicia el juego con las palabras proporcionadas."""
    global palabras_originales, palabras_desordenadas, ventana_juego, entries_letras, boton_validar, start_time, pistas_restantes, label_pistas # Para poder usarlas globalmente
    
    palabras_originales = [palabra.strip() for palabra in entrada_palabras.split(",") if palabra.strip()] # Limpia y divide

    if not palabras_originales:
        messagebox.showerror("Error", "Debes introducir al menos una palabra.")
        return

    # Limpiar widgets de la ventana principal (root) en lugar de crear una nueva
    for widget in root.winfo_children():
        widget.destroy()
   
    palabras_desordenadas = [desordenar_palabra(palabra) for palabra in palabras_originales]
    entries_letras = []  # Lista para guardar los tk.Entry de cada letra
    
    start_time = time.time()  # Iniciar cronómetro
    pistas_restantes = 3 # Inicializar las pistas disponibles

    # --- Interfaz del juego (en la misma ventana principal) ---
    
    # Frame para las palabras y entradas
    frame_palabras = tk.Frame(root)
    frame_palabras.pack(pady=10)

    for i, palabra_desordenada in enumerate(palabras_desordenadas):
       
        label_palabra = tk.Label(frame_palabras, text=f"Palabra {i+1}: {palabra_desordenada}")
        label_palabra.grid(row=i*2, column=0, sticky=tk.W, padx=5, pady=2) # Usar grid dentro del frame

        
        frame_letras = tk.Frame(frame_palabras) # Frame para las letras de cada palabra
        frame_letras.grid(row=i*2+1, column=0, sticky=tk.W)
        
        entries_palabra = []
        for j, _ in enumerate(palabra_desordenada):
            entry = tk.Entry(frame_letras, width=3)  # Entry para cada letra
            entry.grid(row=0, column=j, padx=2)       # Grid dentro del frame_letras
            entry.bind("<KeyRelease>", lambda event, row=i, col=j: actualizar_color(row, col)) #Validar al teclear
            entries_palabra.append(entry)
            
        entries_letras.append(entries_palabra)

    # Botón de validación y pistas
    boton_validar = tk.Button(root, text="Validar", command=validar_respuestas)
    boton_validar.pack(pady=5)
    
    label_pistas = tk.Label(root, text=f"Pistas restantes: {pistas_restantes}")
    label_pistas.pack()

    boton_pista = tk.Button(root, text="Pista", command=mostrar_pista)
    boton_pista.pack(pady=5)
    
    # --- Configurar nivel de dificultad ---
    frame_dificultad = tk.Frame(root)
    frame_dificultad.pack(pady=10)
    
    label_dificultad = tk.Label(frame_dificultad, text="Nivel de Dificultad:")
    label_dificultad.pack(side=tk.LEFT)

    opciones_dificultad = ["Fácil", "Medio", "Difícil"]
    seleccion_dificultad = tk.StringVar(value="Fácil")  # Valor por defecto
    menu_dificultad = tk.OptionMenu(frame_dificultad, seleccion_dificultad, *opciones_dificultad, command=ajustar_dificultad)
    menu_dificultad.pack(side=tk.LEFT)


def ajustar_dificultad(dificultad):
    """
    Ajusta la dificultad del juego.  
    Por ahora solo modifica el numero de pistas.  
    En un futuro se podría cambiar el largo de las palabras, o el numero de palabras a ordenar.
    """
    global pistas_restantes

    if dificultad == "Fácil":
        pistas_restantes = 5
    elif dificultad == "Medio":
        pistas_restantes = 3
    else:  # Difícil
        pistas_restantes = 1
        
    label_pistas.config(text=f"Pistas restantes: {pistas_restantes}")


def actualizar_color(fila, columna):
    """Actualiza el color de fondo de un Entry según si la letra es correcta."""
    
    entry = entries_letras[fila][columna]
    letra_ingresada = entry.get().lower()
    letra_correcta = palabras_originales[fila][columna].lower()

    if letra_ingresada == letra_correcta:
        entry.config(bg="lightgreen")
    elif letra_ingresada == "":
        entry.config(bg="white")  # Resetear el color si está vacío
    else:
        entry.config(bg="lightcoral")
        

def mostrar_pista():
    """Muestra una pista al usuario (la primera letra de una palabra aleatoria)."""
    global pistas_restantes, label_pistas
    
    if pistas_restantes <= 0:
        messagebox.showinfo("Sin Pistas", "No te quedan pistas.")
        return

    #Elegir una palabra al azar que no esté ya completada correctamente
    palabras_disponibles = []
    for i in range(len(palabras_originales)):
        palabra_completa = "".join([entry.get() for entry in entries_letras[i]]).lower()
        if palabra_completa != palabras_originales[i].lower():
            palabras_disponibles.append(i)

    if not palabras_disponibles: #Si ya se completaron todas las palabras, no dar pistas.
        messagebox.showinfo("Información", "Ya has completado todas las palabras!")
        return

    indice_palabra = random.choice(palabras_disponibles)
    primera_letra = palabras_originales[indice_palabra][0]

    # Encontrar el primer entry vacío o incorrecto en esa palabra
    for j, entry in enumerate(entries_letras[indice_palabra]):
      if entry.get().lower() != palabras_originales[indice_palabra][j].lower():
            entry.delete(0, tk.END)
            entry.insert(0, primera_letra)
            actualizar_color(indice_palabra, j)
            break # Dar solo *una* letra de pista por cada pulsación del botón.

    pistas_restantes -= 1
    label_pistas.config(text=f"Pistas restantes: {pistas_restantes}")



def validar_respuestas():
    """Valida las respuestas del usuario y muestra la puntuación."""
    global start_time
    
    respuestas_usuario = []
    for palabra_entries in entries_letras:
        respuesta = "".join([entry.get() for entry in palabra_entries])
        respuestas_usuario.append(respuesta)
    
    correctas = 0
    for i in range(len(palabras_originales)):
        if validar_palabra(palabras_originales[i], respuestas_usuario[i]):
            correctas += 1

    end_time = time.time()
    tiempo_transcurrido = end_time - start_time

    # Mostrar resultados
    mensaje = f"Palabras correctas: {correctas} / {len(palabras_originales)}\n"
    mensaje += f"Tiempo empleado: {tiempo_transcurrido:.2f} segundos\n"
    
    if correctas == len(palabras_originales):
      mensaje += "¡Felicidades! Has completado todas las palabras."
    
    messagebox.showinfo("Resultados", mensaje)

    # Preguntar si quiere jugar de nuevo
    if messagebox.askyesno("Jugar de nuevo", "¿Quieres jugar de nuevo?"):
        reiniciar_juego()
    else:
        root.destroy()  # Cerrar la aplicación

def reiniciar_juego():
    """Reinicia el juego."""
    
    #Destruir los widgets de la ventana de juego, en lugar de crear una nueva ventana.
    for widget in root.winfo_children():
        widget.destroy()
    crear_interfaz_entrada()



# --- Ventana principal ---
root = tk.Tk()
root.title("Juego de Ordenar Letras")
root.geometry("500x400")  # Tamaño inicial

crear_interfaz_entrada()  # Mostrar la interfaz de entrada

root.mainloop()
