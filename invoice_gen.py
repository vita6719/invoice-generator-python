import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode

def generate_invoice(name, service, amount):
    # Создаем папку для готовых счетов, если её нет
    if not os.path.exists("invoices"):
        os.makedirs("invoices")
    
    pdf_path = os.path.join("invoices", f"Invoice_{name}.pdf")
    qr_path = f"temp_qr_{name}.png"
    
    # Подключаем шрифт Arial (стандарт для Windows)
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        font_name = 'Arial'
    else:
        font_name = 'Helvetica'

    # 1. Генерируем QR-код
    qr = qrcode.make(f"https://pay.com{name}?amount={amount}")
    qr.save(qr_path)

    # 2. Рисуем PDF
    c = canvas.Canvas(pdf_path)
    c.setFont(font_name, 20)
    c.drawString(50, 800, f"СЧЕТ ДЛЯ: {name}")
    
    c.setFont(font_name, 14)
    c.drawString(50, 770, f"Услуга: {service}")
    c.drawString(50, 750, f"К оплате: ${amount}")
    
    # Вставляем QR и подпись
    c.drawImage(qr_path, 50, 600, width=120, height=120)
    c.setFont(font_name, 10)
    c.drawString(50, 580, "Отсканируйте для быстрой оплаты")
    
    c.save()

    # 3. Убираем временный файл QR
    if os.path.exists(qr_path):
        os.remove(qr_path)
    
    print(f"✅ Успех! Счёт сохранен в папку 'invoices' как: Invoice_{name}.pdf")

if __name__ == "__main__":
    # Тестовый запуск
    
      
