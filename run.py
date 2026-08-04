from app import create_app, db
from app.models import User, Todo, Category 
app = create_app()
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User' : User, 'Todo': Todo, 'Category': Category }
if __name__ == '__main__':
    app.run(debug=True)
    