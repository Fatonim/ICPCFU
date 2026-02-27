import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def get_money(self, user_id):
        result = self.cursor.execute("SELECT `money` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]
    def add_money(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `money` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def add_exp(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `exp` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_exp(self, user_id):
        result = self.cursor.execute("SELECT `exp` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_name(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_name(self, user_id):
        result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_task(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `problem` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_task(self, user_id):
        result = self.cursor.execute("SELECT `problem` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_diff(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `difficulty` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_diff(self, user_id):
        result = self.cursor.execute("SELECT `difficulty` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_problemset(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `problemset` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_problemset(self, user_id):
        result = self.cursor.execute("SELECT `problemset` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_level(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `level` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_level(self, user_id):
        result = self.cursor.execute("SELECT `level` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_time_bonus(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `time_bonus` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_time_bonus(self, user_id):
        result = self.cursor.execute("SELECT `time_bonus` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_cur_bonus(self, user_id, value):
        self.cursor.execute("UPDATE `users` SET `cur_bonus` = ? WHERE `user_id` = ?", (value, user_id,))
        return self.conn.commit()

    def get_cur_bonus(self, user_id):
        result = self.cursor.execute("SELECT `cur_bonus` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_leaders(self):
        result = self.cursor.execute("SELECT `nickname`, `level` FROM `users` ORDER BY `level` DESC")
        return result.fetchall()

    def close(self):
        self.connection.close()
