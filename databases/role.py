from database import *


class RoleCommands(DataBase):
    def __init__(self, connection: CMySQLConnection) -> None:
        """Initialization"""
        super().__init__(connection)

        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.create_table_roles_query)
            cursor.execute(RoleQueries.create_table_user_customize_query)
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

            self.connection.commit()

            return cursor.lastrowid

    def update_student_role(self, user_id: int, new_role_id: int) -> None:
        """Updates student's role with new role_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_student_role_query.format(new_role_id, user_id))
            self.connection.commit()

    def update_all_roles(self, old_role_id: int, new_role_id: int) -> None:
        """Updates students' role with new role_id"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_all_roles_query.format(new_role_id, old_role_id))
            self.connection.commit()

    def update_user_customize_role_id(self, user_id: int, role_id) -> None:
        """Update role_id that user is customizing"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_user_customize_role_id_query.format(role_id, user_id))
            self.connection.commit()

    def update_role_name(self, role_id: int, new_name: str) -> None:
        """Updates roles' name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_role_name_query.format(new_name, role_id))
            self.connection.commit()

    def update_change_standard_week(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_standard_week"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_standard_week_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_current_week(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_current_week"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_current_week_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_next_week(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_next_week"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_next_week_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_current_homework(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_current_homework"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_current_homework_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_next_homework(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_next_homework"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_next_homework_query.format(new_value, role_id))
            self.connection.commit()

    def update_kick_members(self, role_id: int, new_value: bool) -> None:
        """Updates roles' kick_members"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_kick_members_query.format(new_value, role_id))
            self.connection.commit()

    def update_invite_members(self, role_id: int, new_value: bool) -> None:
        """Updates roles' invite_members"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_invite_members_query.format(new_value, role_id))
            self.connection.commit()

    def update_notify(self, role_id: int, new_value: bool) -> None:
        """Updates roles' notify"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_notify_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_classroom_name(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_classroom_name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_classroom_name_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_school_name(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_school_name"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_school_name_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_classroom_access(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_classroom_access"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_classroom_access_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_description(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_description"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_description_query.format(new_value, role_id))
            self.connection.commit()

    def update_change_members_limit(self, role_id: int, new_value: bool) -> None:
        """Updates roles' change_members_limit"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.update_change_members_limit_query.format(new_value, role_id))
            self.connection.commit()

    def delete_role(self, role_id: int) -> None:
        """Deletes role"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.delete_role_query.format(role_id))
            self.connection.commit()


class RoleQueries:
    create_table_roles_query = """CREATE TABLE IF NOT EXISTS Role(
        role_id INT PRIMARY KEY AUTO_INCREMENT,
        classroom_id INT,
        role_name TEXT,
        change_standard_week BOOLEAN DEFAULT 1,
        change_current_week BOOLEAN DEFAULT 1,
        change_next_week BOOLEAN DEFAULT 1,
        change_current_homework BOOLEAN DEFAULT 1,
        change_next_homework BOOLEAN DEFAULT 1,
        kick_members BOOLEAN DEFAULT 0,
        invite_members BOOLEAN DEFAULT 1,
        notify BOOLEAN DEFAULT 1,
        change_classroom_name BOOLEAN DEFAULT 1,
        change_school_name BOOLEAN DEFAULT 1,
        change_classroom_access BOOLEAN DEFAULT 1,
        change_description BOOLEAN DEFAULT 1,
        change_members_limit BOOLEAN DEFAULT 1,
        is_default_member BOOLEAN DEFAULT 0,
        is_admin BOOLEAN DEFAULT 0,
        
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
    )"""

    create_table_user_customize_query = """CREATE TABLE IF NOT EXISTS UserCustomize(
        user_id INT UNIQUE,
        classroom_id INT,
        role_id INT,
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE SET NULL,
        FOREIGN KEY (role_id) REFERENCES Role (role_id) ON DELETE SET NULL
    )"""

    create_table_student_query = """CREATE TABLE IF NOT EXISTS Student(
        user_id INT,
        classroom_id INT,
        role_id INT,
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES Role (role_id)
    )"""

    get_customizing_role_id_query = """SELECT role_id FROM UserCustomize WHERE user_id={}"""
    get_default_role_name_query = """SELECT role_name FROM Role WHERE classroom_id={} AND is_default_member=1"""
    get_admin_role_name_query = """SELECT role_name FROM Role WHERE classroom_id={} AND is_admin=1"""
    get_role_name_query = """SELECT role_name FROM Role WHERE role_id={}"""
    get_default_role_id_query = """SELECT role_id FROM Role WHERE classroom_id={} AND is_default_member=1"""
    get_admin_role_id_query = """SELECT role_id FROM Role WHERE classroom_id={} AND is_admin=1"""
    get_role_id_by_name_query = """SELECT role_id FROM Role WHERE classroom_id={} AND role_name='{}'"""
    get_all_role_names_from_classroom_query = """SELECT role_name FROM Role WHERE classroom_id={}"""
    get_all_role_properties_query = """SELECT * FROM Role WHERE role_id={}"""

    insert_new_default_role_query = """INSERT INTO Role 
    (classroom_id, role_name, kick_members, is_default_member, is_admin) VALUES(
        {}, '{}', {}, {}, {}
    )"""

    insert_new_role_query = """INSERT INTO ROLE
    (classroom_id, role_name, change_standard_week, change_current_week, change_next_week, change_current_homework,
    change_next_homework, kick_members, invite_members, notify, change_classroom_name, change_school_name,
    change_classroom_access, change_description, change_members_limit) VALUES(
        {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
    )"""

    update_student_role_query = """UPDATE Student SET role_id={} WHERE user_id={}"""
    update_all_roles_query = """UPDATE Student SET role_id={} WHERE role_id={}"""
    update_user_customize_role_id_query = """UPDATE UserCustomize SET role_id={} WHERE user_id={}"""

    update_role_name_query = """UPDATE Role SET role_name='{}' WHERE role_id={}"""
    update_change_standard_week_query = """UPDATE Role SET change_standard_week={} WHERE role_id={}"""
    update_change_current_week_query = """UPDATE Role SET change_current_week={} WHERE role_id={}"""
    update_change_next_week_query = """UPDATE Role SET change_next_week={} WHERE role_id={}"""
    update_change_current_homework_query = """UPDATE Role SET change_current_homework={} WHERE role_id={}"""
    update_change_next_homework_query = """UPDATE Role SET change_next_homework={} WHERE role_id={}"""
    update_kick_members_query = """UPDATE Role SET kick_members={} WHERE role_id={}"""
    update_invite_members_query = """UPDATE Role SET invite_members={} WHERE role_id={}"""
    update_notify_query = """UPDATE Role SET notify={} WHERE role_id={}"""
    update_change_classroom_name_query = """UPDATE Role SET change_classroom_name={} WHERE role_id={}"""
    update_change_school_name_query = """UPDATE Role SET change_school_name={} WHERE role_id={}"""
    update_change_classroom_access_query = """UPDATE Role SET change_classroom_access={} WHERE role_id={}"""
    update_change_description_query = """UPDATE Role SET change_description={} WHERE role_id={}"""
    update_change_members_limit_query = """UPDATE Role SET change_members_limit={} WHERE role_id={}"""

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
