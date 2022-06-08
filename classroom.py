from config import *


class ClassroomCommands:
    def __init__(self, classroom_id):
        self.classroom_id = classroom_id

    def get_classroom_name(self):
        try:
            with connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(ClassroomQueries.get_classroom_name_query.format(self.classroom_id))
                    classroom_name = cursor.fetchone()[0]

                    return classroom_name

        except Error as e:
            print(e)

    def set_classroom_name(self, new_classroom_name):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(ClassroomQueries.set_classroom_name_query.format(new_classroom_name, self.classroom_id))
                    connection.commit()

        except Error as e:
            print(e)

    # finish this function with Ilya
    def add_new_user_in_classroom(self):
        pass

    def set_role_of_user(self, user_id, user_role):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(ClassroomQueries.set_user_role_query.format(user_role, user_id))
                    connection.commit()

        except Error as e:
            print(e)

    def get_list_of_classroom_users(self):
        try:
            with connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=DATABASE_NAME
            ) as connection:
                with connection.cursor() as cursor:
                    users_dictionary = {}
                    cursor.execute(ClassroomQueries.get_list_of_classroom_users_query.format(self.classroom_id))
                    for (user_id, user_role) in cursor:
                        users_dictionary[user_id] = user_role

                    return users_dictionary

        except Error as e:
            print(e)


class ClassroomQueries:
    get_classroom_name_query = """SELECT classroom_name FROM Classroom WHERE classroom_id={}"""

    set_classroom_name_query = """UPDATE Classroom SET classroom_name={} WHERE classroom_id={}"""

    insert_new_classroom_user_query = """INSERT INTO Student VALUES=({}, {}, {})"""  # finish this query with Ilya

    set_user_role_query = """UPDATE Student SET role={} WHERE user_id={}"""

    del_user_from_classroom_query = """DELETE FROM Student WHERE user_id={}"""

    get_list_of_classroom_users_query = """SELECT user_id, role FROM Student WHERE classroom_id={}"""


if __name__ == "__main__":
    pass
