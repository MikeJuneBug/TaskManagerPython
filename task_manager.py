import os
from datetime import date, datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None, task_number = 0):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        self_task_number: Integer   
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed
        self.task_number = task_number            # Added self.task_number attribute to hold the task number

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to objectpleted
        '''
        tasks = task_str.split(";")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        task_number = tasks[6]                    # Read in the task_number from the tasks.txt
        self.__init__(username, title, description, due_date, assigned_date, completed, task_number)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No",
            str(self.task_number)          # Cast task_number to a string for writing back to tasks.txt
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        # Added more space in the form of tabs to make it more readable. Also bolded the title line
        disp_str = "\033[1m" +f"Task: \t\t\t\t\t {self.title}" +f"\033[0m\n"
        disp_str += f"Task No: \t\t\t\t {self.task_number}\n"
        disp_str += f"Assigned to: \t\t\t\t {self.username}\n"
        disp_str += f"Date Assigned: \t\t\t\t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t\t\t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n\t{self.description}"
        return disp_str
        


# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")



# Read in user_data
with open("user.txt", 'r+') as user_file:    # Changed from a+ due to ValueError 'not enough values to unpack' in VS Code. 
    user_data = user_file.read().split("\n")


# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))
        


# This reg_user function was created on 15.11.2022 by MSullivan
# Coding has been moved from the main program and incorporated here
# This function is called in the main program when the user has admin privileges and r is selected on the menu
# When called the function requests input of a new username and a new password
# The username and password are passed to the check_username_and_password function to checked if they are safe for storage
# If safe for storage then the user is asked to re-enter the password
# If the password and re-entered passwords are the same then the username and password are passed to the write_usernames_to_file function
# If the password and re-entered passwords are not the same then an error message is displayed

def reg_user():  
    while curr_user != 'admin':
        print("Registering new users requires admin privileges")
        return

    # The below while loop requests input of a new username 
    # Checks in username_password.keys if it's been used before. 
    # If it's been used before the user is prompted within a while loop to enter another username
    # The while loop prompting for a new username will only exit when brand new username is entered

    while True:
        new_username = input("New Username: ")
        if new_username in username_password.keys():
            print("User already exists. Please try another username: ")
            continue
        else:
            break

    # Request input of a new password
    new_password = input("New Password: ")

    if check_username_and_password(new_username, new_password):   
    # Username or password is not safe for storage

    # Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
            print("New user added")

        # Add to dictionary and write to file
            username_password[new_username] = new_password
            write_usernames_to_file(username_password)

        # Otherwise you present a relevant message.
        else:
            print("Passwords do not match")
    
    

# This add_task function was created on 15.11.2022 by MSullivan
# Coding has been moved from the main program and incorporated here
# The valid user_name is passed from the main program to add_task as task_username
        
def add_task():  # Add a new task

        # Prompt a user for the following: 
        #     A username of the person whom the task is assigned to,
        #     A title of a task,
        #     A description of the task and 
        #     the due date of the task.
        #     Assign a task number to the task

    # Ask for username

    while True:
        
        task_username = input("Name of person assigned to task: ")
        if task_username in username_password.keys():
            # Get title of task and ensure safe for storage
        
            while True:
        
                task_title = input("Title of Task: ")
                if validate_string(task_title):
                    break

            # Get description of task and ensure safe for storage
            while True:
                task_description = input("Description of Task: ")
                if validate_string(task_description):
                    break

        
            # Obtain and parse due date
            while True:
                try:
                    task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)  # Due date must be in the format DATETIME_STRING_FORMAT "%Y-%m-%d"
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")

            # Obtain and parse current date
            curr_date = date.today()
        
            # Assign a new task number to the new task
            task_task_number = len(task_list) + 1


            # Create a new Task object and append to list of tasks
            new_task = Task(task_username, task_title, task_description, due_date_time,curr_date, False, task_task_number)
            task_list.append(new_task)

            # Write to tasks.txt
            with open("tasks.txt", "w") as task_file:           
                task_file.write("\n".join([t.to_string() for t in task_list]))

            break
        
        else:
            print("User does not exist. Please enter a valid username")
            break
        
    

  
# This view_all function was created on 15.11.2022 by MSullivan
# Coding has been moved from the main program and incorporated here

        
def view_all():

    print("---------------------------------------------------------------------------------")  # Extended these lines for readability 

    if len(task_list) == 0:
        print("There are no tasks.")
        print("---------------------------------------------------------------------------------")  

    for t in task_list:
        print(t.display())
        print("---------------------------------------------------------------------------------")



# This view_all function was created on 15.11.2022 by MSullivan
# Coding has been moved from the main program and incorporated here

def view_mine():

    print("---------------------------------------------------------------------------------")
    has_task = False
    for t in task_list:
        if t.username == curr_user:
            has_task = True
            print(t.display())
            print("---------------------------------------------------------------------------------")

            
    
    if has_task == True:
        view_task()                   # Call a new function view_task to specify which task to view  

    if not has_task:
        print("You have no tasks.")
        print("---------------------------------------------------------------------------------")



# New function, view_task to specify task to view
# This function asks which number task the user would like to view
# The while loop will repeatedly request a task to show and will display it until -1 is enter
# When -1 is entered the user is returned to the menu

def view_task():                        
    
    get_task_no = input("Enter task number to view (-1 to return to main menu): ")

    while get_task_no != '-1':

        # The for loop checks every task_number in the task_list and checks if it is the one selected. 
        # If it's the task_number selected then this task will call the display function and the task will be displayed

        for t in task_list:
            if t.task_number == get_task_no:
                print(t.display())
                print("---------------------------------------------------------------------------------") 

                # edit_or_amend is a variable requested from the user for them to choose either to edit a task, mark as complete or exit
                edit_or_amend = input("\nEnter 'e' to edit or 'c' to mark task complete (-1 to exit): \n")

                # If c is chosen then this for loop will go through the task_list and find the matching task number, then mark the completed field as True

                if edit_or_amend == 'c':
                    for t2 in task_list:
                        if t2.task_number == get_task_no:
                            t2.completed = True

                            # Write to tasks.txt
                            with open("tasks.txt", "w") as task_file:
                                task_file.write("\n".join([t.to_string() for t in task_list]))

                            print("Amendment added to file")

                            break        # This will return user to the main menu
                

                # If e is chosen then this for loop will go through the task_list and find the matching task number and check if it's been completed
                # If it's been completed it will inform the user that the task has been completed and can't be edited, then return to the main menu

                elif edit_or_amend == 'e':
                
                    for t2 in task_list:
                        if t2.task_number == get_task_no:
                            if t2.completed is True:
                                print("\nTask has been completed and can't be edited")
                                break  # This will return user to the main menu
                            
                            # If the task hasn't been completed then program requests a new username to assign to the task
                            print(f"The username assigned to the task is: {t2.username}\n")
                            new_username = input("Please enter a new username to assign the task to: \n")

                            print(f"Updated: Task removed from: {t2.username}")   
                            t2.username = new_username                  # The task is then updated with the new username
     
            
                            print(f"\nThe due date of the task is: {t2.due_date}")  # This shows the task's current due date
                    
                            # This requests a new due date and puts it into the right format
                            # An error message is displayed if an incorrect format is input
                            while True:
                                try:
                                    task_new_due_date = input("New due date of task (YYYY-MM-DD): ")
                                    new_due_date_time = datetime.strptime(task_new_due_date, DATETIME_STRING_FORMAT)
                                    break
                                except ValueError:
                                    print("Invalid datetime format. Please use the format specified")

                            t2.due_date = new_due_date_time            # The task is then updated with the new due date and completed message displayed
                            print("Update completed. You will return to the menu\n")
                            
                
                            # Write to tasks.txt
                            with open("tasks.txt", "w") as task_file:
                                task_file.write("\n".join([t.to_string() for t in task_list]))

                            break

        
        break




# This new make_reports function will generate reports and them into files: task_overview.txt and user_overview.txt

def make_reports():

    # Calculations for task_overview.txt

    # Total number of tasks. This calculation is simply the len of the task_list
    total_tasks = len(task_list)

    # The total number of completed tasks. This calculation loops through the task_list and counts every task marked as complete (True)
    total_completed = 0

    for t3 in task_list:
        if t3.completed == True:
            total_completed += 1

    # The total number of incomplete tasks. This calculation loops through the task_list and counts every task marked as not complete (False) 
    total_incomplete = 0

    for t4 in task_list:
        if t4.completed == False:
            total_incomplete += 1
    
    
    # The total number of tasks that haven’t been completed and are overdue.
    # This calculation loops through the task_list and counts every task marked as not complete (False) and with a due date less than today
    total_overdue_incomplete = 0
    
    for t9 in task_list:
        if t9.completed == False and t9.due_date < datetime.today(): # Uses datetime function and today() method to compare the date today with the due_date
            total_overdue_incomplete += 1
 

    # This calculates the percentage of tasks that haven’t been completed and are overdue.
    # If the total_incomplete or total_tasks are 0 then the percent_incomplete will be set to 0
    if total_overdue_incomplete == 0 or  total_tasks == 0:
        percent_incomplete = 0

    percent_incomplete = round(total_overdue_incomplete / total_tasks * 100,2)   # Displays rounded to 2 decimal places

    # The percentage of tasks that are overdue (and not completed)
    total_overdue = 0
    percentage_overdue = 0.0
    
    for t5 in task_list:
        
        if t5.completed == False and t5.due_date < datetime.today(): # Uses datetime function and today() method to compare the date today with the due_date
            total_overdue += 1

    if total_overdue == 0 or  total_tasks == 0:   # If the total_incomplete or total_tasks are 0 then the percent_incomplete will be set to 0
        percentage_overdue = 0
    percentage_overdue = round(total_overdue / total_tasks * 100,2)


    # Open file task_overview.txt and write the above calculations to the file on each line
    with open("task_overview.txt", "w") as file:
        file.write("Total tasks:\t\t\t\t" + str(total_tasks) + "\n")
        file.write("Total completed:\t\t\t\t" + str(total_completed) + "\n")
        file.write("Total not completed:\t\t\t" + str(total_incomplete) + "\n")
        file.write("Total incomplete & overdue:\t\t" + str(total_overdue_incomplete)+ "\n")
        file.write("Tasks not completed (%):\t\t" + str(percent_incomplete)+"\n")
        file.write("Tasks overdue (%):\t\t\t" + str(percentage_overdue) + "\n")


    # Calculations for user_overview.txt
 
    # The total number of users is the len of the username_password dictionary
    total_users = len(username_password.keys())

    # The total number of tasks is the length of the task list
    total_tasks = len(task_list)

    # The total number of tasks assigned to that user. 
    total_user_tasks = 0        # The integer variable, total_user_tasks, will count the no of tasks the user has in the task list

    # This for loop iterates through the task list and if the username for that iteration matches the username of the signed in user, curr_user
    # Then total_user_tasks is increased by 1
    for t5 in task_list:
        if t5.username == curr_user:
            total_user_tasks += 1

    # The percentage of the total number of tasks that have been assigned to that user
    # If the total_user_tasks is 0 or the total_tasks is 0 then the percent_user_complete is set to 0
    if total_user_tasks == 0 or total_tasks == 0:
        percent_user_complete = 0.0

    percent_user_tasks = round(total_user_tasks / total_tasks * 100,2)

    # The percentage of the tasks assigned to that user that have been completed
    total_user_complete = 0
    percent_user_complete = 0.0

    for t6 in task_list:
        if t6.completed == True and t6.username == curr_user:
            total_user_complete += 1

    # If the total_user_complete is 0 or the total_user_tasks is 0 then the percent_user_complete is set to 0
    if total_user_complete > 0 and total_user_tasks > 0:
        percent_user_complete = round(total_user_complete / total_user_tasks * 100,2)
    elif total_user_complete == 0 or total_user_tasks == 0:
        percent_user_complete = 0.0

    # The percentage of the tasks assigned to that user that must still be completed
    percent_user_incomplete = 100-percent_user_complete

    # The percentage of the tasks assigned to that user that have not yet been completed and are overdue
    total_user_overdue_incomplete = 0
    percentage_user_overdue_incomplete = 0.0

    for t6 in task_list:
        # If statement will pull out the not completed, overdue for the current user. 
        # Then it will increment the total_user_overdue_incomplete counter by 1
        # Use datetime function and today() method to compare the date today with the due_date

        if t6.completed == False and t6.due_date < datetime.today() and t6.username == curr_user:
            total_user_overdue_incomplete += 1

    # This calculates the percentage_user_overdue_incomplete.
    # If total_user_overdue_incomplete or total_user_tasks is 0 then percentage_user_overdue_incomplete is set to 0
    if total_user_overdue_incomplete > 0 and total_user_tasks > 0:      
        percentage_user_overdue_incomplete = round(total_user_overdue_incomplete / total_user_tasks * 100,2)
    elif total_user_overdue_incomplete == 0 or total_user_tasks == 0:
        percentage_user_overdue_incomplete == 0.0

    
    # Open user_overview.txt and write these calculations to the file as strings
    with open("user_overview.txt", "w") as file:
        file.write("Total number of users:\t\t\t" + str(total_users) + "\n")
        file.write("Total tasks:\t\t\t\t\t" + str(total_tasks) + "\n")
        file.write("Total tasks assigned to you:\t\t" + str(total_user_tasks) + "\n")
        file.write("Tasks assigned to you (%):\t\t\t" + str(percent_user_tasks) + "\n")
        file.write("Tasks you have completed (%):\t\t" + str(percent_user_complete) + "\n")
        file.write("Your incomplete tasks (%):\t\t\t" + str(percent_user_incomplete) + "\n")
        file.write("Your uncompleted & overdue tasks (%):\t" + str(percentage_user_overdue_incomplete))


def display_stats():

    # Call the make_reports function to run to update the files
    make_reports()                                 

   # Display task_overview.txt
   
    # Open the task_overview.txt and assign it to task_overview_file. Read into task_overview_data

    with open("task_overview.txt", 'r') as task_overview_file:
        task_overview_data = task_overview_file.read().split("\n")     # task_overview_file is read and split to form the task_overview_data list    
        task_overview_data = [t for t in task_overview_data if t != ""]

    # Convert to a dictionary

    dict_task_overview_data = {}        # An empty dictionary is declared
    for item in task_overview_data:     # Every iteration splits the task_overview_data on the colon into Calculation_Description and Value1
        Calculation_Description, Value1 = item.split(":")
        dict_task_overview_data[Calculation_Description] = Value1  # For every iteration value1 is assigned to the Calculation_Description key
    
    # Print the task overview dictionary, dict_task_overview_data
    # For all keys and values in the dict_task_overview_data are prints using the items method

    print("----------------------------------------------")
    print("               Task Overview                  ")
    print("----------------------------------------------")
    for keys, values in dict_task_overview_data.items():
        print(keys, ":", values)
    print("----------------------------------------------")



    # Display user_overview.txt

    # Open the user_overview.txt and assign it to user_overview_file. Read into user_overview_data
    with open("user_overview.txt", 'r') as user_overview_file:
        user_overview_data = user_overview_file.read().split("\n")      # user_overview_file is read and split to form the user_overview_data list
        user_overview_data = [v for v in user_overview_data if v != ""]

    # Convert user_overview_data list to a dictionary called dict_user_overview_data
    dict_user_overview_data = {}            # An empty dictionary is declared
    for item2 in user_overview_data:        # Every iteration splits the user_overview_data on the colon into Calculation_Description2 and Value2
        Calculation_Description2, Value2 = item2.split(":")       
        dict_user_overview_data[Calculation_Description2] = Value2  # For every iteration value2 is assigned to the Calculation_Description2 key
    
    # Print the user overview dictionary, dict_user_overview_data
    # For all keys and values in the dict_user_overview_data are prints using the items method
    print("\n----------------------------------------------")
    print("                User Overview                 ")
    print("----------------------------------------------")
    for keys1, values1 in dict_user_overview_data.items():
        print(keys1, ":", values1)

    print("----------------------------------------------")




#########################
# Main Program
######################### 

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports                   
    ds - display statistics
    e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - view my task
    gr - generate reports
    e - Exit
    : ''').lower()

    if menu == 'r': # Register new user (if admin)

        reg_user() # Call the reg_user function

    elif menu == 'a': 
  
        add_task() # Call the add_task function


    elif menu == 'va': # View all tasks

        view_all() # Call the view_all function


    elif menu == 'vm': # View my tasks

        view_mine() # Call the view_mine function

    
    elif menu == 'gr': # Generate reports

        make_reports() # Call the make_reports function


    elif menu == 'ds' and curr_user == 'admin': # If admin, display statistics

        display_stats() # Call the new display_stats function


    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else: # Default case
        print("You have made a wrong choice, Please Try again")