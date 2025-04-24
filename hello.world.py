import tkinter as tk
from tkinter import messagebox
from datetime import datetime

current_year = datetime.now().year

def calculate_age():
    try:
        birth_year = int(birth_entry.get())
        age = current_year - birth_year
        messagebox.showinfo("Your Age", f"You are {age} years old!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid year!")

# Create main window
window = tk.Tk()
window.title("Age Calculator")
window.geometry("300x150")

# Create and pack widgets
label = tk.Label(window, text="Enter the year you were born:")
label.pack(pady=10)

birth_entry = tk.Entry(window)
birth_entry.pack(pady=5)

calc_button = tk.Button(window, text="Calculate Age", command=calculate_age)
calc_button.pack(pady=10)

window.mainloop()
