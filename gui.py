from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from functions_for_gui import *

class App:
    def __init__(self, root):
        # definisanje root fajla, naslova i ikonice
        self.root = root
        self.root.title('to-do app')
        self.root.geometry('600x400')
        self.root.configure(background='#002D62')
        try:
            img = Image.open("img/favicon.ico") 
            photo = ImageTk.PhotoImage(img)
            root.iconphoto(True, photo)
        except Exception as e:
            print(f"Greška pri učitavanju ikone: {e}")
        
        # menu bar
        self.menubar_root = Menu(self.root)
        self.root['menu'] = self.menubar_root
        self.menubar_root.add_command(label='Admin panel', command=lambda: self.admin_panel_login(1))

        #label iznad dugmadi
        self.text = Label(self.root, text='Dobro dosli u To-do listu!', font=('Helvetica', 20), background='#002D62', fg='white')
        self.text.place(relx=0.5, rely=0.4, anchor=CENTER)

        # login i register dugme
        self.open_login_button = Button(self.root, text='Login', width=10, command=lambda: self.login_page(1)) 
        self.open_login_button.grid(row=0, column=0)
        self.open_login_button.place(relx=0.41, rely=0.5, anchor=CENTER)

        self.open_register_button = Button(self.root, text='Register', width=10, command=self.register_page) 
        self.open_register_button.grid(row=0, column=1)
        self.open_register_button.place(relx=0.56, rely=0.5, anchor=CENTER)


    '''PROZOR ZA LOGOVANJE U ADMIN PANEL'''
    def admin_panel_login(self, n):
        if n == 1:
            self.root.withdraw()
        
        if n == 2:
            self.main.destroy()

        self.admin_login = Toplevel(self.root)
        self.admin_login.title('Admin panel login')
        self.admin_login.configure(background='#002D62')

        self.admin_username_label = Label(self.admin_login, text='admin username', anchor='w', width=35, background='#002D62', fg='white')
        self.admin_username_label.grid(row=0, column=0, padx=10, pady=5)
        self.admin_username_entry = Entry(self.admin_login, width=40)
        self.admin_username_entry.grid(row=1, column=0, padx=10, pady=10, ipady=3)

        self.admin_password_label = Label(self.admin_login, text='admin password', anchor='w', width=35, background='#002D62', fg='white')
        self.admin_password_label.grid(row=2, column=0, padx=10, pady=5)
        self.admin_password_entry = Entry(self.admin_login, width=40)
        self.admin_password_entry.grid(row=3, column=0, padx=10, pady=10, ipady=3)

        self.admin_button = Button(self.admin_login, text='Login', width=10, command=self.check_admin)
        self.admin_button.grid(row=4, column=0, padx=10, pady=10)

        # kada pritisnem enter, to je kao kada sam stisnuo login dugme
        self.admin_login.bind('<Return>', lambda event: self.admin_panel())

        # zatvori root kada izadjem iz prozora
        self.admin_login.protocol("WM_DELETE_WINDOW", self.on_closing)

    
    '''PROVERA LOGIN PODATAKA ZA ADMINA - ADMIN LOGIN PROZOR'''
    def check_admin(self):
        self.admin_username = self.admin_username_entry.get()
        self.admin_password = self.admin_password_entry.get()

        if hasattr(self, 'error_admin_username_login'):
            self.error_admin_username.destroy()

        if hasattr(self, 'error_admin_password_login'):
            self.error_admin_password.destroy()

        if self.admin_username != 'admin':
            self.error_admin_username = Label(self.admin_login, text='Ime nije dobro!', background='#002D62', fg='red')
            self.error_admin_username.grid(row=5, column=0, padx=10, pady=5)
        
        if self.admin_password != 'admin123':
            self.error_admin_password = Label(self.admin_login, text='Sifra nije dobra!', background='#002D62', fg='red')
            self.error_admin_password.grid(row=6, column=0, padx=10, pady=5)
        
        if self.admin_username == 'admin' and self.admin_password == 'admin123':
            self.admin_panel()


    '''PROZOR ZA ADMIN PANEL'''
    def admin_panel(self):
        self.admin_login.destroy()
        self.admin = Toplevel(self.root)
        self.admin.title('Admin panel')
        self.admin.configure(background='#002D62')

        # napravi listu za sve korisnike
        self.users_list = Listbox(self.admin, width=80, background='#002D62', fg='white')
        self.users_list.grid(row=0, column=0, padx=10, pady=10, ipady=3)

        # delete korisnika label, entry i dugme
        self.delete_user_frame = Frame(self.admin, background='#002D62')
        self.delete_user_frame.grid(row=1, column=0, padx=10, pady=10)
        self.delete_user_label = Label(self.delete_user_frame, text='Unesi id korisnika kojeg zelis da izbrises \n(ukucaj 12345 da izbrises sve): ', anchor='w', width=35, background='#002D62', fg='white')
        self.delete_user_label.grid(row=0, column=0)
        self.delete_user_entry = Entry(self.delete_user_frame, width=40)
        self.delete_user_entry.grid(row=1, column=0, padx=10, pady=5, ipady=3)
        self.delete_user_button = Button(self.delete_user_frame, text='Izbrisi', command=self.delete_user, width=10)
        self.delete_user_button.grid(row=1, column=1, padx=2, pady=10)

        # refresh tabelu
        self.refresh_users()

        # kada pritisnem enter, to je kao kada sam stisnuo izbrisi dugme
        self.admin.bind('<Return>', lambda event: self.delete_user())

        # zatvori root kada izadjem iz prozora
        self.admin.protocol("WM_DELETE_WINDOW", self.on_closing)


    '''PROZOR ZA LOGOVANJE'''
    def login_page(self, n):
        if n == 1:
            self.root.withdraw()
        
        if n == 2:
            self.main.destroy()

        self.login_menu = Toplevel(self.root)
        self.login_menu.title('Login')
        self.login_menu.configure(background='#002D62')

        self.login_label = Label(self.login_menu, text='Unesite vase podatke da se ulogujete', font=('Helvetica', 14), background='#002D62', fg='white')
        self.login_label.grid(row=0, column=0, padx=10, pady=10)

        self.login_frame = Frame(self.login_menu, background='#002D62')
        self.login_frame.grid(row=1, column=0, pady=10)

        self.username_login_label = Label(self.login_frame, text='username', anchor='w', width=35, background='#002D62', fg='white')
        self.username_login_label.grid(row=0, column=0)
        self.username_login_entry = Entry(self.login_frame, width=40)
        self.username_login_entry.grid(row=1, column=0, pady=5, ipady=3)

        self.email_login_label = Label(self.login_frame, text='email', anchor='w', width=35, background='#002D62', fg='white')
        self.email_login_label.grid(row=2, column=0)
        self.email_login_entry = Entry(self.login_frame, width=40)
        self.email_login_entry.grid(row=3, column=0, pady=5, ipady=3)

        self.password_login_label = Label(self.login_frame, text='password', anchor='w', width=35, background='#002D62', fg='white')
        self.password_login_label.grid(row=4, column=0)
        self.password_login_entry = Entry(self.login_frame, width=40, show='*')
        self.password_login_entry.grid(row=5, column=0, pady=5, ipady=3)

        self.show_password_login = Checkbutton(self.login_frame, text='prikazi sifru', anchor='w', width=33, background='#002D62', fg='white', command=self.show_login)
        self.show_password_login.grid(row=6, column=0, padx=5, pady=3)

        self.submit_login_button = Button(self.login_menu, text='Login', width=10, command=self.check_login)
        self.submit_login_button.grid(row=3, column=0, padx=10, pady=10)

        # kada pritisnem enter, to je kao kada sam stisnuo login dugme
        self.login_menu.bind('<Return>', lambda event: self.check_login())

        # zatvori root kada izadjem iz prozora
        self.login_menu.protocol("WM_DELETE_WINDOW", self.on_closing)


    '''PROVERA INPUTA - LOGIN PROZOR'''
    def check_login(self):
        # provera da li se username nalazi u bazi
        self.validation_username_login = check_username_in_base_login(self.username_login_entry.get())
        self.check_login_username(self.validation_username_login if self.validation_username_login != 'OK' else None, 4, 'username')

        # provera inputa za email
        self.validation_email_login_entry = email_validation_login(self.email_login_entry.get())
        self.email_error_login(self.validation_email_login_entry if self.validation_email_login_entry != 'OK' else None, 5, 'email')

        # provera da li se username i email podudaraju
        self.validation_email_login = check_username_and_email_login(self.username_login_entry.get(), self.email_login_entry.get())
        self.check_email_login(self.validation_email_login if self.validation_email_login != 'OK' else None, 5, 'email')

        # provera da li se email i sifra podudaraju
        self.validation_password_login = check_email_and_password_login(self.email_login_entry.get(), self.password_login_entry.get())
        self.check_password_login(self.validation_password_login if self.validation_password_login != 'OK' else None, 6, 'password')


        if self.validation_username_login == 'OK' and self.validation_email_login == 'OK' and self.validation_password_login == 'OK':
            self.email_login = self.email_login_entry.get()
            self.open_main(1, self.email_login)


    '''PROZOR ZA REGISTROVANJE'''
    def register_page(self):
        self.root.withdraw()
        self.register_menu = Toplevel(self.root)
        self.register_menu.title('Register')
        self.register_menu.configure(background='#002D62')

        self.register_label = Label(self.register_menu, text='Unesite podatke da se registrujete', font=('Helvetica', 14), background='#002D62', fg='white')
        self.register_label.grid(row=0, column=0, padx=10, pady=10)

        self.register_frame = Frame(self.register_menu, background='#002D62')
        self.register_frame.grid(row=1, column=0, pady=10)

        self.username_register_label = Label(self.register_frame, text='username', anchor='w', width=35, background='#002D62', fg='white')
        self.username_register_label.grid(row=0, column=0)
        self.username_register_entry = Entry(self.register_frame, width=40)
        self.username_register_entry.grid(row=1, column=0, pady=5, ipady=3)

        self.email_register_label = Label(self.register_frame, text='email', anchor='w', width=35, background='#002D62', fg='white')
        self.email_register_label.grid(row=2, column=0)
        self.email_register_entry = Entry(self.register_frame, width=40)
        self.email_register_entry.grid(row=3, column=0, pady=5, ipady=3)

        self.password_register_label = Label(self.register_frame, text='password', anchor='w', width=35, background='#002D62', fg='white')
        self.password_register_label.grid(row=4, column=0)
        self.password_register_entry = Entry(self.register_frame, width=40, show='*')
        self.password_register_entry.grid(row=5, column=0, pady=5, ipady=3)

        self.show_password_register = Checkbutton(self.register_frame, text='prikazi sifru', anchor='w', width=33, background='#002D62', fg='white', command=self.show_register)
        self.show_password_register.grid(row=6, column=0, padx=5, pady=3)

        self.submit_register_button = Button(self.register_menu, text='Register', width=10, command=self.add_user)
        self.submit_register_button.grid(row=3, column=0, padx=10, pady=10)

        # kada pritisnem enter, to je kao kada sam stisnuo register dugme
        self.register_menu.bind('<Return>', lambda event: self.add_user())

        # zatvori root kada izadjem iz prozora
        self.register_menu.protocol("WM_DELETE_WINDOW", self.on_closing)


    '''PROVERAVANJE INPUTA I UBACIVANJE U BAZU PODATAKA, REGISTRACIONI PROZOR'''
    def add_user(self):
        # provera inputa za username
        self.validation_username_register = username_validation(self.username_register_entry.get())
        self.display_error(self.validation_username_register if self.validation_username_register != 'OK' else None, 4, 'username')
        
        # provera da li se ime nalazi u bazi
        self.username_in_base = check_username_in_base_register(self.username_register_entry.get())
        self.display_database_error(self.username_in_base if self.username_in_base != 'OK' else None, 4, 'username')

        # provera inputa za email
        self.validation_email_register = email_validation(self.email_register_entry.get())
        self.display_error(self.validation_email_register if self.validation_email_register != 'OK' else None, 5, 'email')

        # provera da li se email nalazi u bazi
        self.email_in_base = check_email_in_base_register(self.email_register_entry.get())
        self.display_database_error(self.email_in_base if self.email_in_base != 'OK' else None, 5, 'email')

        # provera inputa za password
        self.validation_password_register = password_validation(self.password_register_entry.get())
        self.display_error(self.validation_password_register if self.validation_password_register != 'OK' else None, 6, 'password')
        
        if self.validation_username_register == 'OK' and self.username_in_base == 'OK' and self.validation_email_register == 'OK' and self.email_in_base == 'OK' and self.validation_password_register == 'OK':
            # kreiranje veze i kursora
            self.conn = sqlite3.connect('login_data.db')
            self.c = self.conn.cursor()
            
            # ubacivanje u tabelu
            self.c.execute('INSERT INTO login_data VALUES (:username, :email, :password)',
                        {
                            'username': self.username_register_entry.get(),
                            'email': self.email_register_entry.get(),
                            'password': self.password_register_entry.get()
                        })

            self.email_register = self.email_register_entry.get()

            # cuvanje promena i zatvaranje konekcije
            self.conn.commit()
            self.conn.close()

            # ciscenje entry polja
            self.username_register_entry.delete(0, END)
            self.email_register_entry.delete(0, END)
            self.password_register_entry.delete(0, END)

            self.open_main(2, self.email_register)


    '''GLAVNI MENI - OVDE DOLAZE KADA SE REGISTRUJU/ULOGUJU'''
    def open_main(self, n, email):
        if n == 1:
            self.login_menu.destroy()
        elif n == 2:
            self.register_menu.destroy()

        self.email = email
        self.main = Toplevel(self.root)
        self.main.title('Main menu')
        self.main.configure(background='#002D62')
        self.main.option_add('*tearOff', FALSE)

        # menu bar
        self.menubar = Menu(self.main)
        self.main['menu'] = self.menubar
        self.menubar.add_command(label='Admin panel', command=lambda: self.admin_panel_login(2))
        self.menubar.add_command(label='Log out', command=lambda: self.login_page(2))

        # prikazivanje unosa za task, datum i submit dugme
        self.header_frame = Frame(self.main, background='#002D62')
        self.header_frame.grid(row=0, column=0, padx=15, pady=15)

        self.add_task_label = Label(self.header_frame, text='Unesite task', anchor='w', width=44, background='#002D62', fg='white')
        self.add_task_label.grid(row=0, column=0, pady=1)
        self.add_task_entry = Entry(self.header_frame, bd=3, width=50, background='#002D62', fg='white')
        self.add_task_entry.grid(row=1, column=0, ipady=3)

        self.add_date_label = Label(self.header_frame, text='Unesite datum', anchor='w', width=14, background='#002D62', fg='white')
        self.add_date_label.grid(row=0, column=1, pady=1)
        self.add_date = Entry(self.header_frame, bd=3, width=15, background='#002D62', fg='white')
        self.add_date.grid(row=1, column=1, ipady=3)

        self.submit_button = Button(self.header_frame, text='Dodaj task', command=self.combined_commands)
        self.submit_button.grid(row=1, column=2, padx=5, pady=3)

        # kada pritisnem enter, to je kao kada sam stisnuo dodaj task dugme
        self.main.bind('<Return>', lambda event: self.combined_commands())

        # prikazivanje taskova
        self.listbox_frame = Frame(self.main, background='#002D62')
        self.listbox_frame.grid(row=1, column=0, padx=15, pady=15)

        self.task_list = Listbox(self.listbox_frame, width=80, background='#002D62', fg='white')
        self.task_list.grid(row=0, column=0, ipady=3)

        self.refresh_tasks()

        # Brisanje taskova
        self.delete_frame = Frame(self.main, background='#002D62')
        self.delete_frame.grid(row=2, column=0, padx=15, pady=15)

        self.delete_task_label = Label(self.delete_frame, text='Unesite ID taska koji zelite da izbrisete \n(ukucajte 123456789 ako zelite da izbrisete sve taskove)', anchor='w', width=44, background='#002D62', fg='white')
        self.delete_task_label.grid(row=0, column=0, pady=1)
        self.delete_task_entry = Entry(self.delete_frame, bd=3, width=50, background='#002D62', fg='white')
        self.delete_task_entry.grid(row=1, column=0, ipady=3)

        self.submit_button = Button(self.delete_frame, text='Izbrisi task', command=self.delete_task)
        self.submit_button.grid(row=1, column=1, padx=5, pady=3)

        # kada pritisnem delete, to je kao kada sam stisnuo izbrisi task dugme
        self.main.bind('<Delete>', lambda event: self.delete_task())
    
        # zatvori root kada izadjem iz prozora
        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
    

    '''SLUZI ZA DODAVANJE TAKSA - MAIN PROZOR'''
    def add_task(self):
        self.task = self.add_task_entry.get()
        self.date = self.add_date.get()

        # otvaranje konekcije i pravljenje kursora
        self.conn = sqlite3.connect('login_data.db')
        self.c = self.conn.cursor()
        
        self.c.execute(f'''INSERT INTO task_table VALUES ('{self.email}', '{self.task}', '{self.date}')''')

        # zatvaranje konekcije
        self.conn.commit()
        self.conn.close()
        
        # Očisti Entry polja
        self.add_task_entry.delete(0, END)
        self.add_date.delete(0, END)
        
        # Osveži listu taskova
        self.refresh_tasks()


    '''REFRESUJE I PROKAZUJE PODATKE - MAIN PROZOR'''
    def refresh_tasks(self):
        # Očisti postojeće podatke u Listbox-u
        self.task_list.delete(0, END)
        
        # definisanje conn i cursora
        self.conn = sqlite3.connect('login_data.db')
        self.c = self.conn.cursor()

        self.result = self.c.execute(f'SELECT oid, task, date FROM task_table WHERE email = ?', (self.email,))
        for self.index, self.data in enumerate(self.result):
            self.task_list.insert(self.index, f'{self.data[0]}. {self.data[1]} -------------------- DATUM: {self.data[2]}')

        # zatvaranje conn
        self.conn.commit()
        self.conn.close()


    '''SLUZI DA POZOVE OBE FUNKCIJE KADA STISNEM DUGME'''
    def combined_commands(self):
        # provera inputa za task i datum
        self.validation_task_input = task_input_validation(self.add_task_entry.get())
        self.validation_date_input = date_input_validation(self.add_date.get())

        self.is_valid_task = self.task_input_check(self.validation_task_input if self.validation_task_input != 'OK' else None, 6, 'task_input')
        self.is_valid_date = self.date_input_check(self.validation_date_input if self.validation_date_input != 'OK' else None, 7, 'date_input')

        if self.is_valid_task and self.is_valid_date:
            self.add_task()  
    

    '''OVE FUNKCIJE ISPOD SLUZE ZA PROVERU TASK, DATUM i IZBRISI INPUTA - MAIN PROZOR'''
    def task_input_check(self, error_message, row, field):
        if hasattr(self, 'error_message_task_input') and field == 'task_input':
            self.error_message_task_input.destroy()

        
        if error_message and field == 'task_input':
                self.error_message_task_input = Label(self.header_frame, text=error_message, anchor='w', width=44, background='#002D62', fg='red')
                self.error_message_task_input.grid(row=row, column=0, padx=10, pady=5)
                return False
        return True

    def date_input_check(self, error_message, row, field):
        if hasattr(self, 'error_message_date_input') and field == 'date_input':
            self.error_message_date_input.destroy()

        if error_message and field == 'date_input':
                self.error_message_date_input = Label(self.header_frame, text=error_message, anchor='w', width=44, background='#002D62', fg='red')
                self.error_message_date_input.grid(row=row, column=0, padx=10, pady=5)
                return False
        return True

    def delete_input_check(self, error_message, row, field):
        if hasattr(self, 'error_message_date_input') and field == 'delete_input':
            self.error_message_date_input.destroy()

        if error_message and field == 'delete_input':
                self.error_message_date_input = Label(self.delete_frame, text=error_message, anchor='w', width=30, background='#002D62', fg='red')
                self.error_message_date_input.grid(row=row, column=0, padx=10, pady=5)


    '''SLUZI ZA BRISANJE TASKA - MAIN PROZOR'''
    def delete_task(self):
        self.task_to_delete = self.delete_task_entry.get()
        self.validation_delete_input = delete_input_validation(self.delete_task_entry.get())
        self.delete_input_check(self.validation_delete_input if self.validation_delete_input != 'OK' else None, 3, 'delete_input')

        self.task_to_delete = int(self.task_to_delete)

        # definisanje conn i cursora
        self.conn = sqlite3.connect('login_data.db')
        self.c = self.conn.cursor()

        # izbirsi sve taskove
        if self.task_to_delete == 123456789:
            self.c.execute(f'DELETE FROM task_table WHERE email = "{self.email}"')

        # izbrisi odgovarajuci task
        self.result = self.c.execute(f'SELECT oid, task FROM task_table WHERE oid = ?', (self.task_to_delete,))
        for self.data in self.result:
            if self.task_to_delete == self.data[0]:
                self.c.execute(f'''DELETE FROM task_table WHERE oid = '{self.task_to_delete}' ''')
        
        # azuriraj id-eve u tabeli
        self.c.execute('UPDATE task_table SET oid = oid - 1 WHERE oid > ?', (self.task_to_delete,))

        # cuvanje promena i zatvaranje veze
        self.conn.commit()
        self.conn.close()

        # ocisti entry polja i refresh listu
        self.delete_task_entry.delete(0, END)

        self.refresh_tasks()

    
    '''SLUZI ZA BRISANJE USERA - ADMIN PROZOR'''
    def delete_user(self):
        self.user_to_delete = self.delete_user_entry.get()
        self.validation_delete_user_input = delete_user_input_validation(self.user_to_delete)
        self.delete_user_check(self.validation_delete_user_input if self.validation_delete_user_input != 'OK' else None, 2, 'delete_user_input')

        self.user_to_delete = int(self.user_to_delete)

        # definisanje conn i cursora
        self.conn = sqlite3.connect('login_data.db')
        self.c = self.conn.cursor()

        # izbirsi sve usere
        if self.user_to_delete == 12345:
            self.c.execute(f'DELETE FROM login_data')

        # izbrisi odgovarajuceg usera
        self.result = self.c.execute(f'SELECT oid, * FROM login_data WHERE oid = ?', (self.user_to_delete,))
        for self.data in self.result:
            if self.user_to_delete == self.data[0]:
                self.c.execute(f'''DELETE FROM login_data WHERE oid = '{self.user_to_delete}' ''')
        
        # azuriraj id-eve u tabeli
        self.c.execute('UPDATE login_data SET oid = oid - 1 WHERE oid > ?', (self.user_to_delete,))

        # cuvanje promena i zatvaranje konekcije
        self.conn.commit()
        self.conn.close()

        # ocisti entry polja i refresh listu
        self.delete_user_entry.delete(0, END)

        self.refresh_users()


    '''SLUZI ZA VALIDACIJU UNOSA ZA BRISANJE KORISNIKA - ADMIN PROZOR'''
    def delete_user_check(self, error_message, row, field):
        if hasattr(self, 'error_message_delete_user_input') and field == 'delete_user_input':
            self.error_message_delete_user_input.destroy()

        if error_message and field == 'delete_user_input':
                self.error_message_delete_user_input = Label(self.delete_user_frame, text=error_message, anchor='w', width=30, background='#002D62', fg='red')
                self.error_message_delete_user_input.grid(row=row, column=0, padx=10, pady=5)


    '''REFRESUJE I PROKAZUJE USERE - ADMIN PROZOR'''
    def refresh_users(self):
        # Očisti postojeće podatke u Listbox-u
        self.users_list.delete(0, END)
        
        # definisanje veze i cursora
        self.conn = sqlite3.connect('login_data.db')
        self.c = self.conn.cursor()

        self.admin_result = self.c.execute(f'SELECT oid, * FROM login_data')
        for self.indexxx, self._user_data in enumerate(self.admin_result):
            self.users_list.insert(self.indexxx, f'{self._user_data[0]}.  IME: {self._user_data[1]};  MEJL: {self._user_data[2]};  SIFRA: {self._user_data[3]}')

        # cuvanje promena i zatvaranje veze
        self.conn.commit()
        self.conn.close()


    '''IZBACUJE GRESKU AKO USERNAME, EMAIL i SIFRA NISU DOBRI - REGISTRACIONA STRANA'''
    def display_error(self, error_message, row, field):
        # Uništi prethodne greške, ali samo za određeno polje
        if field == 'username' and hasattr(self, 'error_message_username'):
            self.error_message_username.destroy()
        elif field == 'email' and hasattr(self, 'error_message_email'):
            self.error_message_email.destroy()
        elif field == 'password' and hasattr(self, 'error_message_password'):
            self.error_message_password.destroy()

        # Prikazi grešku samo ako je prisutna
        if error_message:
            if field == 'username':
                self.error_message_username = Label(self.register_menu, text=error_message, background='#002D62', fg='red')
                self.error_message_username.grid(row=row, column=0, padx=10, pady=5)
            elif field == 'email':
                self.error_message_email = Label(self.register_menu, text=error_message, background='#002D62', fg='red')
                self.error_message_email.grid(row=row, column=0, padx=10, pady=5)
            elif field == 'password':
                self.error_message_password = Label(self.register_menu, text=error_message, background='#002D62', fg='red')
                self.error_message_password.grid(row=row, column=0, padx=10, pady=5)


    '''IZBACUJE GRESKU AKO SE IME ILI MEJL PODADARAJU SA NEKIM IMENOM ILI MEJLOM U BAZI - REGISTRACIONA STRANA'''
    def display_database_error(self, error_message, row, field):
        # Uništi prethodne greške, ali samo za određeno polje
        if hasattr(self, 'error_message_username_exist') and field == 'username':
            self.error_message_username_exist.destroy()
        elif hasattr(self, 'error_message_email_exist') and field == 'email':
            self.error_message_email_exist.destroy()

        if error_message:
            if field == 'username' and error_message:
                # Kreiraj vezu sa bazom
                self.conn = sqlite3.connect('login_data.db')
                self.c = self.conn.cursor()

                # Proveri da li username već postoji u bazi
                self.c.execute('SELECT username FROM login_data WHERE username = ?', (self.username_register_entry.get(),))
                result = self.c.fetchone()  # Vrati prvi red rezultata (ako postoji)

                if result:
                    self.error_message_username_exist = Label(self.register_menu, text=error_message, background='#002D62', fg='red')
                    self.error_message_username_exist.grid(row=row, column=0, padx=10, pady=5)

                # Zatvori konekciju sa bazom
                self.conn.commit()
                self.conn.close()

            if field == 'email' and error_message:
                # Kreiraj vezu sa bazom
                self.conn = sqlite3.connect('login_data.db')
                self.c = self.conn.cursor()

                # Proveri da li username već postoji u bazi
                self.c.execute('SELECT email FROM login_data WHERE email = ?', (self.email_register_entry.get(),))
                result = self.c.fetchone()  # Vrati prvi red rezultata (ako postoji)

                if result:
                    self.error_message_email_exist = Label(self.register_menu, text=error_message, background='#002D62', fg='red')
                    self.error_message_email_exist.grid(row=row, column=0, padx=10, pady=5)

                # Zatvori konekciju sa bazom
                self.conn.commit()
                self.conn.close()


    '''PROVERA DA LI SE USERNAME NALAZI U BAZI PODATAKA - LOGIN PROZOR'''
    def check_login_username(self, error_message, row, field):
        if hasattr(self, 'error_message_username_login') and field == 'username':
            self.error_message_username_login.destroy()

        if field == 'username' and error_message:
                # Kreiraj vezu sa bazom
                self.conn = sqlite3.connect('login_data.db')
                self.c = self.conn.cursor()

                # Proveri da li username već postoji u bazi
                self.c.execute('SELECT username FROM login_data WHERE username = ?', (self.username_login_entry.get(),))
                result = self.c.fetchone()  # Vrati prvi red rezultata (ako postoji)

                if not result:
                    self.error_message_username_login = Label(self.login_menu, text=error_message, background='#002D62', fg='red')
                    self.error_message_username_login.grid(row=row, column=0, padx=10, pady=5)

                # Zatvori konekciju sa bazom
                self.conn.commit()
                self.conn.close()


    '''VALIDIRA EMAIL - LOGIN PROZOR'''
    def email_error_login(self, error_message, row, field):
        if field == 'email' and hasattr(self, 'error_message_email'):
            self.error_message_email.destroy()

        # Prikazi grešku samo ako je prisutna
        if error_message:
            if field == 'email':
                self.error_message_email = Label(self.login_menu, text=error_message, background='#002D62', fg='red')
                self.error_message_email.grid(row=row, column=0, padx=10, pady=5)


    '''PROVERA DA LI SE USERNAME I EMAIL PODUDARAJU - LOGIN PROZOR'''
    def check_email_login(self, error_message, row, field):
        if hasattr(self, 'error_message_email_login') and field == 'email':
            self.error_message_email_login.destroy()

        if field == 'email' and error_message:
            # Kreiraj vezu sa bazom
                self.conn = sqlite3.connect('login_data.db')
                self.c = self.conn.cursor()

                # Proveri da li username već postoji u bazi
                self.c.execute('SELECT email FROM login_data WHERE username = ?', (self.username_login_entry.get(),))
                result = self.c.fetchone()  # Vrati prvi red rezultata (ako postoji)

                if result != self.email_login_entry.get():
                    self.error_message_email_login = Label(self.login_menu, text=error_message, background='#002D62', fg='red')
                    self.error_message_email_login.grid(row=row, column=0, padx=10, pady=5)

                # Zatvori konekciju sa bazom
                self.conn.commit()
                self.conn.close()


    '''PROVERA DA LI SE EMAIL I SIFRA PODUDARAJU - LOGIN PROZOR'''
    def check_password_login(self, error_message, row, field):
        if hasattr(self, 'error_message_password_login') and field == 'password':
            self.error_message_password_login.destroy()

        if field == 'password' and error_message:
            # Kreiraj vezu sa bazom
                self.conn = sqlite3.connect('login_data.db')
                self.c = self.conn.cursor()

                # Proveri da li username već postoji u bazi
                self.c.execute('SELECT password FROM login_data WHERE email = ?', (self.email_login_entry.get(),))
                result = self.c.fetchone()  # Vrati prvi red rezultata (ako postoji)

                if result != self.password_login_entry.get():
                    self.error_message_password_login = Label(self.login_menu, text=error_message, background='#002D62', fg='red')
                    self.error_message_password_login.grid(row=row, column=0, padx=10, pady=5)

                # Zatvori konekciju sa bazom
                self.conn.commit()
                self.conn.close()



    '''MALE FUNKCIJE POTREBNE ZA KOD'''
    # ove dve funckije ispod sluze za prikazivanje i sakrivanje sifre kod register prozora   
    def show_register(self):
        self.password_register_entry.configure(show='')
        self.show_password_register.configure(command=self.hide_register, text='sakrij sifru')

    def hide_register(self):
        self.password_register_entry.configure(show='*')
        self.show_password_register.configure(command=self.show_register, text='prikazi sifru')

    # ove dve funckije ispod sluze za prikazivanje i sakrivanje sifre kod lo0gin prozora   
    def show_login(self):
        self.password_login_entry.configure(show='')
        self.show_password_login.configure(command=self.hide_login, text='sakrij sifru')

    def hide_login(self):
        self.password_login_entry.configure(show='*')
        self.show_password_login.configure(command=self.show_login, text='prikazi sifru')

    # ova funkcija je napravljena da kada zatvorim neki prozor, da on zatvori i root fajl
    def on_closing(self):
        self.root.destroy()


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()        