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
                currency_name = currencies[selected_code]
                messagebox.showinfo('Курс обмена', f'Курс: {
                                    exchange_rate:.3f} - {currency_name} за 1 РУБ')
            else:
                messagebox.showerror('Ошибка', f'Валюта с кодом {
                                     selected_code} не найдена')
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка - {e}')
    else:
        messagebox.showwarning('Внимание', 'Поле выбора пустое')


root = tk.Tk()
root.title('Курсы обмена валют')
root.geometry('500x500')

# Загрузка данных о валютах
currencies = load_currencies()

# Создание метки для выбора валюты
tk.Label(text='Выберите код валюты').pack(padx=10, pady=10)

# Создание выпадающего списка с кодами валют
combobox = ttk.Combobox(width=30, height=30, values=list(currencies.keys()))
combobox.pack()
combobox.current(0)
combobox.bind('<<ComboboxSelected>>', update_currency_label)

# Метка для отображения названия выбранной валюты
currency_label = tk.Label(text='Российский рубль')
currency_label.pack(padx=10, pady=10)

# Кнопка для получения курса обмена
tk.Button(text='Получить курс обмена', justify='center',
          command=get_exchange_rate).pack(padx=10, pady=10)

# Запуск основного цикла приложения
root.mainloop()
