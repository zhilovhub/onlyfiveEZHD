from database import *


class AdminCommands(DataBase):
    def __init__(self, connection) -> None:
        """Initialization"""
        super().__init__(connection)

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(AdminQueries.create_table_admin_panel_query)

                # Insert admin row if not exists
                cursor.execute(AdminQueries.insert_admin_row_query, (ADMIN_ID,))

        except Error as e:
            print(e)


class AdminQueries:
    create_table_admin_panel_query = """CREATE TABLE IF NOT EXISTS admin_panel(
        user_id SERIAL NOT NULL UNIQUE PRIMARY KEY,
        
        maintenance BOOLEAN DEFAULT False
    )"""

    insert_admin_row_query = """INSERT INTO admin_panel (user_id) VALUES(%s) ON CONFLICT DO NOTHING"""
