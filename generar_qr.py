import qrcode
from PIL import Image

def crear_qr(url, nombre_archivo, logo_path):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    
    # QR en Blanco y Negro
    img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    
    try:
        logo = Image.open(logo_path).convert("RGBA")
        
        # Quitar fondo (hacer transparente lo que sea claro)
        logo_gray = logo.convert("L")
        newData = []
        for val in logo_gray.getdata():
            # Umbral moderado para quitar el fondo naranja/blanco
            if val > 180: 
                newData.append((255, 255, 255, 0))
            else:
                # Mantener el tono original del dibujo en escala de grises para no distorsionar
                newData.append((val, val, val, 255))
        logo.putdata(newData)

        # Ajustar tamaño del logo (25% del QR es el estándar de seguridad)
        qr_width, qr_height = img_qr.size
        logo_size = int(qr_width * 0.25)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        # POSICIÓN del logo
        pos_x = (qr_width - logo_size) // 2
        pos_y = (qr_height - logo_size) // 2
        
        # LIMPIAR ÁREA CENTRAL (Mínimo necesario para que no haya ruido)
        # Reducimos el pad a 10 pixeles como pidió el usuario (que no se vea tanto blanco)
        clear_pad = 10
        for x in range(pos_x - clear_pad, pos_x + logo_size + clear_pad):
            for y in range(pos_y - clear_pad, pos_y + logo_size + clear_pad):
                if 0 <= x < qr_width and 0 <= y < qr_height:
                    img_qr.putpixel((x, y), (255, 255, 255, 255))
        
        # Pegar el logo sobre el área limpia
        img_qr.paste(logo, (pos_x, pos_y), logo)
        
    except Exception as e:
        print(f"No se pudo procesar el logo para {nombre_archivo}: {e}")
        
    # Convertir de vuelta a RGB para guardar como PNG estándar
    img_qr.convert('RGB').save(nombre_archivo)
    print(f"Archivo {nombre_archivo} generado con logo limpio y B&W.")

link_menu = "https://marisquerianat.velezmen.me/index.html"
link_pago = "https://marisquerianat.velezmen.me/pago.html"

crear_qr(link_menu, "qr_menu.png", "assets/logo_nat.jpg")
crear_qr(link_pago, "qr_pago.png", "assets/logo_nat.jpg")