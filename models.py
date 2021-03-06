from werkzeug.security import generate_password_hash, check_password_hash

from main import db

contest_users = db.Table('contest_user', db.Column('contest_id', db.Integer, db.ForeignKey('contests.contest_id'), primary_key=True),
                                            db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(40))
    name = db.Column(db.String(50))
    surname = db.Column(db.String(200))
    e_mail = db.Column(db.String(50))
    country = db.Column(db.String(50))
    
    contests = db.relationship('Contest', secondary=contest_users, lazy='dynamic')

    def __init__(self, username, password, name, surname, e_mail, country):
        self.username = username
        self.password = self.set_password(password)
        self.name = name
        self.surname = surname
        self.e_mail = e_mail
        self.country = country

    def __repr__(self):
        return 'User(%r, %r)' % (self.username, self.e_mail)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def add_friend(self, friend_id):
        friendship = Friendship(self.user_id, friend_id)
        friendship.save()

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Friendship(db.Model):
    __tablename__ = 'friendships'

    user_id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, friend_id):
        self.user_id = user_id
        self.friend_id = friend_id

    def __repr__(self):
        return 'Friendship(%r, %r)' % (self.user_id, self.friend_id)

    def save(self):
        db.session.add(self)
        db.session.commit()


contest_tasks = db.Table('contest_tasks', db.Column('contest_id', db.Integer, db.ForeignKey('contests.contest_id')),
					    db.Column('task_id', db.Integer, db.ForeignKey('tasks.task_id'))
)


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    text = db.Column(db.Text)
    memory = db.Column(db.Integer)
    time_limit = db.Column(db.Float)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    author = db.relationship('User', backref='tasks')

    def __init__(self, name, text, memory, time_limit, author):
        self.name = name
        self.text = text
        self.memory = memory
        self.time_limit = time_limit
        self.author = author

    def __repr__(self):
        return 'Task(%r)' % (self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()


class Contest(db.Model):
	__tablename__ = 'contests'

	contest_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	start = db.Column(db.DateTime())
	duration = db.Column(db.Integer)
	author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

	tasks = db.relationship('Task', secondary=contest_tasks, lazy='dynamic')
	users = db.relationship('User', secondary=contest_users, lazy='dynamic')

	def __init__(self, name, start, duration, author_id):
		self.name = name
		self.start = start
		self.duration = duration
		self.author_id = author_id

	def __repr__(self):
		return 'Contest(%r)' % (self.name)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def set_tasks(self, tasks):
		self.tasks = tasks
        

class Submission(db.Model):
    __tablename__ = 'submissions'

    submission_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    language = db.Column(db.String(30))
    timestamp = db.Column(db.DateTime())
    task_name = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'))
    contest_id = db.Column(db.Integer, db.ForeignKey('contests.contest_id'))

    def __init__(self, status, language, timestamp, task_name, user_id, task_id, contest_id):
        self.status = status
        self.language = language
        self.timestamp = timestamp
        self.task_name = task_name
        self.user_id = user_id
        self.task_id = task_id
        self.contest_id = contest_id

    def __repr__(self):
        return 'Submission {}'.format(submission_id)

    def save(self):
        db.session.add(self)
        db.session.commit()
