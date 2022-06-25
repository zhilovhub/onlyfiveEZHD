from database import *


class DiaryHomeworkCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(DiaryHomeworkQueries.create_table_diary_standard_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_diary_current_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_diary_next_week_query)
                cursor.execute(DiaryHomeworkQueries.create_table_temp_weekday_diary)

        except Error as e:
            print(e)

    def get_all_days_lessons_from_week(self, classroom_id: int, week: str) -> list:
        """Returns everyday diary from week"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_all_days_from_week_query.format(week, classroom_id))
            all_lessons = cursor.fetchone()[1:]

            formatted_all_lessons = []
            for i in range(0, len(all_lessons), 12):
                formatted_all_lessons.append(all_lessons[i:i+12])

        return formatted_all_lessons

    def get_weekday_lessons_from_week(self, classroom_id: int, week: str, weekday: str) -> tuple:
        """Returns weekday diary from week"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_weekday_lessons_query(weekday, week).format(classroom_id))
            lessons = cursor.fetchone()

        return lessons

    def get_weekday_lessons_from_temp_table(self, user_id: int) -> tuple:
        """Returns weekday's lessons from the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_weekday_lessons_from_temp_table_query.format(user_id))
            lessons = cursor.fetchone()[3:]

        return lessons

    def get_weekday_name_from_temp_table(self, user_id: int) -> str:
        """Returns weekday's name from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_temp_weekday_name_query.format(user_id))
            weekday = cursor.fetchone()[0]

        return weekday

    def get_week_type_from_temp_table(self, user_id: int) -> str:
        """Returns week's type from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_week_type_from_temp_table_query.format(user_id))
            week_type = cursor.fetchone()[0]

        return week_type

    def insert_classroom_id(self, classroom_id: int) -> None:
        """Inserts classroom_id into the tables"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_standard_week_query.format(classroom_id))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_current_week_query.format(classroom_id))
            cursor.execute(DiaryHomeworkQueries.insert_classroom_id_next_week_query.format(classroom_id))
            self.connection.commit()

    def insert_row_into_temp_weekday_table(self, user_id: int, week_type: str) -> None:
        """Inserts new row into temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.insert_new_row_into_temp_weekday_diary_query.format(user_id, week_type))
            self.connection.commit()

    def update_all_lessons_in_temp_weekday_table(self, user_id: int, weekday: str, lessons: list) -> None:
        """Updates lessons in temp weekday table"""
        query = DiaryHomeworkQueries.update_all_lessons_in_temp_table
        for lesson in lessons:
            query = query.replace("NULL", f"'{lesson}'", 1)

        with self.connection.cursor() as cursor:
            cursor.execute(query.format(weekday, user_id))
            self.connection.commit()

    def update_weekday_in_week(self, classroom_id: int, lessons: tuple, week_type: str, weekday: str) -> None:
        """Updates week's weekday"""
        query = DiaryHomeworkQueries.update_weekday_lessons_query(weekday, f"diary_{week_type}_week")
        for lesson in lessons:
            query = query.replace("NULL", f"'{lesson}'", 1) if lesson is not None else query

        with self.connection.cursor() as cursor:
            cursor.execute(query.format(classroom_id))
            self.connection.commit()

    def update_add_new_lesson_into_temp_table(self, user_id: int, lesson: str, new_lesson_index: int) -> None:
        """Update the row with new lesson"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_add_new_lesson_into_temp_weekday_diary_query.format(
                new_lesson_index, lesson, user_id)
            )
            self.connection.commit()

    def update_delete_all_lessons_from_temp_table(self, user_id: int) -> None:
        """Deletes all lessons from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_all_lessons_from_temp_table_query.format(user_id))
            self.connection.commit()

    def update_lesson_in_temp_table(self, user_id: int, lesson_name: str, lesson_index: int) -> None:
        """Updates lesson's name in temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_lesson_in_temp_table.format(lesson_index, lesson_name, user_id))
            self.connection.commit()

    def update_delete_lesson_from_temp_table(self, user_id: int, lesson_index: int) -> None:
        """Deletes lesson from the row in the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_lesson_from_temp_table.format(lesson_index, user_id))
            self.connection.commit()

    def update_delete_weekday_from_temp_table(self, user_id: int) -> None:
        """Deletes weekday from the row in the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_weekday_from_temp_table.format(user_id))
            self.connection.commit()

    def delete_row_from_temp_weekday_table(self, user_id: int) -> None:
        """Deletes row from temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.delete_row_from_temp_weekday_diary_query.format(user_id))
            self.connection.commit()


class DiaryHomeworkQueries:
    @staticmethod
    def get_weekday_lessons_query(weekday: str, week: str) -> str:
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
                      FROM diary_week_type_week WHERE classroom_id={}"""
        return template.replace("weekday", weekday).replace("week_type", week)

    @staticmethod
    def update_weekday_lessons_query(weekday: str, table_name: str) -> str:
        """Creates update_weekday query"""
        template = """UPDATE table_name SET
                        weekday_lesson1=NULL,
                        weekday_lesson2=NULL,
                        weekday_lesson3=NULL,
                        weekday_lesson4=NULL,
                        weekday_lesson5=NULL,
                        weekday_lesson6=NULL,
                        weekday_lesson7=NULL,
                        weekday_lesson8=NULL,
                        weekday_lesson9=NULL,
                        weekday_lesson10=NULL,
                        weekday_lesson11=NULL,
                        weekday_lesson12=NULL
                      WHERE classroom_id={}"""
        return template.replace("weekday", weekday).replace("table_name", table_name)
    
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
        user_id INT UNIQUE,
        weekday TEXT,
        week_type TEXT,
        FOREIGN KEY (user_id) REFERENCES User (user_id) ON DELETE CASCADE,
        
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

    get_all_days_from_week_query = """SELECT * FROM diary_{}_week WHERE classroom_id={}"""

    get_weekday_lessons_from_temp_table_query = """SELECT * FROM temp_weekday_diary WHERE user_id={}"""
    get_week_type_from_temp_table_query = """SELECT week_type FROM temp_weekday_diary WHERE user_id={}"""
    get_temp_weekday_name_query = """SELECT weekday FROM temp_weekday_diary WHERE user_id={}"""

    insert_classroom_id_standard_week_query = "INSERT INTO diary_standard_week (classroom_id) VALUES({})"
    insert_classroom_id_current_week_query = "INSERT INTO diary_current_week (classroom_id) VALUES({})"
    insert_classroom_id_next_week_query = "INSERT INTO diary_next_week (classroom_id) VALUES({})"

    insert_new_row_into_temp_weekday_diary_query = """INSERT INTO temp_weekday_diary VALUES(
        {}, NULL, '{}', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL
    )"""

    update_all_lessons_in_temp_table = """UPDATE temp_weekday_diary SET
        weekday='{}',
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
    WHERE user_id={}
        """

    update_add_new_lesson_into_temp_weekday_diary_query = """UPDATE temp_weekday_diary SET lesson{}='{}'
        WHERE user_id={}"""

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
    WHERE user_id={}"""

    update_lesson_in_temp_table = "UPDATE temp_weekday_diary SET lesson{}='{}' WHERE user_id={}"
    update_delete_lesson_from_temp_table = """UPDATE temp_weekday_diary SET lesson{}=NULL WHERE user_id={}"""
    update_delete_weekday_from_temp_table = """UPDATE temp_weekday_diary SET weekday=NULL WHERE user_id={}"""

    delete_row_from_temp_weekday_diary_query = """DELETE FROM temp_weekday_diary WHERE user_id={}"""


if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    diary_homework_db = DiaryHomeworkCommands(connection)
    print(diary_homework_db.get_weekday_lessons_from_week(1, "standard", "wednesday"))
    print(diary_homework_db.get_weekday_lessons_from_week(2, "current", "monday"))
    print(diary_homework_db.get_weekday_lessons_from_week(2, "next", "friday"))
    # diary_homework_db.insert_lessons_into_temp_weekday_table(341106876, "wednesay", [])
    # print(diary_homework_db.get_weekday_lessons_from_temp_table(341106876))
    # diary_homework_db.delete_row_from_temp_weekday_table(341106876)
