from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import fitz  # PyMuPDF para leer el PDF

# Cargar clave pública
def cargar_clave_publica(nombre):
    with open(f"keys/publica_{nombre}.pem", "rb") as file:
        return RSA.import_key(file.read())

# Generar hash del documento PDF
def generar_hash_pdf(nombre_pdf):
    with open(nombre_pdf, "rb") as file:
        datos_pdf = file.read()
    return SHA256.new(datos_pdf)  # 🔹 Generamos el mismo hash usado en la firma

# Extraer la firma desde el PDF
def extraer_firma_pdf(nombre_pdf, firmante="Alice"):
    doc = fitz.open(nombre_pdf)
    page = doc[0]  # Primera página

    # Buscar la firma dentro del PDF
    for texto in page.get_text("text").split("\n"):
        if f"Firma {firmante}:" in texto:
            firma_hex = texto.replace(f"Firma {firmante}:", "").strip().replace("...", "")
            return bytes.fromhex(firma_hex)  # Convertir de hexadecimal a bytes

    print(f"❌ No se encontró la firma de {firmante} en el PDF.")
    return None

# Verificar la firma en el PDF
def verificar_firma_pdf(nombre_pdf, clave_publica, firmante="Alice"):
    hash_obj = generar_hash_pdf(nombre_pdf)  # Generamos el mismo hash del PDF

    # Extraer la firma del PDF
    firma = extraer_firma_pdf(nombre_pdf, firmante)
    if firma is None:
        return

    try:
        pkcs1_15.new(clave_publica).verify(hash_obj, firma)  # Verificamos la firma
        print(f"✅ La firma de {firmante} en el PDF es válida.")
    except (ValueError, TypeError):
        print(f"❌ La firma de {firmante} en el PDF NO es válida.")

# ✅ Función principal
def main():
    clave_publica_alice = cargar_clave_publica("alice")
    verificar_firma_pdf("NDA_firmado.pdf", clave_publica_alice)

    clave_publica_ac = cargar_clave_publica("ac")
    verificar_firma_pdf("NDA_firmado_ac.pdf", clave_publica_ac, firmante="AC")

# ✅ Si se ejecuta directamente, llamar a main()
if __name__ == "__main__":
    main()
