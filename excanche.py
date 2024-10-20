import requests
import json
import tkinter as tk
from tkinter import messagebox, ttk



root = tk.Tk()
root.title('Курсы обмена валюты')
root.geometry('500x500')

tk.Label(text='Введите код валюты').pack(padx=10, pady=10)

ent = ttk.Entry(root, width=30, font=("Arial", 12))
ent.pack()
ent.config(background="white", foreground="black", state="normal", style="TEntry", cursor="arrow", takefocus=1)
tk.Button(text='Получить курс обмена', justify='center' , command=exchange).pack(padx=10, pady=10)
root.mainloop()
