import tkinter as tk
from tkinter import ttk
import sqlite3



# создание основного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # хранение и инициализации объектов графического интерфейса
    def init_main(self):
        # создание панели инструментов
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        # создание кнопки добавления
        btn_open_dialogue = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img, command=self.open_dialogue)
        # упаковка и выравнивание по левому краю
        btn_open_dialogue.pack(side=tk.LEFT)

        # создание кнопки изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialogue = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                    image=self.update_img, command=self.open_refresh_dialogue)
        btn_edit_dialogue.pack(side=tk.LEFT)

        # создание кнопки удаления записи
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img, command=self.open_search_dialogue )
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Добавляем Treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'),
                                 height=45, show='headings')
        
        # параметры столбцов
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        # подписи столбцов
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("salary", text='Зарплата')

        # упаковка
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # добавление данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # обновление данных
    def refresh_record(self, name, phone, email, salary):
        self.db.c.execute('''UPDATE db SET name=?, phone=?, email=?, salary=? WHERE ID=?''',
                          (name, phone, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # вывод данных в виджет таблицы
    def view_records(self):
        # выбираем информацию из БД
        self.db.c.execute('''SELECT * FROM db''')
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]
        
    # удаление записей
    def delete_records(self):
        # цикл по выбранным записям
        for selection_item in self.tree.selection():
            # удаление из БД
            self.db.c.execute('''DELETE FROM db WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        # сохранение изменений в БД
        self.db.conn.commit()
        # обновление виджета таблицы
        self.view_records()

    # поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    # метод - вызов дочернего окна
    def open_dialogue(self):
        Child()

    # метод - вызов окна для изменения данных
    def open_refresh_dialogue(self):
        Refresh()

    # метод - вызов окна для поиска
    def open_search_dialogue(self):
        Search()

# класс дочерних окон
# Toplevel - окно верхнего уровня
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # заголовок окна
        self.title('Добавить')
        # размер окна
        self.geometry('230x174')
        # запрет на изменение размеров окна
        self.resizable(False, False)

        # перехватываем все события в приложении
        self.grab_set()
        # захватываем фокус
        self.focus_set()

        # названия строк
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=7, y=10)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=7, y=40)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=7, y=70)
        label_pay = tk.Label(self, text='Зарплата')
        label_pay.place(x=7, y=100)

        # строка ввода наименования
        self.entry_name = ttk.Entry(self)
        # устанавливаем ей координаты
        self.entry_name.place(x=94, y=10)

        # строка ввода телефона
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=94, y=40)

        # строка ввода email
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=94, y=70)

        # строка ввода зарплаты
        self.entry_wage = ttk.Entry(self)
        self.entry_wage.place(x=94, y=100)

        # кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=77, y=140)
        # срабатывание по ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаюся значения из строк ввода
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_phone.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_wage.get()))
    

# класс окна для обновления
class Refresh(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=70, y=140)
        btn_edit.bind('<Button-1>', lambda event: self.view.refresh_record(self.entry_name.get(),
                                                                          self.entry_phone.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_wage.get()))

# обращаемся к базе данных для получения данных об ID записи, соответствующей выбранному элементу дерева.
    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        # получаем доступ к первой записи из выборки
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_wage.insert(0, row[4])


# класс поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('230x94')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=10, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=60, y=20, width=150)


        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=77, y=60)
        btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')


# класс БД
class Database:
    def __init__(self):
        #соединение с БД
        self.conn = sqlite3.connect('db.db')
        # создание объекта класса cursor, используемый для взаимодействия с БД
        self.c = self.conn.cursor()
        # выполнение запроса к БД
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS db (id integer primary key, name text, phone text, email text, salary text)''')
        # сохранение изменений БД
        self.conn.commit()

    # метод добавления в БД
    def insert_data(self, name, tel, email, salary):
        self.c.execute('''INSERT INTO db (name, phone, email, salary) VALUES (?, ?, ?, ?)''',
                       (name, tel, email,salary))
        self.conn.commit()




if __name__ == '__main__':
    root = tk.Tk()
    # экземпляр класса Database
    db = Database()
    app = Main(root)
    app.pack()
    # заголовок окна
    root.title('Список сотрудников компании')
    # размер окна
    root.geometry('800x600')
    # запрет на изменение размеров окна
    root.resizable(False, False)
    root.mainloop()