# Application Readme

## Hierarchy KanBan Board

### Loom Demo link: 
https://www.loom.com/share/75f6d63974e44767a07d4b5d5345dae4?t=246&sid=f741ad1b-f0c1-4103-ba18-cbb7791123ac

### Introduction
The Hierarchy KanBan Board is a web application developed using Flask, which allows users to manage tasks in a hierarchical manner. It provides features for user registration, login, and task management. Users can create, update, and delete tasks, and organize them into different status categories (e.g., "todo," "doing," "done"). Tasks can also have parent-child relationships, creating a hierarchy for better organization.

### Installation <a name="installation"></a>
1.Clone the repository to your local machine:
   ```git clone https://github.com/fadyFH19/Hierarchical-Kanban-Board```
2. Change into the project directory:
   ```cd Hierarchical Kanban Board```
3. Create a virtual environment:
   ```python -m venv venv```
4. Activate the virtual environment:
   ```source venv/bin/activate```
5. Install the required packages:
   ```pip install -r requirements.txt```
6. Run the app:
    ```python3 main.py```

### Usage <a name="usage"></a>
- **Registration:** Users can create an account by providing a username and password.
- **Login:** Registered users can log in using their credentials.
- **Task Management:** Once logged in, users can:
  - Create new tasks, specifying a title and status (e.g., "todo," "doing," "done").
  - Organize tasks into a hierarchy by associating a task as a child of another task.
  - Update the title, status, and parent task of existing tasks.
  - Delete tasks and their children recursively.

### Features <a name="features"></a>
- User registration and authentication.
- Create, update, and delete tasks.
- Organize tasks into a hierarchy with parent-child relationships.
- Task statuses (e.g., "todo," "doing," "done").

### Screenshots <a name="screenshots"></a>
<img width="1440" alt="Screenshot 2023-10-26 at 15 13 11" src="https://github.com/fadyFH194/Nourhelp/assets/131557935/31031325-b5ea-4fed-891c-c392edc0d51a">
<img width="1440" alt="Screenshot 2023-10-26 at 15 13 35" src="https://github.com/fadyFH194/Nourhelp/assets/131557935/810122a8-f64c-4951-997e-8035b7bc6698">
<img width="1440" alt="Screenshot 2023-10-26 at 15 14 00" src="https://github.com/fadyFH194/Nourhelp/assets/131557935/1d072da1-3e85-41c7-ab9c-617a1eb1a8e5">
<img width="1440" alt="Screenshot 2023-10-26 at 15 14 13" src="https://github.com/fadyFH194/Nourhelp/assets/131557935/76dd5576-8334-49ef-b1bb-7a06a4281b88">

### Contributing <a name="contributing"></a>
If you'd like to contribute to this project, please follow these steps:
1. Fork the project on GitHub.
2. Create a new branch with a descriptive name for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch to your fork.
5. Create a pull request from your fork to the original repository.

Thank you for your contributions!

Feel free to contact the project maintainer for any questions or issues.

**Maintainer:** [Fady Hanna](https://github.com/fadyFH194)

**Project Repository:** [Repo](https://github.com/fadyFH19/Hierarchical-Kanban-Board)



