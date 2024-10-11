import sys
import getopt
import subprocess
import requests
import time

def mostrar_ayuda():
    print("""
    Opciones:
    -m, --mac: Consulta el fabricante de una dirección MAC específica. Ejemplo: -m aa:bb:cc:00:00:00
    -a, --arp: Muestra los fabricantes de los host disponibles en la tabla arp.
    -h, --help: Muestra este mensaje.
    """)

def obtener_fabricante(mac_solicitado):
    """
    Consulta la API maclookup.app para obtener el fabricante de la MAC solicitada.
    """
    url = f"https://api.maclookup.app/v2/macs/{mac_solicitado}"
    
    try:
        # Realiza la solicitud
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data["found"]:
                # Devuelve el fabricante
                return data["company"]
            else:
                return "Fabricante no encontrado."
        else:
            return "Error: No se pudo obtener la información."
    except requests.RequestException as e:
        return f"Error: {e}"

def ejecutar_arp():
    try:
        # Ejecuta el comando 'arp -a' y captura la salida
        result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()

        print("Mac/Fabricante:")
        for line in lines:
            # Extrae la MAC y reemplaza guiones por dos puntos
            parts = line.split()
            if len(parts) >= 2:
                mac_address = parts[1].replace('-', ':')
                fabricante = obtener_fabricante(mac_address)  # Llama a la función para obtener el fabricante
                print(f"{mac_address} / {fabricante}")
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar arp -a:", e)

def main(argv):
    # En el caso de que no haya argumentos, se muestra los parametros disponibles
    if len(argv) == 0:
        mostrar_ayuda()
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "m:ah", ["mac=", "arp", "help"])
    except getopt.GetoptError:
        mostrar_ayuda()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            mostrar_ayuda()
            sys.exit()
        elif opt in ("-m", "--mac"):
            start_time = time.time()  # Inicio del temporizador
            fabricante = obtener_fabricante(arg)
            end_time = time.time()  # Fin del temporizador
            elapsed_time_ms = (end_time - start_time) * 1000  # Tiempo en milisegundos
            print(f"Dirección MAC: {arg}\nFabricante: {fabricante}\nTiempo de búsqueda: {elapsed_time_ms:.2f} ms")
        elif opt in ("-a", "--arp"):
            ejecutar_arp()  # Llama a la función que muestra la tabla ARP

if __name__ == "__main__":
    main(sys.argv[1:])
