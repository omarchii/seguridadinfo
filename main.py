import firmaRSA
import verificacion

def main():
    print("\n Firmando documento...")
    firmaRSA.main()  # Alice firma el documento

    print("\n Verificando firma de Alice en la AC...")
    verificacion.main()  # La AC verifica la firma de Alice

    print("\n La AC firma el documento y se lo envía a Bob...")
    firmaRSA.firmar_con_ac("NDA_firmado.pdf")  # orrección aquí

    print("\n Bob verifica la firma de la AC...")
    clave_publica_ac = verificacion.cargar_clave_publica("ac")
    verificacion.verificar_firma_pdf("NDA_firmado_ac.pdf", clave_publica_ac, firmante="AC")

    print("\n Proceso completo.")

if __name__ == "__main__":
    main()
