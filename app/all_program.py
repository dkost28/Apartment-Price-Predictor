import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, askyesno
import numpy as np
import sqlite3 as sq
import joblib
import warnings
import pickle

warnings.filterwarnings('ignore', category=UserWarning, module='sklearn.base')


def get_current_selection_hasStorageRoom():
    return current_selection_hasStorageRoom.get()


def get_current_selection_security():
    return current_selection_security.get()


def get_elevator():
    return current_selection.get()


def get_restaurantDistance():
    return restaurantDistance.get()


def get_poiCount():
    return poiCount.get()


def get_build():
    return buildYear.get()


def get_rooms():
    return rooms.get()


def get_square():
    return square.get()


def get_name_reg():
    return name_reg.get()


def get_email_reg():
    return email_reg.get()


def get_pass_reg():
    return password_reg.get()


def get_email_login():
    return email_login.get()


def get_password_login():
    return password_login.get()


def first_page():
    global all_data, email_login, password_login, type_apartmentBuilding, email_reg, type_blockOfFlats, password_reg, name_reg, square, rooms, buildYear, poiCount, type_of_build, res, restaurantDistance, current_selection, current_selection_security, current_selection_hasStorageRoom

    root = tk.Tk()
    root.title('Apartment Price Calculation')

    window_width, window_height = 1100, 700
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    center_x, center_y = (screen_width - window_width) // 2, (screen_height - window_height) // 2
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)
    root.iconbitmap(r'C:\Users\dkost\Desktop\DS_projects\Poland_appartment\OIP.ico')

    font_large = ('Arial', 14)

    container = tk.Frame(root)
    container.pack(expand=True, fill='both')
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    email_login = tk.StringVar()
    password_login = tk.StringVar()
    name_reg = tk.StringVar()
    email_reg = tk.StringVar()
    password_reg = tk.StringVar()
    square = tk.DoubleVar()
    rooms = tk.IntVar()
    buildYear = tk.IntVar()
    poiCount = tk.IntVar()
    restaurantDistance = tk.DoubleVar()
    type_of_build = tk.BooleanVar()
    current_selection_security = tk.BooleanVar()
    current_selection_hasStorageRoom = tk.BooleanVar()
    current_selection = tk.BooleanVar()
    type_blockOfFlats = tk.BooleanVar()
    type_apartmentBuilding = tk.BooleanVar()
    current_selection_security = tk.BooleanVar()
    current_selection_hasStorageRoom = tk.BooleanVar()

    def show_frame(frame):
        frame.tkraise()

    #Frame with data

    frame_main = tk.Frame(container)
    frame_main.grid(row=0, column=0, sticky='nsew')
    frame_main.pack_propagate(False)
    frame_main.config(pady=150)

    # Login Frame
    frame_login = tk.Frame(container)
    frame_login.grid(row=0, column=0, sticky='nsew')
    frame_login.pack_propagate(False)
    frame_login.config(pady=150)

    #Login
    ttk.Label(frame_login, text='Email Address:', font=font_large).pack(pady=10)
    email_entry = ttk.Entry(frame_login, textvariable=email_login, font=font_large, width=30)
    email_entry.pack(pady=5)

    ttk.Label(frame_login, text='Password:', font=font_large).pack(pady=10)
    password_entry = ttk.Entry(frame_login, textvariable=password_login, show="•", font=font_large, width=30)
    password_entry.pack(pady=5)

    def login_clicked():
        con = sq.connect('appartment_price_users.db')
        cur = con.cursor()

        user_email = get_email_login()
        user_password = get_password_login()

        try:
            cur.execute('SELECT password FROM users WHERE email = ?', (user_email,))
            user = cur.fetchone()

            if user:
                true_pass = user[0]
                if true_pass == user_password:
                    msg1 = f"You entered email: {user_email} and correct password"
                    showinfo(title="Information", message=msg1)
                    show_frame(frame_main)
                else:
                    msg2 = f"You entered email: {user_email} and incorrect password"
                    showinfo(title="Information", message=msg2)
            else:
                msg3 = f"Email {user_email} not found"
                showinfo(title="Information", message=msg3)

        except sq.Error as e:
            print(f"Error: {e}")
        finally:
            con.close()

    ttk.Button(frame_login, text='Login', command=login_clicked, style='TButton').pack(pady=20)
    ttk.Button(frame_login, text='Registration', command=lambda: show_frame(frame_registr), style='TButton').pack()

    # Main Frame
    current_selection = tk.BooleanVar()

    a = np.arange(0, 1000, 1)

    ttk.Label(frame_main, text='Enter apartment details', font=font_large).place(x=430, y=-120)
    ttk.Label(frame_main, text='Square meters of apartment:', font=font_large).place(x=5, y=1)

    spin_box = ttk.Spinbox(frame_main, values=a, textvariable=square, wrap=True)
    spin_box.place(x=250, y=2)

    ttk.Label(frame_main, text='Rooms:', font=font_large).place(x=5, y=35)
    spin_box = ttk.Spinbox(frame_main, from_=0, to=50, textvariable=rooms, wrap=True)
    spin_box.place(x=100, y=39)

    ttk.Label(frame_main, text='Year built:', font=font_large).place(x=5, y=70)
    spin_box = ttk.Spinbox(frame_main, from_=1500, to=2025, textvariable=buildYear, wrap=True)
    spin_box.place(x=100, y=78)

    ttk.Label(frame_main, text='Number of points of interest in 500m:', font=font_large).place(x=5, y=105)
    spin_box = ttk.Spinbox(frame_main, from_=0, to=50, textvariable=poiCount, wrap=True)
    spin_box.place(x=320, y=110)

    ttk.Label(frame_main, text='Distance to the nearest restaurant in km:', font=font_large).place(x=5, y=140)
    spin_box = ttk.Spinbox(frame_main, from_=0, to=30, textvariable=restaurantDistance, wrap=True)
    spin_box.place(x=350, y=142)

    ttk.Label(frame_main, text='Does the apartment have an elevator?', font=font_large).place(x=550, y=1)
    radio1 = ttk.Radiobutton(frame_main, text='Yes', value=True, variable=current_selection)
    radio1.place(x=880, y=4)
    radio2 = ttk.Radiobutton(frame_main, text='No', value=False, variable=current_selection)
    radio2.place(x=930, y=4)

    ttk.Label(frame_main, text='Does the apartment have security?', font=font_large).place(x=550, y=36)
    radio1 = ttk.Radiobutton(frame_main, text='Yes', value=True, variable=current_selection_security)
    radio1.place(x=880, y=40)
    radio2 = ttk.Radiobutton(frame_main, text='No', value=False, variable=current_selection_security)
    radio2.place(x=930, y=40)

    ttk.Label(frame_main, text='Does the apartment have storage room?', font=font_large).place(x=550, y=71)
    radio1 = ttk.Radiobutton(frame_main, text='Yes', value=True, variable=current_selection_hasStorageRoom)
    radio1.place(x=900, y=75)
    radio2 = ttk.Radiobutton(frame_main, text='No', value=False, variable=current_selection_hasStorageRoom)
    radio2.place(x=950, y=75)  # Does the house have security?

    res = [False] * 15

    def on_selection(event):
        selected_value = combobox.get()
        try:
            index = options.index(selected_value)
        except ValueError:
            print("Selected city is not in the options.")
            return

        global res
        res = [False] * len(options)
        res[index] = True

        print(res)

    def reset_selection():
        combobox.set('-')
        global res
        res = [False] * len(options)
        print("Selection reset.")

    options = ['Bialystok', 'Bydgoszcz', 'Czestochowa', 'Gdansk', 'Gdynia', 'Katowice', 'Krakow', 'Lodz', 'Lublin',
               'Poznan', 'Radom', 'Rzeszow', 'Szczecin', 'Warszawa', 'Wroclaw']

    ttk.Label(frame_main, text='Select a city: ', font=font_large).place(x=550, y=107)
    combobox = ttk.Combobox(frame_main, values=options)
    combobox.set('-')
    combobox.bind('<<ComboboxSelected>>', on_selection)
    combobox.place(x=680, y=110)

    reset_button = ttk.Button(frame_main, text='Reset Selection', command=reset_selection)
    reset_button.place(x=860, y=110)

    print(email_login, password_login, email_reg, password_reg, name_reg, square, rooms, buildYear, poiCount,
          type_of_build, restaurantDistance, current_selection, current_selection_security,
          current_selection_hasStorageRoom)

    all_data = [False] * 24

    def save_data():
        global all_data
        all_data.clear()

        year = 2024
        square = get_square()
        rooms = get_rooms()
        buildYear = get_build()
        poiCount = get_poiCount()
        restaurantDistance = get_restaurantDistance()
        current_selection = get_elevator()
        current_selection_security = get_current_selection_security()
        current_selection_hasStorageRoom = get_current_selection_hasStorageRoom()
        global res

        all_data.extend(
            [square, rooms, buildYear, poiCount, restaurantDistance, current_selection, current_selection_security,
             current_selection_hasStorageRoom, year, *res])
        return all_data
        #print(all_data)

    def pred_data():
        save_data()
        global all_data

        if not all_data:
            showinfo(title="Error", message="No data available for prediction")
            return
        print(all_data)
        #with open('random_forest_model008.pkl', 'rb') as f:
            #rf_loaded = pickle.load(f)
        rf_loaded = joblib.load('random_forest_model008.pkl')
        reshape_all_data = np.array(all_data).reshape(1, -1)
        print(all_data)
        predicted_value = rf_loaded.predict(reshape_all_data)
        predicted_value = round(predicted_value[0], 1)
        print(predicted_value)

        msg = f"Apartment price: {predicted_value} zł"
        showinfo(title="Price", message=msg)

        print(*predicted_value, 'zł')
        return all_data.clear()

    ttk.Button(frame_main, text='Apartment price:', command=pred_data, style='TButton').place(x=485, y=230)

    #ttk.Button(frame_main, text='-', command=save_data, style='TButton').place(x=430, y=200)

    # Registration Frame
    frame_registr = tk.Frame(container)
    frame_registr.grid(row=0, column=0, sticky='nsew')

    ttk.Label(frame_registr, text='Name:', font=font_large).pack(pady=10)
    name_entry = ttk.Entry(frame_registr, textvariable=name_reg, font=font_large, width=30)
    name_entry.pack(pady=5)

    ttk.Label(frame_registr, text='Email Address:', font=font_large).pack(pady=10)
    email_reg_entry = ttk.Entry(frame_registr, textvariable=email_reg, font=font_large, width=30)
    email_reg_entry.pack(pady=5)

    ttk.Label(frame_registr, text='Password:', font=font_large).pack(pady=10)
    password_reg_entry = ttk.Entry(frame_registr, textvariable=password_reg, show="•", font=font_large, width=30)
    password_reg_entry.pack(pady=5)

    def check_name():
        name = get_name_reg()
        symbols = r'[!@#$%^&*(),<>?/.\|[\]{}+=\-_0-9]'

        for symbol in symbols:
            if symbol in name:
                name = name.strip()
                msg = f"Invalid character found in your name: {symbol}"
                if askyesno("Delete Symbol", f"Do you want to delete symbol '{symbol}'?"):
                    name = name.replace(symbol, "")
                    if len(name) < 1:
                        showinfo(title="Problem with name", message="You wrote only symbols.")
                        break
                    elif symbol in name:
                        showinfo(title="Name Updated", message=f"Your name without symbols: {name}")
                else:
                    return

        msg = f"Registered:\nName: {name}\nEmail: {get_email_reg()}\nPassword: {get_pass_reg()}"
        showinfo(title="Registration Successful", message=msg)

        user_data = [name, get_email_reg(), get_pass_reg()]
        print(user_data)

        con = sq.connect('appartment_price_users.db')
        cur = con.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,  
                password TEXT NOT NULL
            )
            ''')

        try:
            cur.execute("BEGIN")
            cur.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', user_data)
            con.commit()
        except sq.Error as e:
            print(f"Error {e}")
        finally:
            con.close()
        show_frame(frame_login)

    ttk.Button(frame_registr, text='Register', command=check_name, style='TButton').pack(pady=20)

    ttk.Button(frame_registr, text='Back to Login', command=lambda: show_frame(frame_login), style='TButton').pack(
        pady=10)

    ttk.Button(frame_main, text='Exit', command=lambda: show_frame(frame_login), style='TButton').place(
        x=5, y=-150)

    show_frame(frame_login)
    root.mainloop()
