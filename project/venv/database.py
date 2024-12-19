import json
import tkinter as tk
from tkinter import messagebox
import os
import random
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side


class Database:
    def __init__(self):
        self.db_file = "database.json"

        if not os.path.exists(self.db_file):
            self.reset_database()

        with open(self.db_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def reset_database(self):
        self.data = {
            "users": [],
            "subjects": [],
            "schedule": []
        }
        self.save_database()

    def save_database(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_users(self):
        return self.data["users"]

    def check_login(self, username, password):
        for user in self.data["users"]:
            if user["username"] == username and user["password"] == password:
                return user
        return None

    def get_speciality_from_group(self, group_name):
        if not group_name:
            return None

        specialties = {
            "ИС": "Информационные системы и программирование",
            "Т": "Туризм",
            "У": "Экономика и бухгалтерский учет",}

        for code, specialty in specialties.items():
            if code in group_name:
                return specialty

        return "Неизвестная специальность"

    def extract_course_from_group(self, group_name):
        if not group_name or not group_name[:3].isdigit():
            return None

        try:
            group_year = int(group_name[:3])
            if 100 <= group_year < 200:
                return 1
            elif 200 <= group_year < 300:
                return 2
            elif 300 <= group_year < 400:
                return 3
            elif 400 <= group_year < 500:
                return 4
            else:
                return None
        except ValueError:
            return None

    def insert_user(self, real_name, username, password, role, group_name=None, subjects=None):
        user_id = len(self.data["users"]) + 1
        specialty = self.get_speciality_from_group(group_name) if role == "Студент" else None
        course = self.extract_course_from_group(group_name) if role == "Студент" else None

        new_user = {
            "id": user_id,
            "real_name": real_name,
            "username": username,
            "password": password,
            "role": role,
            "group_name": group_name,
            "specialty": specialty,
            "course": course,
            "subjects": subjects if role == "Преподаватель" else None,
        }

        self.data["users"].append(new_user)

        if specialty and course:
            self.insert_specialties_and_subjects(specialty, course)

        self.save_database()

    def update_user_profile(self, updated_user):
        for user in self.data["users"]:
            if user["username"] == updated_user["username"]:
                user.update(updated_user)
                self.save_database()
                return True
        raise ValueError("Пользователь не найден в базе данных")

    def insert_specialties_and_subjects(self, specialty_name=None, course=None):
        specialties = {
            "Информационные системы и программирование": {
                1: [("Русский язык", "406"), ("Литература", "628"), ("Обществознание", "317"), ("История", "416"),
                    ("Математика", "425"), ("Иностранный язык", "410"), ("Астрономия", "207"), ("Физика", "627"),
                    ("Физическая культура", "Спортзал"), ("География", "205")],
                2: [("Разработка программных модулей", "К65"), ("Психология общения", "203"),
                    ("Архитектура аппаратных средств", "К605"), ("Информационные технологии", "К420"),
                    ("Основы проектирования баз данных", "К64"), ("Основы алгоритмизации и программирования", "К53"),
                    ("Компьютерные сети", "К227"), ("Элементы высшей математики", "423"),
                    ("Физическая культура", "Спортзал"), ("История", "416")],
                3: [("Поддержка и тестирование программных модулей", "К515"),
                    ("Разработка программных модулей", "К65"),
                    ("Внедрение и поддержка компьютерных систем", "К505"),
                    ("Технология разработки и защиты баз данных", "К615"), ("Физическая культура", "Спортзал"),
                    ("Численные методы", "К56"), ("Экологические основы природопользования", "616"),
                    ("Иностранный язык в профессиональной деятельности", "406"),
                    ("Основы алгоритмизации и программирования", "К53")],
                4: [("Иностранный язык в профессиональной деятельности", "406"), ("Основы философии", "216"),
                    ("Разработка мобильных приложений", "К509"), ("Физическая культура", "Спортзал"),
                    ("Экономика отрасли", "210"), ("Менеджмент в профессиональной деятельности", "314")]
            },
            "Туризм": {
                1: [("Русский язык", "406"), ("Литература", "628"), ("Обществознание", "317"), ("История", "416"),
                    ("Математика", "425"), ("Иностранный язык", "410"), ("Астрономия", "207"), ("Физика", "627"),
                    ("Физическая культура", "Спортзал"), ("География", "205")],
                2: [("Иностранный язык в профессиональной деятельности", "201"),
                    ("Безопасность жизнедеятельности", "202"),
                    ("Правовое и документационное обеспечение в туризме и гостеприимстве", "223"),
                    ("Физическая культура", "Спортзал"), ("Основы проектной деятельности", "224"),
                    ("Основы финансовой грамотности", "326")],
                3: [("Основы финансовой грамотности", "326"), ("Индустрия гостеприимства", "612"),
                    ("Психология делового общения", "212"),
                    ("Иностранный язык в сфере профессиональной коммуникации", "404"),
                    ("Управление деятельностью функционального подразделения", "424"),
                    ("Организация досуга туристов", "529"), ("Технология продаж и продвижения турподукта", "429")]
            },
            "Экономика и бухгалтерский учет": {
                1: [("Русский язык", "406"), ("Литература", "628"), ("Обществознание", "317"), ("История", "416"),
                    ("Математика", "425"), ("Иностранный язык", "410"), ("Астрономия", "207"), ("Физика", "627"),
                    ("Физическая культура", "Спортзал"), ("География", "205")],
                2: [("Экономика организации", "А201"), ("Математика", "425"),
                    ("Основы предпринимательской деятельности", "427"),
                    ("Основы бухгалтерского учета", "А204"), ("Экологические основы природопользования", "616"),
                    ("Документационное обеспечение управления", "512"), ("История", "416"),
                    ("Основы финансовой грамотности", "326")],
                3: [("Экономический анализ", "211"), ("Иностранный язык в профессиональной деятельности", "406"),
                    ("Основы анализа бухгалтерской отчетности", "313"),
                    ("Бухгалтерская технология проведения и оформления инвентаризации", "304"),
                    ("Организация расчетов с бюджетом и внебюджетными фондами", "305"),
                    ("Практические основы бухгалтерского учета источников формирования активов организации", "306")]
            },
        }

        if specialty_name and course:
            subjects_for_course = specialties.get(specialty_name, {}).get(course, [])
            for subject, classroom in subjects_for_course:
                if not any(sub["specialty"] == specialty_name and sub["name"] == subject and sub["course"] == course
                           for sub in self.data["subjects"]):
                    new_subject = {
                        "id": len(self.data["subjects"]) + 1,
                        "name": subject,
                        "specialty": specialty_name,
                        "course": course,
                        "classroom": classroom,
                    }
                    self.data["subjects"].append(new_subject)
        else:
            for specialty, courses in specialties.items():
                for course_num, subjects in courses.items():
                    for subject, classroom in subjects:
                        if not any(
                                sub["specialty"] == specialty and sub["name"] == subject and sub["course"] == course_num
                                for sub in self.data["subjects"]):
                            new_subject = {
                                "id": len(self.data["subjects"]) + 1,
                                "name": subject,
                                "specialty": specialty,
                                "course": course_num,
                                "classroom": classroom,
                            }
                            self.data["subjects"].append(new_subject)

        self.save_database()

    def generate_schedule_for_all_users(self):
        self.data["schedule"] = []

        # Подготовка данных о студентах, преподавателях и аудиториях
        groups = {user["group_name"]: user for user in self.data["users"] if user["role"] == "Студент"}
        teachers = {
            user["id"]: {
                "name": user["real_name"],
                "subjects": user["subjects"],
                "daily_pairs": {day: 0 for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]},
                "occupied_slots": {day: set() for day in
                                   ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]}
            } for user in self.data["users"] if user["role"] == "Преподаватель"
        }
        rooms = {subj["id"]: subj["classroom"] for subj in self.data["subjects"]}  # Кабинеты берутся из subjects
        room_occupied_slots = {
            room_id: {day: set() for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]}
            for room_id in set(rooms.values())  # Уникальные кабинеты
        }

        # Параметры расписания
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        times = ["08:20-09:40", "09:50-11:10", "11:20-12:40", "12:50-14:10", "14:40-16:00", "16:10-17:30",
                 "17:40-19:00"]
        week_types = ["Четная", "Нечетная"]
        teacher_assignment = {}

        for group_name, student in groups.items():
            specialty = student["specialty"]
            course = student.get("course")
            subjects = [sub for sub in self.data["subjects"] if
                        sub["specialty"] == specialty and sub["course"] == course]

            if not subjects:
                continue

            group_occupied_slots = {day: set() for day in days}

            for week_type in week_types:
                weekly_schedule = {day: [] for day in days}

                total_pairs = random.randint(16, 18)
                daily_pairs_limits = {day: 2 for day in days}
                total_pairs -= 2 * len(days)
                daily_pairs_limits["Суббота"] += random.randint(2, 3)
                total_pairs -= daily_pairs_limits["Суббота"] - 2

                while total_pairs > 0:
                    for day in days:
                        if total_pairs <= 0:
                            break
                        if daily_pairs_limits[day] < 4:
                            daily_pairs_limits[day] += 1
                            total_pairs -= 1

                for day in days:
                    available_times = list(times)

                    while daily_pairs_limits[day] > 0 and available_times:
                        time = available_times.pop(0)
                        if time in group_occupied_slots[day]:
                            continue

                        subject = random.choice(subjects)
                        subject_classroom = subject["classroom"]

                        # Проверяем учителя
                        if (group_name, subject["id"]) not in teacher_assignment:
                            available_teachers = [
                                tid for tid, tinfo in teachers.items() if subject["name"] in tinfo["subjects"]
                            ]
                            teacher_id = random.choice(available_teachers) if available_teachers else None
                            teacher_name = teachers[teacher_id]["name"] if teacher_id else "Вакансия"

                            if teacher_id and (
                                    teachers[teacher_id]["daily_pairs"][day] >= 5 or time in
                                    teachers[teacher_id]["occupied_slots"][day]):
                                continue

                            teacher_assignment[(group_name, subject["id"])] = {
                                "teacher_id": teacher_id,
                                "teacher_name": teacher_name
                            }

                        teacher_info = teacher_assignment[(group_name, subject["id"])]

                        # Проверка занятости кабинета
                        if time in room_occupied_slots[subject_classroom][day]:
                            # Ищем альтернативный кабинет
                            available_rooms = [room for room in rooms.values() if
                                               time not in room_occupied_slots[room][day]
                                               and room != "Спортзал"]  # Спортзал обрабатывается отдельно
                            if available_rooms:
                                subject_classroom = random.choice(available_rooms)
                            else:
                                continue

                        # Добавление пары
                        weekly_schedule[day].append({
                            "day_of_week": day,
                            "time": time,
                            "subject_id": subject["id"],
                            "subject_name": subject["name"],
                            "group_name": group_name,
                            "teacher_id": teacher_info["teacher_id"],
                            "teacher_name": teacher_info["teacher_name"],
                            "week_type": week_type,
                            "classroom": subject_classroom,
                        })

                        # Обновляем занятость
                        group_occupied_slots[day].add(time)
                        room_occupied_slots[subject_classroom][day].add(time)
                        if teacher_info["teacher_id"]:
                            teachers[teacher_info["teacher_id"]]["daily_pairs"][day] += 1
                            teachers[teacher_info["teacher_id"]]["occupied_slots"][day].add(time)

                        daily_pairs_limits[day] -= 1

                for day, entries in weekly_schedule.items():
                    self.data["schedule"].extend(entries)

        self.save_database()
        print("Расписание успешно сгенерировано!")

    def add_subject(self, specialty_name, course, subject_name, classroom):
        if not specialty_name or not subject_name or not isinstance(course, int) or not classroom:
            raise ValueError("Необходимо указать корректные данные для добавления предмета и аудитории.")

        specialties = {s["specialty"] for s in self.data["subjects"]}
        if specialty_name not in specialties:
            raise ValueError(f"Специальность '{specialty_name}' отсутствует в базе.")

        if any(
                sub["specialty"] == specialty_name and sub["course"] == course and sub["name"] == subject_name
                for sub in self.data["subjects"]
        ):
            raise ValueError(
                f"Предмет '{subject_name}' уже существует для специальности '{specialty_name}' на курсе {course}.")

        new_subject = {
            "id": len(self.data["subjects"]) + 1,
            "name": subject_name,
            "specialty": specialty_name,
            "course": course,
            "classroom": classroom
        }
        self.data["subjects"].append(new_subject)

        self.save_database()

    def export_schedule_to_excel(self, filename="schedule.xlsx", database_path="database.json"):
        wb = Workbook()
        even_fill = PatternFill(start_color="D6EAF8", end_color="D6EAF8", fill_type="solid")
        odd_fill = PatternFill(start_color="FAD7A0", end_color="FAD7A0", fill_type="solid")
        bold_font = Font(bold=True)
        group_font = Font(size=14, bold=True)
        border = Border(left=Side(style="thin"),right=Side(style="thin"),top=Side(style="thin"),bottom=Side(style="thin"),)
        def adjust_column_width(sheet):
            for column_cells in sheet.columns:
                max_length = 0
                column_letter = column_cells[0].column_letter
                for cell in column_cells:
                    try:
                        max_length = max(max_length, len(str(cell.value or "")))
                    except:
                        pass
                sheet.column_dimensions[column_letter].width = min(max_length + 2, 20)
        def fill_schedule(sheet, schedule, groups_or_teachers, key, week_type, fill, row_offset):
            sheet.cell(row=row_offset, column=1, value=week_type).alignment = Alignment(horizontal="center")
            sheet.cell(row=row_offset, column=1).font = group_font
            sheet.cell(row=row_offset, column=1).fill = fill
            row_offset += 1

            for item in groups_or_teachers:
                sheet.cell(row=row_offset, column=1, value=item).alignment = Alignment(horizontal="center")
                sheet.cell(row=row_offset, column=1).font = group_font
                row_offset += 1

                filtered_schedule = [entry for entry in schedule if entry[key] == item]

                days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

                for col, day in enumerate(days, start=2):
                    cell = sheet.cell(row=row_offset, column=col, value=day)
                    cell.alignment = Alignment(horizontal="center")
                    cell.font = bold_font
                    cell.border = border

                row_offset += 1

                times = sorted(set(entry["time"] for entry in filtered_schedule))
                for time in times:
                    sheet.cell(row=row_offset, column=1, value=time).alignment = Alignment(horizontal="center")
                    sheet.cell(row=row_offset, column=1).border = border

                    for col, day in enumerate(days, start=2):
                        subjects = [
                            f"{entry['subject_name']} ({entry.get('classroom', 'N/A')})"
                            for entry in filtered_schedule if entry["day_of_week"] == day and entry["time"] == time]
                        cell = sheet.cell(row=row_offset, column=col, value=", ".join(subjects))
                        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
                        cell.border = border

                    row_offset += 1
                row_offset += 1
            return row_offset
        students_sheet = wb.active
        students_sheet.title = "Студенты"
        schedule = self.get_schedule()
        even_week_schedule = [entry for entry in schedule if entry["week_type"] == "Четная"]
        odd_week_schedule = [entry for entry in schedule if entry["week_type"] == "Нечетная"]
        groups = sorted(set(entry["group_name"] for entry in schedule if entry["group_name"]))
        row_offset = 1
        for week_type, week_schedule, fill in zip(["Четная", "Нечетная"], [even_week_schedule, odd_week_schedule],[even_fill, odd_fill]):
            row_offset = fill_schedule(students_sheet, week_schedule, groups, "group_name", week_type, fill, row_offset)
        adjust_column_width(students_sheet)
        teachers_sheet = wb.create_sheet(title="Преподаватели")
        with open(database_path, "r", encoding="utf-8") as db_file:
            database = json.load(db_file)
        teacher_id_to_name = {user["id"]: user["real_name"]
            for user in database["users"]
            if user.get("role") == "Преподаватель" and "real_name" in user}
        filtered_schedule = [entry for entry in schedule if entry.get("teacher_id") in teacher_id_to_name]
        for entry in filtered_schedule:
            teacher_id = entry["teacher_id"]
            entry["teacher_name"] = teacher_id_to_name[teacher_id]
        teachers = sorted(set(entry["teacher_name"] for entry in filtered_schedule))
        row_offset = 1
        for week_type, week_schedule, fill in zip(["Четная", "Нечетная"],[[e for e in filtered_schedule if e["week_type"] == "Четная"],[e for e in filtered_schedule if e["week_type"] == "Нечетная"]],[even_fill, odd_fill]):
            row_offset = fill_schedule(teachers_sheet, week_schedule, teachers, "teacher_name", week_type, fill,row_offset)
        adjust_column_width(teachers_sheet)
        wb.save(filename)
        os.startfile(filename)
        print(f"Расписание успешно экспортировано в файл {filename} и открыто!")

    def get_schedule(self):
        return self.data["schedule"]



