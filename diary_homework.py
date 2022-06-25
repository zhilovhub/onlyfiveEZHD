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
                cursor.execute(DiaryHomeworkQueries.create_table_week_support)

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
            cursor.execute(DiaryHomeworkQueries.update_lesson_in_temp_table_query.format(lesson_index, lesson_name,
                                                                                         user_id))
            self.connection.commit()

    def update_delete_lesson_from_temp_table(self, user_id: int, lesson_index: int) -> None:
        """Deletes lesson from the row in the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_lesson_from_temp_table_query.format(lesson_index,
                                                                                                  user_id))
            self.connection.commit()

    def update_delete_weekday_from_temp_table(self, user_id: int) -> None:
        """Deletes weekday from the row in the temp table"""
        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_delete_weekday_from_temp_table_query.format(user_id))
            self.connection.commit()

    def update_copy_diary_from_week_into_another_week(self, classroom_id: int, week_type: str,
                                                               week_lessons: list) -> None:
        """Copy week's diary into another type week's diary"""
        all_values = [week_type]
        for weekday_lessons in week_lessons:
            for lesson in weekday_lessons:
                if lesson is None:
                    all_values.append("NULL")
                else:
                    all_values.append(f"'{lesson}'")
        all_values.append(classroom_id)

        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.update_copy_diary_from_week_into_another_week_query.
                           format(*all_values))
            self.connection.commit()

    def update_change_current_and_next_diary(self) -> None:
        """Changes every new week current_week and next_week_diary"""
        current_week_index = int(datetime.now().strftime("%W"))

        with self.connection.cursor() as cursor:
            cursor.execute(DiaryHomeworkQueries.get_week_index_query)
            week_index_row = cursor.fetchone()

            if week_index_row is not None:
                last_week_index = week_index_row[0]

                if current_week_index != last_week_index:
                    cursor.execute(DiaryHomeworkQueries.update_week_index_week_support_query.format(current_week_index))
                    cursor.execute(DiaryHomeworkQueries.get_all_classroom_ids_query)

                    classroom_ids = [row[0] for row in cursor.fetchall()]
                    for classroom_id in classroom_ids:
                        formatted_standard_week_lessons = self.get_all_days_lessons_from_week(classroom_id, "standard")
                        formatted_next_week_lessons = self.get_all_days_lessons_from_week(classroom_id, "next")
                        self.update_copy_diary_from_week_into_another_week(classroom_id, "next",
                                                                           formatted_standard_week_lessons)
                        self.update_copy_diary_from_week_into_another_week(classroom_id, "current",
                                                                           formatted_next_week_lessons)

                    self.connection.commit()
            else:
                cursor.execute(DiaryHomeworkQueries.insert_week_index_week_support_query.format(current_week_index))
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

    create_table_week_support = """CREATE TABLE IF NOT EXISTS week_support(
        week_index INT
    )"""

    get_all_days_from_week_query = """SELECT * FROM diary_{}_week WHERE classroom_id={}"""

    get_weekday_lessons_from_temp_table_query = """SELECT * FROM temp_weekday_diary WHERE user_id={}"""
    get_week_type_from_temp_table_query = """SELECT week_type FROM temp_weekday_diary WHERE user_id={}"""
    get_temp_weekday_name_query = """SELECT weekday FROM temp_weekday_diary WHERE user_id={}"""

    get_week_index_query = """SELECT week_index FROM week_support"""
    get_all_classroom_ids_query = """SELECT classroom_id FROM classroom"""

    insert_classroom_id_standard_week_query = "INSERT INTO diary_standard_week (classroom_id) VALUES({})"
    insert_classroom_id_current_week_query = "INSERT INTO diary_current_week (classroom_id) VALUES({})"
    insert_classroom_id_next_week_query = "INSERT INTO diary_next_week (classroom_id) VALUES({})"

    insert_week_index_week_support_query = "INSERT INTO week_support VALUES({})"

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

    update_lesson_in_temp_table_query = "UPDATE temp_weekday_diary SET lesson{}='{}' WHERE user_id={}"
    update_delete_lesson_from_temp_table_query = """UPDATE temp_weekday_diary SET lesson{}=NULL WHERE user_id={}"""
    update_delete_weekday_from_temp_table_query = """UPDATE temp_weekday_diary SET weekday=NULL WHERE user_id={}"""

    update_week_index_week_support_query = "UPDATE week_support SET week_index={}"

    update_copy_diary_from_week_into_another_week_query = """UPDATE diary_{}_week SET
        monday_lesson1={},
        monday_lesson2={},
        monday_lesson3={},
        monday_lesson4={},
        monday_lesson5={},
        monday_lesson6={},
        monday_lesson7={},
        monday_lesson8={},
        monday_lesson9={},
        monday_lesson10={},
        monday_lesson11={},
        monday_lesson12={},
        
        tuesday_lesson1={},
        tuesday_lesson2={},
        tuesday_lesson3={},
        tuesday_lesson4={},
        tuesday_lesson5={},
        tuesday_lesson6={},
        tuesday_lesson7={},
        tuesday_lesson8={},
        tuesday_lesson9={},
        tuesday_lesson10={},
        tuesday_lesson11={},
        tuesday_lesson12={},
        
        wednesday_lesson1={},
        wednesday_lesson2={},
        wednesday_lesson3={},
        wednesday_lesson4={},
        wednesday_lesson5={},
        wednesday_lesson6={},
        wednesday_lesson7={},
        wednesday_lesson8={},
        wednesday_lesson9={},
        wednesday_lesson10={},
        wednesday_lesson11={},
        wednesday_lesson12={},
        
        thursday_lesson1={},
        thursday_lesson2={},
        thursday_lesson3={},
        thursday_lesson4={},
        thursday_lesson5={},
        thursday_lesson6={},
        thursday_lesson7={},
        thursday_lesson8={},
        thursday_lesson9={},
        thursday_lesson10={},
        thursday_lesson11={},
        thursday_lesson12={},
        
        friday_lesson1={},
        friday_lesson2={},
        friday_lesson3={},
        friday_lesson4={},
        friday_lesson5={},
        friday_lesson6={},
        friday_lesson7={},
        friday_lesson8={},
        friday_lesson9={},
        friday_lesson10={},
        friday_lesson11={},
        friday_lesson12={},
        
        saturday_lesson1={},
        saturday_lesson2={},
        saturday_lesson3={},
        saturday_lesson4={},
        saturday_lesson5={},
        saturday_lesson6={},
        saturday_lesson7={},
        saturday_lesson8={},
        saturday_lesson9={},
        saturday_lesson10={},
        saturday_lesson11={},
        saturday_lesson12={},
        
        sunday_lesson1={},
        sunday_lesson2={},
        sunday_lesson3={},
        sunday_lesson4={},
        sunday_lesson5={},
        sunday_lesson6={},
        sunday_lesson7={},
        sunday_lesson8={},
        sunday_lesson9={},
        sunday_lesson10={},
        sunday_lesson11={},
        sunday_lesson12={}
    WHERE classroom_id={}"""

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

    print(diary_homework_db)
