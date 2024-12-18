class TaskManager:
    def __init__(self):
        """ Initialize the TaskManager with an empty list of tasks. """
        self.tasks = []

    def add_task(self):
        """ Prompt the user to add a task. """
        task_name = input("\033[96mEnter task name: \033[0m")  # Cyan for task name input
        task = {
            "task_name": task_name,
            "completed": False
        }
        self.tasks.append(task)
        print("\033[92mTask added successfully!\033[0m")  # Green text for success

    def view_tasks(self):
        """ Display all tasks with their completion status. """
        if not self.tasks:
            print("\033[93mNo tasks available.\033[0m")  # Yellow text if no tasks exist
        else:
            print("\033[35m\nCurrent tasks:\033[0m")  # Magenta for task list header
            for idx, task in enumerate(self.tasks, start=1):
                status = "Completed" if task["completed"] else "Pending"
                status_color = "\033[32m" if task["completed"] else "\033[91m"
                print(f"{idx}. \033[94m{task['task_name']}\033[0m - {status_color}{status}\033[0m")

    def update_task(self):
        """ Update the completion status of a task. """
        if not self.tasks:
            print("\033[93mNo tasks to update.\033[0m")  # Yellow if no tasks to update
            return

        task_id = input("\033[96mEnter task number to update: \033[0m")
        try:
            task_id = int(task_id) - 1
            if 0 <= task_id < len(self.tasks):
                self.tasks[task_id]["completed"] = not self.tasks[task_id]["completed"]
                status = "Completed" if self.tasks[task_id]["completed"] else "Pending"
                print(f"\033[92mTask '{self.tasks[task_id]['task_name']}' marked as {status}.\033[0m")
            else:
                print("\033[91mInvalid task number.\033[0m")  # Red if invalid task number
        except ValueError:
            print("\033[91mPlease enter a valid number.\033[0m")  # Red for invalid input

    def delete_task(self):
        """ Delete a task from the list. """
        if not self.tasks:
            print("\033[93mNo tasks to delete.\033[0m")  # Yellow if no tasks to delete
            return

        task_id = input("\033[96mEnter task number to delete: \033[0m")
        try:
            task_id = int(task_id) - 1
            if 0 <= task_id < len(self.tasks):
                deleted_task = self.tasks.pop(task_id)
                print(f"\033[92mTask '{deleted_task['task_name']}' deleted.\033[0m")  # Green for success
            else:
                print("\033[91mInvalid task number.\033[0m")  # Red for invalid task number
        except ValueError:
            print("\033[91mPlease enter a valid number.\033[0m")  # Red for invalid input

def print_ascii_art():
    """ Print ASCII art for 'Task Manager' """
    ascii_art = """
████████╗██╗  ██╗ █████╗ ███████╗    ███████╗████████╗███████╗
╚══██╔══╝██║  ██║██╔══██╗██╔════╝    ██╔════╝╚══██╔══╝██╔════╝
   ██║   ███████║███████║███████╗    █████╗     ██║   █████╗  
   ██║   ██╔══██║██╔══██║╚════██║    ██╔══╝     ██║   ██╔══╝  
   ██║   ██║  ██║██║  ██║███████╗    ███████╗   ██║   ███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚══════╝   ╚═╝   ╚══════╝
    """
    print("\033[35m" + ascii_art + "\033[0m")  # Magenta color for the ASCII art


def print_credits():
    """ Print credits and website link. """
    credits = """
\033[93mTask Manager\033[0m
Developed by [Your Name]
Visit us at: \033[96mhttps://www.example.com\033[0m
    """
    print(credits)

def main():
    task_manager = TaskManager()

    while True:
        print_ascii_art()
        print("\033[97m" + "-" * 40 + "\033[0m")  # White line separator
        print("\033[93m1. Add Task\033[0m")
        print("\033[93m2. View Tasks\033[0m")
        print("\033[93m3. Update Task\033[0m")
        print("\033[93m4. Delete Task\033[0m")
        print("\033[91m5. Exit\033[0m")
        print("\033[97m" + "-" * 40 + "\033[0m")  # White line separator
        choice = input("\033[96mEnter your choice: \033[0m")

        if choice == '1':
            task_manager.add_task()
        elif choice == '2':
            task_manager.view_tasks()
        elif choice == '3':
            task_manager.update_task()
        elif choice == '4':
            task_manager.delete_task()
        elif choice == '5':
            print("\033[92mGoodbye!\033[0m")  # Green for exit
            print_credits()  # Print credits and website link
            break
        else:
            print("\033[91mInvalid choice, please try again.\033[0m")  # Red for invalid choice

if __name__ == "__main__":
    main()
