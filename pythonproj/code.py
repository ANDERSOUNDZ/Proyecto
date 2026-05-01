pip install pyserial

import serial
import time
import sys

# Configuración de constantes
PORT = "rfc2217://localhost:4000"
BAUD_RATE = 115200

def transmitir(ser_obj, mensaje):
    """
    Envía el mensaje al Arduino agregando un salto de línea
    y convirtiendo el string a bytes (UTF-8).
    """
    try:
        # Limpiamos el mensaje de espacios extras
        mensaje_limpio = mensaje.strip()
        ser_obj.write(f"{mensaje_limpio}\n".encode('utf-8'))
    except Exception as e:
        print(f"Error al enviar datos: {e}")

def main():
    print("--- Iniciando Comunicación con Arduino ---")
    
    try:
        # serial_for_url es ideal para rfc2217
        arduino = serial.serial_for_url(PORT, baudrate=BAUD_RATE, timeout=1)
        
        # El tiempo de espera es vital para que el Arduino procese el reinicio serial
        print("Esperando conexión...")
        time.sleep(2)
        
        if arduino.is_open:
            print(f"Conectado exitosamente a: {PORT}")
            print("Estados permitidos: 'free', 'busy', 'off'")
        
        while True:
            # Capturamos la entrada del usuario
            texto = input("\nIngrese estado (o 'salir'): ").lower().strip()
            
            if texto == 'salir':
                print("Finalizando programa...")
                break
            
            if texto in ['free', 'busy', 'off']:
                transmitir(arduino, texto)
                print(f"Comando '{texto}' enviado.")
            else:
                print("Comando no reconocido. Use: free, busy u off.")

    except serial.SerialException as e:
        print(f"\nError de puerto serial: {e}")
        print("Asegúrate de que el servidor RFC2217 esté corriendo en el puerto 4000.")
    except KeyboardInterrupt:
        print("\n\nPrograma detenido por el usuario (Ctrl+C).")
    finally:
        if 'arduino' in locals() and arduino.is_open:
            arduino.close()
            print("Puerto serial cerrado correctamente.")

if __name__ == "__main__":
    main()