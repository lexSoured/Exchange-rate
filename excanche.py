import requests
import json
import tkinter as tk
from tkinter import messagebox, ttk

def load_currencies():
    with open(r'currencies.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        currencies = [(key, value) for key, value in data.items()]
    return currencies


def exchange():
    selected_currency = combobox.get()
    code, description = selected_currency.split(' - ')

    if code:
        try:
            response = requests.get('https://open.er-api.com/v6/latest/RUB')
            response.raise_for_status()
            data = response.json()
            if code in data['rates']:
                exchange_rate = data['rates'][code]
                messagebox.showinfo('Exchange rate', f'Rate: {exchange_rate:.3f} -{code} for 1 RUB')
            else:
                 messagebox.showerror('Error', f'Currency with {code} not found' )    
        except Exception as e:
                messagebox.showerror('Error', f'Error - {e}')
    else:
         messagebox.showwarning('Attention', 'Entry is empty')


root = tk.Tk()
root.title('Currency exchange rates')
root.geometry('500x500')

currencies = load_currencies()

tk.Label(text='Select currency code').pack(padx=10, pady=10)

combobox = ttk.Combobox(values=[f'{code} - {name}' for code, name in currencies])
combobox.pack()

# ent = ttk.Entry(root, width=30, font=("Arial", 12))
# ent.pack()
# ent.config(background="white", foreground="black", state="normal", style="TEntry", cursor="arrow", takefocus=1)
tk.Button(text='Get exchange rate', justify='center' , command=exchange).pack(padx=10, pady=10)
root.mainloop()
