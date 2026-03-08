import os
import tkinter as tk
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode

def generate_invoice(name, service, amount):
    if not os.path.exists("invoices"):
        os.makedirs("invoices")
    
    pdf_path = os.path.join("invoices", f"Invoice_{name}.pdf")
    qr_path = f"temp_qr_{name}.png"
    
    font_path = "C:/Windows/Fonts/arial.ttf"
    font_name = 'Arial' if os.path.exists(font_path) else 'Helvetica'
    if font_name == 'Arial':
        pdfmetrics.registerFont(TTFont('Arial', font_path))

    qr = qrcode.make(f"PAY_TO:{name}_AMT:{amount}")
    qr.save(qr_path)

    c = canvas.Canvas(pdf_path)
    c.setFont(font_name, 20)
    c.drawString(50, 800, f"СЧЕТ ДЛЯ: {name}")
    c.setFont(font_name, 12)
    c.drawString(50, 770, f"Услуга: {service}")
    c.drawString(50, 750, f"Сумма: ${amount}")
    c.drawImage(qr_path, 50, 600, width=100, height=100)
    c.save()

    if os.path.exists(qr_path):
        os.remove(qr_path)
    return pdf_path

# ФУНКЦИЯ ДЛЯ КНОПКИ В ОКНЕ
def on_submit():
    name = entry_name.get()
    service = entry_service.get()
    amount = entry_amount.get()
    
    if name and service and amount:
        try:
            path = generate_invoice(name, service, amount)
            messagebox.showinfo("Успех", f"Счет для {name} создан!\nПуть: {path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Что-то пошло не так: {e}")
    else:
        messagebox.showwarning("Внимание", "Заполните все поля!")

# СОЗДАНИЕ ОКНА
root = tk.Tk()
root.title("Генератор счетов v1.1")
root.geometry("300x250")

tk.Label(root, text="Имя клиента:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Услуга:").pack(pady=5)
entry_service = tk.Entry(root)
entry_service.pack()

tk.Label(root, text="Сумма ($):").pack(pady=5)
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Button(root, text="Создать PDF", command=on_submit, bg="green", fg="white").pack(pady=20)

root.mainloop()
