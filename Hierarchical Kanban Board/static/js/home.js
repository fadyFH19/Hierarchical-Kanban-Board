const deadlineForm = document.querySelector('#deadlineCatch');
const selectorForm = document.querySelector('#selector');


selectorForm.addEventListener('change',function(){

    if (selectorForm.value == 'backlog' || selectorForm.value == 'todo' || selectorForm.value == 'done' || selectorForm.value == 'doing' ){
        deadlineForm.style.display = 'block';
    }else{
        deadlineForm.style.display = 'none';
    }

});


function startEditing(button) {
    const editButton = button;
    const editField = editButton.nextElementSibling;
    const saveButton = editButton.nextElementSibling.nextElementSibling;
    editButton.style.display = "none";
    editField.style.display = "inline-block";
    saveButton.style.display = "inline-block";
    editField.value = editField.previousElementSibling.value;
  }

  function saveChanges(button) {
    const saveButton = button;
    const editField = saveButton.previousElementSibling;
    const form = saveButton.parentElement;
    form.querySelector('input[name="new_title"]').value = editField.value;
    form.submit();
  }



  function toggleSubCard(button) {
    var taskRow = button.closest('tr');
    var subCardContainer = document.querySelector('.sub-card-container');
    var subCardTitle = subCardContainer.querySelector('.sub-card-title');
    var taskTitle = taskRow.querySelector('.taskNotif').textContent;
    subCardTitle.textContent = taskTitle;
    
    if (subCardContainer.style.display === 'none') {
      subCardContainer.style.display = 'block';
    } else {
      subCardContainer.style.display = 'none';
    }
  }


  function confirmUpdate(selectElement) {
    const form = selectElement.closest(".update-form");
    if (confirm("Confirm update to " + selectElement.value + "?")) {
      form.submit();
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.task-list').forEach(taskList => {
        const taskItems = Array.from(taskList.querySelectorAll('.task-item'));
        const taskMap = {};

        // Create a map of task ID to task element
        taskItems.forEach(taskItem => {
            const taskId = taskItem.getAttribute('data-task-id');
            taskMap[taskId] = taskItem;
        });

        // Nest the tasks
        taskItems.forEach(taskItem => {
            const parentId = taskItem.getAttribute('data-parent-id');
            if (parentId && parentId !== "None") {
                let parentTask = taskMap[parentId];
                if (parentTask) {
                    let sublist = parentTask.querySelector('.subtask-list');
                    if (!sublist) {
                        sublist = document.createElement('ul');
                        sublist.className = 'subtask-list';
                        parentTask.appendChild(sublist);
                    }
                    sublist.appendChild(taskItem);
                }
            }
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
  const taskItems = document.querySelectorAll(".task-item[data-parent-id]");

  for (const taskItem of taskItems) {
    const parentId = taskItem.getAttribute("data-parent-id");
    const parentTaskItem = document.querySelector(`.task-item[data-task-id="${parentId}"]`);
    const editLink = taskItem.querySelector('.edit-link');

    // Create a button element for collapse/expand
    const expandButton = document.createElement("button");
    expandButton.className = "expand-button";
    expandButton.textContent = "Expand";

    expandButton.addEventListener("click", function (e) {
      e.preventDefault(); // Prevent the default button behavior

      const isExpanded = taskItem.classList.contains("expanded");
      if (isExpanded) {
        taskItem.classList.remove("expanded");
        expandButton.textContent = "Expand";
      } else {
        taskItem.classList.add("expanded");
        expandButton.textContent = "Collapse";
      }

      // Loop through all child tasks and toggle their visibility
      const childTasks = taskItem.querySelectorAll(`.task-item[data-parent-id="${taskItem.getAttribute("data-task-id")}"]`);
      for (const childTask of childTasks) {
        childTask.style.display = isExpanded ? "none" : "list-item";
      }
    });

    // Check if the task has a parent and set the initial state accordingly
    if (parentTaskItem) {
      taskItem.classList.remove("expanded");
      expandButton.textContent = "Expand";
      taskItem.style.display = "none"; // Collapsed by default
    } else {
      taskItem.classList.add("expanded");
      expandButton.textContent = "Expand";
    }

    // Insert the expandButton after the edit-link
    taskItem.insertBefore(expandButton, editLink.nextSibling);
  }
});