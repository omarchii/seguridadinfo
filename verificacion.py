from Crypto.Signature import pkcs1_15 #pip install pycryptdome
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import fitz  #pip install pymupdf

def cargar_clave_publica(nombre):
    """Carga una clave pública desde un archivo."""
    with open(f"keys/publica_{nombre}.pem", "rb") as file:
        return RSA.import_key(file.read())

def generar_hash_pdf(nombre_pdf):
    """Genera el hash SHA-256 del documento PDF."""
    with open(nombre_pdf, "rb") as file:
        datos_pdf = file.read()
    hash_obj = SHA256.new(datos_pdf)
    print(f" Hash generado para {nombre_pdf}: {hash_obj.hexdigest()}")
    return hash_obj

def extraer_firma_pdf(nombre_pdf, firmante="Alice"):
    """
    Extrae la firma desde el PDF y la convierte a bytes.
    """
    doc = fitz.open(nombre_pdf)
    page = doc[-1]  
    texto_completo = page.get_text("text")
    
    for texto in texto_completo.split("\n"):
        if f"Firma {firmante}:" in texto:
            firma_hex = texto.replace(f"Firma {firmante}:", "").strip()
            try:
                firma_bytes = bytes.fromhex(firma_hex)  # Convertir de hexadecimal a bytes
                print(f"Firma de {firmante} extraída correctamente: {firma_bytes.hex()[:20]}...")
                return firma_bytes
            except ValueError:
                print(f"Error al convertir la firma de {firmante} desde el PDF.")
                return None

    print(f" No se encontró una firma válida de {firmante} en el PDF.")
    return None


def verificar_firma_pdf(nombre_pdf, clave_publica, firmante="Alice"):
    """
    Verifica si la firma en el PDF es válida.
    """
    print(f"\n Verificando la firma de {firmante} en {nombre_pdf}...")

    hash_obj = generar_hash_pdf(nombre_pdf)  # Generamos el hash antes de verificar
    print(f" Hash esperado: {hash_obj.hexdigest()}")

    firma = extraer_firma_pdf(nombre_pdf, firmante)
    if firma is None:
        return

    try:
        pkcs1_15.new(clave_publica).verify(hash_obj, firma)
        print(f" La firma de {firmante} en el PDF es válida.")
    except (ValueError, TypeError) as e:
        print(f" La firma de {firmante} en el PDF NO es válida. Error: {e}")


def main():
    """Función principal."""
    clave_publica_alice = cargar_clave_publica("alice")
    verificar_firma_pdf("NDA_firmado.pdf", clave_publica_alice)

    clave_publica_ac = cargar_clave_publica("ac")
    verificar_firma_pdf("NDA_firmado_ac.pdf", clave_publica_ac, firmante="AC")

if __name__ == "__main__":
    main()
