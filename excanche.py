import requests
import json
import tkinter as tk
from tkinter import messagebox, ttk


def load_currencies():
    """Загружает данные о валютах из JSON файла."""
    with open(r'currencies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        # Создаем словарь, где ключи - коды валют, а значения - их названия
        currencies = {code: value for code, value in data.items()}
    return currencies


def update_currency_label(event):
    """Обновляет метку с названием выбранной валюты."""
    selected_code = event.widget.get()
    currency_name = currencies[selected_code]
    currency_label.config(text=currency_name)


def get_exchange_rate():
    """Получает курс обмена валюты."""
    selected_code = combobox.get()

    if selected_code:
        try:
            response = requests.get('https://open.er-api.com/v6/latest/RUB')
            response.raise_for_status()
            data = response.json()
            if selected_code in data['rates']:
                exchange_rate = data['rates'][selected_code]
                messagebox.showinfo('Exchange rate', f'Rate: {
                                    exchange_rate:.3f} - {selected_code} for 1 RUB')
            else:
                messagebox.showerror('Error', f'Currency with {
                                     selected_code} not found')
        except Exception as e:
            messagebox.showerror('Error', f'Error - {e}')
    else:
        messagebox.showwarning('Attention', 'Entry is empty')


root = tk.Tk()
root.title('Currency exchange rates')
root.geometry('500x500')

# Загрузка данных о валютах
currencies = load_currencies()

# Создание метки для выбора валюты
tk.Label(text='Select currency code').pack(padx=10, pady=10)

# Создание выпадающего списка с кодами валют
combobox = ttk.Combobox(width=30, height=30, values=list(currencies.keys()))
combobox.pack()
combobox.bind('<<ComboboxSelected>>', update_currency_label)

# Метка для отображения названия выбранной валюты
currency_label = tk.Label()
currency_label.pack(padx=10, pady=10)

# Кнопка для получения курса обмена
tk.Button(text='Get exchange rate', justify='center',
          command=get_exchange_rate).pack(padx=10, pady=10)

# Запуск основного цикла приложения
root.mainloop()
