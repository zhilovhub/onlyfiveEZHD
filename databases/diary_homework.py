from database import *


class DiaryHomeworkCommands(DataBase):
    def __init__(self, connection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DiaryHomeworkQueries.create_table_homework_current_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_homework_next_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_diary_standard_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_diary_current_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_diary_next_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_temp_weekday_diary)

        except Error as e:
            print(e)

    def get_all_days_lessons_from_week(self, classroom_id: int, week_type: str, homework=False) -> list:
        """Returns everyday diary from week"""
        week_type_dict = {
            "standard": "diary_standard_week",
            "current": "diary_current_week" if not homework else "homework_current_week",
            "next": "diary_next_week" if not homework else "homework_next_week"
        }
        table_name = week_type_dict[week_type]

        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_all_days_from_week_query.format(table_name), (classroom_id,))
            all_lessons = cursor.fetchone()[1:]

            formatted_all_lessons = []
            for i in range(0, len(all_lessons), 12):
                formatted_all_lessons.append(all_lessons[i:i + 12])

        return formatted_all_lessons

    def get_weekday_lessons_from_week(self, classroom_id: int, week_type: str, weekday: str, homework=False) -> tuple:
        """Returns weekday from week"""
        week_type_dict = {
            "standard": "diary_standard_week",
            "current": "diary_current_week" if not homework else "homework_current_week",
            "next": "diary_next_week" if not homework else "homework_next_week"
        }
        table_name = week_type_dict[week_type]

        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_weekday_lessons_query(weekday, table_name), (classroom_id,))
            lessons = cursor.fetchone()

        return lessons

    def get_weekday_lessons_from_temp_table(self, user_id: int) -> tuple:
        """Returns weekday's lessons from the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_weekday_lessons_from_temp_table_query, (user_id,))
            lessons = cursor.fetchone()[4:]

        return lessons

    def get_weekday_name_from_temp_table(self, user_id: int) -> str:
        """Returns weekday's name from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_temp_weekday_name_query, (user_id,))
            weekday = cursor.fetchone()[0]

        return weekday

    def get_week_type_from_temp_table(self, user_id: int) -> str:
        """Returns week's type from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_week_type_from_temp_table_query, (user_id,))
            week_type = cursor.fetchone()[0]

        return week_type

    def insert_classroom_id(self, classroom_id: int) -> None:
        """Inserts classroom_id into the tables"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_homework_current_week_query, (classroom_id,))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_homework_next_week_query, (classroom_id,))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_standard_week_query, (classroom_id,))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_current_week_query, (classroom_id,))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_next_week_query, (classroom_id,))

    def insert_row_into_temp_weekday_table(self, student_id: int, user_id: int, week_type: str) -> None:
        """Inserts new row into temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.insert_new_row_into_temp_weekday_diary_query,
                           (student_id, user_id, week_type))

    def update_all_lessons_in_temp_weekday_table(self, user_id: int, weekday: str, lessons: tuple) -> None:
        """Updates lessons in temp weekday table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_all_lessons_in_temp_table, (weekday, *lessons, user_id))

    def update_weekday_in_week(self, classroom_id: int, lessons: tuple, week_type: str, weekday: str,
                               homework=False) -> None:
        """Updates week's weekday"""
        week_type_dict = {
            "standard": "diary_standard_week",
            "current": "diary_current_week" if not homework else "homework_current_week",
            "next": "diary_next_week" if not homework else "homework_next_week"
        }
        table_name = week_type_dict[week_type]

        query = DiaryHomeworkQueries.update_weekday_lessons_query(weekday, table_name)

        with self.connection.cursor() as cursor:
            cursor.execute(query, (*lessons, classroom_id))

    def update_add_new_lesson_into_temp_table(self, user_id: int, lesson: str, new_lesson_index: int) -> None:
        """Update the row with new lesson"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_add_new_lesson_into_temp_weekday_diary_query.format(
                new_lesson_index), (lesson, user_id)
            )

    def update_delete_all_lessons_from_temp_table(self, user_id: int) -> None:
        """Deletes all lessons from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_all_lessons_from_temp_table_query, (user_id,))

    def update_lesson_in_temp_table(self, user_id: int, lesson_name: str, lesson_index: int) -> None:
        """Updates lesson's name in temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_lesson_in_temp_table_query.format(lesson_index), (lesson_name,
                                                                                                         user_id))

    def update_delete_lesson_from_temp_table(self, user_id: int, lesson_index: int) -> None:
        """Deletes lesson from the row in the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_lesson_from_temp_table_query.format(lesson_index),
                           (user_id,))

    def update_delete_weekday_from_temp_table(self, user_id: int) -> None:
        """Deletes weekday from the row in the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_weekday_from_temp_table_query, (user_id,))

    def update_copy_diary_from_week_into_another_week(self, classroom_id: int, week_type: str,
                                                      week_lessons: list, homework=False) -> None:
        """Copy week's diary into another type week's diary"""
        week_type_dict = {
            "standard": "diary_standard_week",
            "current": "diary_current_week" if not homework else "homework_current_week",
            "next": "diary_next_week" if not homework else "homework_next_week"
        }
        table_name = week_type_dict[week_type]

        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_copy_diary_from_week_into_another_week_query.
                           format(table_name), (*[lesson for weekday_lessons in week_lessons
                                                  for lesson in weekday_lessons], classroom_id))

    def update_clear_week(self, classroom_id: int, week_type: str, homework=False) -> None:
        """Clears week"""
        week_type_dict = {
            "standard": "diary_standard_week",
            "current": "diary_current_week" if not homework else "homework_current_week",
            "next": "diary_next_week" if not homework else "homework_next_week"
        }
        table_name = week_type_dict[week_type]

        none_list = [None] * 84
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_copy_diary_from_week_into_another_week_query.format(table_name),
                           (*none_list, classroom_id))

    async def update_change_current_and_next_diary(self) -> None:
        """Changes every new week current_week and next_week_diary"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_all_classroom_ids_query)

            classroom_ids = [row[0] for row in cursor.fetchall()]
            for classroom_id in classroom_ids:
                formatted_standard_week_lessons = self.get_all_days_lessons_from_week(classroom_id, "standard")
                formatted_next_week_lessons = self.get_all_days_lessons_from_week(classroom_id, "next")
                formatted_next_week_homework = self.get_all_days_lessons_from_week(classroom_id, "next",
                                                                                   homework=True)
                self.update_copy_diary_from_week_into_another_week(classroom_id, "next",
                                                                   formatted_standard_week_lessons)
                self.update_copy_diary_from_week_into_another_week(classroom_id, "current",
                                                                   formatted_next_week_lessons)
                self.update_copy_diary_from_week_into_another_week(classroom_id, "current",
                                                                   formatted_next_week_homework, homework=True)
                self.update_clear_week(classroom_id, "next", homework=True)

    def delete_row_from_temp_weekday_table(self, user_id: int) -> None:
        """Deletes row from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.delete_row_from_temp_weekday_diary_query, (user_id,))


class DiaryHomeworkQueries:
    @staticmethod
    def get_weekday_lessons_query(weekday: str, table_name: str) -> str:
        """Creates get_weekday query"""
        template = """SELECT 
                        weekday_lesson1,
                        weekday_lesson2,
                        weekday_lesson3,
                        weekday_lesson4,
                        weekday_lesson5,
                        weekday_lesson6,
                        weekday_lesson7,
                        weekday_lesson8,
                        weekday_lesson9,
                        weekday_lesson10,
                        weekday_lesson11,
                        weekday_lesson12
                      FROM table_name WHERE classroom_id=%s"""
        return template.replace("weekday", weekday).replace("table_name", table_name)

    @staticmethod
    def update_weekday_lessons_query(weekday: str, table_name: str) -> str:
        """Creates update_weekday query"""
        template = """UPDATE table_name SET
                        weekday_lesson1=%s,
                        weekday_lesson2=%s,
                        weekday_lesson3=%s,
                        weekday_lesson4=%s,
                        weekday_lesson5=%s,
                        weekday_lesson6=%s,
                        weekday_lesson7=%s,
                        weekday_lesson8=%s,
                        weekday_lesson9=%s,
                        weekday_lesson10=%s,
                        weekday_lesson11=%s,
                        weekday_lesson12=%s
                      WHERE classroom_id=%s"""
        return template.replace("table_name", table_name).replace("weekday", weekday)

    create_table_homework_current_week_query = """CREATE TABLE IF NOT EXISTS homework_current_week(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        monday_lesson1 TEXT,
        monday_lesson2 TEXT,
        monday_lesson3 TEXT,
        monday_lesson4 TEXT,
        monday_lesson5 TEXT,
        monday_lesson6 TEXT,
        monday_lesson7 TEXT,
        monday_lesson8 TEXT,
        monday_lesson9 TEXT,
        monday_lesson10 TEXT,
        monday_lesson11 TEXT,
        monday_lesson12 TEXT,
        
        tuesday_lesson1 TEXT,
        tuesday_lesson2 TEXT,
        tuesday_lesson3 TEXT,
        tuesday_lesson4 TEXT,
        tuesday_lesson5 TEXT,
        tuesday_lesson6 TEXT,
        tuesday_lesson7 TEXT,
        tuesday_lesson8 TEXT,
        tuesday_lesson9 TEXT,
        tuesday_lesson10 TEXT,
        tuesday_lesson11 TEXT,
        tuesday_lesson12 TEXT,
        
        wednesday_lesson1 TEXT,
        wednesday_lesson2 TEXT,
        wednesday_lesson3 TEXT,
        wednesday_lesson4 TEXT,
        wednesday_lesson5 TEXT,
        wednesday_lesson6 TEXT,
        wednesday_lesson7 TEXT,
        wednesday_lesson8 TEXT,
        wednesday_lesson9 TEXT,
        wednesday_lesson10 TEXT,
        wednesday_lesson11 TEXT,
        wednesday_lesson12 TEXT,
        
        thursday_lesson1 TEXT,
        thursday_lesson2 TEXT,
        thursday_lesson3 TEXT,
        thursday_lesson4 TEXT,
        thursday_lesson5 TEXT,
        thursday_lesson6 TEXT,
        thursday_lesson7 TEXT,
        thursday_lesson8 TEXT,
        thursday_lesson9 TEXT,
        thursday_lesson10 TEXT,
        thursday_lesson11 TEXT,
        thursday_lesson12 TEXT,
        
        friday_lesson1 TEXT,
        friday_lesson2 TEXT,
        friday_lesson3 TEXT,
        friday_lesson4 TEXT,
        friday_lesson5 TEXT,
        friday_lesson6 TEXT,
        friday_lesson7 TEXT,
        friday_lesson8 TEXT,
        friday_lesson9 TEXT,
        friday_lesson10 TEXT,
        friday_lesson11 TEXT,
        friday_lesson12 TEXT,
        
        saturday_lesson1 TEXT,
        saturday_lesson2 TEXT,
        saturday_lesson3 TEXT,
        saturday_lesson4 TEXT,
        saturday_lesson5 TEXT,
        saturday_lesson6 TEXT,
        saturday_lesson7 TEXT,
        saturday_lesson8 TEXT,
        saturday_lesson9 TEXT,
        saturday_lesson10 TEXT,
        saturday_lesson11 TEXT,
        saturday_lesson12 TEXT,
        
        sunday_lesson1 TEXT,
        sunday_lesson2 TEXT,
        sunday_lesson3 TEXT,
        sunday_lesson4 TEXT,
        sunday_lesson5 TEXT,
        sunday_lesson6 TEXT,
        sunday_lesson7 TEXT,
        sunday_lesson8 TEXT,
        sunday_lesson9 TEXT,
        sunday_lesson10 TEXT,
        sunday_lesson11 TEXT,
        sunday_lesson12 TEXT
    )"""

    create_table_homework_next_week_query = """CREATE TABLE IF NOT EXISTS homework_next_week(
            classroom_id INT,
            FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,

            monday_lesson1 TEXT,
            monday_lesson2 TEXT,
            monday_lesson3 TEXT,
            monday_lesson4 TEXT,
            monday_lesson5 TEXT,
            monday_lesson6 TEXT,
            monday_lesson7 TEXT,
            monday_lesson8 TEXT,
            monday_lesson9 TEXT,
            monday_lesson10 TEXT,
            monday_lesson11 TEXT,
            monday_lesson12 TEXT,

            tuesday_lesson1 TEXT,
            tuesday_lesson2 TEXT,
            tuesday_lesson3 TEXT,
            tuesday_lesson4 TEXT,
            tuesday_lesson5 TEXT,
            tuesday_lesson6 TEXT,
            tuesday_lesson7 TEXT,
            tuesday_lesson8 TEXT,
            tuesday_lesson9 TEXT,
            tuesday_lesson10 TEXT,
            tuesday_lesson11 TEXT,
            tuesday_lesson12 TEXT,

            wednesday_lesson1 TEXT,
            wednesday_lesson2 TEXT,
            wednesday_lesson3 TEXT,
            wednesday_lesson4 TEXT,
            wednesday_lesson5 TEXT,
            wednesday_lesson6 TEXT,
            wednesday_lesson7 TEXT,
            wednesday_lesson8 TEXT,
            wednesday_lesson9 TEXT,
            wednesday_lesson10 TEXT,
            wednesday_lesson11 TEXT,
            wednesday_lesson12 TEXT,

            thursday_lesson1 TEXT,
            thursday_lesson2 TEXT,
            thursday_lesson3 TEXT,
            thursday_lesson4 TEXT,
            thursday_lesson5 TEXT,
            thursday_lesson6 TEXT,
            thursday_lesson7 TEXT,
            thursday_lesson8 TEXT,
            thursday_lesson9 TEXT,
            thursday_lesson10 TEXT,
            thursday_lesson11 TEXT,
            thursday_lesson12 TEXT,

            friday_lesson1 TEXT,
            friday_lesson2 TEXT,
            friday_lesson3 TEXT,
            friday_lesson4 TEXT,
            friday_lesson5 TEXT,
            friday_lesson6 TEXT,
            friday_lesson7 TEXT,
            friday_lesson8 TEXT,
            friday_lesson9 TEXT,
            friday_lesson10 TEXT,
            friday_lesson11 TEXT,
            friday_lesson12 TEXT,

            saturday_lesson1 TEXT,
            saturday_lesson2 TEXT,
            saturday_lesson3 TEXT,
            saturday_lesson4 TEXT,
            saturday_lesson5 TEXT,
            saturday_lesson6 TEXT,
            saturday_lesson7 TEXT,
            saturday_lesson8 TEXT,
            saturday_lesson9 TEXT,
            saturday_lesson10 TEXT,
            saturday_lesson11 TEXT,
            saturday_lesson12 TEXT,

            sunday_lesson1 TEXT,
            sunday_lesson2 TEXT,
            sunday_lesson3 TEXT,
            sunday_lesson4 TEXT,
            sunday_lesson5 TEXT,
            sunday_lesson6 TEXT,
            sunday_lesson7 TEXT,
            sunday_lesson8 TEXT,
            sunday_lesson9 TEXT,
            sunday_lesson10 TEXT,
            sunday_lesson11 TEXT,
            sunday_lesson12 TEXT
        )"""

    create_table_diary_standard_week_query = """CREATE TABLE IF NOT EXISTS diary_standard_week(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        monday_lesson1 TEXT,
        monday_lesson2 TEXT,
        monday_lesson3 TEXT,
        monday_lesson4 TEXT,
        monday_lesson5 TEXT,
        monday_lesson6 TEXT,
        monday_lesson7 TEXT,
        monday_lesson8 TEXT,
        monday_lesson9 TEXT,
        monday_lesson10 TEXT,
        monday_lesson11 TEXT,
        monday_lesson12 TEXT,
        
        tuesday_lesson1 TEXT,
        tuesday_lesson2 TEXT,
        tuesday_lesson3 TEXT,
        tuesday_lesson4 TEXT,
        tuesday_lesson5 TEXT,
        tuesday_lesson6 TEXT,
        tuesday_lesson7 TEXT,
        tuesday_lesson8 TEXT,
        tuesday_lesson9 TEXT,
        tuesday_lesson10 TEXT,
        tuesday_lesson11 TEXT,
        tuesday_lesson12 TEXT,
        
        wednesday_lesson1 TEXT,
        wednesday_lesson2 TEXT,
        wednesday_lesson3 TEXT,
        wednesday_lesson4 TEXT,
        wednesday_lesson5 TEXT,
        wednesday_lesson6 TEXT,
        wednesday_lesson7 TEXT,
        wednesday_lesson8 TEXT,
        wednesday_lesson9 TEXT,
        wednesday_lesson10 TEXT,
        wednesday_lesson11 TEXT,
        wednesday_lesson12 TEXT,
        
        thursday_lesson1 TEXT,
        thursday_lesson2 TEXT,
        thursday_lesson3 TEXT,
        thursday_lesson4 TEXT,
        thursday_lesson5 TEXT,
        thursday_lesson6 TEXT,
        thursday_lesson7 TEXT,
        thursday_lesson8 TEXT,
        thursday_lesson9 TEXT,
        thursday_lesson10 TEXT,
        thursday_lesson11 TEXT,
        thursday_lesson12 TEXT,
        
        friday_lesson1 TEXT,
        friday_lesson2 TEXT,
        friday_lesson3 TEXT,
        friday_lesson4 TEXT,
        friday_lesson5 TEXT,
        friday_lesson6 TEXT,
        friday_lesson7 TEXT,
        friday_lesson8 TEXT,
        friday_lesson9 TEXT,
        friday_lesson10 TEXT,
        friday_lesson11 TEXT,
        friday_lesson12 TEXT,
        
        saturday_lesson1 TEXT,
        saturday_lesson2 TEXT,
        saturday_lesson3 TEXT,
        saturday_lesson4 TEXT,
        saturday_lesson5 TEXT,
        saturday_lesson6 TEXT,
        saturday_lesson7 TEXT,
        saturday_lesson8 TEXT,
        saturday_lesson9 TEXT,
        saturday_lesson10 TEXT,
        saturday_lesson11 TEXT,
        saturday_lesson12 TEXT,
        
        sunday_lesson1 TEXT,
        sunday_lesson2 TEXT,
        sunday_lesson3 TEXT,
        sunday_lesson4 TEXT,
        sunday_lesson5 TEXT,
        sunday_lesson6 TEXT,
        sunday_lesson7 TEXT,
        sunday_lesson8 TEXT,
        sunday_lesson9 TEXT,
        sunday_lesson10 TEXT,
        sunday_lesson11 TEXT,
        sunday_lesson12 TEXT
    )"""

    create_table_diary_current_week_query = """CREATE TABLE IF NOT EXISTS diary_current_week(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,   
        
        monday_lesson1 TEXT,
        monday_lesson2 TEXT,
        monday_lesson3 TEXT,
        monday_lesson4 TEXT,
        monday_lesson5 TEXT,
        monday_lesson6 TEXT,
        monday_lesson7 TEXT,
        monday_lesson8 TEXT,
        monday_lesson9 TEXT,
        monday_lesson10 TEXT,
        monday_lesson11 TEXT,
        monday_lesson12 TEXT,
        
        tuesday_lesson1 TEXT,
        tuesday_lesson2 TEXT,
        tuesday_lesson3 TEXT,
        tuesday_lesson4 TEXT,
        tuesday_lesson5 TEXT,
        tuesday_lesson6 TEXT,
        tuesday_lesson7 TEXT,
        tuesday_lesson8 TEXT,
        tuesday_lesson9 TEXT,
        tuesday_lesson10 TEXT,
        tuesday_lesson11 TEXT,
        tuesday_lesson12 TEXT,
        
        wednesday_lesson1 TEXT,
        wednesday_lesson2 TEXT,
        wednesday_lesson3 TEXT,
        wednesday_lesson4 TEXT,
        wednesday_lesson5 TEXT,
        wednesday_lesson6 TEXT,
        wednesday_lesson7 TEXT,
        wednesday_lesson8 TEXT,
        wednesday_lesson9 TEXT,
        wednesday_lesson10 TEXT,
        wednesday_lesson11 TEXT,
        wednesday_lesson12 TEXT,
        
        thursday_lesson1 TEXT,
        thursday_lesson2 TEXT,
        thursday_lesson3 TEXT,
        thursday_lesson4 TEXT,
        thursday_lesson5 TEXT,
        thursday_lesson6 TEXT,
        thursday_lesson7 TEXT,
        thursday_lesson8 TEXT,
        thursday_lesson9 TEXT,
        thursday_lesson10 TEXT,
        thursday_lesson11 TEXT,
        thursday_lesson12 TEXT,
        
        friday_lesson1 TEXT,
        friday_lesson2 TEXT,
        friday_lesson3 TEXT,
        friday_lesson4 TEXT,
        friday_lesson5 TEXT,
        friday_lesson6 TEXT,
        friday_lesson7 TEXT,
        friday_lesson8 TEXT,
        friday_lesson9 TEXT,
        friday_lesson10 TEXT,
        friday_lesson11 TEXT,
        friday_lesson12 TEXT,
        
        saturday_lesson1 TEXT,
        saturday_lesson2 TEXT,
        saturday_lesson3 TEXT,
        saturday_lesson4 TEXT,
        saturday_lesson5 TEXT,
        saturday_lesson6 TEXT,
        saturday_lesson7 TEXT,
        saturday_lesson8 TEXT,
        saturday_lesson9 TEXT,
        saturday_lesson10 TEXT,
        saturday_lesson11 TEXT,
        saturday_lesson12 TEXT,
        
        sunday_lesson1 TEXT,
        sunday_lesson2 TEXT,
        sunday_lesson3 TEXT,
        sunday_lesson4 TEXT,
        sunday_lesson5 TEXT,
        sunday_lesson6 TEXT,
        sunday_lesson7 TEXT,
        sunday_lesson8 TEXT,
        sunday_lesson9 TEXT,
        sunday_lesson10 TEXT,
        sunday_lesson11 TEXT,
        sunday_lesson12 TEXT
    )"""

    create_table_diary_next_week_query = """CREATE TABLE IF NOT EXISTS diary_next_week(
        classroom_id INT,
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        
        monday_lesson1 TEXT,
        monday_lesson2 TEXT,
        monday_lesson3 TEXT,
        monday_lesson4 TEXT,
        monday_lesson5 TEXT,
        monday_lesson6 TEXT,
        monday_lesson7 TEXT,
        monday_lesson8 TEXT,
        monday_lesson9 TEXT,
        monday_lesson10 TEXT,
        monday_lesson11 TEXT,
        monday_lesson12 TEXT,
        
        tuesday_lesson1 TEXT,
        tuesday_lesson2 TEXT,
        tuesday_lesson3 TEXT,
        tuesday_lesson4 TEXT,
        tuesday_lesson5 TEXT,
        tuesday_lesson6 TEXT,
        tuesday_lesson7 TEXT,
        tuesday_lesson8 TEXT,
        tuesday_lesson9 TEXT,
        tuesday_lesson10 TEXT,
        tuesday_lesson11 TEXT,
        tuesday_lesson12 TEXT,
        
        wednesday_lesson1 TEXT,
        wednesday_lesson2 TEXT,
        wednesday_lesson3 TEXT,
        wednesday_lesson4 TEXT,
        wednesday_lesson5 TEXT,
        wednesday_lesson6 TEXT,
        wednesday_lesson7 TEXT,
        wednesday_lesson8 TEXT,
        wednesday_lesson9 TEXT,
        wednesday_lesson10 TEXT,
        wednesday_lesson11 TEXT,
        wednesday_lesson12 TEXT,
        
        thursday_lesson1 TEXT,
        thursday_lesson2 TEXT,
        thursday_lesson3 TEXT,
        thursday_lesson4 TEXT,
        thursday_lesson5 TEXT,
        thursday_lesson6 TEXT,
        thursday_lesson7 TEXT,
        thursday_lesson8 TEXT,
        thursday_lesson9 TEXT,
        thursday_lesson10 TEXT,
        thursday_lesson11 TEXT,
        thursday_lesson12 TEXT,
        
        friday_lesson1 TEXT,
        friday_lesson2 TEXT,
        friday_lesson3 TEXT,
        friday_lesson4 TEXT,
        friday_lesson5 TEXT,
        friday_lesson6 TEXT,
        friday_lesson7 TEXT,
        friday_lesson8 TEXT,
        friday_lesson9 TEXT,
        friday_lesson10 TEXT,
        friday_lesson11 TEXT,
        friday_lesson12 TEXT,
        
        saturday_lesson1 TEXT,
        saturday_lesson2 TEXT,
        saturday_lesson3 TEXT,
        saturday_lesson4 TEXT,
        saturday_lesson5 TEXT,
        saturday_lesson6 TEXT,
        saturday_lesson7 TEXT,
        saturday_lesson8 TEXT,
        saturday_lesson9 TEXT,
        saturday_lesson10 TEXT,
        saturday_lesson11 TEXT,
        saturday_lesson12 TEXT,
        
        sunday_lesson1 TEXT,
        sunday_lesson2 TEXT,
        sunday_lesson3 TEXT,
        sunday_lesson4 TEXT,
        sunday_lesson5 TEXT,
        sunday_lesson6 TEXT,
        sunday_lesson7 TEXT,
        sunday_lesson8 TEXT,
        sunday_lesson9 TEXT,
        sunday_lesson10 TEXT,
        sunday_lesson11 TEXT,
        sunday_lesson12 TEXT
    )"""

    create_table_temp_weekday_diary = """CREATE TABLE IF NOT EXISTS temp_weekday_diary(
        student_id INT UNIQUE,
        user_id INT UNIQUE,
        weekday TEXT,
        week_type TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES Student (student_id) ON DELETE CASCADE,
        
        lesson1 TEXT,
        lesson2 TEXT,
        lesson3 TEXT,
        lesson4 TEXT,
        lesson5 TEXT,
        lesson6 TEXT,
        lesson7 TEXT,
        lesson8 TEXT,
        lesson9 TEXT,
        lesson10 TEXT,
        lesson11 TEXT,
        lesson12 TEXT
    )"""

    get_all_days_from_week_query = """SELECT * FROM {} WHERE classroom_id=%s"""

    get_weekday_lessons_from_temp_table_query = """SELECT * FROM temp_weekday_diary WHERE user_id=%s"""
    get_week_type_from_temp_table_query = """SELECT week_type FROM temp_weekday_diary WHERE user_id=%s"""
    get_temp_weekday_name_query = """SELECT weekday FROM temp_weekday_diary WHERE user_id=%s"""

    get_all_classroom_ids_query = """SELECT classroom_id FROM classroom"""

    insert_classroom_id_homework_current_week_query = "INSERT INTO homework_current_week (classroom_id) VALUES(%s)"
    insert_classroom_id_homework_next_week_query = "INSERT INTO homework_next_week (classroom_id) VALUES(%s)"
    insert_classroom_id_standard_week_query = "INSERT INTO diary_standard_week (classroom_id) VALUES(%s)"
    insert_classroom_id_current_week_query = "INSERT INTO diary_current_week (classroom_id) VALUES(%s)"
    insert_classroom_id_next_week_query = "INSERT INTO diary_next_week (classroom_id) VALUES(%s)"

    insert_new_row_into_temp_weekday_diary_query = """INSERT INTO temp_weekday_diary VALUES(
        %s, %s, NULL, %s, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
    )"""

    update_all_lessons_in_temp_table = """UPDATE temp_weekday_diary SET
        weekday=%s,
        lesson1=%s,
        lesson2=%s,
        lesson3=%s,
        lesson4=%s,
        lesson5=%s,
        lesson6=%s,
        lesson7=%s,
        lesson8=%s,
        lesson9=%s,
        lesson10=%s,
        lesson11=%s,
        lesson12=%s
    WHERE user_id=%s
        """

    update_add_new_lesson_into_temp_weekday_diary_query = """UPDATE temp_weekday_diary SET lesson{}=%s
        WHERE user_id=%s"""

    update_delete_all_lessons_from_temp_table_query = """UPDATE temp_weekday_diary SET
        lesson1=NULL,
        lesson2=NULL,
        lesson3=NULL,
        lesson4=NULL,
        lesson5=NULL,
        lesson6=NULL,
        lesson7=NULL,
        lesson8=NULL,
        lesson9=NULL,
        lesson10=NULL,
        lesson11=NULL,
        lesson12=NULL
    WHERE user_id=%s"""

    update_lesson_in_temp_table_query = "UPDATE temp_weekday_diary SET lesson{}=%s WHERE user_id=%s"
    update_delete_lesson_from_temp_table_query = """UPDATE temp_weekday_diary SET lesson{}=NULL WHERE user_id=%s"""
    update_delete_weekday_from_temp_table_query = """UPDATE temp_weekday_diary SET weekday=NULL WHERE user_id=%s"""

    update_copy_diary_from_week_into_another_week_query = """UPDATE {} SET
        monday_lesson1=%s,
        monday_lesson2=%s,
        monday_lesson3=%s,
        monday_lesson4=%s,
        monday_lesson5=%s,
        monday_lesson6=%s,
        monday_lesson7=%s,
        monday_lesson8=%s,
        monday_lesson9=%s,
        monday_lesson10=%s,
        monday_lesson11=%s,
        monday_lesson12=%s,
        
        tuesday_lesson1=%s,
        tuesday_lesson2=%s,
        tuesday_lesson3=%s,
        tuesday_lesson4=%s,
        tuesday_lesson5=%s,
        tuesday_lesson6=%s,
        tuesday_lesson7=%s,
        tuesday_lesson8=%s,
        tuesday_lesson9=%s,
        tuesday_lesson10=%s,
        tuesday_lesson11=%s,
        tuesday_lesson12=%s,
        
        wednesday_lesson1=%s,
        wednesday_lesson2=%s,
        wednesday_lesson3=%s,
        wednesday_lesson4=%s,
        wednesday_lesson5=%s,
        wednesday_lesson6=%s,
        wednesday_lesson7=%s,
        wednesday_lesson8=%s,
        wednesday_lesson9=%s,
        wednesday_lesson10=%s,
        wednesday_lesson11=%s,
        wednesday_lesson12=%s,
        
        thursday_lesson1=%s,
        thursday_lesson2=%s,
        thursday_lesson3=%s,
        thursday_lesson4=%s,
        thursday_lesson5=%s,
        thursday_lesson6=%s,
        thursday_lesson7=%s,
        thursday_lesson8=%s,
        thursday_lesson9=%s,
        thursday_lesson10=%s,
        thursday_lesson11=%s,
        thursday_lesson12=%s,
        
        friday_lesson1=%s,
        friday_lesson2=%s,
        friday_lesson3=%s,
        friday_lesson4=%s,
        friday_lesson5=%s,
        friday_lesson6=%s,
        friday_lesson7=%s,
        friday_lesson8=%s,
        friday_lesson9=%s,
        friday_lesson10=%s,
        friday_lesson11=%s,
        friday_lesson12=%s,
        
        saturday_lesson1=%s,
        saturday_lesson2=%s,
        saturday_lesson3=%s,
        saturday_lesson4=%s,
        saturday_lesson5=%s,
        saturday_lesson6=%s,
        saturday_lesson7=%s,
        saturday_lesson8=%s,
        saturday_lesson9=%s,
        saturday_lesson10=%s,
        saturday_lesson11=%s,
        saturday_lesson12=%s,
        
        sunday_lesson1=%s,
        sunday_lesson2=%s,
        sunday_lesson3=%s,
        sunday_lesson4=%s,
        sunday_lesson5=%s,
        sunday_lesson6=%s,
        sunday_lesson7=%s,
        sunday_lesson8=%s,
        sunday_lesson9=%s,
        sunday_lesson10=%s,
        sunday_lesson11=%s,
        sunday_lesson12=%s
    WHERE classroom_id=%s"""

    delete_row_from_temp_weekday_diary_query = """DELETE FROM temp_weekday_diary WHERE user_id=%s"""


if __name__ == '__main__':
    pass
    # connection = connect(DATABASE_URL)
    #
    # diary_homework_db = DiaryHomeworkCommands(connection)
    # diary_homework_db.delete_row_from_temp_weekday_table(341106876)
    #
    # connection.commit()
    # connection.close()
