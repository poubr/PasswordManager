from tkinter import *
from tkinter import messagebox
import json
from string import ascii_letters, punctuation, digits
from random import randint, choice, shuffle
import pyperclip

# setting up the window and canvas background
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=280, height=280)
logo_img = PhotoImage(file="catknight.png")
logo = canvas.create_image(180, 140, image=logo_img)
canvas.grid(row=0, column=1)


# will save the data on data.txt
def add_data():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {website: {
            "username": username,
            "password": password,
                    }
                }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Cannot save data", message="Data fields cannot be empty.")

    else:
        is_ok = messagebox.askokcancel(title="Save data=?",
                                       message=f"Are you sure you want to save the following data?\n\n"
                                               f"Website: {website}\n"
                                               f"Username: {username}\n"
                                               f"Password: {password}\n")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            else:
                data.update(new_data)
            finally:
                reset_ui()


def reset_ui():
    website_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    username_entry.insert(0, "name@email.com")


# will generate random password
def generate_password():
    letters = [choice(ascii_letters) for i in range(randint(8, 12))]
    symbols = [choice(punctuation) for x in range(randint(4, 6))]
    numbers = [choice(digits) for z in range(randint(4, 6))]

    password_list = letters + symbols + numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# searches for a password among saved websites
def search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Password not found", message="You don't have any passwords saved yet.")
    else:
        if website in data:
            messagebox.showinfo(title="login Info", message=f"Website: {website}\n"
                                                            f"Username: {data[website]['username']}\n"
                                                            f"Password: {data[website]['password']}")
        else:
            messagebox.showerror(title="Password not found", message="You don't have this password saved.")


# UI set up - labels, entries, button
website_label = Label(text="Website:", font=("Arial", 14))
website_label.grid(row=1, column=0)

website_entry = Entry(width=31)
website_entry.grid(row=1, column=1)
website_entry.focus()

search_button = Button(text="Search", font=("Arial", 14), width=15, command=search)
search_button.grid(row=1, column=2)

username_label = Label(text="Email/Username:", font=("Arial", 14))
username_label.grid(row=2, column=0)

username_entry = Entry(width=48)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, "name@email.com")

password_label = Label(text="Password:", font=("Arial", 14))
password_label.grid(row=3, column=0)

password_entry = Entry(width=31)
password_entry.grid(row=3, column=1)

generate_pswd_button = Button(text="Generate password", font=("Arial", 14), width=15, command=generate_password)
generate_pswd_button.grid(row=3, column=2)

spacer_label = Label()
spacer_label.grid(row=4, column=0)

add_button = Button(text="Add", font=("Arial", 14), width=36, command=add_data)
add_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
