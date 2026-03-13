
# Librerias
import time
import os

# Inicio del juego y selección de ficha
def InicioJuego():
    print("Bienvenido")
    time.sleep(1)
    
    while True:
        ficha = input("Selecciona tu ficha (X/O): ")
        ficha = ficha.upper()
        
        if ficha == "X":
            humano = "X"
            ia = "O"
            break
        
        elif ficha == "O":
            humano = "O"
            ia = "X"
            break
        
        else:
            print("Opción no válida.")
    
    return (humano, ia)

# Tablero
def Tablero():
    print("Tic Tac Toe" + "\n")
    print("1  {}  |2  {}  |3  {}  ".format(matriz[0], matriz[1], matriz[2]))
    print("   ---|------|---")
    print("4  {}  |5  {}  |6  {}  ".format(matriz[3], matriz[4], matriz[5]))
    print("   ---|------|---")
    print("7  {}  |8  {}  |9  {}  ".format(matriz[6], matriz[7], matriz[8]))

# Finales del juego
def Empate(matriz):
    empate = True
    i = 0
    
    while (empate == True) and (i < 9):
        if matriz[i] == " ":
            empate = False
        i += 1
    
    return empate

def Victoria(matriz):
    if (matriz[0] == matriz[1] == matriz[2] != " " or
        matriz[3] == matriz[4] == matriz[5] != " " or
        matriz[6] == matriz[7] == matriz[8] != " " or
        matriz[0] == matriz[3] == matriz[6] != " " or
        matriz[1] == matriz[4] == matriz[7] != " " or
        matriz[2] == matriz[5] == matriz[8] != " " or
        matriz[0] == matriz[4] == matriz[8] != " " or
        matriz[2] == matriz[4] == matriz[6] != " "):
        return True
    
    else:
        return False

# Movimiento del jugador
def MovimientoJugador():
    while True:
        posiciones = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        casilla = int(input("Selecciona una casilla (1-9): "))
        
        if casilla not in posiciones:
            print("Opción no válida.")
        
        else:
            
            if matriz[casilla - 1] == " ":
                matriz[casilla - 1] = humano
                break
            
            else:
                print("Casilla ocupada.")

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

    matriz[MejorCasilla] = ia

# Partida
while True:
    matriz = [" "] * 9
    os.system("cls")
    humano, ia = InicioJuego() # Seleccion de ficha
    partida = True
    ganador = 0
    
    while partida:
        ganador += 1
        os.system("cls")
        Tablero()
    
        if Victoria(matriz):
            if ganador % 2 == 0:
                print("Gana el jugador")
                print("Reiniciando...")
                time.sleep(5)
                partida = False
            
            else:
                print("Gana la IA")
                print("Reiniciando...")
                time.sleep(5)
                partida = False
        
        elif Empate(matriz):
            print("Empate")
            print("Reiniciando...")
            time.sleep(5)
            partida = False
        
        elif ganador % 2 == 0:
            print("La IA está pensando...")
            time.sleep(2)
            MovimientoIA()
        
        else:
            MovimientoJugador()