
import tkinter as tk
from tkinter import messagebox

# Variables globales
matriz = [" "] * 9
humano = None
ia = None
botones = []
turno_jugador = False

# Colores de la interfaz
COLOR_FONDO = "#121212"
COLOR_TABLERO = "#1e1e1e"
COLOR_TEXTO = "#e0e0e0"
COLOR_X = "#4dabf7"
COLOR_O = "#ff6b6b"
COLOR_LINEA = "#444444"

# Función para ver si hay un empate
def Empate(tablero):
    return " " not in tablero

# Función para ver si hay una victoria
def Victoria(tablero):
    return (
        tablero[0] == tablero[1] == tablero[2] != " " or
        tablero[3] == tablero[4] == tablero[5] != " " or
        tablero[6] == tablero[7] == tablero[8] != " " or
        tablero[0] == tablero[3] == tablero[6] != " " or
        tablero[1] == tablero[4] == tablero[7] != " " or
        tablero[2] == tablero[5] == tablero[8] != " " or
        tablero[0] == tablero[4] == tablero[8] != " " or
        tablero[2] == tablero[4] == tablero[6] != " "
    )

# Algoritmo MiniMax
def MiniMax(tablero, es_ia):

    # Caso 1: Victoria de alguno de los jugadores
    if Victoria(tablero):
        return 1 if not es_ia else -1

    # Caso 2: Empate
    if Empate(tablero):
        return 0

    # Caso 3: Recursión para ver movimientos a futuro
    if es_ia: # Aquí es el turno de la IA donde busca el máximo puntaje posible
        mejor = -float("inf") # Peor valor posible para la IA
        
        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = ia # La IA prueba poner su ficha
                puntuacion = MiniMax(tablero, False)
                tablero[i] = " " # Backtracking
                mejor = max(mejor, puntuacion) # Se guarda el valor mayor

        return mejor

    else: # Aquí es el turno del humano donde busca el mínimo puntaje posible
        mejor = float("inf") # Mejor valor posible para el humano

        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = humano # El humano prueba poner su ficha
                puntuacion = MiniMax(tablero, True)
                tablero[i] = " " # Backtracking
                mejor = min(mejor, puntuacion) # Se guarda el valor menor

        return mejor

# Movimiento de la IA
def MovimientoIA():

    MejorPuntuacion = -float("inf") # Peor valor posible para la IA
    MejorCasilla = None

    for i in range(9):
        if matriz[i] == " ":
            matriz[i] = ia # La IA prueba poner su ficha
            puntuacion = MiniMax(matriz, False)
            matriz[i] = " " # Backtracking

            if puntuacion > MejorPuntuacion:
                MejorPuntuacion = puntuacion
                MejorCasilla = i

    matriz[MejorCasilla] = ia # La IA hace su movimiento en la mejor casilla encontrada

    botones[MejorCasilla]["text"] = ia
    botones[MejorCasilla]["fg"] = COLOR_O if ia == "O" else COLOR_X

# Funcion para manejar el click del jugador
def ClickJugador(i):
    
    global turno_jugador

    if not turno_jugador:
        return

    if matriz[i] == " ":

        matriz[i] = humano # El humano coloca su ficha

        botones[i]["text"] = humano
        botones[i]["fg"] = COLOR_X if humano == "X" else COLOR_O

        if Victoria(matriz):
            messagebox.showinfo("Fin", "Ganaste!")
            Reiniciar()
            return

        if Empate(matriz):
            messagebox.showinfo("Fin", "Empate")
            Reiniciar()
            return
        
        turno_label["text"] = "Turno de la IA..."
        turno_jugador = False

        # IA pensando
        ventana.after(2000, TurnoIA)

# Función para el turno de la IA
def TurnoIA():
    
    global turno_jugador

    MovimientoIA()

    if Victoria(matriz):
        messagebox.showinfo("Fin", "Gana la IA")
        Reiniciar()
        return

    if Empate(matriz):
        messagebox.showinfo("Fin", "Empate")
        Reiniciar()
        return

    turno_label["text"] = "Turno del jugador"
    turno_jugador = True

# Función para elegir la ficha del jugador
def ElegirFicha(ficha):

    global humano, ia, turno_jugador

    humano = ficha
    ia = "O" if ficha == "X" else "X"

    frame_inicio.pack_forget()
    frame_tablero.pack()

    turno_label["text"] = "Turno del jugador"
    turno_jugador = True

# Función para reiniciar el juego
def Reiniciar():

    global matriz, turno_jugador
    matriz = [" "] * 9

    for b in botones:
        b["text"] = ""
        b["fg"] = COLOR_TEXTO

    turno_label["text"] = "Turno del jugador"
    turno_jugador = True

# Configuración de la ventana
ventana = tk.Tk()
ventana.title("Tic Tac Toe")

# Tamaño de ventana
ancho = 360
alto = 420

# Centrar ventana
pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()

x = (pantalla_ancho // 2) - (ancho // 2)
y = (pantalla_alto // 2) - (alto // 2)

ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
ventana.configure(bg=COLOR_FONDO)

# Interfaz de selección de ficha
frame_inicio = tk.Frame(ventana, bg=COLOR_FONDO)
frame_inicio.pack(pady=60)

tk.Label(
    frame_inicio,
    text="Elige tu ficha",
    font=("Segoe UI", 18, "bold"),
    fg=COLOR_TEXTO,
    bg=COLOR_FONDO
).pack(pady=20)

tk.Button(
    frame_inicio,
    text="X",
    font=("Segoe UI", 14),
    width=15,
    bg="#1f1f1f",
    fg=COLOR_X,
    command=lambda: ElegirFicha("X")
).pack(pady=8)

tk.Button(
    frame_inicio,
    text="O",
    font=("Segoe UI", 14),
    width=15,
    bg="#1f1f1f",
    fg=COLOR_O,
    command=lambda: ElegirFicha("O")
).pack(pady=8)

# Interfaz del tablero
frame_tablero = tk.Frame(ventana, bg=COLOR_FONDO)

frame_grid = tk.Frame(frame_tablero, bg=COLOR_TABLERO)
frame_grid.pack(pady=20)

for i in range(9):

    boton = tk.Button(
        frame_grid,
        text="",
        font=("Segoe UI", 28, "bold"),
        width=3,
        height=1,
        bg=COLOR_TABLERO,
        fg=COLOR_TEXTO,
        bd=2,
        relief="solid",
        highlightbackground=COLOR_LINEA,
        command=lambda i=i: ClickJugador(i)
    )

    boton.grid(row=i//3, column=i%3, padx=2, pady=2)
    botones.append(boton)

# Texto de turno
turno_label = tk.Label(
    frame_tablero,
    text="",
    font=("Segoe UI", 15, "bold"),
    fg=COLOR_TEXTO,
    bg=COLOR_FONDO
)

turno_label.pack(pady=10)

ventana.mainloop()