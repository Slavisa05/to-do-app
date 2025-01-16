import sqlite3
import re
from tkinter import *


def username_validation(username):
    """Validacija korisničkog imena."""
    username = username.strip().lower()
    if len(username) < 5:
        return "Ime je prekratko!"
    elif len(username) > 15:
        return "Ime je predugacko!"
    
    # ovo vracam ovako zbog validacije u GUI
    return 'OK'


def email_validation(email):
    email = email.strip()
    if match := re.search(r'^[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$', email, re.IGNORECASE):
        return 'OK'
    else:
        return 'Email nije dobar!'
    

def email_validation_login(email):
    email = email.strip()
    if match := re.search(r'^[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$', email, re.IGNORECASE):
        return 'OK'
    
    if email == '':
        return 'Email polje ne sme biti prazno'
    else:
        return 'Mejl i username se ne podudaraju!'


def password_validation(password):
    password = password.strip()

    if len(password) < 8:
        return 'Sifra prekratka!'
    
    if match := re.search(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-.]).{8,20}$", password):
        # ovo vracam ovako zbog validaciju u GUI
        return 'OK'
    else:
        return 'Sifra ne ispunjava zahteve!'
    

def check_username_in_base_register(username_input):
    # Kreiraj vezu sa bazom
    conn = sqlite3.connect('login_data.db')
    c = conn.cursor()

    # Proveri da li username već postoji u bazi
    c.execute('SELECT username FROM login_data WHERE username = ?', (username_input,))
    # Vrati prvi red rezultata, ako postoji
    result = c.fetchone()

    if result:
        return 'Korisnicko ime zauzeto'
    else:
        return 'OK'

    # Zatvori konekciju sa bazom
    conn.close()


def check_email_in_base_register(email_input):
    # Kreiraj vezu sa bazom
    conn = sqlite3.connect('login_data.db')
    c = conn.cursor()

    # Proveri da li username već postoji u bazi
    c.execute('SELECT email FROM login_data WHERE email = ?', (email_input,))
    # Vrati prvi red rezultata, ako postoji
    result = c.fetchone()

    if result:
        return 'Email je vec u upotrebi!'
    else:
        return 'OK'

    # Zatvori konekciju sa bazom
    conn.close()


def check_username_in_base_login(username_input):
    # Kreiraj vezu sa bazom
    conn = sqlite3.connect('login_data.db')
    c = conn.cursor()

    # Proveri da li username već postoji u bazi
    c.execute('SELECT username FROM login_data WHERE username = ?', (username_input,))
    # Vrati prvi red rezultata, ako postoji
    result = c.fetchone() 

    if result:
        return 'OK'
    else:
        return 'Korisnicko ime ne postoji'

    # Zatvori konekciju sa bazom
    conn.close()


def check_username_and_email_login(username_input, email_input):
    # Kreiraj vezu sa bazom
    conn = sqlite3.connect('login_data.db')
    c = conn.cursor()
    
    check_user_email = c.execute(f'''SELECT username FROM login_data WHERE email = '{email_input}' ''')
    for names in check_user_email:
        if names[0] != username_input:
            return 'Mejl i username  se ne podudaraju!'
        else:
            return 'OK'
                

    # Zatvori konekciju sa bazom
    conn.close()


def check_email_and_password_login(email_input, password_input):
    # Kreiraj vezu sa bazom
    conn = sqlite3.connect('login_data.db')
    c = conn.cursor()
    
    check_user_email = c.execute(f'''SELECT password FROM login_data WHERE email = '{email_input}' ''')
    for passwords in check_user_email:
        if password_input == '':
            return 'Polje za sifru ne sme biti prazno!'
        
        if passwords[0] != password_input:
            return 'Sifra i mejl se ne podudaraju!'
        else:
            return 'OK'
                

    # Zatvori konekciju sa bazom
    conn.close()


def task_input_validation(task):
    if task == '':
        return 'Task polje ne sme biti prazno!'
    
    return 'OK'


def date_input_validation(date):
    if date == '':
        return 'Polje za datum ne sme biti prazno!'

    return 'OK'


def delete_input_validation(delete):
    if delete == '':
        return 'Polje za brisanje ne moze biti prazno!'

    return 'OK'


def delete_user_input_validation(delete_user):
    if delete_user == '':
        return 'Polje za brisanje ne moze biti prazno!'

    return 'OK'