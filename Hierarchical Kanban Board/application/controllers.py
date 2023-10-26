from flask import render_template
from flask import redirect, request, flash
from flask import current_app as app
from flask import g 
from flask import session
from flask_login import LoginManager, current_user, login_user, login_required
from application.models import *
from datetime import date, datetime

# Initialize the login manager for the Flask app
login = LoginManager()
login.init_app(app)
login.login_view = 'login'

# Define the HierarchyTask model
class HierarchyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

# Create the database tables (you might want to do this in a separate script)
db.create_all()

# Route for the home page, redirects to the login page
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return redirect('login')

# User loader function for Flask-Login
@login.user_loader
def load_user(username):
    return User.query.get(username)

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if len(request.form['password']) == 0:
            error = 'Please fill in the password'
        elif len(request.form['password']) < 8:
            error = 'Your password needs to be a little longer, try again.'
            return render_template('register.html', error=error)

        if request.form['password'] != request.form['repeat']:
            error = "Passwords don't match :( "
            return render_template('register.html', error=error)

        # Create a new user and add to the database
        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    elif request.method == 'GET':
        return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if len(request.form['password']) < 8:
            error = 'Your password needs to be at least 8 characters long, try again.'
            return render_template('login.html', error=error)
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user is None:
            error = "Make sure you get the username and password right :("
            return render_template('login.html', error=error)
        login_user(user)
        return redirect("/main")
    elif request.method == 'GET':
        return render_template('login.html')

# Route for user logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    return redirect('login')

# Route for the main page, accessible only to logged-in users
@app.route('/main', methods=["GET", "POST"])
@login_required
def home():
    g.user = current_user
    tasks = None
    error = None
    data = [{'status': 'todo'},
            {'status': 'doing'},
            {'status': 'done'}]
    deadline = request.form.get('deadline')
    parent_task_id = request.form.get("parent_task")
    today = date.today()
    d = today.strftime("%d/%m/%Y")

    # Handling form submission
    if request.form:
        try:
            # Check if the task title is unique
            if request.form.get("title") in [task.title for task in Task.query.all()]:
                error = "Please fill in a new task :)"
            else:
                if request.form.get('title'):
                    if not request.form.get('status') or request.form.get("status") == 'None':
                        error = 'Please select a status for the task.'
                    else:
                        if request.form.get('deadline'):
                            task = Task(title=request.form.get("title"), status=request.form.get("status"), user_id=g.user.id, deadline=deadline)
                            ftdDateList = deadline.split('-')
                            ftdDate = date(int(ftdDateList[0]), int(ftdDateList[1]), int(ftdDateList[2]))
                        else:
                            task = Task(title=request.form.get("title"), status=request.form.get("status"), user_id=g.user.id)

                        # Parent Task Assignment
                        parent_task_title = request.form.get('parent_task')
                        if parent_task_title != "None":
                            parent_task = Task.query.filter_by(title=parent_task_title, user_id=g.user.id).first()
                            if parent_task:
                                task.parent_id = parent_task.id
                            else:
                                error = "Parent task not found"
                        db.session.add(task)
                        db.session.commit()
        except Exception as e:
            error = e

    tasks = Task.query.filter_by(user_id=g.user.id).all()
    parent_tasks = Task.query.filter_by(user_id=g.user.id).all()
    todo = Task.query.filter_by(status='todo', user_id=g.user.id).all()
    doing = Task.query.filter_by(status='doing', user_id=g.user.id).all()
    done = Task.query.filter_by(status='done', user_id=g.user.id).all()
    task_dict = {
        'todo': todo,
        'current': doing,
        'done': done
    }

    return render_template("home.html", error=error, task_dict=task_dict, tasks_list=tasks, data=data, myuser=current_user, today=d, parent_tasks=parent_tasks)

# Route to update the status of a task
@app.route("/update", methods=["POST"])
def update():
    try:
        new_status = request.form.get("newstatus")
        name = request.form.get("name")
        target_list = request.form.get("targetlist")  # Updated to get the target list

        task = Task.query.filter_by(title=name).first()

        if task:
            if new_status == task.status:
                flash(f'Task "{name}" status remains unchanged.')
            else:
                task.status = new_status
                flash(f'Task "{name}" status updated to {new_status}.')

            if target_list and target_list != task.status:
                task.status = target_list
                flash(f'Task "{name}" moved to {target_list}.')

            db.session.commit()
        else:
            flash(f'Task "{name}" not found.')

    except Exception as e:
        flash("Task status update failed")
        flash(e)

    return redirect("/main")

# Route to edit a task
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        try:
            new_title = request.form.get("new_title")
            old_title = request.form.get("old_title")
            task = Task.query.filter_by(title=old_title, user_id=current_user.id).first()
            if task:
                if new_title:
                    task.title = new_title
                db.session.commit()
            else:
                print("Task not found")
        except Exception as e:
            print("Task edit failed")
            print(e)
    return redirect("/main")

# Route to associate a parent task with a child task
@app.route("/assosciate_parent", methods=['POST'])
def assosciate_parent():
    try:
        parent = request.form.get("parent")
        child = request.form.get("child")
        parent_task = Task.query.filter_by(title=parent, user_id=current_user.id).first()
        child_task = Task.query.filter_by(title=child, user_id=current_user.id).first()
        if parent == "None" and child_task:
            child_task.parent_id = None
        if parent_task and child_task:
            child_task.parent_id = parent_task.id
            child_task.status = parent_task.status
            db.session.commit()
        else:
            print("Parent or child task not found")
    except Exception as e:
        print("Parent-child association failed")
        print(e)
    return redirect("/main")

# Route to edit a task's details
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    g.user = current_user
    task = Task.query.get(task_id)
    tasks = Task.query.filter_by(user_id=g.user.id).all()
    if task is None:
        flash("Task not found")
        return redirect("/main")

    # Check if the current user is the owner of the task
    if task.user_id != current_user.id:
        flash("Unauthorized access")
        return redirect("/main")

    # Function to update the status of a task and its children recursively
    def update_task_and_children(task, new_status):
        task.status = new_status
        for child_task in task.children:
            update_task_and_children(child_task, new_status)

    if request.method == "GET":
        return render_template("edit_task.html", task=task, all_tasks=tasks)

    if request.method == "POST":
        try:
            new_title = request.form.get("new_title")
            new_status = request.form.get("new_status")
            parent_title = request.form.get("parent")

            if new_title:
                task.title = new_title

            if new_status:
                if task.status != new_status:
                    task.status = new_status
                    # Update the status of children tasks recursively
                    update_task_and_children(task, new_status)

            if parent_title == "None":
                task.parent_id = None
            else:
                parent_task = Task.query.filter_by(title=parent_title, user_id=current_user.id).first()
                if parent_task:
                    task.parent_id = parent_task.id
                    task.status = parent_task.status
                else:
                    flash("Parent task not found")
                    return render_template("edit_task.html", task=task, all_tasks=tasks)

            db.session.commit()
            flash("Task updated successfully")
        except Exception as e:
            flash("Task update failed")
            flash(str(e))

        return redirect("/main")

# Route to delete a task
@app.route("/delete", methods=["POST"])
def delete():
    task_id = request.form.get("task_id")
    task = Task.query.get(task_id)
    
    if task:
        # Function to delete a task and its children recursively
        def delete_task_and_children(task):
            children = task.children[:]
            for child_task in children:
                delete_task_and_children(child_task)
                db.session.delete(child_task)
            
            db.session.delete(task)
        
        delete_task_and_children(task)
        db.session.commit()
    
    return redirect("/main")