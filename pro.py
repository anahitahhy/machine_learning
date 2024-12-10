import tkinter as tk
from tkinter import ttk, messagebox
import json

try:
    path = "database.json"
    with open(path, 'r') as f:
        database = json.load(f)
except FileNotFoundError:
    database = {}
    with open(path, 'w') as f:
        json.dump(database, f, indent=4)

# Save database to file
def save_database():
    with open(path, 'w') as f:
        json.dump(database, f, indent=4)

# Refresh listbox
def refresh_contact_list():
    contact_list.delete(*contact_list.get_children())
    for name, details in database.items():
        contact_list.insert('', 'end', values=(name, details['phone'], details['email']))

# Add contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if not name or not phone or not email:
        messagebox.showerror("Error", "All fields are required.")
        return

    if name in database:
        messagebox.showerror("Error", f"{name} already exists.")
        return

    database[name] = {"phone": phone, "email": email}
    save_database()
    refresh_contact_list()
    clear_fields()
    messagebox.showinfo("Success", f"Contact '{name}' has been added.")

# Delete contact
def delete_contact():
    selected_item = contact_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a contact to delete.")
        return

    selected_name = contact_list.item(selected_item)['values'][0]
    del database[selected_name]
    save_database()
    refresh_contact_list()
    messagebox.showinfo("Success", f"Contact '{selected_name}' has been deleted.")

# Edit contact
def edit_contact():
    selected_item = contact_list.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a contact to edit.")
        return

    selected_name = contact_list.item(selected_item)['values'][0]
    selected_phone = contact_list.item(selected_item)['values'][1]
    selected_email = contact_list.item(selected_item)['values'][2]

    name_entry.delete(0, tk.END)
    name_entry.insert(0, selected_name)
    phone_entry.delete(0, tk.END)
    phone_entry.insert(0, selected_phone)
    email_entry.delete(0, tk.END)
    email_entry.insert(0, selected_email)

    def save_edit():
        new_name = name_entry.get().strip()
        new_phone = phone_entry.get().strip()
        new_email = email_entry.get().strip()

        if not new_name or not new_phone or not new_email:
            messagebox.showerror("Error", "All fields are required.")
            return

        del database[selected_name]
        database[new_name] = {"phone": new_phone, "email": new_email}
        save_database()
        refresh_contact_list()
        clear_fields()
        messagebox.showinfo("Success", f"Contact '{new_name}' has been updated.")
        save_button.config(state=tk.DISABLED)

    save_button.config(state=tk.NORMAL, command=save_edit)

# Clear fields
def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# GUI Setup
window = tk.Tk()
window.title("Contact List")
window.geometry("700x500")
window.configure(bg="#d0e7ff")

# Input frame
input_frame = tk.Frame(window, bg="#d0e7ff")
input_frame.pack(pady=20)

tk.Label(input_frame, text="Name:", font=("Arial", 12), bg="#d0e7ff").grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Phone:", font=("Arial", 12), bg="#d0e7ff").grid(row=1, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
phone_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Email:", font=("Arial", 12), bg="#d0e7ff").grid(row=2, column=0, padx=10, pady=5, sticky="w")
email_entry = tk.Entry(input_frame, font=("Arial", 12), width=25)
email_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
button_frame = tk.Frame(window, bg="#d0e7ff")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Contact", font=("Arial", 12), bg="#007bff", fg="white", command=add_contact)
add_button.grid(row=0, column=0, padx=10)

edit_button = tk.Button(button_frame, text="Edit Contact", font=("Arial", 12), bg="#ffc107", fg="white", command=edit_contact)
edit_button.grid(row=0, column=1, padx=10)

save_button = tk.Button(button_frame, text="Save Edit", font=("Arial", 12), bg="#32CD32", fg="white", state=tk.DISABLED)
save_button.grid(row=0, column=2, padx=10)

delete_button = tk.Button(button_frame, text="Delete Contact", font=("Arial", 12), bg="#dc3545", fg="white", command=delete_contact)
delete_button.grid(row=0, column=3, padx=10)

# Contact list
contact_list_frame = tk.Frame(window, bg="#f8f9fa")
contact_list_frame.pack(pady=20)

columns = ("Name", "Phone", "Email")
contact_list = ttk.Treeview(contact_list_frame, columns=columns, show="headings", height=10)
for col in columns:
    contact_list.heading(col, text=col)
    contact_list.column(col, width=200)

contact_list.pack()

refresh_contact_list()

# Run the GUI
window.mainloop()