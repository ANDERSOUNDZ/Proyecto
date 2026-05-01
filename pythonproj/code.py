import serial
import time
import sys

PORT = "rfc2217://localhost:4000"
BAUD_RATE = 9600

# Estado de las 6 oficinas
estado = [0, 0, 0, 0, 0, 0]

def enviar_estado(ser):
    data = ''.join(map(str, estado))
    ser.write((data + '\n').encode())

def main():
    arduino = serial.serial_for_url(PORT, baudrate=BAUD_RATE, timeout=1)
    time.sleep(2)

    print("Comandos:")
    print("ocupar: b-n (1-6)")
    print("ocupar todo: b-all")
    print("liberar: f-n (1-6)")
    print("apagar: o-n (1-6)")
    print("apagar todo: off")
    print("prender o liberar todo: on")
    print("salir")

    while True:
        cmd = input(">> ").lower().strip()

        if cmd == "salir":
            break
        elif cmd == "off":
            for i in range(6):
                estado[i] = 2
            enviar_estado(arduino)
            print("Se apagaron todas las oficinas")
            continue
        elif cmd == "on":
            for i in range(6):
                estado[i] = 0
            enviar_estado(arduino)
            print("Se liberaron todas las oficinas")
            continue
        elif cmd == "b-all":
            for i in range(6):
                estado[i] = 1
            enviar_estado(arduino)
            print("Se ocuparon todas las oficinas")
            continue

        try:
            accion, num = cmd.split('-')
            idx = int(num) - 1

            if 0 <= idx < 6:
                if accion == "b":
                    estado[idx] = 1
                    print("Se ocupó la oficina", num)
                elif accion == "f":
                    estado[idx] = 0
                    print("Se liberó la oficina", num)
                elif accion == "o":
                    estado[idx] = 2
                    print("Se apagó la oficina", num)
                else:
                    print("Acción inválida")
                    continue

                enviar_estado(arduino)
            else:
                print("Número fuera de rango")

        except:
            print("Formato: f-1 | b-1 | o-1 | off | on | b-all")

    arduino.close()

if __name__ == "__main__":
    main()