import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db=db
        self.viwe_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X )
        self.add_img = tk.PhotoImage(file='./img/add.png')
        
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)
        
        # Добавим таблицу данных
        self.tree = ttk.Treeview(self, columns=('ID', 'FIO', 'tel', 'email', 'zpl'),height=45, show='headings')
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("FIO", width=250, anchor=tk.CENTER)
        self.tree.column("tel", width=120, anchor=tk.CENTER)
        self.tree.column("email", width=120, anchor=tk.CENTER)
        self.tree.column("zpl", width=120, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("FIO", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("zpl", text='Зарплата')

        self.tree.pack(side=tk.LEFT)
       
        # Добавим кнопку редактировать на панель инструментов
        self.update_img = tk.PhotoImage(file='./img/update.png')
        button_update_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        button_update_dialog.pack(side=tk.LEFT)
        #Кнопка удаления
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        button_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_records)
        button_delete.pack(side=tk.LEFT)

        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        button_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        button_search.pack(side=tk.LEFT)




    # вызов дочернего окна
    def open_dialog (self):
        Child()

    #добавляем новую запись в дочернее окно
    def records(self, FIO, tel, email, zpl):
        self.db.insert_data(FIO, tel, email, zpl)
        self.viwe_records()
       
    # просмотр записей базы данных в главном окне
    def viwe_records(self):
        self.db.cursor.execute('SELECT * FROM db')
        [self.tree.delete(i)  for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]
        
    
    #метод открытия  обновления записи
    def open_update_dialog(self):
        update()

    def update_records(self, FIO, tel, email, zpl):
       self.db.cursor.execute('''UPDATE db SET FIO=?,tel=?, email=?, zpl=? WHERE id=?''', (FIO, tel, email, zpl, self.tree.set(self.tree.selection() [0], '#1'))) 
       self.db.conn.commit()
       self.viwe_records()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('DELETE FROM db WHERE id=?', (self.tree.set(selection_item, '#1')))
        self.db.conn.commit()
        self.viwe_records()

    # вызов окна поиска
    def open_search_dialog(self):
        Search()

    def search_records(self, name):
        name = ('%'+name+'%')
        self.db.cursor.execute('SELECT * FROM db WHERE FIO LIKE ?', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]
        
        

class Child (tk.Toplevel):
    def __init__(self):
        super().__init__(root)        
        self.init_chaild()
        self.view = app

    def init_chaild(self):
        self.title('Добавить нового сотрудника' )
        self.geometry('400x220')
        self.resizable (False, False)
        
        self.grab_set()
        self.focus_set()
        # имена полей ввода
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=10, y=20)
        label_tel = tk.Label(self, text = 'Телефон:')
        label_tel.place(x=10, y=50)
        ladel_email = tk.Label(self, text='E-mail:')
        ladel_email.place(x=10, y=80)
        ladel_zpl = tk.Label(self, text='Зарплата:')
        ladel_zpl.place(x=10, y=110)
        # поля ввода данных
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=80, y=20)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=80, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=80, y=80)
        self.entry_zpl = ttk.Entry(self)
        self.entry_zpl.place(x=80, y=110)
        
        # кнопки таблицы
        self.btn_cansel=ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cansel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)

        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_tel.get(),
                                           self.entry_email.get(),
                                           self.entry_zpl.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')
        
        

class update(Child):
    def __init__(self):
        super().__init__()        
        self.init_edit()
        self.view = app
        self.db=db
        self.default_data()
    
    
    def init_edit(self):
        self.title('Редактировать сотрудника')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind("<Button-1>", lambda event:
                      self.view.update_records(self.entry_name.get(), self.entry_tel.get(), self.entry_email.get(), self.entry_zpl.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cursor.execute('SELECT * FROM db WHERE id=?', self.view.tree.set(self.view.tree.selection() [0], '#1'))
        row = self.db.cursor.fetchall()
        self.entry_name.insert(0, row[0][1])
        self.entry_tel.insert(0, row[0][2])
        self.entry_email.insert(0, row[0][3])
        self.entry_zpl.insert(0, row[0][4])

# класс для поиска в базе
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view=app

    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x150')
        self.resizable(False,False)

        label_search = tk.Label(self, text='Сотрудник:')
        label_search.place(x=30,y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=120, y=20, width=150)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=80)
        btn_search.bind('<Button-1>', lambda event: 
                        self.view.search_records(self.entry_search.get()))

        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_cancel = ttk.Button(self, text='Закрыть')
        btn_cancel.place(x=185, y=80)
        btn_cancel.bind('<Button-1>', lambda event: self.destroy())


# Создаем базу данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db') 
        self.cursor = self.conn.cursor() 
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FIO TEXT,
            tel TEXT,
            email TEXT,
            zpl TEXT
            )'''
        ) 
        self.conn.commit()
    #Ввод данных в таблицу
    def insert_data(self, FIO, tel, email, zpl ):
        self.cursor.execute(
            '''INSERT INTO db(FIO, tel, email, zpl) VALUES(?,?,?,?)''', (FIO, tel, email, zpl)
        )
        self.conn.commit()

if __name__ =='__main__':
    db = DB()
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()