from database import *


class RoleCommands(DataBase):
    def __init__(self, pool: Pool) -> None:
        """Initialization"""
        super().__init__(pool)

    @classmethod
    async def get_self(cls, pool: Pool):
        self = cls(pool)

        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(RoleQueries.create_table_roles_query)
                    await cursor.execute(RoleQueries.create_table_student_query)

        except Error as e:
            print(e)

        return self

    async def get_role_name(self, role_id: int) -> str:
        """Returns role name"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_role_name_query.format(role_id))
                role_name = list(await cursor.fetchone())[0]

                return role_name

    async def get_customizing_role_id(self, user_id: int) -> int:
        """Select role_id that user_id is customizing"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_customizing_role_id_query.format(user_id))
                role_id = list(await cursor.fetchone())[0]

                return role_id

    async def get_default_role_id(self, classroom_id: int) -> int:
        """Returns default role's id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_default_role_id_query.format(classroom_id))
                role_id = list(await cursor.fetchone())[0]

                return role_id

    async def get_admin_role_id(self, classroom_id: int) -> int:
        """Returns admin role's id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_admin_role_id_query.format(classroom_id))
                role_id = list(await cursor.fetchone())[0]

                return role_id

    async def get_role_id_by_name(self, classroom_id: int, role_name: str) -> int:
        """Returns role's id by name"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_role_id_by_name_query.format(classroom_id, role_name))
                role_id = list(await cursor.fetchone())[0]

                return role_id

    async def get_role_id_by_user_id(self, user_id: int, classroom_id: id) -> int:
        """Returns role's id by user_id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_role_id_by_user_id_query.format(user_id, classroom_id))
                role_id = list(await cursor.fetchone())[0]

                return role_id

    async def get_default_role_name(self, classroom_id: int) -> str:
        """Returns default role's name"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_default_role_name_query.format(classroom_id))
                default_role_name = list(await cursor.fetchone())[0]

                return default_role_name

    async def get_admin_role_name(self, classroom_id: int) -> str:
        """Returns admin role's name"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_admin_role_name_query.format(classroom_id))
                admin_role_name = list(await cursor.fetchone())[0]

                return admin_role_name

    async def get_all_role_names_from_classroom(self, classroom_id: int) -> list:
        """Returns all role names from classroom"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.get_all_role_names_from_classroom_query.format(classroom_id))
                role_names = [row[0] for row in list(await cursor.fetchall())]

                return role_names

    async def get_role_properties_dict(self, role_id: int) -> dict:
        """Returns all role's properties"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.show_columns_query)
                property_names = [row[0] for row in list(await cursor.fetchall())][2:]

                await cursor.execute(RoleQueries.get_all_role_properties_query.format(role_id))
                property_values = list(await cursor.fetchone())[2:]

                return {name: value for name, value in zip(property_names, property_values)}

    async def get_diary_role_properties_dict(self, role_id: int) -> dict:
        """Returns role's diary properties"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                property_names = [
                    "change_current_homework",
                    "change_next_homework",
                    "change_standard_week",
                    "change_current_week",
                    "change_next_week",
                    "role_name",
                    "is_default_member",
                    "is_admin"
                ]

                await cursor.execute(RoleQueries.get_diary_role_properties_query.format(role_id))
                property_values = list(await cursor.fetchone())

                return {name: value for name, value in zip(property_names, property_values)}

    async def get_members_role_properties_dict(self, role_id: int) -> dict:
        """Returns role's members properties"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                property_names = [
                    "kick_members",
                    "invite_members",
                    "accept_requests",
                    "notify",
                    "redact_events",
                    "role_name",
                    "is_default_member",
                    "is_admin"
                ]

                await cursor.execute(RoleQueries.get_members_role_properties_query.format(role_id))
                property_values = list(await cursor.fetchone())

                return {name: value for name, value in zip(property_names, property_values)}

    async def get_classroom_role_properties_dict(self, role_id: int) -> dict:
        """Returns role's classroom properties"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                property_names = [
                    "change_classroom_name",
                    "change_school_name",
                    "change_classroom_access",
                    "change_description",
                    "change_members_limit",
                    "role_name",
                    "is_default_member",
                    "is_admin"
                ]

                await cursor.execute(RoleQueries.get_classroom_role_properties_query.format(role_id))
                property_values = list(await cursor.fetchone())

                return {name: value for name, value in zip(property_names, property_values)}

    async def insert_new_role(self, classroom_id: int, role_name: str, is_default_member=False, is_admin=False) -> int:
        """Inserts new role into Role"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                if is_admin:
                    kick_members = True
                else:
                    kick_members = False

                if is_default_member or is_admin:
                    await cursor.execute(
                        RoleQueries.insert_new_default_role_query.format(classroom_id, role_name, kick_members,
                                                                         is_default_member, is_admin))
                else:
                    await cursor.execute(RoleQueries.get_default_role_id_query.format(classroom_id))
                    default_role_id = list(await cursor.fetchone())[0]
                    await cursor.execute(RoleQueries.get_all_role_properties_query.format(default_role_id))
                    default_role_properties = list(await cursor.fetchone())[3:-2]
                    await cursor.execute(RoleQueries.insert_new_role_query.format(classroom_id, role_name,
                                                                                  *default_role_properties, False,
                                                                                  False))

                await connection.commit()

                return cursor.lastrowid

    async def update_student_role(self, user_id: int, new_role_id: int) -> None:
        """Updates student's role with new role_id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.update_student_role_query.format(new_role_id,
                                                                                  user_id))
                await connection.commit()

    async def update_all_roles(self, old_role_id: int, new_role_id: int) -> None:
        """Updates students' role with new role_id"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.update_all_roles_query.format(new_role_id, old_role_id))
                await connection.commit()

    async def update_user_customize_role_id(self, user_id: int, role_id) -> None:
        """Update role_id that user is customizing"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.update_user_customize_role_id_query.format(role_id, user_id))
                await connection.commit()

    async def update_role_name(self, role_id: int, new_name: str) -> None:
        """Updates role's name"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.update_role_name_query.format(new_name, role_id))
                await connection.commit()

    async def update_role_privilege(self, role_id: int, new_value: bool, privilege_type: str) -> None:
        """Updates role's privilege_type"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.update_role_privilege_query.format(privilege_type, new_value, role_id))
                await connection.commit()

    async def delete_role(self, role_id: int) -> None:
        """Deletes role"""
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(RoleQueries.delete_role_query.format(role_id))
                await connection.commit()


class RoleQueries:
    create_table_roles_query = """CREATE TABLE IF NOT EXISTS Role(
        role_id INT PRIMARY KEY AUTO_INCREMENT,
        classroom_id INT,
        role_name TEXT,
        change_current_homework BOOLEAN DEFAULT 1,
        change_next_homework BOOLEAN DEFAULT 1,
        change_standard_week BOOLEAN DEFAULT 1,
        change_current_week BOOLEAN DEFAULT 1,
        change_next_week BOOLEAN DEFAULT 1,
        kick_members BOOLEAN DEFAULT 0,
        invite_members BOOLEAN DEFAULT 1,
        accept_requests BOOLEAN DEFAULT 1,
        notify BOOLEAN DEFAULT 1,
        redact_events BOOLEAN DEFAULT 1,
        change_classroom_name BOOLEAN DEFAULT 1,
        change_school_name BOOLEAN DEFAULT 1,
        change_classroom_access BOOLEAN DEFAULT 1,
        change_description BOOLEAN DEFAULT 1,
        change_members_limit BOOLEAN DEFAULT 1,
        is_default_member BOOLEAN DEFAULT 0,
        is_admin BOOLEAN DEFAULT 0,
        
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
    )"""

    create_table_student_query = """CREATE TABLE IF NOT EXISTS Student(
        student_id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        classroom_id INT,
        role_id INT,
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES Role (role_id) ON DELETE SET NULL
    )"""

    get_customizing_role_id_query = """SELECT role_id FROM UserCustomize WHERE user_id={}"""
    get_default_role_name_query = """SELECT role_name FROM Role WHERE classroom_id={} AND is_default_member=1"""
    get_admin_role_name_query = """SELECT role_name FROM Role WHERE classroom_id={} AND is_admin=1"""
    get_role_name_query = """SELECT role_name FROM Role WHERE role_id={}"""
    get_default_role_id_query = """SELECT role_id FROM Role WHERE classroom_id={} AND is_default_member=1"""
    get_admin_role_id_query = """SELECT role_id FROM Role WHERE classroom_id={} AND is_admin=1"""
    get_role_id_by_name_query = """SELECT role_id FROM Role WHERE classroom_id={} AND role_name='{}'"""
    get_role_id_by_user_id_query = """SELECT role_id FROM Student WHERE user_id={} AND classroom_id={}"""
    get_all_role_names_from_classroom_query = """SELECT role_name FROM Role WHERE classroom_id={}"""
    get_all_role_properties_query = """SELECT * FROM Role WHERE role_id={}"""

    get_diary_role_properties_query = """SELECT 
        change_current_homework, 
        change_next_homework, 
        change_standard_week,
        change_current_week,
        change_next_week,
        role_name,
        is_default_member,
        is_admin
    FROM Role WHERE role_id={}"""

    get_members_role_properties_query = """SELECT
        kick_members,
        invite_members,
        accept_requests,
        notify,
        redact_events,
        role_name,
        is_default_member,
        is_admin
    FROM Role WHERE role_id={}"""

    get_classroom_role_properties_query = """SELECT
        change_classroom_name,
        change_school_name,
        change_classroom_access,
        change_description,
        change_members_limit,
        role_name,
        is_default_member,
        is_admin
    FROM Role WHERE role_id={}"""

    insert_new_default_role_query = """INSERT INTO Role 
    (classroom_id, role_name, kick_members, is_default_member, is_admin) VALUES(
        {}, '{}', {}, {}, {}
    )"""

    insert_new_role_query = """INSERT INTO ROLE
    (classroom_id, role_name, change_standard_week, change_current_week, change_next_week, change_current_homework,
    change_next_homework, kick_members, invite_members, accept_requests, notify, redact_events, change_classroom_name,
    change_school_name, change_classroom_access, change_description, change_members_limit) VALUES(
        {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    )"""

    update_student_role_query = """UPDATE Student SET role_id={} WHERE user_id={}"""
    update_all_roles_query = """UPDATE Student SET role_id={} WHERE role_id={}"""
    update_user_customize_role_id_query = """UPDATE UserCustomize SET role_id={} WHERE user_id={}"""

    update_role_name_query = """UPDATE Role SET role_name='{}' WHERE role_id={}"""
    update_role_privilege_query = """UPDATE Role SET {}={} WHERE role_id={}"""

    delete_role_query = """DELETE FROM Role WHERE role_id={}"""

    # extra queries
    show_columns_query = """SHOW columns FROM Role"""


if __name__ == '__main__':
    pass
    # connection = connect(
    #     host=HOST,
    #     user=USER,
    #     password=PASSWORD,
    #     db=DATABASE_NAME
    # )
    #
    # roles_db = RoleCommands(connection)
    # print(roles_db.get_role_properties_dict(28))
