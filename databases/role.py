from database import *


class RoleCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.create_table_roles_query)
            cursor.execute(RoleQueries.create_table_student_query)

    def get_role_name(self, role_id: int) -> str:
        """Returns role name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_role_name_query.format(role_id))
            role_name = cursor.fetchone()[0]

            return role_name

    def get_customizing_role_id(self, user_id: int) -> int:
        """Select role_id that user_id is customizing"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_customizing_role_id_query.format(user_id))
            role_id = cursor.fetchone()[0]

            return role_id

    def get_default_role_id(self, classroom_id: int) -> int:
        """Returns default role's id"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_default_role_id_query.format(classroom_id))
            role_id = cursor.fetchone()[0]

            return role_id

    def get_admin_role_id(self, classroom_id: int) -> int:
        """Returns admin role's id"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_admin_role_id_query.format(classroom_id))
            role_id = cursor.fetchone()[0]

            return role_id

    def get_role_id_by_name(self, classroom_id: int, role_name: str) -> int:
        """Returns role's id by name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_role_id_by_name_query.format(classroom_id, role_name))
            role_id = cursor.fetchone()[0]

            return role_id

    def get_role_id_by_user_id(self, user_id: int, classroom_id: id) -> int:
        """Returns role's id by user_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_role_id_by_user_id_query.format(user_id, classroom_id))
            role_id = cursor.fetchone()[0]

            return role_id

    def get_default_role_name(self, classroom_id: int) -> str:
        """Returns default role's name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_default_role_name_query.format(classroom_id))
            default_role_name = cursor.fetchone()[0]

            return default_role_name

    def get_admin_role_name(self, classroom_id: int) -> str:
        """Returns admin role's name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_admin_role_name_query.format(classroom_id))
            admin_role_name = cursor.fetchone()[0]

            return admin_role_name

    def get_all_role_names_from_classroom(self, classroom_id: int) -> list:
        """Returns all role names from classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_all_role_names_from_classroom_query.format(classroom_id))
            role_names = [row[0] for row in cursor.fetchall()]

            return role_names

    def get_role_properties_dict(self, role_id: int) -> dict:
        """Returns all role's properties"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.show_columns_query)
            property_names = [row[0] for row in cursor.fetchall()][2:]

            cursor.execute(RoleQueries.get_all_role_properties_query.format(role_id))
            property_values = cursor.fetchone()[2:]

            return {name: value for name, value in zip(property_names, property_values)}

    def get_diary_role_properties_dict(self, role_id: int) -> dict:
        """Returns role's diary properties"""
        with self.connection.cursor() as cursor:
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

            cursor.execute(RoleQueries.get_diary_role_properties_query.format(role_id))
            property_values = cursor.fetchone()

            return {name: value for name, value in zip(property_names, property_values)}

    def get_members_role_properties_dict(self, role_id: int) -> dict:
        """Returns role's members properties"""
        with self.connection.cursor() as cursor:
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

            cursor.execute(RoleQueries.get_members_role_properties_query.format(role_id))
            property_values = cursor.fetchone()

            return {name: value for name, value in zip(property_names, property_values)}

    def get_classroom_role_properties_dict(self, role_id: int) -> dict:
        """Returns role's classroom properties"""
        with self.connection.cursor() as cursor:
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

            cursor.execute(RoleQueries.get_classroom_role_properties_query.format(role_id))
            property_values = cursor.fetchone()

            return {name: value for name, value in zip(property_names, property_values)}

    def insert_new_role(self, classroom_id: int, role_name: str, is_default_member=False, is_admin=False) -> int:
        """Inserts new role into Role"""
        with self.connection.cursor() as cursor:
            if is_admin:
                kick_members = True
            else:
                kick_members = False

            if is_default_member or is_admin:
                cursor.execute(RoleQueries.insert_new_default_role_query.format(classroom_id, role_name, kick_members,
                                                                                is_default_member, is_admin))
            else:
                cursor.execute(RoleQueries.get_default_role_id_query.format(classroom_id))
                default_role_id = cursor.fetchone()[0]
                cursor.execute(RoleQueries.get_all_role_properties_query.format(default_role_id))
                default_role_properties = cursor.fetchone()[3:-2]
                cursor.execute(RoleQueries.insert_new_role_query.format(classroom_id, role_name,
                                                                        *default_role_properties, False, False))

            return cursor.lastrowid

    def update_student_role(self, user_id: int, new_role_id: int) -> None:
        """Updates student's role with new role_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_student_role_query.format(new_role_id, user_id))

    def update_all_roles(self, old_role_id: int, new_role_id: int) -> None:
        """Updates students' role with new role_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_all_roles_query.format(new_role_id, old_role_id))

    def update_user_customize_role_id(self, user_id: int, role_id) -> None:
        """Update role_id that user is customizing"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_user_customize_role_id_query.format(role_id, user_id))

    def update_role_name(self, role_id: int, new_name: str) -> None:
        """Updates role's name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_role_name_query.format(new_name, role_id))

    def update_role_privilege(self, role_id: int, new_value: bool, privilege_type: str) -> None:
        """Updates role's privilege_type"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_role_privilege_query.format(privilege_type, new_value, role_id))

    def delete_role(self, role_id: int) -> None:
        """Deletes role"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.delete_role_query.format(role_id))


class RoleQueries:
    create_table_roles_query = """CREATE TABLE IF NOT EXISTS Role(
        role_id SERIAL PRIMARY KEY,
        classroom_id INT,
        role_name TEXT,
        change_current_homework BOOLEAN DEFAULT True,
        change_next_homework BOOLEAN DEFAULT True,
        change_standard_week BOOLEAN DEFAULT True,
        change_current_week BOOLEAN DEFAULT True,
        change_next_week BOOLEAN DEFAULT True,
        kick_members BOOLEAN DEFAULT False,
        invite_members BOOLEAN DEFAULT True,
        accept_requests BOOLEAN DEFAULT True,
        notify BOOLEAN DEFAULT True,
        redact_events BOOLEAN DEFAULT True,
        change_classroom_name BOOLEAN DEFAULT True,
        change_school_name BOOLEAN DEFAULT True,
        change_classroom_access BOOLEAN DEFAULT True,
        change_description BOOLEAN DEFAULT True,
        change_members_limit BOOLEAN DEFAULT True,
        is_default_member BOOLEAN DEFAULT False,
        is_admin BOOLEAN DEFAULT False,
        
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
    )"""

    create_table_student_query = """CREATE TABLE IF NOT EXISTS Student(
        student_id SERIAL NOT NULL UNIQUE PRIMARY KEY,
        user_id INT,
        classroom_id INT,
        role_id INT,
        FOREIGN KEY (user_id) REFERENCES Users (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES Role (role_id) ON DELETE SET NULL
    )"""

    get_customizing_role_id_query = """SELECT role_id FROM UserCustomize WHERE user_id={}"""
    get_default_role_name_query = """SELECT role_name FROM Role WHERE classroom_id={} AND is_default_member=True"""
    get_admin_role_name_query = """SELECT role_name FROM Role WHERE classroom_id={} AND is_admin=True"""
    get_role_name_query = """SELECT role_name FROM Role WHERE role_id={}"""
    get_default_role_id_query = """SELECT role_id FROM Role WHERE classroom_id={} AND is_default_member=True"""
    get_admin_role_id_query = """SELECT role_id FROM Role WHERE classroom_id={} AND is_admin=True"""
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
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    roles_db = RoleCommands(connection)
    print(roles_db.get_role_properties_dict(28))
