from database import *


class ClassroomCommands(DataBase):
    """Initialization"""
    def __init__(self, connection: CMySQLConnection) -> None:
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(ClassroomQueries.create_table_classroom_query)
                cursor.execute(ClassroomQueries.create_table_student_query)

        except Error as e:
            print(e)

    def insert_new_classroom(self, user_id: int) -> None:
        """Insert new classroom and student-owner"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.insert_classroom_query)
            self.insert_new_user_in_classroom(user_id, cursor.lastrowid, "owner")

    def delete_not_created_classroom(self, user_id: int) -> None:
        """Delete classroom and its owner from Student"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.delete_classroom_query.format(user_id))
            self.connection.commit()


    def get_classroom_name(self, classroom_id: int) -> str:
        """Get name of the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.get_classroom_name_query.format(classroom_id))
            classroom_name = cursor.fetchone()[0]

            return classroom_name

    def update_classroom_name(self, classroom_id: int, new_classroom_name: str) -> None:
        """Set name to the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_classroom_name_query.format(new_classroom_name, classroom_id))
            self.connection.commit()

    def insert_new_user_in_classroom(self, user_id: int, classroom_id: int, role="member") -> None:
        """Add user to the classroom"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.insert_new_classroom_user_query.format(user_id, classroom_id, role))
            self.connection.commit()

    def update_role_of_user(self, user_id: int, user_role: str) -> None:
        """Set role to the user"""
        with self.connection.cursor() as cursor:
            cursor.execute(ClassroomQueries.update_user_role_query.format(user_role, user_id))
            self.connection.commit()

    def get_list_of_classroom_users(self, classroom_id: int) -> dict:
        """Get dict with classroom's members"""
        with self.connection.cursor() as cursor:
            users_dictionary = {}
            cursor.execute(ClassroomQueries.get_list_of_classroom_users_query.format(classroom_id))
            for (user_id, user_role) in cursor:
                users_dictionary[user_id] = user_role

            return users_dictionary


class ClassroomQueries:
    create_table_classroom_query = """CREATE TABLE IF NOT EXISTS Classroom(
            classroom_id INT NOT NULL UNIQUE AUTO_INCREMENT PRIMARY KEY,
            classroom_name VARCHAR(255),
            school_name VARCHAR(255),
            everyone_can_invite BOOLEAN,
            description TEXT,
            created BOOLEAN
        )"""

    create_table_student_query = """CREATE TABLE IF NOT EXISTS Student(
            user_id INT,
            classroom_id INT,
            role VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES User (user_id),
            FOREIGN KEY (classroom_id) REFERENCES Classroom (classroom_id) ON DELETE CASCADE
        )"""

    insert_classroom_query = """INSERT INTO Classroom VALUES(null, null, null, null, null, FALSE)"""

    get_classroom_name_query = """SELECT classroom_name FROM Classroom WHERE classroom_id={}"""

    update_classroom_name_query = """UPDATE Classroom SET classroom_name={} WHERE classroom_id={}"""

    insert_new_classroom_user_query = """INSERT INTO Student VALUES({}, {}, '{}')"""

    update_user_role_query = """UPDATE Student SET role={} WHERE user_id={}"""

    delete_user_from_classroom_query = """DELETE FROM Student WHERE user_id={}"""

    delete_classroom_query = """DELETE FROM classroom WHERE classroom_id in
                                    (SELECT classroom_id FROM Student WHERE user_id={} AND role='owner')"""

    get_list_of_classroom_users_query = """SELECT user_id, role FROM Student WHERE classroom_id={}"""


if __name__ == "__main__":
    pass
