from Crypto.Cipher import PKCS1_OAEP #pip install pycryptdome
from Crypto.PublicKey import RSA
import hashlib

# Cargar clave pública
def cargar_clave_publica(nombre):
    with open(f"keys/publica_{nombre}.pem", "rb") as file:
        return RSA.import_key(file.read())

# Cargar clave privada
def cargar_clave_privada(nombre):
    with open(f"keys/privada_{nombre}.pem", "rb") as file:
        return RSA.import_key(file.read())

# Generar hash SHA-256 del mensaje
def generar_hash(mensaje):
    return hashlib.sha256(mensaje.encode()).hexdigest()

# Dividir el mensaje en bloques adecuados 
def dividir_mensaje(mensaje, tamano_bloque=86):  
    return [mensaje[i:i + tamano_bloque] for i in range(0, len(mensaje), tamano_bloque)]

# Cifrar cada bloque asegurando que no supere 117 bytes
def cifrar_mensaje(mensajes_divididos, clave_publica):
    cifrador = PKCS1_OAEP.new(clave_publica)
    return [cifrador.encrypt(bloque.encode('utf-8')) for bloque in mensajes_divididos]

# Descifrar los bloques y reconstruir el mensaje original
def descifrar_mensaje(bloques_cifrados, clave_privada):
    descifrador = PKCS1_OAEP.new(clave_privada)
    return "".join([descifrador.decrypt(bloque).decode() for bloque in bloques_cifrados])

# Implementación principal
def main():
    print("Cifrando y Descifrando Mensaje...")

    # Mensaje de 1050 caracteres
    mensaje = "M" * 1050

    # Cargar claves
    clave_publica = cargar_clave_publica("bob")
    clave_privada = cargar_clave_privada("bob")

    # Generar hash del mensaje original
    hash_original = generar_hash(mensaje)

    # Dividir mensaje en bloques
    mensajes_divididos = dividir_mensaje(mensaje)

    # Cifrar los bloques
    bloques_cifrados = cifrar_mensaje(mensajes_divididos, clave_publica)

    # Descifrar los bloques
    mensaje_descifrado = descifrar_mensaje(bloques_cifrados, clave_privada)

    # Generar hash del mensaje descifrado
    hash_descifrado = generar_hash(mensaje_descifrado)

    # Verificar autenticidad del mensaje
    print("¿El mensaje es auténtico?", hash_original == hash_descifrado)

# Ejecutar si es el script principal
if __name__ == "__main__":
    main()
