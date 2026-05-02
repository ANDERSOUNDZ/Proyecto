import serial
import time as t
from pulp import *

PORT = "rfc2217://localhost:4000"
BAUD_RATE = 9600

# ahora trabajamos con HORAS (0–6)
horas = [0]*6


def enviar_estado(ser):
    data = ''.join(map(str, horas))
    ser.write((data + '\n').encode())
    print("Enviado:", data)

    # debug seguro
    t.sleep(0.1)
    try:
        while ser.in_waiting:
            print("Arduino:", ser.readline().decode(errors='ignore').strip())
    except:
        pass


# OPTIMIZACIÓN
def optimizar():
    global horas

    salas = range(6)
    model = LpProblem("Coworking", LpMaximize)

    x = LpVariable.dicts("uso", salas, lowBound=0, upBound=6, cat='Integer')

    model += lpSum([x[i] for i in salas])

    for i in salas:
        if i < 4:
            model += x[i] <= 4
        else:
            model += x[i] <= 6

        model += x[i] + 2 <= 8

    model.solve()

    print("\nResultado optimización:")

    for i in salas:
        horas[i] = int(value(x[i]))
        print(f"Sala {i+1}: {horas[i]}h")


def main():
    arduino = serial.serial_for_url(PORT, baudrate=BAUD_RATE, timeout=1)
    t.sleep(2)

    print("\nComandos:")
    print("opt → optimización")
    print("h-n-x → asignar horas (ej: h-1-3)")
    print("off → todo en 0h")
    print("full → todo en 6h")
    print("demo → ejemplo automático")
    print("salir\n")

    while True:
        cmd = input(">> ").lower().strip()

        if cmd == "salir":
            break

        elif cmd == "opt":
            optimizar()
            enviar_estado(arduino)
            continue

        elif cmd == "off":
            horas[:] = [0]*6
            enviar_estado(arduino)
            continue

        elif cmd == "full":
            horas[:] = [6]*6
            enviar_estado(arduino)
            continue

        elif cmd == "demo":
            horas[:] = [1,2,0,0,3,1]
            enviar_estado(arduino)
            continue

        # asignación directa PRO
        elif cmd.startswith("h-"):
            try:
                _, sala, h = cmd.split('-')
                idx = int(sala) - 1
                h = int(h)

                if 0 <= idx < 6 and 0 <= h <= 6:
                    horas[idx] = h
                    enviar_estado(arduino)
                else:
                    print("Valores fuera de rango")
            except:
                print("Formato: h-1-3")

        else:
            print("Comando inválido")


    arduino.close()


if __name__ == "__main__":
    main()