from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class TodoForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=200)
    ])
    description = TextAreaField('Description', validators=[Optional()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    due_date = DateField('Due Date', validators=[Optional()], format='%Y-%m-%d')
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Save Todo')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    color = StringField('Color', default='#3b82f6')
    submit = SubmitField('Add Category')