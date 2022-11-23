from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

'''明确users表的结构--to be modified'''


class User(db.Model):
    __tablename__ = 'User_tb'  # 定义表名为User_tb
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    emial = db.Column(db.String(120), index=True, unique=True)
    # password = db.Column(db.String(128))
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User %r' % (self.nickname)


db.drop_all()
db.create_all()
if __name__ == '__main__':
    per_one = User(nickname='You', emial='456.@mwee.com')
    per_two = User(nickname='Me', emial='123@mwee.com')
    db.session.add_all([per_one, per_two])  # 向表中添加两条数据
    db.session.commit()
