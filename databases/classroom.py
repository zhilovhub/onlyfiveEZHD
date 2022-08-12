from database import *


class ClassroomCommands(DataBase):
    """Initialization"""

    def __init__(self, pool: Pool) -> None:
        super().__init__(pool)

    @classmethod
    async def get_self(cls, pool: Pool):
        self = cls(pool)

        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(ClassroomQueries.create_table_classroom_query)
                    await cursor.execute(ClassroomQueries.create_table_request_query)

        except Error as e:
            print(e)

        return self

    async def get_student_id(self, user_id: int, classroom_id: int) -> int:
        """Returns student_id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_student_id_query, (user_id, classroom_id))
                return list(await cursor.fetchone())[0]

    async def get_student_ids(self, user_ids: list, classroom_id: int) -> list:
        """Returns student_ids by user_ids and classroom_id"""
        if user_ids:
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(ClassroomQueries.get_student_ids_query.format(",".join(map(str, user_ids))),
                                         (classroom_id,))
                    return [row[0] for row in list(await cursor.fetchall())]

        return []

    async def get_user_ids(self, student_ids: list) -> list:
        """Returns user_ids by student_ids"""
        if student_ids:
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(ClassroomQueries.get_user_ids_query.format(",".join(map(str, student_ids))))
                    return [row[0] for row in list(await cursor.fetchall())]

        return []

    async def get_classroom_name(self, classroom_id: int) -> str:
        """Get name of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_classroom_name_query.format(classroom_id))
                classroom_name = list(await cursor.fetchone())[0]

                return classroom_name

    async def get_classroom_access(self, classroom_id: int) -> str:
        """Get access of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_classroom_access_query.format(classroom_id))
                access = list(await cursor.fetchone())[0]

                return access

    async def get_classroom_members_limit(self, classroom_id: int) -> int:
        """Get access of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_classroom_members_limit_query.format(classroom_id))
                members_limit = list(await cursor.fetchone())[0]

                return members_limit

    async def get_classroom_invite_code(self, classroom_id: int) -> str:
        """Get invite code of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_classroom_invite_code_query, (classroom_id,))
                invite_code = list(await cursor.fetchone())[0]

                return invite_code

    async def get_user_classrooms_with_role_id(self, user_id: int) -> dict:
        """Returns user's classrooms_id and his role_id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                classrooms_dictionary = {}
                await cursor.execute(ClassroomQueries.get_user_classrooms_with_role_id_query.format(user_id))
                for (classroom_id, role_id) in await cursor.fetchall():
                    classrooms_dictionary[classroom_id] = role_id

                return classrooms_dictionary

    async def get_dict_of_classroom_users(self, classroom_id: int) -> dict:
        """Get dict with classroom's members"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                users_dictionary = {}
                await cursor.execute(ClassroomQueries.get_list_of_classroom_users_query.format(classroom_id))
                for (user_id, user_role_id) in await cursor.fetchall():
                    users_dictionary[user_id] = user_role_id

                return users_dictionary

    async def get_dict_of_classroom_roles(self, classroom_id: int) -> dict:
        """Returns dict with classroom's roles"""
        members_dictionary = await self.get_dict_of_classroom_users(classroom_id)

        roles_dictionary = {}
        for member_id, role_id in members_dictionary.items():
            if role_id in roles_dictionary:
                roles_dictionary[role_id].append(member_id)
            else:
                roles_dictionary[role_id] = [member_id]

        return roles_dictionary

    async def get_customizing_classroom_id(self, user_id: int) -> int:
        """Select classroomd_id that user_id is customizing"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_customizing_classroom_id_query.format(user_id))
                classroom_id = list(await cursor.fetchone())[0]

                return classroom_id

    async def get_information_of_classroom(self, classroom_id: id) -> tuple:
        """Returns name, school_name, access and description"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_information_for_creating_query.format(classroom_id))
                classroom_name, school_name, access, description = await cursor.fetchone()

                return classroom_name, school_name, access, description

    async def get_list_of_classroom_ids(self) -> list:
        """Returns list of all classroom ids"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_list_of_classroom_ids_query)
                classroom_ids = [row[0] for row in list(await cursor.fetchall())]

                return classroom_ids

    async def get_request_information(self, user_id: int, classroom_id: int) -> tuple:
        """Returns information about request"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_request_information_query.format(user_id, classroom_id))
                request_information = await cursor.fetchone()

                return request_information

    async def get_list_of_request_information(self, classroom_id: int) -> list:
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_list_of_request_information_query.format(classroom_id))

                request_information_list = []
                for user_id, request_classroom_id, request_text, request_datetime in list(await cursor.fetchall()):
                    request_information_list.append(
                        {
                            "user_id": user_id,
                            "classroom_id": request_classroom_id,
                            "request_text": request_text,
                            "datetime": request_datetime
                        }
                    )

                return request_information_list

    async def get_classroom_by_invite_code(self, invite_code: str) -> int:
        """Returns classroom id by invite code"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.get_classroom_by_invite_code, (invite_code,))
                classroom_id = list(await cursor.fetchone())

                return classroom_id[0] if classroom_id else -1

    async def insert_new_customizer(self, user_id: int) -> None:
        """Insert customizer into UserCustomize"""
        async with self.pool.acquire() as connection:
            try:
                async with connection.cursor() as cursor:
                    await cursor.execute(ClassroomQueries.insert_new_customizer_query.format(user_id))
                    await connection.commit()
            except Error as e:
                print(e)

    async def insert_new_user_in_classroom(self, user_id: int, classroom_id: int, role_id: int) -> int:
        """Add user to the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    ClassroomQueries.insert_new_classroom_user_query.format(user_id, classroom_id, role_id))
                await cursor.execute(ClassroomQueries.get_last_primary_id)
                student_id = list(await cursor.fetchone())[0]
                await connection.commit()

            return student_id

    async def insert_new_classroom(self) -> int:
        """Insert new classroom and student-owner"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.insert_classroom_query)
                classroom_id = cursor.lastrowid
                await connection.commit()

        return classroom_id

    async def insert_new_request(self, user_id: int, classroom_id: int, request_text: str) -> None:
        """Inserts new request"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.insert_request_query.format(user_id, classroom_id, request_text,
                                                                                  current_datetime))
                await connection.commit()

    async def update_classroom_name(self, classroom_id: int, new_classroom_name: str) -> None:
        """Set name to the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    ClassroomQueries.update_classroom_name_query.format(new_classroom_name, classroom_id))
                await connection.commit()

    async def update_school_name(self, classroom_id: int, new_school_name: str) -> None:
        """Update school name of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.update_school_name_query.format(new_school_name, classroom_id))
                await connection.commit()

    async def update_classroom_access(self, classroom_id: int, access: str) -> None:
        """Update access of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.update_classroom_access_query.format(access, classroom_id))
                await connection.commit()

    async def update_classroom_description(self, classroom_id: int, description: str) -> None:
        """Update description of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    ClassroomQueries.update_classroom_description_query.format(description, classroom_id))
                await connection.commit()

    async def update_classroom_members_limit(self, classroom_id: int, members_limit: int) -> None:
        """Update members_limit of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    ClassroomQueries.update_classroom_members_limit_query.format(members_limit, classroom_id))
                await connection.commit()

    async def update_classroom_invite_code(self, classroom_id: int, invite_code: str) -> None:
        """Update invite code of the classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.update_classroom_invite_code_query, (invite_code, classroom_id))
                await connection.commit()

    async def update_classroom_created(self, classroom_id: int, created: bool) -> None:
        """Update created of classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.update_classroom_created_query.format(created, classroom_id))
                await connection.commit()

    async def update_role_id_of_user(self, user_id: int, user_role_id: int) -> None:
        """Set role_id to the user"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.update_user_role_id_query.format(user_role_id, user_id))
                await connection.commit()

    async def update_user_customize_classroom_id(self, user_id: int, classroom_id) -> None:
        """Update classroom_id that user is customizing"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    ClassroomQueries.update_user_customize_classroom_id_query.format(classroom_id, user_id))
                await connection.commit()

    async def update_request(self, user_id: int, classroom_id: int, new_request_text: str) -> None:
        """Updates request"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.update_request_query.format(new_request_text, current_datetime,
                                                                                  user_id, classroom_id))

    async def delete_classroom(self, classroom_id: int) -> None:
        """Delete classroom and its owner from Student"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.delete_classroom_query.format(classroom_id))
                await connection.commit()

    async def delete_student(self, classroom_id: int, user_id: int) -> None:
        """Deletes user from classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.delete_user_from_classroom_query.format(user_id, classroom_id))
                await connection.commit()

    async def delete_request(self, user_id: int, classroom_id: int) -> None:
        """Deletes request from Request"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(ClassroomQueries.delete_request_query.format(user_id, classroom_id))
                await connection.commit()


class ClassroomQueries:
    create_table_classroom_query = """CREATE TABLE IF NOT EXISTS Classroom(
            classroom_id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
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
        datetime DATETIME,
        
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
    )"""

    get_customizing_classroom_id_query = """SELECT classroom_id FROM UserCustomize WHERE user_id={}"""
    get_information_for_creating_query = """SELECT 
        classroom_name, 
        school_name,
        access,
        description
    FROM Classroom WHERE classroom_id={}"""
    get_user_classrooms_with_role_id_query = """SELECT classroom_id, role_id FROM Student WHERE user_id={}"""
    get_student_id_query = """SELECT student_id FROM Student WHERE user_id=%s AND classroom_id=%s"""
    get_student_ids_query = """SELECT student_id FROM Student WHERE user_id IN ({}) AND classroom_id=%s"""
    get_user_ids_query = """SELECT user_id FROM Student WHERE student_id IN ({})"""
    get_classroom_name_query = """SELECT classroom_name FROM Classroom WHERE classroom_id={}"""
    get_classroom_access_query = """SELECT access FROM Classroom WHERE classroom_id={}"""
    get_classroom_members_limit_query = """SELECT members_limit FROM Classroom WHERE classroom_id={}"""
    get_classroom_invite_code_query = """SELECT invite_code FROM Classroom WHERE classroom_id=%s"""
    get_classroom_by_invite_code = """SELECT classroom_id FROM Classroom WHERE invite_code=%s"""
    get_list_of_classroom_users_query = """SELECT user_id, role_id FROM Student WHERE classroom_id={}"""
    get_list_of_classroom_ids_query = """SELECT classroom_id FROM Classroom WHERE created=1"""
    get_request_information_query = """SELECT * FROM Request WHERE user_id={} AND classroom_id={}"""
    get_list_of_request_information_query = """SELECT * FROM Request WHERE classroom_id={}"""
    get_last_primary_id = """SELECT MAX(student_id) FROM Student"""

    insert_classroom_query = """INSERT INTO Classroom (members_limit, created) VALUES(40, FALSE)"""
    insert_new_classroom_user_query = """INSERT INTO Student (user_id, classroom_id, role_id) VALUES({}, {}, {})"""
    insert_new_customizer_query = """INSERT INTO UserCustomize VALUES({}, null, null, null)"""
    insert_request_query = """INSERT INTO Request VALUES({}, {}, '{}', '{}')"""

    update_classroom_name_query = """UPDATE Classroom SET classroom_name="{}" WHERE classroom_id={}"""
    update_school_name_query = """UPDATE Classroom SET school_name="{}" WHERE classroom_id={}"""
    update_classroom_access_query = """UPDATE Classroom SET access="{}" WHERE classroom_id={}"""
    update_classroom_description_query = """UPDATE Classroom SET description="{}" WHERE classroom_id={}"""
    update_classroom_members_limit_query = """UPDATE Classroom SET members_limit={} WHERE classroom_id={}"""
    update_classroom_invite_code_query = """UPDATE Classroom SET invite_code=%s WHERE classroom_id=%s"""
    update_user_role_id_query = """UPDATE Student SET role_id={} WHERE user_id={}"""
    update_user_customize_classroom_id_query = """UPDATE UserCustomize SET classroom_id={} WHERE user_id={}"""
    update_classroom_created_query = """UPDATE Classroom SET created={} WHERE classroom_id={}"""
    update_request_query = """UPDATE 
        Request SET request_text='{}', datetime='{}' 
    WHERE user_id={} AND classroom_id={}"""

    delete_user_from_classroom_query = """DELETE FROM Student WHERE user_id={} AND classroom_id={}"""
    delete_classroom_query = """DELETE FROM classroom WHERE classroom_id={}"""
    delete_request_query = """DELETE FROM Request WHERE user_id={} AND classroom_id={}"""


if __name__ == "__main__":
    flag = input("Тестовый режим: ")

    # connection = connect(
    #     host=HOST,
    #     user=USER,
    #     password=PASSWORD,
    #     db=DATABASE_NAME
    # )
    #
    # db = ClassroomCommands(connection)
    #
    # if flag == "new":
    #     for i in range(1, 55):
    #         if randint(0, 1):
    #             db.insert_new_user_in_classroom(i, 12, choice([32, 33, 33, 34, 35, 36, 37]))
    # elif flag == "del":
    #     for i in range(1, 55):
    #         with connection.cursor() as cursor:
    #             await cursor.execute(ClassroomQueries.delete_user_from_classroom_query.format(i))
    #             connection.commit()
