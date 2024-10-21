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
    currency_name = currencies.get(selected_code, 'Недоступно')
    label.config(text=currency_name)


def get_exchange_rate():
    """Получает курс обмена валюты."""
    target_code = target_currency_combobox.get()
    if not target_code:
        target_label.config(text='Код целевой валюты не введен',
                            font=('Arial', 12), fg='red')
        return

    base_codes = {
        'base1': base1_currency_combobox.get(),
        'base2': base2_currency_combobox.get()
    }

    for prefix, base_code in base_codes.items():
        if not base_code:
            base1_label.config(
                text='Код базовой валюты не введен', font=('Arial', 12), fg='red')
            return

        try:
            # Отправляем запрос на API для получения курса обмена
            response = requests.get(
                f'https://open.er-api.com/v6/latest/{base_code}')
            response.raise_for_status()
            data = response.json()
            rates = data.get('rates', {})
            exchange_rate = rates.get(target_code, 'Недоступно')
            target_name = currencies.get(target_code, 'Недоступно')
            base_name = currencies.get(base_code, 'Недоступно')

            # Проверяем, является ли введенное значение числом
            try:
                int_target = int(entry.get())
            except ValueError:
                messagebox.showerror('Ошибка', 'Введите корректное число')
                return

            # Рассчитываем сумму целевой валюты
            sum_target = int_target * exchange_rate

            # Показываем результат в диалоговом окне
            messagebox.showinfo('Курс обмена', f'{int_target} {
                                base_name} - {sum_target:.2f} {target_name}')
        except requests.RequestException as e:
            messagebox.showerror('Ошибка', f'Ошибка запроса - {e}')
        except KeyError as e:
            messagebox.showerror('Ошибка', f'Ключ не найден - {e}')
        except Exception as e:
            messagebox.showerror('Ошибка', f'Неизвестная ошибка - {e}')

    # Очищаем поле ввода после успешного расчета
    try:
        entry.delete(0, tk.END)
    except Exception:
        entry.insert(0, '1')


root = tk.Tk()
root.title('Курсы обмена валют')
root.geometry('500x500')

# Загрузка данных о валютах
currencies = load_currencies()

# Метка и поле ввода для количества валюты
entry_label = tk.Label(root, text='Введите количество обмениваемой валюты')
entry_label.pack(padx=10, pady=10)

entry = ttk.Entry(root, justify="center")
entry.pack(padx=10, pady=10)
entry.insert(0, '1')  # Устанавливаем значение по умолчанию

# Метка и выпадающий список для первой базовой валюты
base1_currency_label = ttk.Label(root, text='Выберите базовую валюту:')
base1_currency_label.pack(pady=[10, 10])

base1_currency_combobox = ttk.Combobox(
    root, width=30, values=list(currencies.keys()))
base1_currency_combobox.pack(pady=[10, 10])
base1_currency_combobox.bind('<<ComboboxSelected>>', lambda event: update_label(
    base1_currency_combobox, base1_label))
base1_currency_combobox.current(146)  # Устанавливаем значение по умолчанию
base1_label = tk.Label(root)
base1_label.pack(padx=10, pady=10)

# Метка и выпадающий список для второй базовой валюты
base2_currency_label = ttk.Label(root, text='Выберите базовую валюту:')
base2_currency_label.pack(pady=[10, 10])

base2_currency_combobox = ttk.Combobox(
    root, width=30, values=list(currencies.keys()))
base2_currency_combobox.pack(pady=[10, 10])
base2_currency_combobox.bind('<<ComboboxSelected>>', lambda event: update_label(
    base2_currency_combobox, base2_label))
base2_currency_combobox.current(43)  # Устанавливаем значение по умолчанию
base2_label = tk.Label(root)
base2_label.pack(padx=10, pady=10)

# Метка и выпадающий список для целевой валюты
target_currency_label = ttk.Label(root, text='Выберите код целевой валюты:')
target_currency_label.pack(pady=[10, 10])

target_currency_combobox = ttk.Combobox(
    root, width=30, values=list(currencies.keys()))
target_currency_combobox.pack(pady=[10, 10])
target_currency_combobox.current(0)  # Устанавливаем значение по умолчанию
target_currency_combobox.bind('<<ComboboxSelected>>', lambda event: update_label(
    target_currency_combobox, target_label))

# Метка для отображения названия выбранной валюты
target_label = tk.Label(root)
target_label.pack(padx=10, pady=10)

# Кнопка для получения курса обмена
tk.Button(root, text='Получить курс обмена', width=30, height=3,
          command=get_exchange_rate).pack(padx=10, pady=10)

# Обновление меток при запуске приложения
update_label(target_currency_combobox, target_label)
update_label(base1_currency_combobox, base1_label)
update_label(base2_currency_combobox, base2_label)

# Запуск основного цикла приложения
root.mainloop()
