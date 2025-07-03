import qrcode
from PIL import Image
import io
import base64

def create_phishing_qr(url, save_path="phishing_qr.png"):
    """
    Genera un QR code que dirija a la página de phishing demo
    """
    
    # Configuración del QR
    qr = qrcode.QRCode(
        version=1,  # Controla el tamaño (1 es el más pequeño)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # ~7% error correction
        box_size=10,  # Tamaño de cada "caja" en píxeles
        border=5,     # Grosor del borde
    )
    
    # Agregar la URL (reemplaza con tu URL real)
    qr.add_data("https://quishing-ashy.vercel.app/")
    qr.make(fit=True)
    
    # Crear imagen del QR
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Crear una imagen más grande con texto
    from PIL import ImageDraw, ImageFont
    
    # Crear lienzo más grande
    canvas_width = 400
    canvas_height = 500
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    
    # Redimensionar QR para que quepa bien
    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Pegar QR en el centro
    qr_x = (canvas_width - qr_size) // 2
    qr_y = 50
    canvas.paste(qr_img, (qr_x, qr_y))
    
    # Agregar texto
    draw = ImageDraw.Draw(canvas)
    
    try:
        # Intentar usar una fuente más bonita
        title_font = ImageFont.truetype("arial.ttf", 24)
        subtitle_font = ImageFont.truetype("arial.ttf", 16)
    except:
        # Fallback a fuente por defecto
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Título
    title_text = "📱 Recursos de la Conferencia"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (canvas_width - title_width) // 2
    draw.text((title_x, 15), title_text, fill="black", font=title_font)
    
    # Subtítulo
    subtitle_text = "Escanea para descargar diapositivas"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (canvas_width - subtitle_width) // 2
    draw.text((subtitle_x, 370), subtitle_text, fill="gray", font=subtitle_font)
    
    # URL (pequeña, abajo)
    url_short = url if len(url) < 40 else url[:37] + "..."
    url_bbox = draw.textbbox((0, 0), url_short, font=subtitle_font)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (canvas_width - url_width) // 2
    draw.text((url_x, 395), url_short, fill="lightgray", font=subtitle_font)
    
    # Guardar imagen
    canvas.save(save_path, "PNG", quality=95)
    print(f"✅ QR Code generado: {save_path}")
    
    return save_path

def create_presentation_slide_qr(url):
    """
    Versión específica para mostrar en presentación
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,  # Más grande para presentación
        border=2,
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # QR simple, sin decoraciones (para presentación)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("presentation_qr.png", "PNG")
    print("✅ QR para presentación generado: presentation_qr.png")
    
    return "presentation_qr.png"

# Ejemplo de uso
if __name__ == "__main__":
    # ⚠️ IMPORTANTE: Reemplaza con tu URL real donde hosteas la página
    demo_url = "https://quishing-ashy.vercel.app/"
    
    print("🎯 Generando QRs para demo de QRphishing...")
    print(f"📡 URL objetivo: {'https://quishing-ashy.vercel.app/'}")
    print()
    
    # Generar QR decorado
    create_phishing_qr(demo_url, "qr_phishing_decorado.png")
    
    # Generar QR simple para presentación
    create_presentation_slide_qr(demo_url)
    
    print()
    print("🚨 RECORDATORIOS IMPORTANTES:")
    print("1. Usa esto SOLO para fines educativos y con consentimiento")
    print("2. Informa claramente que es una demostración")
    print("3. No recolectes datos reales de participantes sin autorización")
    print("4. Hostea la página en un dominio que controles")
    
    # Información adicional para la presentación
    print()    
    print("1. 'Vamos a hacer una demostración práctica...'")
    print("2. 'Aquí tienen un QR con recursos adicionales de la charla'")
    print("3. 'Es completamente seguro, solo escanéenlo'")
    print("4. [Esperar que escaneen]")
    print("5. 'Perfecto, ahora veamos qué información obtuve...'")
    print("6. [Mostrar revelación]")