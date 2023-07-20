from datetime import datetime as dt

tasks = []

# define the task template that will be use to render new templates to the page
task_template = Element("task-template").select(".task", from_content=True)
task_list = Element("list-tasks-container")
new_task_content = Element("new-task-content")

def add_task(*args, **kws):
    # ignore empty task
    if not new_task_content.element.value:
        return None

    # create task
    task = "you: " + new_task_content.element.value
    tasks.append(task)

    # add the task element to the page as new node in the list by cloning from a
    # template
    task_html = task_template.clone()
    task_html_content = task_html.select("p")
    task_html_content.element.innerText = task
    task_list.element.appendChild(task_html.element)

    new_task_content.clear()



def add_task_event(e):
    if e.key == "Enter":
        add_task()


new_task_content.element.onkeypress = add_task_event