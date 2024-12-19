import json
import tkinter as tk
import PIL
from pathlib import Path
from tkinter import messagebox, ttk, simpledialog, filedialog, Scrollbar
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from database import Database
from PIL import Image, ImageTk

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.db_file = "database.json"
        self.current_user = None
        self.week_type = "Четная"
        self.root.title("Компас")
        root.geometry("1280x832")
        root.configure(bg="#75DDE0")
        self.root.resizable(False, False)
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(r"C:\Users\user\PycharmProjects\курсач сан\.venv\images")
        self.relative_to_assets = lambda path: self.ASSETS_PATH / Path(path)
        root.icon = Image.open("image_2.png")  # Открываем изображение
        root.icon = root.icon.resize((64, 64))  # Уменьшаем размер (по желанию)
        root.icon = ImageTk.PhotoImage(root.icon)  # Конвертация в поддерживаемый формат
        root.tk.call('wm', 'iconphoto', root._w, root.icon)

        self.canvas = Canvas(root, bg="#F0F0F0")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.create_login_window()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_window(self):
        self.clear_window()
        self.canvas = Canvas(self.root,bg="#75DDE0",height=832,width=1280,bd=0,highlightthickness=0,relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0.0,0.0,1280.0,69.0,fill="#FFFFFF", outline="")
        self.canvas.create_text(545.0,189.0,anchor="nw",text="Вход",fill="#FFFFFF",font=("UNCAGE Regular", 64 * -1, "bold"))
        self.canvas.create_rectangle(409, 467, 866, 472, fill="#000000", outline="")
        self.canvas.create_rectangle(409, 390, 866, 395, fill="#000000", outline="")
        self.canvas.create_text(416.0,351.0,anchor="nw",text="Логин:",fill="#000000",font=("AA Stetica Regular", 28 * -1),)
        self.canvas.create_text(416.0,427.0,anchor="nw",text="Пароль:",fill="#000000",font=("AA Stetica Regular", 28 * -1),)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = self.canvas.create_image(637.0, 508.0, image=self.button_image_1, anchor="center")
        self.canvas.tag_bind(self.button_1, "<Button-1>", lambda e: self.create_register_window())  # Привязка клика
        self.canvas.tag_bind(self.button_1, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))  # Курсор "рука"
        self.canvas.tag_bind(self.button_1, "<Leave>", lambda e: self.canvas.config(cursor=""))  # Сброс курсора

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = self.canvas.create_image(640.0, 602.0, image=self.button_image_2,anchor="center")  # Создание изображения
        self.canvas.tag_bind(self.button_2, "<Button-1>", lambda e: self.login())  # Привязка клика
        self.canvas.tag_bind(self.button_2, "<Enter>",lambda e: self.canvas.config(cursor="hand2"))  # Курсор "рука" при наведении
        self.canvas.tag_bind(self.button_2, "<Leave>", lambda e: self.canvas.config(cursor=""))  # Сброс курсора

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(686.0, 363.5, image=self.entry_image_1)
        self.username_entry = Entry(self.root, bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 18))
        self.username_entry.place(x=506.0, y=350.0, width=360.0, height=37.0)
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(704.0, 439.5, image=self.entry_image_2)
        self.password_entry = Entry(self.root, bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, show="*", font=("AA Stetica Regular", 18))
        self.password_entry.place(x=528.0, y=426.0, width=360.0, height=37.0)
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(100.0, 38.0, image=self.image_1)
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(1218.0, 761.0, image=self.image_2)
        self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(1051.0, 656.0, image=self.image_3)
        self.image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(115.0, 628.9, image=self.image_4)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.db.check_login(username, password)
        if user:
            self.current_user = user
            self.create_dashboard()
        else:
            messagebox.showerror("Ошибка", "Неверные данные")

    def create_register_window(self):
        self.clear_window()
        self.canvas = Canvas(self.root, bg="#75DDE0", height=832, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 832.0, fill="#75DDE0", outline="")
        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 69.0, fill="#FFFFFF", outline="")
        self.canvas.create_text(380.0,140.0,anchor="nw",text="Регистрация",fill="#FFFFFF",font=("UNCAGE Regular", 64 * -1))
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(100.0, 38.0, image=self.image_1)
        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(1218.0, 761.0, image=self.image_2)
        self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(1051.0, 656.0, image=self.image_3)
        self.image_4 = PhotoImage(file=self.relative_to_assets("image_4.png"))
        self.canvas.create_image(115.0, 628.9, image=self.image_4)

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat")
        self.button_1.place(x=430.0,y=603.0,width=390.0,height=80.0)
        self.canvas.create_text(489.0, 318.0, anchor="nw", text="Выберите роль:", fill="#000000",font=("Bombardier", 40 * -1))
        self.canvas.create_text(522.0,398.0, anchor="nw", text="Студент\n\nПреподаватель\n\nАдминистратор", fill="#000000", font=("AA Stetica Regular", 28 * -1))
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_7.png"))
        self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0, command=self.ssr, relief="flat")
        self.button_2.place(x=461.0,y=393.0,width=37.0,height=43.0)
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_8.png"))
        self.button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, command=self.ster, relief="flat")
        self.button_3.place(x=461.0,y=451.0,width=39.0,height=44.0)
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0, command=self.sar, relief="flat")
        self.button_4.place(x=460.0,y=510.0,width=39.0,height=37.0)

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_5 = Button(image=self.button_image_5, borderwidth=0, highlightthickness=0,command=self.create_login_window, relief="flat")
        self.button_5.place(x=0.0, y=101.0, width=141.0, height=133.0)

    def destroy_buttons(self):
        """Удаляет все элементы интерфейса, кроме изображений и фигур на Canvas"""
        for widget in self.root.winfo_children():
            if isinstance(widget, Canvas):
                # Удаляем все элементы Canvas, кроме изображений и фигур
                for item in widget.find_all():
                    item_type = widget.type(item)
                    if item_type not in ["image", "rectangle", "line", "oval", "arc", "polygon"]:
                        widget.delete(item)
            elif widget != self.canvas:  # Сохраняем сам Canvas
                widget.destroy()

    def ssr(self):
        self.clear_window()
        self.create_register_window()
        self.destroy_buttons()

        self.canvas.create_text(380.0,140.0,anchor="nw",text="Регистрация",fill="#FFFFFF",font=("UNCAGE Regular", 64 * -1))
        self.canvas.create_text(395.0,243.0,anchor="nw",text="ФИО:",fill="#000000",font=("AA Stetica Regular", 28 * -1))
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(661.5, 253.5, image=self.entry_image_1)
        real_name_entry = Entry(bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 18))
        real_name_entry.place(x=478.0, y=240.0, width=373.0, height=37.0)
        self.canvas.create_text(398.0,315.0,anchor="nw",text="Логин:",fill="#000000",font=("AA Stetica Regular", 28 * -1))
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(666.5, 326.5, image=self.entry_image_2)
        username_entry = Entry(bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 18))
        username_entry.place(x=488.0, y=313.0, width=363.0, height=37.0)
        self.canvas.create_text(397.0,392.0,anchor="nw",text="Пароль:",fill="#000000",font=("AA Stetica Regular", 28 * -1))
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(680.5, 400.5, image=self.entry_image_3)
        password_entry = Entry(bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, show="*", font=("AA Stetica Regular", 18))
        password_entry.place(x=510.0, y=390.0, width=345.0, height=37.0)
        self.canvas.create_rectangle(392.0, 427.0, 847.0, 431.0, fill="#000000", outline="")
        self.canvas.create_rectangle(391.0, 354.0, 848.0, 359.0, fill="#000000", outline="")
        self.canvas.create_rectangle(393.0, 282.0, 850.0, 287.0, fill="#000000", outline="")

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_5 = Button(image=self.button_image_5, borderwidth=0, highlightthickness=0,command=self.create_login_window, relief="flat", cursor="hand2")
        self.button_5.place(x=0.0, y=101.0, width=141.0, height=133.0)

        # Поле для группы студента
        self.canvas.create_text(480.0,484.0,anchor="nw",text="Введите вашу группу:",fill="#000000",font=("AA Stetica Regular", 28 * -1))
        self.entry_image_11 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(625.0, 560.0, image=self.entry_image_11)
        group_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 16))
        group_entry.place(x=475.0, y=534.0, width=270.0, height=50.0)

        def submit_student():
            if not real_name_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле ФИО не может быть пустым!")
                return
            if not username_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле Логин не может быть пустым!")
                return
            if not password_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле Пароль не может быть пустым!")
                return
            if not group_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле ввода группы не может быть пустым!")
                return
            if not group_entry.get():
                messagebox.showerror("Ошибка", "Заполните все данные!")
                return
            self.db.insert_user(username=username_entry.get(),real_name=real_name_entry.get(),password=password_entry.get(),role="Студент",group_name=group_entry.get())
            messagebox.showinfo("Успех", "Студент зарегистрирован!")
            self.create_login_window()

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat", command = submit_student, cursor="hand2")
        self.button_1.place(x=430.0, y=630.0, width=390.0, height=80.0)

    def ster(self):
        self.clear_window()
        self.create_register_window()
        self.destroy_buttons()

        # Основные элементы первого этапа регистрации
        self.canvas.create_text(380.0, 140.0, anchor="nw", text="Регистрация", fill="#FFFFFF",
                                font=("UNCAGE Regular", 64 * -1))
        self.canvas.create_text(395.0, 243.0, anchor="nw", text="ФИО:", fill="#000000",
                                font=("AA Stetica Regular", 28 * -1))
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(661.5, 253.5, image=self.entry_image_1)
        self.real_name_entry = Entry(self.root, bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0,
                                     font=("AA Stetica Regular", 18))
        self.real_name_entry.place(x=478.0, y=240.0, width=373.0, height=37.0)

        self.canvas.create_text(398.0, 315.0, anchor="nw", text="Логин:", fill="#000000",
                                font=("AA Stetica Regular", 28 * -1))
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(666.5, 326.5, image=self.entry_image_2)
        self.username_entry = Entry(self.root, bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0,
                                    font=("AA Stetica Regular", 18))
        self.username_entry.place(x=488.0, y=313.0, width=363.0, height=37.0)

        self.canvas.create_text(397.0, 392.0, anchor="nw", text="Пароль:", fill="#000000",
                                font=("AA Stetica Regular", 28 * -1))
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(680.5, 400.5, image=self.entry_image_3)
        self.password_entry = Entry(self.root, bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, show="*",
                                    font=("AA Stetica Regular", 18))
        self.password_entry.place(x=510.0, y=390.0, width=345.0, height=37.0)

        self.canvas.create_rectangle(392.0, 427.0, 847.0, 431.0, fill="#000000", outline="")
        self.canvas.create_rectangle(391.0, 354.0, 848.0, 359.0, fill="#000000", outline="")
        self.canvas.create_rectangle(393.0, 282.0, 850.0, 287.0, fill="#000000", outline="")

        self.canvas.create_text(480.0, 484.0, anchor="nw", text="Введите код доступа:", fill="#000000",
                                font=("AA Stetica Regular", 28 * -1))
        self.entry_image_11 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(625.0, 560.0, image=self.entry_image_11)
        self.code_entry = Entry(self.root, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0,
                                font=("AA Stetica Regular", 16))
        self.code_entry.place(x=475.0, y=534.0, width=270.0, height=50.0)

        # Кнопка для перехода ко второму этапу (выбор предметов)
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_1 = Button(self.root, image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat",
                               command=self.subject_choice)
        self.button_1.place(x=430.0, y=630.0, width=390.0, height=80.0)

    def subject_choice(self):
        # Окно для выбора предметов
        self.subject_window = tk.Toplevel(self.root)
        self.subject_window.title("Выбор предметов")
        self.subject_window.geometry("500x400")

        self.canvas2 = tk.Canvas(self.subject_window, bg="#FFFFFF", height=400, width=500)
        self.canvas2.pack(fill="both", expand=True)

        self.canvas2.create_text(115.0, 30.0, anchor="nw", text="Выберите предметы:", fill="#000000",
                                 font=("AA Stetica Regular", 28 * -1))

        subject_frame = tk.Frame(self.subject_window, bg="#FFFFFF")
        subject_frame.place(x=50.0, y=70.0, width=400.0, height=200.0)

        self.subject_listbox = tk.Listbox(subject_frame, selectmode="multiple", bg="#FFFFFF", fg="#000000")
        self.subject_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Добавление предметов в список
        for subject in self.db.data["subjects"]:
            self.subject_listbox.insert(tk.END, subject["name"])

        # Кнопка для подтверждения выбора
        submit_button = Button(self.subject_window, text="Выбрать", bg="#FFFFFF", fg="#000716",
                               font=("AA Stetica Regular", 18), command=self.submit_teacher)
        submit_button.place(x=150.0, y=300.0, width=200.0, height=40.0)

    def submit_teacher(self):
        # Проверка на пустые поля
        if not self.real_name_entry.get().strip():
            messagebox.showerror("Ошибка", "Поле ФИО не может быть пустым!")
            return
        if not self.username_entry.get().strip():
            messagebox.showerror("Ошибка", "Поле Логин не может быть пустым!")
            return
        if not self.password_entry.get().strip():
            messagebox.showerror("Ошибка", "Поле Пароль не может быть пустым!")
            return
        if not self.code_entry.get().strip():
            messagebox.showerror("Ошибка", "Поле Код доступа не может быть пустым!")
            return
        if not self.subject_listbox.curselection():
            messagebox.showerror("Ошибка", "Выберите хотя бы один предмет!")
            return
        if self.code_entry.get() != "54321":
            messagebox.showerror("Ошибка", "Неверный код доступа!")
            return

        # Сохранение выбранных предметов
        selected_subjects = [self.subject_listbox.get(i) for i in self.subject_listbox.curselection()]

        # Добавление преподавателя в базу данных
        self.db.insert_user(username=self.username_entry.get(), real_name=self.real_name_entry.get(),
                            password=self.password_entry.get(), role="Преподаватель", subjects=selected_subjects)

        messagebox.showinfo("Успех", "Преподаватель зарегистрирован!")
        self.create_login_window()

    def sar(self):
        self.clear_window()
        self.create_register_window()
        self.destroy_buttons()

        self.canvas.create_text(380.0, 140.0, anchor="nw", text="Регистрация", fill="#FFFFFF",
                                font=("UNCAGE Regular", 64 * -1))
        self.canvas.create_text(395.0, 243.0, anchor="nw", text="ФИО:", fill="#000000",
                                font=("AA Stetica Regular", 28 * -1))
        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(661.5, 253.5, image=self.entry_image_1)
        real_name_entry = Entry(bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 18))
        real_name_entry.place(x=478.0, y=240.0, width=373.0, height=37.0)
        self.canvas.create_text(398.0, 315.0, anchor="nw", text="Логин:", fill="#000000",
                                font=("AA Stetica Regular", 28 * -1))
        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(666.5, 326.5, image=self.entry_image_2)
        username_entry = Entry(bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 18))
        username_entry.place(x=488.0, y=313.0, width=363.0, height=37.0)
        self.canvas.create_text(397.0, 392.0, anchor="nw", text="Пароль:", fill="#000000",
                                font=("AA Stetica Regular", 28 * -1))
        self.entry_image_3 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        self.canvas.create_image(680.5, 400.5, image=self.entry_image_3)
        password_entry = Entry(bd=0, bg="#75DDE0", fg="#000716", highlightthickness=0, show="*",
                               font=("AA Stetica Regular", 18))
        password_entry.place(x=510.0, y=390.0, width=345.0, height=37.0)
        self.canvas.create_rectangle(392.0, 427.0, 847.0, 431.0, fill="#000000", outline="")
        self.canvas.create_rectangle(391.0, 354.0, 848.0, 359.0, fill="#000000", outline="")
        self.canvas.create_rectangle(393.0, 282.0, 850.0, 287.0, fill="#000000", outline="")

        self.button_image_5 = PhotoImage(file=self.relative_to_assets("button_6.png"))
        self.button_5 = Button(image=self.button_image_5, borderwidth=0, highlightthickness=0,
                               command=self.create_login_window, relief="flat", cursor="hand2")
        self.button_5.place(x=0.0, y=101.0, width=141.0, height=133.0)

        self.canvas.create_text(480.0, 484.0, anchor="nw", text="Введите код доступа:", fill="#000000",font=("AA Stetica Regular", 28 * -1))
        self.entry_image_11 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(625.0, 560.0, image=self.entry_image_11)
        code_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 16))
        code_entry.place(x=475.0, y=534.0, width=270.0, height=50.0)

        def submit_admin():
            if not real_name_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле ФИО не может быть пустым!")
                return
            if not username_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле Логин не может быть пустым!")
                return
            if not password_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле Пароль не может быть пустым!")
                return
            if not code_entry.get().strip():
                messagebox.showerror("Ошибка", "Поле Код доступа не может быть пустым!")
                return
            if code_entry.get() != "12345":
                messagebox.showerror("Ошибка", "Неверный код администратора!")
                return

            self.db.insert_user(username=username_entry.get(),real_name=real_name_entry.get(),password=password_entry.get(),role="Администратор")
            messagebox.showinfo("Успех", "Администратор зарегистрирован!")
            self.create_login_window()

        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, relief="flat",
                               command=submit_admin, cursor="hand2")
        self.button_1.place(x=430.0, y=630.0, width=390.0, height=80.0)

    def create_dashboard(self):
        self.clear_window()
        self.canvas = Canvas(self.root, bg="#FFFFFF", height=832, width=1280, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_5.png"))
        self.canvas.create_image(617.0, 453.0, image=self.image_image_1)
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_6.png"))
        self.canvas.create_image(647.0, 441.0, image=self.image_image_2)
        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 69.0, fill="#75DDE0", outline="")
        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_7.png"))
        self.canvas.create_image(100.0, 38.0, image=self.image_image_3)
        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(1218.0, 761.0, image=self.image_image_4)

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        self.button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0,command=self.open_user_profile, relief="flat")
        self.button_3.place(x=1193.0, y=6.0, width=60.0, height=57.0)
        self.canvas.create_text(300.0,362.0,anchor="nw",text=f"Добро пожаловать, {self.current_user['real_name']}!",fill="#000000",font=("Bombardier", 48 * -1))
        if self.current_user["role"] == "Студент":
            self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_9.png"))
            self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0, command=self.view_schedule, relief="flat")
            self.button_1.place(x=419.0, y=463.0, width=427.0, height=50.0)
            self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_10.png"))
            self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0,command=self.create_login_window, relief="flat")
            self.button_2.place(x=570.0, y=521.0, width=125.0, height=30.0)
        elif self.current_user["role"] == "Преподаватель":
            self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_9.png"))
            self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0,text="Просмотреть расписание", command=self.view_schedule, relief="flat")
            self.button_1.place(x=426.0, y=444.0, width=404.0, height=44.0)
            self.button_image_333 = PhotoImage(file=self.relative_to_assets("button_16.png"))
            self.button_333 = Button(image=self.button_image_333, borderwidth=0, highlightthickness=0, text="Расписание групп", command=self.view_assigned_groups_schedule, relief="flat")
            self.button_333.place(x=478.0, y=498.0, width=315.0, height=47.0)
            self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_17.png"))
            self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0,command=self.create_login_window, relief="flat")
            self.button_2.place(x = 548.0, y = 551.0, width = 164.0, height = 40.0)
        elif self.current_user["role"] == "Администратор":
            self.button_image_33 = PhotoImage(file=self.relative_to_assets("button_12.png"))
            self.button_33 = Button(image=self.button_image_33, borderwidth=0, highlightthickness=0,text= "Генерация расписания",command=self.db.generate_schedule_for_all_users, relief="flat")
            self.button_33.place(x=434.0, y=443.0, width=389.0, height=48.0)
            self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_13.png"))
            self.button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0,text="Добавление предмета", command=self.open_add_subject_window, relief="flat")
            self.button_4.place(x=443.0, y=498.0, width=375.0, height=43.0)
            self.button_image_6 = PhotoImage(file=self.relative_to_assets("button_15.png"))
            self.button_6 = Button(image=self.button_image_6, borderwidth=0, highlightthickness=0, command=self.edit_schedule, relief="flat")
            self.button_6.place(x = 405.0, y = 545.0, width = 450.0, height = 47.0)
            self.button_image_7 = PhotoImage(file=self.relative_to_assets("button_14.png"))
            self.button_7 = Button(image=self.button_image_7, borderwidth=0, highlightthickness=0, command=self.db.export_schedule_to_excel,relief="flat")
            self.button_7.place(x=427.0, y=600.0, width=424.0, height=44.0)
            self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_10.png"))
            self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0,command=self.create_login_window, relief="flat")
            self.button_2.place(x=564.0,y=649.0,width=141.0,height=52.0)

    def view_schedule(self):
        self.clear_window()

        header_canvas = Canvas(self.root, bg="#FFFFFF", height=69, width=1280, bd=0, highlightthickness=0,relief="ridge")
        header_canvas.pack(side="top", fill="x")
        header_canvas.create_rectangle(0.0, 0.0, 1280.0, 69.0, fill="#75DDE0", outline="")

        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0,command=self.open_user_profile, relief="flat")
        button_3.place(x=1193.0, y=6.0, width=60.0, height=57.0)

        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_25.png"))
        button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0, command=self.reate_dashboard, relief="flat")
        button_4.place(x=0.0, y=0.0, width=241.0, height=69.0)

        scroll_canvas = tk.Canvas(self.root, bg="#75DDE0", highlightthickness=0, bd=0)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scroll_frame = tk.Frame(scroll_canvas, bg="#75DDE0", highlightthickness=0, bd=0)
        scroll_bar = tk.Scrollbar(self.root, orient="vertical", command=scroll_canvas.yview)
        scroll_bar.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=scroll_bar.set)
        scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        def update_scroll_region(event):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        self.scroll_frame.bind("<Configure>", update_scroll_region)
        def on_mouse_scroll(event):
            scroll_canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        scroll_canvas.bind_all("<MouseWheel>", on_mouse_scroll)
        def update_schedule():
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            root.focus()
            selected_week_type = week_type_var.get()
            schedule = [
                entry for entry in self.db.get_schedule()
                if entry["week_type"] == selected_week_type and (
                        (self.current_user["role"] == "Студент" and entry["group_name"] == self.current_user[
                            "group_name"]) or
                        (self.current_user["role"] == "Преподаватель" and entry["subject_name"] in self.current_user[
                            "subjects"]) or
                        self.current_user["role"] == "Администратор")]

            if not schedule:
                tk.Label(self.scroll_frame, text="Нет данных для отображения.", font=("AA Stetica Regular", 16)).pack(pady=10)
                return

            grouped_schedule = {}
            for entry in schedule:
                day = entry["day_of_week"]
                if day not in grouped_schedule:
                    grouped_schedule[day] = []
                grouped_schedule[day].append(entry)

            for day in grouped_schedule:
                grouped_schedule[day].sort(key=lambda entry: entry["time"])

            colors = {"Понедельник": "#FFFFFF","Вторник": "#FFFFFF","Среда": "#FFFFFF","Четверг": "#FFFFFF","Пятница": "#FFFFFF","Суббота": "#FFFFFF",}

            for day, entries in grouped_schedule.items():
                day_frame = tk.Frame(self.scroll_frame, bg=colors.get(day, "#FFFFFF"), pady=5, padx=5)
                day_frame.pack(fill="x", pady=5)
                tk.Label(day_frame, text=f"{day}", font=("AA Stetica Regular", 16, "bold"),
                         bg=colors.get(day, "#FFFFFF", )).pack(
                    anchor="w", pady=2)
                for entry in entries:
                    row_frame = tk.Frame(day_frame, bg=colors.get(day, "#FFFFFF"), pady=2, padx=5)
                    row_frame.pack(fill="x", pady=1)

                    teacher_real_name = next(
                        (user["real_name"] for user in self.db.data["users"]
                         if user.get("role") == "Преподаватель" and user["username"] == entry["teacher_name"]),
                        entry["teacher_name"])

                    tk.Label(row_frame,
                             text=f"{entry['time']} — {entry['subject_name']} (Преподаватель: {teacher_real_name}, "f"Аудитория: {entry['classroom']})",font=("AA Stetica Regular", 10), fg="black", bg=colors.get(day, "#FFFFFF")).pack(side="left",anchor="w")

        tk.Label(self.root, text="Выберите тип недели:", bg="#75DDE0", font=("AA Stetica Regular", 14)).pack(pady=5, padx=180)
        week_type_var = tk.StringVar(value="Четная")
        week_type_dropdown = ttk.Combobox(self.root, font=("AA Stetica Regular", 12), textvariable=week_type_var,values=["Четная", "Нечетная"], state="readonly")
        week_type_dropdown.pack(pady=5, padx=20)
        week_type_dropdown.bind("<<ComboboxSelected>>", lambda event: root.focus())

        tk.Button(self.root, text="Обновить", bg="#FFFFFF", font=("AA Stetica Regular", 12),command=update_schedule).pack(pady=5, padx=30)

        tk.Button(self.root, text="Назад", bg="#FFFFFF", font=("AA Stetica Regular", 12),command=self.create_dashboard).pack(pady=5, padx=30)

        update_schedule()

    def view_assigned_groups_schedule(self):
        if self.current_user["role"] != "Преподаватель":
            messagebox.showerror("Ошибка", "Недостаточно прав.")
            return

        self.clear_window()

        header_canvas = Canvas(self.root, bg="#FFFFFF", height=69, width=1280, bd=0, highlightthickness=0,
                               relief="ridge")
        header_canvas.pack(side="top", fill="x")
        header_canvas.create_rectangle(0.0, 0.0, 1280.0, 69.0, fill="#75DDE0", outline="")

        # Кнопка 1
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_3 clicked"), relief="flat")
        button_3.place(x=1193.0, y=6.0, width=60.0, height=57.0)

        # Кнопка 2
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_25.png"))
        button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_4 clicked"), relief="flat")
        button_4.place(x=0.0, y=0.0, width=241.0, height=69.0)

        teacher_id = self.current_user["id"]
        assigned_groups = set(
            entry["group_name"] for entry in self.db.data["schedule"] if entry["teacher_id"] == teacher_id)

        if not assigned_groups:
            tk.Label(self.root, text="Нет привязанных групп.", font=("Arial", 14)).pack(pady=10)
            tk.Button(self.root, text="Назад", command=self.create_dashboard).pack(pady=10)
            return

        scroll_canvas = tk.Canvas(self.root, bg="#75DDE0", highlightthickness=0, bd=0)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scroll_frame = tk.Frame(scroll_canvas, bg="#75DDE0", highlightthickness=0, bd=0)
        scroll_bar = tk.Scrollbar(self.root, orient="vertical", command=scroll_canvas.yview)
        scroll_bar.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=scroll_bar.set)
        scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        def update_scroll_region(event):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

        self.scroll_frame.bind("<Configure>", update_scroll_region)

        def on_mouse_scroll(event):
            scroll_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        scroll_canvas.bind_all("<MouseWheel>", on_mouse_scroll)

        def update_schedule():
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
            selected_week_type = week_type_var.get()
            selected_group = group_var.get()
            root.focus()

            schedule = [
                entry for entry in self.db.data["schedule"]
                if entry["group_name"] == selected_group and entry["week_type"] == selected_week_type
            ]

            if not schedule:
                tk.Label(self.scroll_frame, text="Нет данных для отображения.", font=("Arial", 12)).pack(pady=10)
                return

            username_to_real_name = {
                user["username"]: user["real_name"]
                for user in self.db.data["users"]
                if user.get("role") == "Преподаватель"
            }

            grouped_schedule = {}
            for entry in schedule:
                day = entry["day_of_week"]
                if day not in grouped_schedule:
                    grouped_schedule[day] = []
                grouped_schedule[day].append(entry)

            colors = {
                "Понедельник": "#FFFFFF",
                "Вторник": "#FFFFFF",
                "Среда": "#FFFFFF",
                "Четверг": "#FFFFFF",
                "Пятница": "#FFFFFF",
                "Суббота": "#FFFFFF",
            }

            for day, entries in grouped_schedule.items():
                day_frame = tk.Frame(self.scroll_frame, bg=colors.get(day, "#FFFFFF"), pady=5, padx=5)
                day_frame.pack(fill="x", pady=5)

                day_label_text = f"{day} (дистанционно)" if day == "Суббота" else day
                tk.Label(day_frame, text=day_label_text, font=("Arial", 14, "bold"),
                         bg=colors.get(day, "#FFFFFF")).pack(anchor="w", pady=2)

                for entry in entries:
                    teacher_real_name = username_to_real_name.get(entry["teacher_name"], entry["teacher_name"])
                    classroom = entry.get("classroom", "Не указана")

                    tk.Label(
                        day_frame,
                        text=f"  {entry['time']} — {entry['subject_name']} (Преподаватель: {teacher_real_name}, Аудитория: {classroom})",
                        font=("Arial", 10),
                        fg="black",
                        bg=colors.get(day, "#FFFFFF"),
                    ).pack(anchor="w", pady=1)

        tk.Label(self.root, text="Выберите группу:",bg="#75DDE0", font=("AA Stetica Regular", 14)).pack(pady=5)
        group_var = tk.StringVar(value=list(assigned_groups)[0])
        group_dropdown = ttk.Combobox(self.root, textvariable=group_var, values=list(assigned_groups), state="readonly")
        group_dropdown.pack(pady=5)

        tk.Label(self.root, text="Выберите тип недели:", bg="#75DDE0", font=("AA Stetica Regular", 14)).pack(pady=5,
                                                                                                             padx=30)
        week_type_var = tk.StringVar(value="Четная")
        week_type_dropdown = ttk.Combobox(self.root, font=("AA Stetica Regular", 12), textvariable=week_type_var,
                                          values=["Четная", "Нечетная"], state="readonly")
        week_type_dropdown.pack(pady=5, padx=20)
        week_type_dropdown.bind("<<ComboboxSelected>>", lambda event: root.focus())

        tk.Button(self.root, text="Обновить расписание", bg="#FFFFFF", font=("AA Stetica Regular", 12),
                  command=update_schedule).pack(pady=15, padx=30)
        tk.Button(self.root, text="Назад", bg="#FFFFFF", font=("AA Stetica Regular", 12),
                  command=self.create_dashboard).pack(pady=5, padx=30)

        update_schedule()

    def edit_schedule(self):
        if self.current_user["role"] != "Администратор":
            messagebox.showerror("Ошибка", "Недостаточно прав.")
            return

        self.clear_window()
        header_canvas = Canvas(self.root, bg="#FFFFFF", height=69, width=1280, bd=0, highlightthickness=0,relief="ridge")
        header_canvas.pack(side="top", fill="x")
        header_canvas.create_rectangle(0.0, 0.0, 1280.0, 69.0, fill="#75DDE0", outline="")
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_11.png"))
        button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0,command=self.open_user_profile, relief="flat")
        button_3.place(x=1193.0, y=6.0, width=60.0, height=57.0)
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_25.png"))
        button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0, command=self.reate_dashboard, relief="flat")
        button_4.place(x=0.0, y=0.0, width=241.0, height=69.0)

        def update_group_options():
            if role_var.get() == "Студенты":
                # Сортировка групп по номеру и алфавиту
                groups = sorted(
                    set(entry["group_name"] for entry in self.db.data["schedule"]),
                    key=lambda x: (
                    int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else float('inf'), x)
                )
            else:
                # Сортировка преподавателей по алфавиту
                teachers = sorted(
                    user["real_name"] for user in self.db.data["users"] if user.get("role") == "Преподаватель"
                )
                groups = teachers

            group_var.set(groups[0] if groups else "")
            group_dropdown["values"] = groups

        scroll_canvas = tk.Canvas(self.root, bg="#75DDE0", highlightthickness=0, bd=0)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scroll_frame = tk.Frame(scroll_canvas, bg="#75DDE0", highlightthickness=0, bd=0)
        scroll_bar = tk.Scrollbar(self.root, orient="vertical", command=scroll_canvas.yview)
        scroll_bar.pack(side="right", fill="y")
        scroll_canvas.configure(yscrollcommand=scroll_bar.set)
        scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def update_scroll_region(event):
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        scroll_frame.bind("<Configure>", update_scroll_region)
        def on_mouse_scroll(event):
            scroll_canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        scroll_canvas.bind_all("<MouseWheel>", on_mouse_scroll)
        def update_schedule():
            for widget in scroll_frame.winfo_children():
                widget.destroy()
            selected_group = group_var.get()
            selected_week_type = week_type_var.get()
            selected_role = role_var.get()
            root.focus()

            teacher_real_names = {
                user["real_name"]: user["id"]
                for user in self.db.data["users"]
                if user.get("role") == "Преподаватель"
            }

            if selected_role == "Студенты":
                schedule = [
                    entry for entry in self.db.data["schedule"]
                    if entry["group_name"] == selected_group and entry["week_type"] == selected_week_type
                ]
            else:
                teacher_id = teacher_real_names.get(selected_group)
                schedule = [
                    entry for entry in self.db.data["schedule"]
                    if entry.get("teacher_id") == teacher_id and entry["week_type"] == selected_week_type
                ]

            if not schedule:
                tk.Label(scroll_frame, text="Нет данных для отображения.", font=("AA Stetica Regular", 16)).pack(pady=10)
                return

            grouped_schedule = {}
            for entry in schedule:
                day = entry["day_of_week"]
                if day not in grouped_schedule:
                    grouped_schedule[day] = []
                grouped_schedule[day].append(entry)

            for day in grouped_schedule:
                grouped_schedule[day].sort(key=lambda entry: entry["time"])

            colors = {
                "Понедельник": "#FFFFFF",
                "Вторник": "#FFFFFF",
                "Среда": "#FFFFFF",
                "Четверг": "#FFFFFF",
                "Пятница": "#FFFFFF",
                "Суббота": "#FFFFFF",
            }

            for day, entries in grouped_schedule.items():
                day_frame = tk.Frame(scroll_frame, bg=colors.get(day, "#FFFFFF"), pady=5, padx=5)
                day_frame.pack(fill="x", pady=5)
                tk.Label(day_frame, text=f"{day}", font=("AA Stetica Regular", 16, "bold"),
                         bg=colors.get(day, "#FFFFFF")).pack(
                    anchor="w", pady=2)
                for entry in entries:
                    row_frame = tk.Frame(day_frame, bg=colors.get(day, "#FFFFFF"), pady=2, padx=5)
                    row_frame.pack(fill="x", pady=1)

                    teacher_real_name = next(
                        (user["real_name"] for user in self.db.data["users"]
                         if user.get("role") == "Преподаватель" and user["username"] == entry["teacher_name"]),
                        entry["teacher_name"]
                    )

                    tk.Label(row_frame,
                             text=f"{entry['time']} — {entry['subject_name']} (Преподаватель: {teacher_real_name}, "
                                  f"Аудитория: {entry['classroom']})",
                             font=("AA Stetica Regular", 10), fg="black", bg=colors.get(day, "#FFFFFF")).pack(
                        side="left",
                        anchor="w")

                    tk.Button(row_frame, text="Редактировать", command=lambda e=entry: self.edit_entry_generic(e),
                              bg="#75DDE0").pack(side="right", padx=5)
                    tk.Button(row_frame, text="Удалить", command=lambda e=entry: self.delete_entry_generic(e),
                              bg="#75DDE0", fg="black").pack(side="right")

        tk.Label(self.root, text="Для кого расписание:", bg="#75DDE0", font=("AA Stetica Regular", 14)).pack(pady=5,padx=30)
        role_var = tk.StringVar(value="Студенты")
        role_dropdown = ttk.Combobox(self.root, font=("AA Stetica Regular", 12), textvariable=role_var,values=["Студенты", "Преподаватели"], state="readonly")
        role_dropdown.pack(pady=5, padx=20)
        role_dropdown.bind("<<ComboboxSelected>>", lambda event: root.focus())
        role_var.trace("w", lambda *args: update_group_options())
        tk.Label(self.root, text="Выберите группу или преподавателя:", bg="#75DDE0",font=("AA Stetica Regular", 14)).pack( pady=5, padx=30)
        groups = sorted(set(entry["group_name"] for entry in self.db.data["schedule"]),key=lambda x: (int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else float('inf'), x))
        group_var = tk.StringVar(value=groups[0] if groups else "")
        group_dropdown = ttk.Combobox(self.root, font=("AA Stetica Regular", 12), textvariable=group_var, values=groups,state="readonly")
        group_dropdown.pack(pady=5, padx=20)
        group_dropdown.bind("<<ComboboxSelected>>", lambda event: root.focus())
        tk.Label(self.root, text="Выберите тип недели:", bg="#75DDE0", font=("AA Stetica Regular", 14)).pack(pady=5,padx=30)
        week_type_var = tk.StringVar(value="Четная")
        week_type_dropdown = ttk.Combobox(self.root, font=("AA Stetica Regular", 12), textvariable=week_type_var, values=["Четная", "Нечетная"], state="readonly")
        week_type_dropdown.pack(pady=5, padx=20)
        week_type_dropdown.bind("<<ComboboxSelected>>", lambda event: root.focus())
        tk.Button(self.root, text="Обновить расписание", bg="#FFFFFF", font=("AA Stetica Regular", 12),command=update_schedule).pack(pady=15, padx=30)
        tk.Button(self.root, text="Назад", bg="#FFFFFF", font=("AA Stetica Regular", 12),command=self.create_dashboard).pack(pady=5, padx=30)

        update_schedule()

    def edit_entry_generic(self, entry):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование записи")
        edit_window.geometry("400x350")
        edit_window.configure(bg="#FFFFFF")
        tk.Label(edit_window, text="Время пары:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        time_var = tk.StringVar(value=entry["time"])
        ttk.Entry(edit_window, textvariable=time_var).pack(pady=5)

        tk.Label(edit_window, text="Название предмета:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        subject_var = tk.StringVar(value=entry["subject_name"])
        ttk.Entry(edit_window, textvariable=subject_var).pack(pady=5)

        tk.Label(edit_window, text="Имя преподавателя:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        teacher_var = tk.StringVar(value=entry["teacher_name"])
        ttk.Entry(edit_window, textvariable=teacher_var).pack(pady=5)

        tk.Label(edit_window, text="Аудитория:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        room_var = tk.StringVar(value=entry["classroom"])
        ttk.Entry(edit_window, textvariable=room_var).pack(pady=5)

        def save_changes():
            entry["time"] = time_var.get()
            entry["subject_name"] = subject_var.get()
            entry["teacher_name"] = teacher_var.get()
            entry["classroom"] = room_var.get()
            self.db.save_database()
            messagebox.showinfo("Успех", "Изменения сохранены!")
            edit_window.destroy()
            self.edit_schedule()

        tk.Button(edit_window, text="Сохранить",bg = "#FFFFFF", font=("AA Stetica Regular", 12), command=save_changes).pack(pady=10)

    def delete_entry_generic(self, entry):
        self.db.data["schedule"].remove(entry)
        self.db.save_database()
        messagebox.showinfo("Успех", "Запись удалена!")

    def open_add_subject_window(self):
        def submit_subject():
            try:
                # Получаем значения из полей ввода
                specialty_name = specialty_var.get()
                course = int(course_entry.get())
                subject_name = subject_entry.get()
                classroom = classroom_entry.get()

                # Вызов метода добавления предмета
                self.db.add_subject(specialty_name, course, subject_name, classroom)

                # Уведомление об успешном добавлении
                messagebox.showinfo(
                    "Успех",
                    f"Предмет '{subject_name}' успешно добавлен для специальности '{specialty_name}' на курсе {course}."
                )
                self.db.add_subject_window.destroy()
            except ValueError as e:
                # Показываем ошибку, если она возникла
                messagebox.showerror("Ошибка", str(e))
            except Exception as ex:
                # Общая обработка ошибок
                messagebox.showerror("Непредвиденная ошибка", f"Ошибка: {str(ex)}")

        # Создание окна для добавления предмета
        self.db.add_subject_window = tk.Toplevel()
        self.db.add_subject_window.title("Добавить новый предмет")
        self.db.add_subject_window.geometry("400x350")  # Настройка размера окна
        self.db.add_subject_window.configure(bg="#FFFFFF")

        # Получаем список доступных специальностей из базы данных
        specialties = {subject["specialty"] for subject in self.db.data["subjects"]}

        # Поле выбора специальности
        tk.Label(self.db.add_subject_window, text="Специальность:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        specialty_var = tk.StringVar()
        if specialties:
            specialty_var.set(next(iter(specialties)))  # Устанавливаем первую специальность как значение по умолчанию
        specialty_dropdown = tk.OptionMenu(self.db.add_subject_window, specialty_var, *specialties)
        # Меняем цвет фона и текста OptionMenu
        specialty_dropdown.config(bg="white", fg="black", activebackground="white", activeforeground="black",
                                  relief="flat")

        # Изменяем цвет меню (самих опций внутри списка)
        specialty_dropdown["menu"].config(bg="white", fg="black")
        specialty_dropdown.pack(pady=5)

        # Поле ввода курса
        tk.Label(self.db.add_subject_window, text="Курс:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        course_entry = tk.Entry(self.db.add_subject_window)
        course_entry.pack(pady=5)

        # Поле ввода названия предмета
        tk.Label(self.db.add_subject_window, text="Название предмета:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        subject_entry = tk.Entry(self.db.add_subject_window)
        subject_entry.pack(pady=5)

        # Поле ввода аудитории
        tk.Label(self.db.add_subject_window, text="Аудитория:",bg = "#FFFFFF", font=("AA Stetica Regular", 12)).pack(pady=5)
        classroom_entry = tk.Entry(self.db.add_subject_window)
        classroom_entry.pack(pady=5)

        # Кнопка для отправки данных
        submit_button = tk.Button(self.db.add_subject_window, text="Добавить предмет",bg = "#FFFFFF", font=("AA Stetica Regular", 12), command=submit_subject)
        submit_button.pack(pady=10)

        self.db.add_subject_window.mainloop()

    def open_user_profile(self):
        self.clear_window()
        self.canvas = Canvas(self.root, bg="#75DDE0", height=832, width=1280, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)

        # Фоновые изображения и текст
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(1218.0, 761.0, image=self.image_image_1)
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_8.png"))
        self.canvas.create_image(1118.99951171875, 250.0, image=self.image_image_2)
        self.image_image_3 = PhotoImage(file=self.relative_to_assets("image_9.png"))
        self.canvas.create_image(153.0, 762.18359375, image=self.image_image_3)
        self.image_image_4 = PhotoImage(file=self.relative_to_assets("image_10.png"))
        self.canvas.create_image(1235.0, 111.0, image=self.image_image_4)
        self.canvas.create_text(71.0, 153.0, anchor="nw", text="Личный кабинет", fill="#000000",
                                font=("Bombardier", 64 * -1))
        self.canvas.create_rectangle(0.0, 0.0, 1280.0, 69.0, fill="#FFFFFF", outline="")

        # Кнопка возврата
        self.button_image_4 = PhotoImage(file=self.relative_to_assets("button_22.png"))
        self.button_4 = Button(image=self.button_image_4, borderwidth=0, highlightthickness=0,
                               command=self.create_dashboard, relief="flat")
        self.button_4.place(x=0.0, y=0.0, width=208.0, height=69.0)

        user_data = self.current_user

        # Чтение аватарки из базы данных
        avatar_path = user_data.get("avatar", self.relative_to_assets("image_11.png"))

        # Загружаем сохраненную аватарку или дефолтную
        self.default_avatar = ImageTk.PhotoImage(Image.open(avatar_path).resize((255, 255)))
        self.current_avatar_image = self.default_avatar
        self.avatar_item = self.canvas.create_image(183.0, 413.0, image=self.current_avatar_image)

        def save_profile():
            birthday = birthday_entry.get()
            email = email_entry.get()

            if not birthday or not email:
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
                return

            user_data["birthday"] = birthday
            user_data["email"] = email

            # Сохраняем текущий путь аватарки в базе данных
            if hasattr(self, "selected_avatar_path"):
                user_data["avatar"] = self.selected_avatar_path

            self.db.update_user_profile(user_data)  # Обновляем данные в базе
            messagebox.showinfo("Успех", "Профиль успешно обновлен!")

        def choose_avatar():
            avatar_window = tk.Toplevel(self.root)
            avatar_window.title("Выбор аватарки")

            # Загрузка и сохранение всех изображений
            avatar_paths = ["avatar1.png", "avatar2.png", "avatar3.png",
                            "avatar4.png", "avatar5.png", "avatar6.png"]
            self.avatar_images = {path: ImageTk.PhotoImage(Image.open(path).resize((100, 100))) for path in
                                  avatar_paths}

            def set_avatar(path):
                self.selected_avatar_path = path
                new_avatar = Image.open(path).resize((255, 255))  # Подгоняем размер для Canvas
                self.current_avatar_image = ImageTk.PhotoImage(new_avatar)

                # Обновляем изображение на Canvas
                self.canvas.itemconfig(self.avatar_item, image=self.current_avatar_image)
                avatar_window.destroy()

            # Создаем виджет для отображения аватарок
            tk.Label(avatar_window, text="Выберите аватарку :)", font=("AAStetica Regular", 28 * -1)).pack(pady=10)
            avatar_frame = tk.Frame(avatar_window)
            avatar_frame.pack()

            for i, path in enumerate(avatar_paths):
                img = self.avatar_images[path]
                avatar_button = tk.Button(avatar_frame, image=img, command=lambda p=path: set_avatar(p))
                avatar_button.grid(row=i // 3, column=i % 3, padx=10, pady=10)

        # Кнопка выбора аватарки
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_21.png"))
        self.button_3 = Button(image=self.button_image_3, borderwidth=0, highlightthickness=0, command=choose_avatar,
                               relief="flat")
        self.button_3.place(x=54.0, y=571.0, width=256.0, height=55.0)

        # Текстовые поля и информация профиля
        self.canvas.create_text(348.0, 305.0, anchor="nw", text="Ваше ФИО:", fill="#000000",
                                font=("AA Stetica Regular", 32 * -1))
        self.canvas.create_text(630.0, 322.0, text=user_data.get("real_name", "Не указано"),
                                font=("AA Stetica Regular", 32 * -1))

        if user_data.get("role") == "Студент":
            self.canvas.create_text(348.0, 369.0, anchor="nw", text="Ваша группа:", fill="#000000",
                                    font=("AA Stetica Regular", 32 * -1))
            self.canvas.create_text(630.0, 387.0, text=user_data.get("group_name", "Не указано"), font=("AA Stetica Regular", 32 * -1))
        elif user_data.get("role") == "Преподаватель":
            self.canvas.create_text(348.0, 369.0, anchor="nw", text="Ваши предметы:", fill="#000000", font=("AA Stetica Regular", 32 * -1))
            subjects = user_data.get("subjects", [])
            subjects_text = ", ".join(subjects) if subjects else "Не указаны"
            self.canvas.create_text(750.0,387.0, text=subjects_text, font=("AA Stetica Regular", 32 * -1))
        elif user_data.get("role") == "Администратор":
            self.canvas.create_text(348.0, 369.0, anchor="nw", text="Вы - администратор", fill="#000000",
                                    font=("AA Stetica Regular", 32 * -1))

        self.entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        self.canvas.create_image(750.0, 453.0, image=self.entry_image_1)
        self.canvas.create_text(348.0, 433.0, anchor="nw", text="День рождения:", fill="#000000",
                                font=("AA Stetica Regular", 32 * -1))
        birthday_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 18))
        birthday_entry.insert(0, user_data.get("birthday", ""))
        birthday_entry.place(x=607.0, y=432.0, width=236.0, height=40.0)

        self.entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_4.png"))
        self.canvas.create_image(656.0, 527.0, image=self.entry_image_2)
        self.canvas.create_text(350.0, 511.0, anchor="nw", text="E-mail:", fill="#000000",
                                font=("AA Stetica Regular", 32 * -1))
        email_entry = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, font=("AA Stetica Regular", 18))
        email_entry.insert(0, user_data.get("email", ""))
        email_entry.place(x=480.0, y=508.0, width=360.0, height=38.0)

        # Кнопки сохранения и возврата
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_19.png"))
        self.button_1 = Button(image=self.button_image_1, borderwidth=0, highlightthickness=0,
                               command=save_profile, relief="flat")
        self.button_1.place(x=474.0, y=661.0, width=332.0, height=54.0)

        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_20.png"))
        self.button_2 = Button(image=self.button_image_2, borderwidth=0, highlightthickness=0,
                               command=self.create_dashboard, relief="flat")
        self.button_2.place(x=583.0, y=737.0, width=114.0, height=54.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()





