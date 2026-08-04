from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Todo, Category
from app.todo.forms import TodoForm, CategoryForm
from app.utils import format_date, days_until
from datetime import datetime

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('todo.dashboard'))
    return render_template('index.html', title='Welcome')

@todo_bp.route('/dashboard')
@login_required
def dashboard():
    filter_status = request.args.get('status', 'all')
    filter_priority = request.args.get('priority', 'all')
    filter_category = request.args.get('category', 'all')
    sort_by = request.args.get('sort', 'due_date')

    query = Todo.query.filter_by(user_id=current_user.id)

    if filter_status == 'completed':
        query = query.filter_by(is_completed=True)
    elif filter_status == 'pending':
        query = query.filter_by(is_completed=False)

    if filter_priority != 'all':
        query = query.filter_by(priority=filter_priority)

    if filter_category != 'all':
        query = query.filter_by(category_id=int(filter_category))

    if sort_by == 'due_date':
        query = query.order_by(Todo.due_date.asc().nullslast(), Todo.created_at.desc())
    elif sort_by == 'priority':
        priority_order = db.case(
            (Todo.priority == 'high', 1),
            (Todo.priority == 'medium', 2),
            (Todo.priority == 'low', 3)
        )
        query = query.order_by(priority_order, Todo.created_at.desc())
    elif sort_by == 'created':
        query = query.order_by(Todo.created_at.desc())
    else:
        query = query.order_by(Todo.created_at.desc())

    todos = query.all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    stats = current_user.get_stats()

    return render_template('dashboard.html',
        title='Dashboard',
        todos=todos,
        categories=categories,
        stats=stats,
        filter_status=filter_status,
        filter_priority=filter_priority,
        filter_category=filter_category,
        sort_by=sort_by,
        format_date=format_date,
        days_until=days_until
    )

@todo_bp.route('/todo/create', methods=['GET', 'POST'])
@login_required
def create_todo():
    form = TodoForm()
    form.category_id.choices = [(0, 'None')] + [
        (c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            user_id=current_user.id,
            category_id=form.category_id.data if form.category_id.data != 0 else None
        )
        db.session.add(todo)
        db.session.commit()
        flash('Todo added successfully!', 'success')
        return redirect(url_for('todo.dashboard'))
    return render_template('create_todo.html', title='New Todo', form=form)

@todo_bp.route('/todo/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user.id:
        abort(403)

    form = TodoForm(obj=todo)
    form.category_id.choices = [(0, 'None')] + [
        (c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.priority = form.priority.data
        todo.due_date = form.due_date.data
        todo.category_id = form.category_id.data if form.category_id.data != 0 else None
        db.session.commit()
        flash('Todo updated!', 'success')
        return redirect(url_for('todo.dashboard'))

    if request.method == 'GET':
        form.category_id.data = todo.category_id or 0
    return render_template('edit_todo.html', title='Edit Todo', form=form, todo=todo)

@todo_bp.route('/todo/<int:id>/toggle', methods=['POST'])
@login_required
def toggle_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    if todo.is_completed:
        todo.mark_incomplete()
        status = 'pending'
    else:
        todo.mark_complete()
        status = 'completed'

    db.session.commit()
    stats = current_user.get_stats()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'status': status,
            'stats': stats,
            'completed_at': format_date(todo.completed_at)
        })
    flash(f'Todo marked as {status}!', 'success')
    return redirect(url_for('todo.dashboard'))

@todo_bp.route('/todo/<int:id>/delete', methods=['POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    if todo.user_id != current_user.id:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted.', 'info')
    return redirect(url_for('todo.dashboard'))

@todo_bp.route('/category/create', methods=['POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        cat = Category(
            name=form.name.data,
            color=form.color.data,
            user_id=current_user.id
        )
        db.session.add(cat)
        db.session.commit()
        flash('Category created!', 'success')
    return redirect(url_for('todo.dashboard'))

@todo_bp.route('/category/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    cat = Category.query.get_or_404(id)
    if cat.user_id != current_user.id:
        abort(403)
    # Remove category from todos
    for todo in cat.todos:
        todo.category_id = None
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.', 'info')
    return redirect(url_for('todo.dashboard'))