import firmaRSA
import verificacion

def main():
    print("🔹 1️⃣ Firmando documento...")
    firmaRSA.main()  # Alice firma el documento

    print("\n🔹 2️⃣ Verificando firma de Alice en la AC...")
    verificacion.main()  # La AC verifica la firma de Alice

    print("\n🔹 3️⃣ La AC firma el documento y se lo envía a Bob...")
    clave_privada_ac = firmaRSA.cargar_clave_privada("ac")
    firmaRSA.firmar_con_ac("NDA_firmado.pdf", clave_privada_ac)

    print("\n🔹 4️⃣ Bob verifica la firma de la AC...")
    clave_publica_ac = verificacion.cargar_clave_publica("ac")
    verificacion.verificar_firma_pdf("NDA_firmado_ac.pdf", clave_publica_ac, firmante="AC")

    print("\n✅ Proceso completo.")

if __name__ == "__main__":
    main()
