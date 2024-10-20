# Currency exchange rates

**Project for learning python on the platform [https://lms.osnovanie.info](https://lms.osnovanie.info)**

#### Program description

The program is a graphical user interface (GUI) in Python using the tkinter and requests libraries. It allows the user to convert currencies using current exchange rates obtained from the exchange rate API.

***Main program components***

*Loading currency data:*  

The exchange() function sends a request to the exchange rate API (https://open.er-api.com/v6/latest/RUB) and loads currency data, forming a list of available currencies, including their codes and names.

*Graphical interface:* 

The main window is created using tk.Tk().

The window contains labels (tk.Label),  
drop-down lists (ttk.Combobox) for selecting currencies,  
and a button (ttk.Button) for performing the conversion. 
