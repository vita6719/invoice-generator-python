import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode

class InvoiceGenerator:
    def __init__(self, output_dir="invoices"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Регистрация шрифта для поддержки кириллицы
        try:
            pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
            self.font = 'Arial'
        except:
            self.font = 'Helvetica'

    def create_invoice(self, client_name, service, amount):
        inv_id = datetime.now().strftime("%Y%m%d-%H%M")
        pdf_path = os.path.join(self.output_dir, f"Invoice_{client_name}.pdf")
        qr_path = f"temp_qr_{client_name}.png"

        # Генерируем QR
        qr = qrcode.make(f"PAY_TO:{client_name}_AMT:{amount}")
        qr.save(qr_path)

        # Создаем PDF
        c = canvas.Canvas(pdf_path)
        c.setFont(self.font, 20)
        c.drawString(50, 800, f"СЧЁТ НА ОПЛАТУ № {inv_id}")
        
        c.setFont(self.font, 12)
        c.line(50, 790, 550, 790) # Декоративная линия
        
        c.drawString(50, 760, f"Клиент: {client_name}")
        c.drawString(50, 740, f"Услуга: {service}")
        c.drawString(50, 720, f"Дата: {datetime.now().strftime('%d.%m.%Y')}")
        
        c.setFont(self.font, 14)
        c.drawString(50, 680, f"ИТОГО К ОПЛАТЕ: ${amount}")
        
        c.drawImage(qr_path, 50, 550, width=100, height=100)
        c.setFont(self.font, 8)
        c.drawString(50, 540, "Отсканируйте для оплаты")
        
        c.save()
        
        if os.path.exists(qr_path):
            os.remove(qr_path)
            
        print(f"[SUCCESS] Счёт для {client_name} создан: {pdf_path}")

if __name__ == "__main__":
    # Демонстрация для портфолио
    app = InvoiceGenerator()
    clients = [
        {"name": "ООО_Вектор", "service": "Разработка ПО", "amount": 1500},
        {"name": "ИП_Иванов", "service": "Консалтинг", "amount": 500}
    ]
    
    for client in clients:
        app.create_invoice(client['name'], client['service'], client['amount'])
