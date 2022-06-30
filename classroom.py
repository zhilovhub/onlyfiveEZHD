from database import *


class ClassroomCommands(DataBase):
    """Initialization"""
    def __init__(self, connection: CMySQLConnection) -> None:
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(ClassroomQueries.create_table_classroom_query)
                cursor.execute(ClassroomQueries.create_table_user_customize_query)

        except Error as e:
            print(e)

    def get_classroom_name(self, classroom_id: int) -> str:
        """Get name of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_name_query.format(classroom_id))
            classroom_name = cursor.fetchone()[0]

            return classroom_name

    def get_classroom_access(self, classroom_id: int) -> str:
        """Get access of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_access_query.format(classroom_id))
            access = cursor.fetchone()[0]

            return access

    def get_classroom_members_limit(self, classroom_id: int) -> int:
        """Get access of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_members_limit_query.format(classroom_id))
            members_limit = cursor.fetchone()[0]

            return members_limit

    def get_user_classrooms_with_role_id(self, user_id: int) -> dict:
        """Returns user's classrooms_id and his role_id"""
        with self.connection.cursor() as cursor:
            classrooms_dictionary = {}
            cursor.execute(ClassroomQueries.get_user_classrooms_with_role_id.format(user_id))
            for (classroom_id, role_id) in cursor:
                classrooms_dictionary[classroom_id] = role_id

            return classrooms_dictionary

    def get_dict_of_classroom_users(self, classroom_id: int) -> dict:
        """Get dict with classroom's members"""
        with self.connection.cursor() as cursor:
            users_dictionary = {}
            cursor.execute(ClassroomQueries.get_list_of_classroom_users_query.format(classroom_id))
            for (user_id, user_role_id) in cursor:
                users_dictionary[user_id] = user_role_id

            return users_dictionary

    def get_dict_of_classroom_roles(self, classroom_id: int) -> dict:
        """Returns dict with classroom's roles"""
        members_dictionary = self.get_dict_of_classroom_users(classroom_id)

        roles_dictionary = {}
        for member_id, role_id in members_dictionary.items():
            if role_id in roles_dictionary:
                roles_dictionary[role_id].append(member_id)
            else:
                roles_dictionary[role_id] = [member_id]

        return roles_dictionary

    def get_customizing_classroom_id(self, user_id: int) -> int:
        """Select classroomd_id that user_id is customizing"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_customizing_classroom_id_query.format(user_id))
            classroom_id = cursor.fetchone()[0]

            return classroom_id

    def get_information_of_classroom(self, classroom_id: id) -> tuple:
        """Returns name, school_name, access and description"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_information_for_creating_query.format(classroom_id))
            classroom_name, school_name, access, description = cursor.fetchone()

            return classroom_name, school_name, access, description

    def get_list_of_classroom_ids(self) -> list:
        """Returns list of all classroom ids"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_list_of_classroom_ids)
            classroom_ids = [row[0] for row in cursor.fetchall()]

            return classroom_ids

    def insert_new_customizer(self, user_id: int) -> None:
        """Insert customizer into UserCustomize"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(ClassroomQueries.insert_new_customizer_query.format(user_id))
                self.connection.commit()

        except Error as e:
            print(e)

    def insert_new_user_in_classroom(self, user_id: int, classroom_id: int, role_id: int) -> None:
        """Add user to the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.insert_new_classroom_user_query.format(user_id, classroom_id, role_id))
            self.connection.commit()

    def insert_new_classroom(self) -> int:
        """Insert new classroom and student-owner"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.insert_classroom_query)
            classroom_id = cursor.lastrowid

        return classroom_id

    def update_classroom_name(self, classroom_id: int, new_classroom_name: str) -> None:
        """Set name to the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_name_query.format(new_classroom_name, classroom_id))
            self.connection.commit()

    def update_school_name(self, classroom_id: int, new_school_name: str) -> None:
        """Update school name of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_school_name_query.format(new_school_name, classroom_id))
            self.connection.commit()

    def update_classroom_access(self, classroom_id: int, access: str) -> None:
        """Update access of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_access_query.format(access, classroom_id))
            self.connection.commit()

    def update_classroom_description(self, classroom_id: int, description: str) -> None:
        """Update description of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_description_query.format(description, classroom_id))
            self.connection.commit()

    def update_classroom_members_limit(self, classroom_id: int, members_limit: int) -> None:
        """Update members_limit of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_members_limit_query.format(members_limit, classroom_id))
            self.connection.commit()

    def update_classroom_created(self, classroom_id: int, created: bool) -> None:
        """Update created of classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_created_query.format(created, classroom_id))
            self.connection.commit()

    def update_role_id_of_user(self, user_id: int, user_role_id: int) -> None:
        """Set role_id to the user"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_user_role_id_query.format(user_role_id, user_id))
            self.connection.commit()

    def update_user_customize_classroom(self, user_id: int, classroom_id) -> None:
        """Update classroom_id that user is customizing"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_user_customize_query.format(classroom_id, user_id))
            self.connection.commit()

    def delete_classroom(self, classroom_id: int) -> None:
        """Delete classroom and its owner from Student"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.delete_classroom_query.format(classroom_id))
            self.connection.commit()

    def delete_student(self, classroom_id: int, user_id: int) -> None:
        """Deletes user from classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.delete_user_from_classroom_query.format(user_id, classroom_id))
            self.connection.commit()


class ClassroomQueries:
    create_table_classroom_query = """CREATE TABLE IF NOT EXISTS Classroom(
            classroom_id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
            classroom_name VARCHAR(255),
            school_name VARCHAR(255),
            access TEXT,
            description TEXT,
            members_limit INT,
            created BOOLEAN
        )"""

    create_table_user_customize_query = """CREATE TABLE IF NOT EXISTS UserCustomize(
            user_id INT UNIQUE,
            classroom_id INT,
            FOREIGN KEY (user_id) REFERENCES User (user_id),
            FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE SET NULL
        )"""

    get_customizing_classroom_id_query = """SELECT classroom_id FROM UserCustomize WHERE user_id={}"""
    get_information_for_creating_query = """SELECT 
        classroom_name, 
        school_name,
        access,
        description
    FROM Classroom WHERE classroom_id={}"""
    get_user_classrooms_with_role_id = """SELECT classroom_id, role_id FROM Student WHERE user_id={}"""
    get_classroom_name_query = """SELECT classroom_name FROM Classroom WHERE classroom_id={}"""
    get_classroom_access_query = """SELECT access FROM Classroom WHERE classroom_id={}"""
    get_classroom_members_limit_query = """SELECT members_limit FROM Classroom WHERE classroom_id={}"""
    get_list_of_classroom_users_query = """SELECT user_id, role_id FROM Student WHERE classroom_id={}"""
    get_list_of_classroom_ids = """SELECT classroom_id FROM Classroom"""

    insert_classroom_query = """INSERT INTO Classroom (members_limit, created) VALUES(40, FALSE)"""
    insert_new_classroom_user_query = """INSERT INTO Student VALUES({}, {}, {})"""
    insert_new_customizer_query = """INSERT INTO UserCustomize VALUES({}, null)"""

    update_classroom_name_query = """UPDATE Classroom SET classroom_name="{}" WHERE classroom_id={}"""
    update_school_name_query = """UPDATE Classroom SET school_name="{}" WHERE classroom_id={}"""
    update_classroom_access_query = """UPDATE Classroom SET access="{}" WHERE classroom_id={}"""
    update_classroom_description_query = """UPDATE Classroom SET description="{}" WHERE classroom_id={}"""
    update_classroom_members_limit_query = """UPDATE Classroom SET members_limit={} WHERE classroom_id={}"""
    update_user_role_id_query = """UPDATE Student SET role_id={} WHERE user_id={}"""
    update_user_customize_query = """UPDATE UserCustomize SET classroom_id={} WHERE user_id={}"""
    update_classroom_created_query = """UPDATE Classroom SET created={} WHERE classroom_id={}"""

    delete_user_from_classroom_query = """DELETE FROM Student WHERE user_id={} AND classroom_id={}"""
    delete_classroom_query = """DELETE FROM classroom WHERE classroom_id={}"""


if __name__ == "__main__":
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    db = ClassroomCommands(connection)
    flag = input("Тестовый режим: ")

    # if flag == "new":
    #     for i in range(1, 55):
    #         if randint(0, 1):
    #             db.insert_new_user_in_classroom(i, 12, choice([32, 33, 33, 34, 35, 36, 37]))
    # elif flag == "del":
    #     for i in range(1, 55):
    #         with connection.cursor() as cursor:
    #             cursor.execute(ClassroomQueries.delete_user_from_classroom_query.format(i))
    #             connection.commit()
