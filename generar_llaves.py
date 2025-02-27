from Crypto.PublicKey import RSA
import os

# Crear carpeta 'keys' si no existe
if not os.path.exists("keys"):
    os.makedirs("keys")

# Función para generar y guardar claves
def generar_claves(nombre):
    clave = RSA.generate(1024)  # 🔹 Generamos clave RSA de 1024 bits

    # Guardar clave privada
    with open(f"keys/privada{nombre}.pem", "wb") as file:
        file.write(clave.export_key())

    # Guardar clave pública
    with open(f"keys/publica_{nombre}.pem", "wb") as file:
        file.write(clave.publickey().export_key())

    print(f"✅ Claves generadas para {nombre}.")

# Generar claves para Alice, Bob y la Autoridad Certificadora (AC)
generar_claves("alice")
generar_claves("bob")
generar_claves("ac")  # 🔹 Generamos claves para la AC

print("\n✅ TODAS LAS CLAVES SE GENERARON CORRECTAMENTE.")
