from flask import request, jsonify
from flask_restful import Resource
import models, time, hashlib, os, ast
from config import *
from permissions import auth_role
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, TimeoutError, OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from datetime import datetime
def parse_iso_datetime(iso_str):
    dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
    return dt
def model_to_dict(obj):
    """
    将 SQLAlchemy 模型对象转换为字典，并将 datetime 对象转换为字符串。
    """
    def convert(value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

    return {c.name: convert(getattr(obj, c.name)) for c in obj.__table__.columns}



# answer
class Answer(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        question_id = request.args.get('question_id')
        if not question_id:
            return {"message": "缺少question_id参数"}, HTTP_BAD_REQUEST
        
        question_id = int(question_id)
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            return model_to_dict(ret), HTTP_OK
        else:
            return {"message": "该答案不存在"}, HTTP_NOT_FOUND

    @auth_role(AUTH_TEACHER)
    def delete(self):
        question_id = request.args.get('question_id')
        if not question_id:
            return {"message": "缺少question_id参数"}, HTTP_BAD_REQUEST

        question_id = int(question_id)
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该答案不存在"}, HTTP_NOT_FOUND


class AnsweredQuestions(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        student_id = int(request.args.get('student_id'))
        my_submits = models.Submission.query.filter_by(student_id=student_id).with_entities(models.Submission.question_id).distinct().all()
        unique_questions = {submit.question_id for submit in my_submits}
        return jsonify(list(unique_questions))





class CheckQuestions(Resource):
    def post(self):
        data = request.get_json()
        question_ids = data.get('questionIds', [])
        invalid_ids = []

        for q_id in question_ids:
            question = models.Question.query.get(q_id)
            if not question:
                invalid_ids.append(q_id)

        return {"invalidIds": invalid_ids}, 200

class CheckStudents(Resource):
    def post(self):
        data = request.get_json()
        student_ids = data.get('studentIds', [])
        invalid_ids = []

        for s_id in student_ids:
            student = models.User.query.get(s_id)
            if not student:
                invalid_ids.append(s_id)

        return {"invalidIds": invalid_ids}, 200
    




# community
class Community(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        article_id = request.args.get('article_id')
        if not article_id:
            return {"message": "缺少article_id参数"}, HTTP_BAD_REQUEST

        article_id = int(article_id)
        ret = models.Article.query.filter_by(id=article_id).first()
        if ret:
            return model_to_dict(ret), HTTP_OK
        else:
            return {"message": "文章不存在"}, HTTP_NOT_FOUND
    
    @auth_role(AUTH_ALL)
    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "无效的请求数据"}, HTTP_BAD_REQUEST

        try:
            user_id = int(data.get('user_id'))
        except ValueError:
            return {"message": "无效的用户ID"}, HTTP_BAD_REQUEST
        
        max_id = db.session.query(func.max(models.Article.id)).scalar()
        max_id = max_id + 1 if max_id else 1
        article = models.Article(
            id=max_id,
            title=data.get('title'),
            content=data.get('content'),
            user_id=user_id,
            question_id=int(data.get('question_id')) if data.get('question_id') else None,
            is_notice=data.get('is_notice', False),
            publish_time=parse_iso_datetime(data.get('publish_time')),
            last_modify_time=parse_iso_datetime(data.get('last_modify_time'))
        )

        if article.title and article.content:
            db.session.add(article)
            db.session.commit()
            return {}, HTTP_CREATED
        else:
            return {"message": "文章缺少标题或内容！"}, HTTP_BAD_REQUEST
    
    @auth_role(AUTH_ALL)
    def put(self):
        data = request.get_json()
        article_id = data.get('article_id')
        if not article_id:
            return {"message": "缺少article_id参数"}, HTTP_BAD_REQUEST

        article_id = int(article_id)
        article = models.Article.query.filter_by(id=article_id).first()
        if not article:
            return {"message": "未找到文章！"}, HTTP_NOT_FOUND

        role = data.get('role', AUTH_STUDENT)
        user_id = data.get('user_id')
        if role == AUTH_STUDENT and article.user_id != user_id:
            return {"message": "没有编辑权限！"}, HTTP_FORBIDDEN
        
        new_content = data.get('new_content')
        if new_content:
            article.content = new_content
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "缺少新的内容"}, HTTP_BAD_REQUEST
    
    @auth_role(AUTH_ADMIN)
    def delete(self):
        article_id = request.args.get('article_id')
        if not article_id:
            return {"message": "缺少article_id参数"}, HTTP_BAD_REQUEST

        article_id = int(article_id)
        article = models.Article.query.filter_by(id=article_id).first()
        if article:
            db.session.delete(article)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "未找到文章！"}, HTTP_NOT_FOUND

# 文章列表类
class CommunityList(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        user_id = int(request.args.get('user_id')) if request.args.get('user_id') else None
        articles = models.Article.query.all()
        if user_id:
            articles = models.Article.query.filter_by(user_id=user_id)
        else:
            articles = models.Article.query.all()
        data = [model_to_dict(article) for article in articles]
        return jsonify(data)


# contest
# 处理单个考试的相关功能
class Contest(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        # 查询单个考试 -> 用于考试查询和显示
        contest_id = int(request.args.get('contest_id'))
        ret = models.Exam.query.filter_by(id=contest_id).first()
        if ret:
            return model_to_dict(ret), HTTP_OK
        else:
            return {"message": "该考试不存在"}, HTTP_NOT_FOUND

    @auth_role(AUTH_TEACHER)
    def delete(self):
        contest_id = int(request.args.get('contest_id'))
        ret = models.Exam.query.filter_by(id=contest_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该考试不存在"}, HTTP_NOT_FOUND
    
    @auth_role(AUTH_TEACHER)
    def post(self):
        c = models.Exam()
        c.teacher_id = int(request.json.get('teacher_id'))
        c.start_time = request.json.get('start_time')
        c.end_time = request.json.get('end_time')

        if not (c.teacher_id and c.start_time and c.end_time):
            return {"message": "考试信息不全，补全缺失项！"}, HTTP_BAD_REQUEST
        db.session.add(c)
        db.session.commit()
        return {"message": "新增考试成功", "id": c.id}, HTTP_CREATED
    
class ContestList(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        # 获取当前用户ID
        current_user_id = request.args.get('user_id')
        current_user_role = request.args.get('user_role')

        if int(current_user_role) == 0:
            # 查询与当前用户相关的考试ID
            student_exams = models.ExamStudent.query.filter_by(student_id=current_user_id).all()
            exam_ids = [exam.exam_id for exam in student_exams]

            # 查询相关考试信息
            contests = models.Exam.query.filter(models.Exam.id.in_(exam_ids)).all()
        else:
            # 查询所有考试信息
            contests = models.Exam.query.all()
        data = [model_to_dict(contest) for contest in contests]
        return jsonify(data)

## 获取和考试对应的题目id
class ContestQuestion(Resource):
    def get(self):
        exam_id = int(request.args.get('contest_id'))
        exam_questions = models.ExamQuestion.query.filter_by(exam_id=exam_id).all()
        if not exam_questions:
            return jsonify({'message': 'No questions found for this exam.'}), 404

        question_ids = [eq.question_id for eq in exam_questions]
        return jsonify({'questionIds': question_ids})
    
    @auth_role(AUTH_TEACHER)
    def post(self):
        exam_id = int(request.json.get('exam_id'))
        question_id = int(request.json.get('question_id'))
        score = int(request.json.get('score'))

        if not (exam_id and question_id and score):
            return {"message": "信息不全，补全缺失项！"}, HTTP_BAD_REQUEST
        
        exam_question = models.ExamQuestion(
            exam_id=exam_id,
            question_id=question_id,
            score=score
        )
        
        db.session.add(exam_question)
        db.session.commit()
        return {"message": "考试-题目关联成功"}, HTTP_CREATED


class ContestStudent(Resource):
    @auth_role(AUTH_TEACHER)
    def post(self):
        exam_id = int(request.json.get('exam_id'))
        student_id = int(request.json.get('student_id'))

        if not (exam_id and student_id):
            return {"message": "信息不全，补全缺失项！"}, HTTP_BAD_REQUEST
        
        exam_student = models.ExamStudent(
            exam_id=exam_id,
            student_id=student_id,
            score=0  # 默认分数为0
        )
        
        db.session.add(exam_student)
        db.session.commit()
        return {"message": "考试-学生关联成功"}, HTTP_CREATED

    @auth_role(AUTH_TEACHER)
    def get(self):
        student_id = int(request.args.get('userId'))
        if not student_id:
            return {"message": "缺少userId参数"}, HTTP_BAD_REQUEST
        
        exam_students = models.ExamStudent.query.filter_by(student_id=student_id).all()
        if not exam_students:
            return {"message": "该学生没有关联的考试"}, HTTP_NOT_FOUND
        
        exam_ids = [exam_student.exam_id for exam_student in exam_students]
        return {"exam_ids": exam_ids}, HTTP_OK


class ContestScores(Resource):
    def get(self):
        contest_id = request.args.get('contest_id')

        if not contest_id:
            return {"message": "缺少考试ID"}, 400

        try:
            contest_id = int(contest_id)
        except ValueError:
            return {"message": "考试ID无效"}, 400

        exam_students = models.ExamStudent.query.filter_by(exam_id=contest_id).order_by(models.ExamStudent.score.desc()).all()
        
        if not exam_students:
            return {"message": "未找到相关成绩"}, 404

        student_scores = [
            {
                "id": exam_student.student_id,
                "score": exam_student.score,
                "rank": index + 1
            }
            for index, exam_student in enumerate(exam_students)
        ]

        return student_scores, 200



class GetScore(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        exam_id = int(request.args.get('exam_id'))
        student_id = int(request.args.get('student_id'))

        if not (exam_id and student_id):
            print(1)
            return {"message": "信息不全，补全缺失项！"}, HTTP_BAD_REQUEST
        
        exam_student = models.ExamStudent.query.filter_by(exam_id=exam_id, student_id=student_id).first()
        if not exam_student:
            print(2)
            return {"message": "该学生没有关联的考试"}, HTTP_NOT_FOUND
        
        score = exam_student.score
        print(score)
        return {"score": score}, HTTP_OK





# judge
# 定义返回结果的字段

class Judge(Resource):
    @auth_role(AUTH_ALL)
    def execute_sql(self, code):
        """
        运行SQL代码，并捕获可能的错误和异常
        :param code: 要执行的SQL代码
        :return: 执行结果，格式为 (error: bool, msg: str)
        """
        # 创建数据库引擎，连接到testdb数据库
        engine = create_engine('mysql+pymysql://ws:3917@localhost/test')
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.begin()  # 开始事务
            start_time = time.time()  # 记录开始时间
            
            result = session.execute(text(code))  # 执行SQL代码
            session.commit()  # 提交事务

            if result.returns_rows:  # 如果返回结果
                output = result.fetchall()  # 获取所有结果
                output = [dict(row) if isinstance(row, dict) else row for row in output]
            else:
                output = "No data"

            elapsed_time = time.time() - start_time  # 计算执行时间

            if elapsed_time > 5:  # 判断是否超时
                return (True, "TLE")  # 超时返回TLE

            return (False, output)  # 返回执行结果

        except OperationalError as e:  # 捕获操作错误异常
            session.rollback()  # 回滚事务
            return (True, str(e))  # 返回错误信息
        except TimeoutError:  # 捕获超时异常
            session.rollback()  # 回滚事务
            return (True, "TLE")  # 返回超时错误信息
        except SQLAlchemyError as e:  # 捕获SQLAlchemy异常
            session.rollback()  # 回滚事务
            return (True, str(e))  # 返回错误信息
        finally:
            session.close()  # 关闭会话

    def drop_tables(self, tablename):
        """
        删除指定的表，避免数据干扰
        :param tablename: 需要删除的表名（可能有多个表名，以逗号分隔）
        """
        # 创建数据库引擎，连接到testdb数据库
        engine = create_engine('mysql+pymysql://root:4546@localhost/test')
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            session.begin()  # 开始事务
            # 关闭外键检查
            session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
            # 删除指定表
            session.execute(text(f'DROP TABLE IF EXISTS {tablename};'))
            # 重新打开外键检查
            session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
            session.commit()  # 提交事务
        except SQLAlchemyError:  # 捕获SQLAlchemy异常
            session.rollback()  # 回滚事务
        finally:
            session.close()  # 关闭会话

    def post(self):
        data = request.get_json()
        submit_sql = data.get('submit_sql')
        question_id = data.get('question_id')
        create_code = data.get('create_code')
        if not submit_sql or not question_id:
            return {"message": "提交信息不全"}, HTTP_BAD_REQUEST

        question_id = int(question_id)
        test_cases = models.TestCase.query.filter_by(question_id=question_id).all()
        results = {}
        
        for test_case in test_cases:
            test_id = test_case.id
            input_sql = str(test_case.input_sql)
            expected_output = ast.literal_eval(test_case.output)
            tablename = test_case.tablename
            self.drop_tables(tablename)

            error, _ = self.execute_sql(create_code)
            error, _ = self.execute_sql(input_sql)
            # if error:
            #     results[test_id] = (True, JUDGE_RUNERROR)
            #     continue

            error, user_output = self.execute_sql(submit_sql)
            if error:
                if user_output == "TLE":
                    results[test_id] = (False, JUDGE_TIMELIMIT_EXCEED)
                elif "MemoryError" in user_output:
                    results[test_id] = (False, JUDGE_MEMLIMIT_EXCEED)
                else:
                    results[test_id] = (False, JUDGE_RUNERROR)
            elif user_output != expected_output:
                results[test_id] = (False, JUDGE_WRONGANSWER)
            else:
                results[test_id] = (True, JUDGE_ACCEPTED)
        # 之后在此更新submit表的信息
        submit_id = int(data.get('submit_id')) if data.get('submit_id') else None
        record = models.Submission.query.filter_by(id=submit_id).first()
        finalresult = [True, 'Pending']
        error_list = []
        for _, result in results.items():
            if not result[0]:
                error_list.append(result[1])
                finalresult[0] = False
        result_map = {
            JUDGE_RUNERROR: 'Runtime error',
            JUDGE_WRONGANSWER: "Wrong answer",
            JUDGE_TIMELIMIT_EXCEED: "Time limit exceeded",
            JUDGE_MEMLIMIT_EXCEED: "Memory limit exceeded"
        }
        if finalresult[0]:
            finalresult[1] = 'Accepted'
            pass_rate = 1
            record.status = JUDGE_ACCEPTED
        else:
            finalresult[1] = result_map[min(error_list)]
            pass_rate = int(10000 * (1.0 - len(error_list) * 1.0 / len(results))) / 100.0 # 可能需要考虑保留小数的问题？
            record.status = min(error_list)

        record.pass_rate = pass_rate
        db.session.commit()
        return {"result": tuple(finalresult), 'pass_rate': pass_rate}, HTTP_OK
    





# login
class Login(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('id')
        password = data.get('password')
        
        if not user_id or not password:
            return {"message": "缺少用户名或密码"}, HTTP_BAD_REQUEST

        user_id = int(user_id)
        user = models.User.query.filter_by(id=user_id, password=hashlib.sha256(password.encode('utf8')).hexdigest()).first()

        if user:
            session_token = hashlib.sha1(os.urandom(24)).hexdigest()
            user.session = session_token
            db.session.commit()
            return model_to_dict(user), HTTP_OK
        else:
            return {"message": '用户名或密码无效'}, HTTP_UNAUTHORIZED
        
    def delete(self):
        session = request.headers.get('session')
        user = models.User.query.filter_by(session=session).first()
        if user:
            user.session = None
            db.session.commit()
            return {"message": '成功退出登录'}, HTTP_OK
        else:
            return {"message": '身份信息无效！请重新登录。'}, HTTP_UNAUTHORIZED
        
    def get(self):
        session = request.headers.get('session')
        user = models.User.query.filter_by(session=session).first()
        if user:
            return {"id": user.id, "name": user.username, "role": user.role}, HTTP_OK
        else:
            return {"message": '身份信息无效！请重新登录。'}, HTTP_UNAUTHORIZED





# manageUsers
class ManageUsers(Resource):
    def get(self):
        # Retrieve all users
        users = models.User.query.all()
        data = [model_to_dict(user) for user in users]
        return jsonify(data)

    def post(self):
        # Delete a user
        user_id = int(request.json.get('id'))
        user = models.User.query.filter_by(id=user_id).first()

        if not user:
            return {"message": "未找到用户。"}, HTTP_NOT_FOUND

        db.session.delete(user)
        db.session.commit()
        return {}, HTTP_OK

    def put(self):
        # Update user role
        user_id = request.json.get('id')
        new_role = request.json.get('role')
        user = models.User.query.filter_by(id=user_id).first()

        if not user:
            return {"message": "未找到用户。"}, HTTP_NOT_FOUND

        user.role = new_role
        db.session.commit()
        return {"message": "切换成功。"}, HTTP_OK
    
    def delete(self):
        user_id = request.args.get('user_id')
        user = models.User.query.filter_by(id=user_id).first()
        if not user:
            return {"message": "未找到用户。"}, HTTP_NOT_FOUND
        
        for exam_student in models.ExamStudent.query.filter_by(student_id=user_id).all():
            db.session.delete(exam_student)
        for submit in models.Submission.query.filter_by(student_id=user_id).all():
            db.session.delete(submit)
        for article in models.Article.query.filter_by(user_id=user_id).all():
            db.session.delete(article)
        for question in models.Exam.query.filter_by(teacher_id=user_id).all():
            db.session.delete(question)
        db.session.delete(user)
        db.session.commit()
        return {"message": "删除成功。"}, HTTP_OK


class StatusCount(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        student_id = int(request.args.get('student_id'))
        pass_count = models.Submission.query.filter_by(student_id=student_id, status=0).distinct(models.Submission.question_id).count()
        status_count = []
        for i in range(5):
            status_count.append(models.Submission.query.filter_by(student_id=student_id, status=i).count())
        return jsonify({'pass_count': pass_count, 'status_count': status_count})

# questions
# 处理单个题目的相关功能
class Question(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        # 查询单个题目 -> 用于题目查询和显示
        question_id = int(request.args.get('question_id'))
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            student_id = int(request.args.get('student_id'))
            all_submits = models.Submission.query.filter_by(question_id=question_id)
            submission_count = all_submits.filter_by(student_id=student_id).count()
            completed = all_submits.filter_by(student_id=student_id, status=0).first() is not None
            accepted_submits = all_submits.filter_by(status=0)
            len_all_submits = all_submits.count()
            len_accepted_submits = accepted_submits.count()
            len_submit_users = all_submits.with_entities(models.Submission.student_id).distinct().count()
            len_users = models.User.query.count()
            if len_users:
                completion_rate = int(10000 * len_submit_users / len_users) / 100.0
            else:
                completion_rate = 0.0
            if len_all_submits:
                accuracy = int(10000 * len_accepted_submits / len_all_submits) / 100.0
            else:
                accuracy = 0.0
            return dict(model_to_dict(ret), **{'accuracy' : accuracy, 
                                               'completion_rate': completion_rate,
                                               'completed': completed,
                                               'submission_count': submission_count}), HTTP_OK
        else:
            return {"message": "该题目不存在"}, HTTP_NOT_FOUND

    @auth_role(AUTH_TEACHER)
    def delete(self):
        question_id = int(request.args.get('question_id'))
        ret = models.Question.query.filter_by(id=question_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该题目不存在"}, HTTP_NOT_FOUND
    
    @auth_role(AUTH_TEACHER)
    def post(self):
        q = models.Question()
        q.title = request.json.get('title')
        q.description = request.json.get('description')
        q.create_code = request.json.get('create_code')
        q.difficulty = int(request.json.get('difficulty', 1))
        q.input_example = request.json.get('input_example', '')
        q.output_example = request.json.get('output_example', '')
        q.answer_example = request.json.get('answer_example', '')
        q.is_public = request.json.get('is_public', False)

        if not (q.title and q.description and q.create_code):
            return {"message": "题目信息不全，补全缺失项！"}, HTTP_BAD_REQUEST
        db.session.add(q)
        db.session.commit()
        return {"message": "新增题目成功", 'question_id': q.id}, HTTP_CREATED

class TestCase(Resource):
    @auth_role(AUTH_TEACHER)
    def post(self):
        test_cases = request.json.get('test_cases')
        question_id = request.json.get('question_id')
        if not test_cases or not question_id:
            return {"message": "测试点信息不全，补全缺失项！"}, HTTP_BAD_REQUEST

        for case in test_cases:
            tc = models.TestCase()
            tc.tablename = case.get('tablename')
            tc.input_sql = case.get('input_sql')
            tc.output = case.get('output')
            tc.question_id = question_id

            db.session.add(tc)

        db.session.commit()
        return {"message": "新增测试点成功"}, HTTP_CREATED

# 处理题目列表的相关功能
class QuestionList(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        # 查询所有题目 -> 用于题目列表的查询和显示
        student_id = int(request.args.get('student_id'))
        questions = models.Question.query.all()
        # 计算题目难度
        data = []
        for question in questions:
            all_submits = models.Submission.query.filter_by(question_id=question.id)
            accepted_submits = all_submits.filter_by(status=0)
            len_all_submits = all_submits.count()
            len_accepted_submits = accepted_submits.count()

            if len_all_submits:
                accuracy = int(10000 * len_accepted_submits / len_all_submits) / 100.0
            else:
                accuracy = 0.0
            ac = accepted_submits.filter_by(student_id=student_id).first() is not None
            data.append(dict(model_to_dict(question), **{'accuracy' : accuracy, 'AC' : ac}))
        return jsonify(data)




# register
class Register(Resource):
    def post(self):
        id = int(request.json.get('id')) if request.json.get('id') else None
        username = request.json.get('username', None)
        password = hashlib.sha256(request.json.get('password', 0).encode('utf8')).hexdigest() 
        
        if models.User.query.filter_by(id=id).first():
            return {"message": "ID撞车了，换一个。"}, HTTP_CONFLICT
        if models.User.query.filter_by(username=username).first():
            return {"message": "有人跟你重名了，换一个。"}, HTTP_CONFLICT
        
        new_user = models.User(id=id, username=username, password=password, role=AUTH_STUDENT)
        db.session.add(new_user)
        db.session.commit()
        return {"message": "成了，快去登录吧！"}, HTTP_CREATED

# students
class Student(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        student_id = int(request.args.get('student_id'))
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            return model_to_dict(ret), HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NOT_FOUND
        
    @auth_role(AUTH_ADMIN)
    def delete(self):
        student_id = int(request.args.get('student_id'))
        ret = models.User.query.filter_by(id=student_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该学生不存在"}, HTTP_NOT_FOUND

    @auth_role(AUTH_ADMIN)
    def post(self):
        student = models.User()
        student.id = int(request.json.get('id'))
        student.password = request.json.get('password')
        student.username = request.json.get('username')
        student.role = AUTH_STUDENT
        if student.id and student.password:
            ret = models.User.query.filter_by(id=student.id).first()
            if ret:
                return {"message": "该学生已存在"}, HTTP_CONFLICT
            db.session.add(student)
            db.session.commit()
            return {}, HTTP_CREATED
        else:
            return {"message": "学生信息不全，补全后提交！"}, HTTP_BAD_REQUEST
    
    # TODO: 添加修改学生信息的函数

class StudentList(Resource):
    @auth_role(AUTH_ADMIN)
    def get(self):
        students = models.User.query.filter_by(role=AUTH_STUDENT)
        data = [model_to_dict(student) for student in students]
        return jsonify(data)




# submit
class Submit(Resource):
    # 删除提交信息
    @auth_role(AUTH_ADMIN)
    def delete(self):
        submit_id = int(request.args.get("submit_id"))
        ret = models.Submission.query.filter_by(id=submit_id).first()
        if ret:
            db.session.delete(ret)
            db.session.commit()
            return {}, HTTP_OK
        else:
            return {"message": "该提交记录不存在"}, HTTP_NOT_FOUND
    
    # 提交 - auth all
    @auth_role(AUTH_ALL)
    def post(self):
        s = models.Submission()
        s.student_id = int(request.json.get('student_id'))
        s.question_id = int(request.json.get('question_id'))
        s.exam_id = int(request.json.get('exam_id')) if request.json.get('exam_id') else None
        s.submit_sql = request.json.get('submit_sql')
        s.submit_time = parse_iso_datetime(request.json.get('submit_time'))
        s.pass_rate = 0
        s.status = JUDGE_PENDING
        if not (s.student_id and s.question_id and s.submit_sql):
            return {"message": "提交信息不全"}, HTTP_BAD_REQUEST
        
        db.session.add(s)
        db.session.commit()

        # 同时返回submit的id
        return {"message": "提交成功", "submit_id": s.id}, HTTP_CREATED
    

    # 根据 question_id, exam_id, user_id获取提交信息
    @auth_role(AUTH_ALL)
    def get(self):
        data = dict(request.args)
        user_id = int(data.get('student_id')) if data.get('student_id') else None
        question_id = int(data.get('question_id')) if data.get('question_id') else None  
        exam_id = int(data.get('exam_id')) if data.get('exam_id') else None

        if user_id and question_id and exam_id:
            submits = models.Submission.query.filter_by(student_id=user_id, question_id=question_id, exam_id=exam_id).all()
            if not submits:
                return {"pass_rate": 0}, HTTP_OK
            else:
                max_pass_rate = max(submit.pass_rate for submit in submits)
                return {"pass_rate": max_pass_rate}, HTTP_OK
        else:
            return {"message": "提交信息不全"}, HTTP_BAD_REQUEST







class SubmitList(Resource):
    @auth_role(AUTH_ALL)
    def get(self):
        data = dict(request.args)
        fetchall = True if data.get('fetchall') == 'true' else False
        userid = int(data.get('user_id')) if data.get('user_id') else None
        if fetchall:
            submits = models.Submission.query.filter_by()
        elif userid:
            submits = models.Submission.query.filter_by(student_id=userid)
        else:
            return {"message": "学生不存在！"}, HTTP_BAD_REQUEST
        data = [model_to_dict(submit) for submit in submits]
        return jsonify(data)
    

class UpdateScoreAPI(Resource):
    @auth_role(AUTH_ALL)
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        exam_id = data.get('exam_id')
        question_id = data.get('question_id')
        old_rate = data.get('old_rate')
        new_rate = data.get('new_rate')

        if not (user_id and exam_id and question_id and old_rate is not None and new_rate is not None):
            return {"message": "参数不全"}, 400

        try:
            # 获取对应的 ExamStudent 项
            exam_student = models.ExamStudent.query.filter_by(exam_id=exam_id, student_id=user_id).first()
            if not exam_student:
                return {"message": "未找到对应的考试学生记录"}, 404

            # 获取对应的 ExamQuestion 项
            exam_question = models.ExamQuestion.query.filter_by(exam_id=exam_id, question_id=question_id).first()
            if not exam_question:
                return {"message": "未找到对应的考试题目记录"}, 404

            # 计算新的总分
            question_score = exam_question.score
            old_total = exam_student.score
            new_total = old_total - old_rate * question_score + new_rate * question_score

            # 更新总分
            exam_student.score = new_total
            db.session.commit()

            return {"message": "得分更新成功", "new_score": new_total}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "数据库错误: {}".format(str(e))}, 500
