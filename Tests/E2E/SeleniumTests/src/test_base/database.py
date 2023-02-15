import mysql.connector


class Database(object):
    def __init__(self):
        self.db = mysql.connector.connect(
          host="localhost",
          user="root",
          password="",
          database="enpj3",
          autocommit=True
        )
        self.cursor = self.db.cursor(buffered=True)

    def delete_user(self, mail):
        self.cursor.execute(f"DELETE FROM account_emailaddress WHERE email = '{mail}'")
        self.cursor.execute(f"DELETE FROM auth_user WHERE email = '{mail}'")

    def get_user_id(self, mail):
        self.cursor.execute(f"SELECT id FROM auth_user WHERE email='{mail}'")
        return self.cursor.fetchone()[0]

    def get_exam_questions(self, mail):
        user_id = self.get_user_id(mail)
        self.cursor.execute(f'SELECT id, category FROM exam WHERE id_user_id = {user_id} ORDER BY id DESC')
        exam = self.cursor.fetchone()
        self.cursor.execute(f"""SELECT exam_questions.question_number , questions.question, questions.answer_a, 
                questions.answer_b, questions.answer_c, questions.media, questions.points , questions.answer_correct, 
                exam_questions.answer
                FROM exam_questions JOIN questions 
                ON exam_questions.id_question_id = questions.id 
                WHERE id_exam_id = {exam[0]}""")
        return self.cursor.fetchall()

    def get_points_from_last_exam(self, mail):
        user_id = self.get_user_id(mail)
        self.cursor.execute(f'SELECT points FROM exam WHERE id_user_id = { user_id } ORDER BY id DESC LIMIT 1;')
        return self.cursor.fetchone()[0]

    def get_questions(self, category, module, amount=1):
        self.cursor.execute(f"""SELECT question, answer_correct, media, source
        FROM questions
        WHERE module = '{module}' AND (categories LIKE '%{category}' OR categories LIKE '%{category},%')
        LIMIT {amount};""")
        return self.cursor.fetchall()