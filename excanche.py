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


def update_label(combobox, label):
    """Обновляет метку с названием выбранной валюты."""
    selected_code = combobox.get()
    currency_name = currencies[selected_code]
    label.config(text=currency_name)


def get_exchange_rate():
    """Получает курс обмена валюты."""
    target_code = target_currency_combobox.get()
    base_code = base_currency_combobox.get()

    if target_code and base_code:
        try:
            response = requests.get(f'https://open.er-api.com/v6/latest/{base_code}')
            response.raise_for_status()
            data = response.json()
            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                target_name = currencies[target_code]
                base_name = currencies[base_code]
                messagebox.showinfo('Курс обмена', f'Курс: {
                                    exchange_rate:.3f} - {target_name} за 1 {base_name}')
            else:
                messagebox.showerror('Ошибка', f'Валюта с кодом {
                                     target_code} не найдена')
        except Exception as e:
            messagebox.showerror('Ошибка', f'Ошибка - {e}')
    else:
        messagebox.showwarning('Внимание', 'Поле выбора пустое')


root = tk.Tk()
root.title('Курсы обмена валют')
root.geometry('500x500')

# Загрузка данных о валютах
currencies = load_currencies()
# Метка и выпадающий список для первой базовой валюты
base_currency_label = ttk.Label(root, text='Выберите базовую валюту:')
base_currency_label.pack(pady=[10, 10])  # Размещаем метку в окне

base_currency_combobox = ttk.Combobox(width=30, height=30, values=list(currencies.keys()))
base_currency_combobox.pack(pady=[10, 10])  # Размещаем выпадающий список в окне
base_currency_combobox.bind('<<ComboboxSelected>>', lambda event: update_label(base_currency_combobox, base_label))
base_label = tk.Label()
base_label.pack(padx=10, pady=10)

# Метка и выпадающий список для целевой валюты
target_currency_label = ttk.Label(root, text='Выберите код целевой валюты:')
target_currency_label.pack(pady=[10, 10])  # Размещаем метку в окне

# Создание выпадающего списка с кодами валют
target_currency_combobox = ttk.Combobox(width=30, height=30, values=list(currencies.keys()))
target_currency_combobox.pack()
target_currency_combobox.current(0)
target_currency_combobox.bind('<<ComboboxSelected>>', lambda event: update_label(target_currency_combobox, target_label))

# Метка для отображения названия выбранной валюты
target_label = tk.Label()
target_label.pack(padx=10, pady=10)

# Кнопка для получения курса обмена
tk.Button(text='Получить курс обмена', justify='center',
          command=get_exchange_rate).pack(padx=10, pady=10)

update_label(target_currency_combobox, target_label)

# Запуск основного цикла приложения
root.mainloop()
