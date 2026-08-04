from datetime import datetime, date

def format_date(d):
    if not d:
        return None
    if isinstance(d, datetime):
        return d.strftime('%b %d, %Y')
    return d.strftime('%b %d, %Y')

def days_until(due_date):
    if not due_date:
        return None
    delta = (due_date - date.today()).days
    if delta < 0:
        return f'{abs(delta)} days overdue'
    elif delta == 0:
        return 'Due today'
    elif delta == 1:
        return 'Due tomorrow'
    else:
        return f'{delta} days left'