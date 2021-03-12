from tkinter import *
from tkinter import messagebox
from random import randint,shuffle,choice
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for char in range(nr_letters)]
    password_symbols = [choice(symbols) for char in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0,password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,

        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")
    else:
        try:
            with open("data.json","r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json","w") as data_file:
                json.dump(new_data,data_file,indent=4)
        else:
            data.update(new_data)
            with open("data.json","w") as data_file:
                json.dump(data,data_file,indent=4)

        finally:
            website_entry.delete(0,END)
            password_entry.delete(0,END)


# ----------------------------Search Password---------------------------#

def search_password():
    website = website_entry.get()
    try:
        with open("data.json","r") as data_file:
            entries = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No Data File Found.")

    else:
        if website in entries:
            email = entries[website]["email"]
            password = entries[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:{email}\nPassword:{password}")
        else:
            messagebox.showinfo(title="Error",message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #

WHITE = "#fff"

window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50,bg=WHITE)

canvas = Canvas(width=200,height=200,bg=WHITE,highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=lock_img)
canvas.grid(row=0,column=1)

#Labels
website_label = Label(text="Website:")
website_label.grid(row=1,column=0)
email_label =  Label(text="Email/Username:")
email_label.grid(row=2,column=0)
password_label = Label(text="Password:")
password_label.grid(row=3,column=0)

#Entries
website_entry = Entry(width=21)
website_entry.grid(row=1,column=1)
website_entry.focus()
email_entry = Entry(width=30)
email_entry.grid(row=2,column=1)
password_entry = Entry(width=21)
password_entry.grid(row=3,column=1)

#Buttons
generate_password_button = Button(text="Generate Password",command=generate_password)
generate_password_button.grid(row=3,column=2)

add_button = Button(text="Add",width=36,command=save)
add_button.grid(row=4,column=1,columnspan=2)

search_button = Button(text="Search",command=search_password,width=13)
search_button.grid(row=1,column=2)

window.mainloop()