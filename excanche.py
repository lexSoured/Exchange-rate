import requests
import json
import tkinter as tk
from tkinter import messagebox, ttk


def exchange():
    code = combobox.get()

    if code:
        try:
            response = requests.get('https://open.er-api.com/v6/latest/RUB')
            response.raise_for_status()
            data = response.json()
            if code in data['rates']:
                exchange_rate = data['rates'][code]
                messagebox.showinfo('Exchange rate', f'Rate: {exchange_rate:.3f} -{code}')
            else:
                 messagebox.showerror('Error', f'Currency with {code} not found' )    
        except Exception as e:
                messagebox.showerror('Error', f'Error - {e}')
    else:
         messagebox.showwarning('Attention', 'Entry is empty')


root = tk.Tk()
root.title('Currency exchange rates')
root.geometry('500x500')

tk.Label(text='Select currency code').pack(padx=10, pady=10)
currency_dict = ['RUB', 'EUR', 'USD', 'GBP', 'CNY', 'AZN', "BYN", "JPY", "TJS" , "TRY",]
combobox = ttk.Combobox(values=currency_dict)
combobox.pack()

# ent = ttk.Entry(root, width=30, font=("Arial", 12))
# ent.pack()
# ent.config(background="white", foreground="black", state="normal", style="TEntry", cursor="arrow", takefocus=1)
tk.Button(text='Get exchange rate', justify='center' , command=exchange).pack(padx=10, pady=10)
root.mainloop()
