from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import fitz  # PyMuPDF para modificar el PDF

# Cargar clave privada
def cargar_clave_privada(nombre):
    with open(f"keys/privada{nombre}.pem", "rb") as file:
        return RSA.import_key(file.read())

# Generar hash del documento PDF
def generar_hash_pdf(nombre_pdf):
    with open(nombre_pdf, "rb") as file:
        datos_pdf = file.read()
    return SHA256.new(datos_pdf)  # 🔹 Generar hash con los datos binarios del PDF

# Firmar el documento y añadir la firma dentro del PDF
def firmar_documento(nombre_pdf, clave_privada, firmante="Alice"):
    hash_obj = generar_hash_pdf(nombre_pdf)  # Generamos el hash del PDF
    firma = pkcs1_15.new(clave_privada).sign(hash_obj)  # Firmamos el hash

    # Convertimos la firma a hexadecimal para almacenarla en el PDF
    firma_hex = firma.hex()

    # Abrimos el PDF y agregamos la firma digital
    doc = fitz.open(nombre_pdf)
    page = doc[0]  # Primera página

    # Insertamos la firma en el PDF
    if firmante == "Alice":
        page.insert_text((50, 50), f"Firma Alice: {firma_hex[:50]}...", fontsize=8, color=(1, 0, 0))
        pdf_firmado = nombre_pdf.replace(".pdf", "_firmado.pdf")
    else:
        page.insert_text((50, 70), f"Firma AC: {firma_hex[:50]}...", fontsize=8, color=(0, 0, 1))
        pdf_firmado = nombre_pdf.replace(".pdf", "_firmado_ac.pdf")

    # Guardamos el PDF firmado
    doc.save(pdf_firmado)
    doc.close()

    print(f"✅ Documento firmado por {firmante}. Guardado en: {pdf_firmado}")

# La AC firma el documento después de verificar la firma de Alice
def firmar_con_ac(nombre_pdf, clave_privada_ac):
    firmar_documento(nombre_pdf, clave_privada_ac, firmante="AC")

# ✅ Función principal
def main():
    clave_privada_alice = cargar_clave_privada("alice")
    firmar_documento("NDA.pdf", clave_privada_alice)

# ✅ Si se ejecuta directamente, llamar a main()
if __name__ == "__main__":
    main()
