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

    def get_all_role_names_from_classroom(self, classroom_id: int) -> list:
        """Return's all role names from classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(RoleQueries.get_all_role_names_from_classroom_query.format(classroom_id))
            role_names = [row[0] for row in cursor.fetchall()]

            return role_names

    def insert_new_role(self, classroom_id: int, role_name: str, is_default_member=False, is_admin=False) -> int:
        """Inserts new role into Role"""
        with self.connection.cursor() as cursor:
            if is_admin:
                kick_members = True
            else:
                kick_members = False

            cursor.execute(RoleQueries.insert_new_role_query.format(classroom_id, role_name, kick_members,
                                                                    is_default_member, is_admin))
            self.connection.commit()

            return cursor.lastrowid


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
        is_default_member BOOLEAN,
        is_admin BOOLEAN,
        
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
    )"""

    create_table_student_query = """CREATE TABLE IF NOT EXISTS Student(
        user_id INT,
        classroom_id INT,
        role_id INT,
        FOREIGN KEY (user_id) REFERENCES User (user_id),
        FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE,
        FOREIGN KEY (role_id) REFERENCES Role (role_id) ON DELETE CASCADE
    )"""

    get_role_name_query = """SELECT role_name FROM Role WHERE role_id={}"""
    get_all_role_names_from_classroom_query = """SELECT role_name FROM Role WHERE classroom_id={}"""

    insert_new_role_query = """INSERT INTO Role 
    (classroom_id, role_name, kick_members, is_default_member, is_admin) VALUES(
        {}, '{}', {}, {}, {}
    )"""


if __name__ == '__main__':
    connection = connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE_NAME
    )

    roles_db = RoleCommands(connection)
