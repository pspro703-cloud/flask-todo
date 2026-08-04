from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    todos = db.relationship('Todo', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    categories = db.relationship('Category', backref='owner', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_stats(self):
        total = self.todos.count()
        completed = self.todos.filter_by(is_completed=True).count()
        pending = total - completed
        return {'total': total, 'completed': completed, 'pending': pending}

    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default='#3b82f6')  # hex color
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    todos = db.relationship('Todo', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    def mark_complete(self):
        self.is_completed = True
        self.completed_at = datetime.utcnow()

    def mark_incomplete(self):
        self.is_completed = False
        self.completed_at = None

    def is_overdue(self):
        if self.due_date and not self.is_completed:
            return self.due_date < date.today()
        return False

    @property
    def priority_color(self):
        return {
            'low': '#10b981',      # green
            'medium': '#f59e0b',   # amber
            'high': '#ef4444'      # red
        }.get(self.priority, '#6b7280')

    @property
    def priority_label(self):
        return {
            'low': 'Low',
            'medium': 'Medium',
            'high': 'High'
        }.get(self.priority, 'Medium')

    def __repr__(self):
        return f'<Todo {self.title}>'