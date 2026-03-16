import qrcode
from PIL import Image

def crear_qr(url, nombre_archivo, logo_path):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    
    img_qr = qr.make_image(fill_color="#d35400", back_color="white").convert('RGB')
    
    try:
        logo = Image.open(logo_path)
        # Ajustar tamaño del logo
        size = img_qr.size[0] // 4
        logo = logo.resize((size, size))
        # Pegar en el centro
        pos = ((img_qr.size[0] - size) // 2, (img_qr.size[1] - size) // 2)
        img_qr.paste(logo, pos)
    except:
        print(f"No se pudo cargar el logo para {nombre_archivo}")
        
    img_qr.save(nombre_archivo)
    print(f"Archivo {nombre_archivo} generado.")

link_menu = "https://marisquerianat.velezmen.me/index.html"
link_pago = "https://marisquerianat.velezmen.me/pago.html"

crear_qr(link_menu, "qr_menu.png", "assets/logo_nat.jpg")
crear_qr(link_pago, "qr_pago.png", "assets/logo_nat.jpg")