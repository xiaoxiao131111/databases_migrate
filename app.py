from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manage

app = Flask(__name__)
#开启csrf保护
# CSRFProtect(app)

#设置数据库配置信息
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:crx199768@127.0.0.1:3306/library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #压制警告信息
db = SQLAlchemy(app)

"""常见关系模板代码"""

'''
# 一对多
示例场景
    用户与其发布的帖子（用户表和帖子表）
    角色与所属于该角色的用户（角色表与多用户表）
'''
class Role(db.Model):
    """角色表"""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 关联关系
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
    """用户表"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)


"""
多对多
# 示例场景
    讲师与其上课的班级（讲师表和班级表）
    用户与其收藏的新闻（用户表和新闻表）
    学生与其选修的课程（学生表和选修课程表）
"""
# 创建中间表
tb_student_course = db.Table('tb_student_course',
                             db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                             db.Column('course_id', db.Integer, db.ForeignKey('courses.id')))

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    courses = db.relationship('Course', secondary=tb_student_course, backref=db.backref('students', lazy='dynamic'),
                              lazy='dynamic')

class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

"""
自关联一对多
# 示例场景
    评论和该评论的子评论（评量表）
    参考网易新闻
"""
class Comment(db.Model):
    """评论"""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    # 评论内容
    content = db.Column(db.Text, nullable=False)
    # 父评论id
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    # 父评论（也是评论模型）
    parent = db.relationship('Comment', remote_side=[id],
                             backref=db.backref('childs', lazy='dynamic'))

"""
自关联多对多
# 示例场景
    用户关注其他用户（用户表、中间表）
"""
# 创建中间表
tb_user_follows = db.Table(
    'tb_user_follows',
    db.Column('follower_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True),  # 粉丝id
    db.Column('followed_id', db.Integer, db.ForeignKey('info_user.id'), primary_key=True)  # 被关注人id
)

class Users(db.Model):
    """用户表"""
    __tablename__ = 'info_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    # 用户所有的粉丝，添加了反向引用followed， 代表用户都关注了哪些人
    followers = db.relationship('Users',
                                secondary=tb_user_follows,
                                primaryjoin=id == tb_user_follows.c.followed.id,
                                secondaryjoin=id == tb_user_follows.c.follower_id,
                                backref=db.backref('followed', lazy='dynamic'),
                                lazy='dynamic'
                                )




@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
