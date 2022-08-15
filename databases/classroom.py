from database import *


class ClassroomCommands(DataBase):
    """Initialization"""

    def __init__(self, connection) -> None:
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(ClassroomQueries.create_table_classroom_query)
                cursor.execute(ClassroomQueries.create_table_request_query)

        except Error as e:
            print(e)

    def get_student_id(self, user_id: int, classroom_id: int) -> int:
        """Returns student_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_student_id_query, (user_id, classroom_id))
            return cursor.fetchone()[0]

    def get_student_ids(self, user_ids: list, classroom_id: int) -> list:
        """Returns student_ids by user_ids and classroom_id"""
        if user_ids:
            with self.connection.cursor() as cursor:
                cursor.execute(ClassroomQueries.get_student_ids_query.format(",".join(map(str, user_ids))),
                               (classroom_id,))
                return [row[0] for row in cursor.fetchall()]

        return []

    def get_user_ids(self, student_ids: list) -> list:
        """Returns user_ids by student_ids"""
        if student_ids:
            with self.connection.cursor() as cursor:
                cursor.execute(ClassroomQueries.get_user_ids_query.format(",".join(map(str, student_ids))))
                return [row[0] for row in cursor.fetchall()]

        return []

    def get_classroom_name(self, classroom_id: int) -> str:
        """Get name of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_name_query, (classroom_id,))
            classroom_name = cursor.fetchone()[0]

            return classroom_name

    def get_classroom_access(self, classroom_id: int) -> str:
        """Get access of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_access_query, (classroom_id,))
            access = cursor.fetchone()[0]

            return access

    def get_classroom_members_limit(self, classroom_id: int) -> int:
        """Get access of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_members_limit_query, (classroom_id,))
            members_limit = cursor.fetchone()[0]

            return members_limit

    def get_classroom_invite_code(self, classroom_id: int) -> str:
        """Get invite code of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_invite_code_query, (classroom_id,))
            invite_code = cursor.fetchone()[0]

            return invite_code

    def get_user_classrooms_with_role_id(self, user_id: int) -> dict:
        """Returns user's classrooms_id and his role_id"""
        with self.connection.cursor() as cursor:
            classrooms_dictionary = {}
            cursor.execute(ClassroomQueries.get_user_classrooms_with_role_id_query, (user_id,))
            for (classroom_id, role_id) in cursor:
                classrooms_dictionary[classroom_id] = role_id

            return classrooms_dictionary

    def get_dict_of_classroom_users(self, classroom_id: int) -> dict:
        """Get dict with classroom's members"""
        with self.connection.cursor() as cursor:
            users_dictionary = {}
            cursor.execute(ClassroomQueries.get_list_of_classroom_users_query, (classroom_id,))
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
            cursor.execute(ClassroomQueries.get_customizing_classroom_id_query, (user_id,))
            classroom_id = cursor.fetchone()[0]

            return classroom_id

    def get_information_of_classroom(self, classroom_id: id) -> tuple:
        """Returns name, school_name, access and description"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_information_for_creating_query, (classroom_id,))
            classroom_name, school_name, access, description = cursor.fetchone()

            return classroom_name, school_name, access, description

    def get_list_of_classroom_ids(self) -> list:
        """Returns list of all classroom ids"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_list_of_classroom_ids_query)
            classroom_ids = [row[0] for row in cursor.fetchall()]

            return classroom_ids

    def get_request_information(self, user_id: int, classroom_id: int) -> tuple:
        """Returns information about request"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_request_information_query, (user_id, classroom_id))
            request_information = cursor.fetchone()

            return request_information

    def get_list_of_request_information(self, classroom_id: int) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_list_of_request_information_query, (classroom_id,))

            request_information_list = []
            for user_id, request_classroom_id, request_text, request_datetime in cursor.fetchall():
                request_information_list.append(
                    {
                        "user_id": user_id,
                        "classroom_id": request_classroom_id,
                        "request_text": request_text,
                        "datetime": request_datetime
                    }
                )

            return request_information_list

    def get_classroom_by_invite_code(self, invite_code: str) -> int:
        """Returns classroom id by invite code"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_by_invite_code, (invite_code,))
            classroom_id = cursor.fetchone()

            return classroom_id[0] if classroom_id else -1

    def insert_new_customizer(self, user_id: int) -> None:
        """Insert customizer into UserCustomize"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(ClassroomQueries.insert_new_customizer_query, (user_id,))

        except Error as e:
            print(e)

    def insert_new_user_in_classroom(self, user_id: int, classroom_id: int, role_id: int) -> int:
        """Add user to the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.insert_new_classroom_user_query, (user_id, classroom_id, role_id))
            cursor.execute(ClassroomQueries.get_last_primary_id)
            student_id = cursor.fetchone()[0]

            return student_id

    def insert_new_classroom(self) -> int:
        """Insert new classroom and student-owner"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.insert_classroom_query)
            classroom_id = cursor.fetchone()[0]
            print(classroom_id)

        return classroom_id

    def insert_new_request(self, user_id: int, classroom_id: int, request_text: str) -> None:
        """Inserts new request"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.insert_request_query, (user_id, classroom_id, request_text,
                                                                   current_datetime))

    def update_classroom_name(self, classroom_id: int, new_classroom_name: str) -> None:
        """Set name to the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_name_query, (new_classroom_name, classroom_id))

    def update_school_name(self, classroom_id: int, new_school_name: str) -> None:
        """Update school name of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_school_name_query, (new_school_name, classroom_id))

    def update_classroom_access(self, classroom_id: int, access: str) -> None:
        """Update access of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_access_query, (access, classroom_id))

    def update_classroom_description(self, classroom_id: int, description: str) -> None:
        """Update description of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_description_query, (description, classroom_id))

    def update_classroom_members_limit(self, classroom_id: int, members_limit: int) -> None:
        """Update members_limit of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_members_limit_query, (members_limit, classroom_id))

    def update_classroom_invite_code(self, classroom_id: int, invite_code: str) -> None:
        """Update invite code of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_invite_code_query, (invite_code, classroom_id))

    def update_classroom_created(self, classroom_id: int, created: bool) -> None:
        """Update created of classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_created_query, (created, classroom_id))

    def update_role_id_of_user(self, user_id: int, user_role_id: int) -> None:
        """Set role_id to the user"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_user_role_id_query, (user_role_id, user_id))

    def update_user_customize_classroom_id(self, user_id: int, classroom_id) -> None:
        """Update classroom_id that user is customizing"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_user_customize_classroom_id_query, (classroom_id, user_id))

    def update_request(self, user_id: int, classroom_id: int, new_request_text: str) -> None:
        """Updates request"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_request_query, (new_request_text, current_datetime,
                                                                   user_id, classroom_id))

    def delete_classroom(self, classroom_id: int) -> None:
        """Delete classroom and its owner from Student"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.delete_classroom_query, (classroom_id,))

    def delete_student(self, classroom_id: int, user_id: int) -> None:
        """Deletes user from classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.delete_user_from_classroom_query, (user_id, classroom_id))

    def delete_request(self, user_id: int, classroom_id: int) -> None:
        """Deletes request from Request"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.delete_request_query, (user_id, classroom_id))


class ClassroomQueries:
    create_table_classroom_query = """CREATE TABLE IF NOT EXISTS Classroom(
            classroom_id SERIAL NOT NULL UNIQUE PRIMARY KEY,
            classroom_name VARCHAR(255),
            school_name VARCHAR(255),
            access TEXT,
            description TEXT,
            members_limit INT,
            invite_code TEXT,
            created BOOLEAN
        )"""

    create_table_request_query = """CREATE TABLE IF NOT EXISTS Request(
        user_id INT,
        classroom_id INT,
        request_text TEXT,
        datetime TIMESTAMP,
        
        FOREIGN KEY (user_id) REFERENCES Users (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
    )"""

    get_customizing_classroom_id_query = """SELECT classroom_id FROM UserCustomize WHERE user_id=%s"""
    get_information_for_creating_query = """SELECT 
        classroom_name, 
        school_name,
        access,
        description
    FROM Classroom WHERE classroom_id=%s"""
    get_user_classrooms_with_role_id_query = """SELECT classroom_id, role_id FROM Student WHERE user_id=%s"""
    get_student_id_query = """SELECT student_id FROM Student WHERE user_id=%s AND classroom_id=%s"""
    get_student_ids_query = """SELECT student_id FROM Student WHERE user_id IN ({}) AND classroom_id=%s"""
    get_user_ids_query = """SELECT user_id FROM Student WHERE student_id IN ({})"""
    get_classroom_name_query = """SELECT classroom_name FROM Classroom WHERE classroom_id=%s"""
    get_classroom_access_query = """SELECT access FROM Classroom WHERE classroom_id=%s"""
    get_classroom_members_limit_query = """SELECT members_limit FROM Classroom WHERE classroom_id=%s"""
    get_classroom_invite_code_query = """SELECT invite_code FROM Classroom WHERE classroom_id=%s"""
    get_classroom_by_invite_code = """SELECT classroom_id FROM Classroom WHERE invite_code=%s"""
    get_list_of_classroom_users_query = """SELECT user_id, role_id FROM Student WHERE classroom_id=%s"""
    get_list_of_classroom_ids_query = """SELECT classroom_id FROM Classroom WHERE created=True"""
    get_request_information_query = """SELECT * FROM Request WHERE user_id=%s AND classroom_id=%s"""
    get_list_of_request_information_query = """SELECT * FROM Request WHERE classroom_id=%s"""
    get_last_primary_id = """SELECT MAX(student_id) FROM Student"""

    insert_classroom_query = """INSERT INTO Classroom (members_limit, created) VALUES(40, FALSE) 
    RETURNING classroom_id"""
    insert_new_classroom_user_query = """INSERT INTO Student (user_id, classroom_id, role_id) VALUES(%s, %s, %s)"""
    insert_new_customizer_query = """INSERT INTO UserCustomize VALUES(%s, null, null, null)"""
    insert_request_query = """INSERT INTO Request VALUES(%s, %s, %s, %s)"""

    update_classroom_name_query = """UPDATE Classroom SET classroom_name=%s WHERE classroom_id=%s"""
    update_school_name_query = """UPDATE Classroom SET school_name=%s WHERE classroom_id=%s"""
    update_classroom_access_query = """UPDATE Classroom SET access=%s WHERE classroom_id=%s"""
    update_classroom_description_query = """UPDATE Classroom SET description=%s WHERE classroom_id=%s"""
    update_classroom_members_limit_query = """UPDATE Classroom SET members_limit=%s WHERE classroom_id=%s"""
    update_classroom_invite_code_query = """UPDATE Classroom SET invite_code=%s WHERE classroom_id=%s"""
    update_user_role_id_query = """UPDATE Student SET role_id=%s WHERE user_id=%s"""
    update_user_customize_classroom_id_query = """UPDATE UserCustomize SET classroom_id=%s WHERE user_id=%s"""
    update_classroom_created_query = """UPDATE Classroom SET created=%s WHERE classroom_id=%s"""
    update_request_query = """UPDATE 
        Request SET request_text=%s, datetime=%s 
    WHERE user_id=%s AND classroom_id=%s"""

    delete_user_from_classroom_query = """DELETE FROM Student WHERE user_id=%s AND classroom_id=%s"""
    delete_classroom_query = """DELETE FROM classroom WHERE classroom_id=%s"""
    delete_request_query = """DELETE FROM Request WHERE user_id=%s AND classroom_id=%s"""


if __name__ == "__main__":
    pass
    # connection = connect(
    #     host=HOST,
    #     user=USER,
    #     password=PASSWORD,
    #     database=DATABASE_NAME
    # )
    #
    # db = ClassroomCommands(connection)
    # flag = input("Тестовый режим: ")

    # if flag == "new":
    #     for i in range(1, 55):
    #         if randint(0, 1):
    #             db.insert_new_user_in_classroom(i, 12, choice([32, 33, 33, 34, 35, 36, 37]))
    # elif flag == "del":
    #     for i in range(1, 55):
    #         with connection.cursor() as cursor:
    #             cursor.execute(ClassroomQueries.delete_user_from_classroom_query.format(i))
    #             connection.commit()
