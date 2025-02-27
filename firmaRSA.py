from Crypto.Signature import pkcs1_15 #pip install pycryptdome
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import fitz  #pip install pymupdf
import os

def cargar_clave_privada(nombre):
    with open(f"keys/privada_{nombre}.pem", "rb") as file:
        return RSA.import_key(file.read())

def generar_hash_pdf(nombre_pdf):
    with open(nombre_pdf, "rb") as file:
        datos_pdf = file.read()
    return SHA256.new(datos_pdf)  # 🔹 Generamos el hash antes de modificar el PDF

def firmar_documento(nombre_pdf, clave_privada, firmante="Alice", nuevo_pdf=None):
    """
    Firma el documento PDF correctamente sin alterar su contenido.
    """
    if nuevo_pdf is None:
        nuevo_pdf = f"NDA_firmado.pdf" if firmante == "Alice" else "NDA_firmado_ac.pdf"

    # Calculamos el hash antes de modificar el PDF
    hash_doc = generar_hash_pdf(nombre_pdf)
    firma = pkcs1_15.new(clave_privada).sign(hash_doc)

    doc = fitz.open(nombre_pdf)
    page = doc.new_page()  # Agregamos una nueva página solo para la firma
    page.insert_text((50, 100), f"Firma {firmante}: {firma.hex()}", fontsize=10)

    doc.save(nuevo_pdf)
    doc.close()
    print(f" Documento firmado por {firmante}. Guardado en: {nuevo_pdf}")

def firmar_con_ac(nombre_pdf):
    """
    La Autoridad Certificadora (AC) firma el documento después de Alice.
    """
    clave_privada_ac = cargar_clave_privada("ac")
    nuevo_pdf = "NDA_firmado_ac.pdf"  
    firmar_documento(nombre_pdf, clave_privada_ac, firmante="AC", nuevo_pdf=nuevo_pdf)
    
    if os.path.exists(nuevo_pdf):
        print(f"Documento firmado por la AC. Guardado en: {nuevo_pdf}")
    else:
        print(f"ERROR: No se pudo crear {nuevo_pdf}")

def main():
    """
    Flujo principal: Alice firma primero, luego la AC verifica y firma.
    """
    clave_privada_alice = cargar_clave_privada("alice")
    firmar_documento("NDA.pdf", clave_privada_alice, firmante="Alice")
    
    firmar_con_ac("NDA_firmado.pdf")

if __name__ == "__main__":
    main()
