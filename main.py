from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
# pip install Bootstrap-Flask==2.3.3
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SelectField, SubmitField, TextAreaField, PasswordField, BooleanField, HiddenField, \
    DateTimeLocalField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)


# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)  # Priority can be an integer value
    due_date = db.Column(db.DateTime, nullable=True)  # Due date can be a datetime object or None
    done = db.Column(db.Boolean, nullable=False, default=False)  # Indicates whether the task is done or not
    before_time = db.Column(db.DateTime, nullable=False) # Last date to do it

    def __repr__(self):
        return f"Todo('{self.task}', priority={self.priority}, due_date={self.due_date}, done={self.done})"

# Create the database tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    # Query tasks from the database
    tasks = Todo.query.all()

    # Format the due_date field
    for task in tasks:
        task.due_date = task.due_date.strftime("%Y-%m-%d %H:%M:%S")

    # Render the template with the formatted data
    return render_template('index.html', data=tasks)




class AddToDo(FlaskForm):
    task = StringField("Task", validators=[DataRequired()])
    priority = SelectField("Priority", choices=[
        (3, "Low priority"),
        (2, "Middle priority"),
        (1, "High priority")
    ], validators=[DataRequired()])
    before_time = DateTimeLocalField("Before Time", format='%Y-%m-%dT%H:%M', render_kw={"class": "datepicker"})
    submit = SubmitField("Add Note")



@app.route('/add', methods=['POST', 'GET'])
def add_todo():
    form = AddToDo()
    if form.validate_on_submit():
        # Extract data from the form
        task = form.task.data
        priority = form.priority.data

        finish_time_str = form.before_time.data
        print(finish_time_str)
        finish_time = finish_time_str

        # Set the due_date to the current date and time
        due_date = datetime.now()

        # Create a new Todo object
        new_todo = Todo(task=task, priority=priority, due_date=due_date, done=False, before_time=finish_time)

        # Add the new todo item to the database
        db.session.add(new_todo)
        db.session.commit()

        # Redirect to the home page or any other route
        return redirect(url_for('index'))

    # If form validation fails or it's a GET request, render the form template again
    return render_template('add_todo.html', form=form)

# Delete todo route
@app.route('/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo_to_delete = Todo.query.get(todo_id)
    if todo_to_delete:
        db.session.delete(todo_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
