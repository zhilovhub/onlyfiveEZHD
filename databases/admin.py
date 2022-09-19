from database import *


class AdminCommands(DataBase):
    def __init__(self, connection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(AdminQueries.create_table_admin_panel_query)

                # Insert admin row if not exists
                cursor.execute(AdminQueries.insert_admin_row_query)

        except Error as e:
            print(e)

    def get_maintenance(self) -> bool:
        """Returns True if maintenance"""
        with self.connection.cursor() as cursor:
            cursor.execute(AdminQueries.get_maintenance_query)
            maintenance = cursor.fetchone()[0]

            return maintenance

    def update_maintenance(self, maintenance) -> None:
        """Updates maintenance"""
        with self.connection.cursor() as cursor:
            cursor.execute(AdminQueries.update_maintenance_query, (maintenance,))


class AdminQueries:
    create_table_admin_panel_query = """CREATE TABLE IF NOT EXISTS admin_panel(
        id INT NOT NULL UNIQUE PRIMARY KEY,
        
        maintenance BOOLEAN DEFAULT False
    )"""

    get_maintenance_query = """SELECT maintenance FROM admin_panel WHERE id=1"""

    insert_admin_row_query = """INSERT INTO admin_panel (id) VALUES(1) ON CONFLICT DO NOTHING"""

    update_maintenance_query = """UPDATE admin_panel SET maintenance=%s WHERE id=1"""
