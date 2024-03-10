# To-Do List App
This is a simple to-do list application built using Flask, SQLAlchemy, Jinja2, and Bootstrap. It allows users to add, delete, and mark tasks as complete.

Features
Add tasks with priority and due date
View tasks sorted by priority and due date
Delete tasks
Mark tasks as complete
Installation
Clone the repository:
bash
Copy code
git clone <repository-url>
Install the dependencies:
Copy code
pip install -r requirements.txt
Set up the database:
scss
Copy code
python
from app import db
db.create_all()
exit()
Usage
Start the Flask server:
Copy code
python app.py
Open your web browser and navigate to http://localhost:5000 to access the application.

Add tasks using the "Add Todo" button. You can specify the task, priority, and due date.

View and manage tasks on the main page. You can mark tasks as complete or delete them.

Contributing
Contributions are welcome! If you find any bugs or have suggestions for new features, please open an issue or submit a pull request.
