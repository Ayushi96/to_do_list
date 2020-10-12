
'''
Package to create and maintain your personal TO-DO list 

@author: Ayushi Vishwakarma
'''
import os
import colorama
from termcolor import colored, cprint
import pyfiglet
import getpass
import glob
# bg-color = 'on_grey'

class User():
	"""
		This class represents the users of the TO-DO list package and contains 
		the attributes of the user as well as defines the functions that a user 
		shall be able to perform 

		Instance Variables:
			username(str): name of the user for logging in 
			pass(str): secret key used to allow the user to view and edit the
			items in the TO-DO list

	"""

	# list containing the list of all registered users
	user_list = []		
	pass_list = []
	# text file mastersheet contains entries in the format:
	# [users, password, user_dir(address)]
	masterfile = "mastersheet.txt"	

	def __init__(self, name):
		"""
			Args:
				name(str): unique user name of the user
				dir_address(str): path to the dir that will store all the to-do
				notes of the user
		"""
		self.username = name
		self.dir_address = os.path.join(os.getcwd(), 'Users', self.username) 

	def welcome_user(self):
		"""
			This method displays a welcome message to the registered user 
			along with the username of the person!
			The text is displayed in Cyan color on a Grey background

			Args:
				None

			Returns:
				None
		"""
		text =  pyfiglet.figlet_format(f"Welcome {self.username}", font="starwars")
		to_print = colored(text)
		colorama.init()
		cprint(text, 'cyan', 'on_grey', attrs=['bold'])

	@classmethod
	def validate_username(cls):
		"""
			This method takes a name string that should not be present in the 
			list of registered users with the User class

			Returns:
				(boolean)
				- True if the input name was unique
				- False if the name provided already has been registered before
				(str)
				- accepted username for the user
		"""
		print("Enter a unique username:")
		name = str(input())
		while(name in cls.user_list):
			print("username already exists!!")
			# TO-DO: give user an option to login using the existing username 
			# or exit by returning False
			#
			print(" please re-enter a unique username")
			name = str(input())
		print("You are a step closer!")
		return True, name

	@staticmethod
	def validate_pass(password):
		"""
			This method takes a password string as input and checks if it follows the
			constraints of a strong password as required by the TO-DO list norms

			Args:
				password(str): a string of 4 to 8 alpha-numeric characters

			Returns: 
				(boolean):
				- True if the password string follows the constraints of a strong password
				- False if it does not 
		"""
		
		# check if the password is at-least 4 and at-max 8 characters long
		if (len(password) < 4 and len(password) > 8):
			return False
		# check if the password contains at-least one digit and one upper case letter 
		if (any(char.isdigit() for char in password) and any(char.isupper() for char in password)):
			return True
		
		return False

	@staticmethod
	def input_pass():

		print("A strong password should contain a number and an uppercase letter \
			(min len: 4  max len: 8) ")
		print("Enter a strong password")
		password = str(getpass.getpass())

		is_strong = False
		first_attempt = True
		while(not is_strong):
			if not first_attempt:
				print("Please provide a strong password")
				first_attempt = False
			is_strong = User.validate_pass(password)
			
			

		return password

	@classmethod
	def register_user(cls):
		"""
			This method adds a new user to the list of registered users:
				
				1. It checks if the username provided is unique
				2. The password contains a number, an uppercase letter and 
				has a length of min 4 chars and max 8 characters
				3. It also creates a directory in the name of the registered
				user to save his notes in 

			Args:
				None

			Returns:
				boolean
				- True if user registration was succesful 
				- False if user registration failed

				dir_address(str)
				- a string containing the file path to the new dir created for 
				the user  

				name(str)
				- username of the registered user

		"""
		# string to be added to the mastersheet 
		mastersheet_line = ""		
		# address of the directory created for the user
		dir_address = ""
		is_unique = False

		#validate the username
		while(not is_unique):
			is_unique, name = User.validate_username()
			if is_unique == False:
				cprint("Username already exists!", 'red', 'on_grey')
				cprint("Enter 1 to try with another username :) ", 'green', 'on_grey')
				cprint("Enter 0 to exit", 'red', 'on_grey')
				try_again = str(input())
				if try_again is "1":
					continue
				else:
					return False, dir_address

			else:
				break

		# input a strong password from user
		password = User.input_pass()

		print("Confirm the password")
		re_pass = str(input())

		# if the re-entered password is not the same as the original password
		# take input again
		while (password != re_pass):
			print("passwords do not match, please re-enter the passwords")
			pasword = input_pass()
			print("Confirm the password")
			re_pass = str(input())

		# store the dir path for the user 
		dir_address = os.path.join(os.getcwd(), 'Users', name)

		# create a dedicated directory for user's notes
		if not os.path.isdir(dir_address):
			os.makedirs(dir_address)
		
		# Registering the user
		# unique username added to the list of users 
		cls.user_list.append(name)

		# record the user in the mastersheet
		with open(User.masterfile, 'w+') as f:
			f.writelines([name, ",", password, ",",  dir_address])
		# display success message 
		cprint("Registration succesful!!", 'green', 'on_grey')

		return True, dir_address, name

	@classmethod
	def authenticate_user(cls):
		"""
			This method matches the entered username and password with the 
			mastersheet and lets the user login into/exit from the TO-DO list
			
			Args:
				None

			Returns:
				(boolean)
				- True if the entered values match an entry in the mastersheet
				- False if the entered values do not match and user wants to exit 

				name(str):
				- the username for User object creation

		"""

		correct_name = False
		while(not correct_name):
			cprint("username:", 'yellow', 'on_grey', attrs=['bold'])
			name = str(input())
			if name in User.user_list:
				correct_name = True
			else:
				cprint("Unrecognized Username", 'red', 'on_grey')
				print("Enter a valid username")
				continue
		
		correct_pass = False					
		while(not correct_pass):
			cprint("password:", "yellow", 'on_grey', attrs=['bold'])
			password = str(getpass.getpass())
			real_pass = cls.pass_list[cls.user_list.index(name)]
			# == can not be replaced by is 
			if real_pass == password:
				# return name and dir address of user
				return True, name
			else:
				cprint("Wrong password, press 1 to try again")
				try_again = str(input())
				if try_again is '1':
					continue
				else:
					return False, ''

	def display_options(self):
		cprint("Choose from the following options:", 'cyan', 'on_grey')
		cprint("1. Create a new to-do list", 'cyan', 'on_grey')
		cprint("2. Add a task to the list", 'cyan', 'on_grey')
		cprint("3. Delete a task from the list ", 'cyan', 'on_grey')
		cprint("4. View a list of all the to-do list", 'cyan', 'on_grey')
		cprint("5. View Content of a to-do list", 'cyan', 'on_grey')
		cprint("6. Mark a task complete", 'cyan', 'on_grey')
		#cprint("7. Sort to-do list by priority", 'cyan', 'on_grey')
		#cprint("8. Edit priority of task ", 'cyan', 'on_grey')
		cprint("7. Delete a to-do list", 'cyan', 'on_grey')
		cprint("Press 0 to Exit", 'cyan', 'on_grey')
		

	@classmethod
	def load_user_data(cls):
		with open(cls.masterfile, 'w+') as f:
			for line in f.readlines():
				line = line.strip()
				creds = line.split(',')
				# add username 
				cls.user_list.append(creds[0])
				# add user pass
				cls.pass_list.append(creds[1])

	def create_note(self):
		"""
			This method creates an empty text file in the user's directory
		"""
		print("What will be the to-do note be about ? \n Please provide a title")
		title = str(input())
		title += ".txt"
		
		os.chdir(self.dir_address)
		print(f"current dir = {os.getcwd()} ")
		with open(title, 'w+') as f:
			f.writelines(["Task", '\t', "Priority", '\t', "Task Status"])
		cprint("To-do note created ")

	def add_task(self):
		"""
			This method takes input of the note title that was created and 
			 writes a line in the note that was created. If the note does not exist
			 it displays the option of note titles that can be chosen for and gives
			 an option to re-enter the title or exit 

		"""
		while(True):

			print("Please enter the title of the note in which you wish to add the task")
			title = str(input())
			# change to user's directory
			os.chdir(self.dir_address)
			title += '.txt'
			if not os.path.isfile(title):
				cprint(f"There is no note titled '{title}'! ", 'red', 'on_grey')
				print("Please provide a title from this list")
				# display all the notes
				self.show_notes()
				print("Press 1 to continue or 0 to exit")
				choice = str(input())
				if choice is "0":
					print("user wants to exit !")
					return
				else:
				 continue
			else:
				print("Please enter the task to be added")
				task = str(input())
				print("Enter the priority of the task[eg. High, Medium or Low]")
				priority = str(input())
				

				with open(title, 'a+') as f:
					f.writelines([task, "\t\t\t\t", priority, '\t\t\t\t', "WIP", '\n'])
				cprint("task added succesfully!", 'green', 'on_grey')
				break
			return

	def delete_task(self):
		"""
			This method takes input of a valid note title and displays the tasks 
			in that note which can be deleted. It then asks for the user to select 
			which task has to be deleted and then removes that line from the ntoe
			file.
		"""
		
		#print("List of tasks in this to-do note:\n")
		# display all the tasks in this to-do note
		n_tasks, title = self.display_tasks()
		if int(n_tasks) == 0:
			cprint("No tasks to delete! Add a task 1st!", 'red', 'on_grey') 
			return
		
		while(True):

			print("Enter the task number which you want to delete")
			choice = str(input())
			print(f"choice = {choice}")
			if int(choice) > n_tasks:
				cprint("Invalid task number", 'red', 'on_grey')
			else:
				break 

		os.chdir(self.dir_address)
		
		with open(title, 'r+') as f:
			tasks = f.readlines()
			f.close()
		
		# delete the specified task from the list 
		del tasks[int(choice) - 1]
		with open(title, 'w+') as f:
			for task in tasks:
				f.writelines([task])
		cprint("deleted the task succesfully!", 'green', 'on_grey')
		

		return

	def show_notes(self):
		"""
			This method displays the title of all the to-do notes added by the 
			user.
		"""
		print("You have the following to-do notes added: \n")
		for n, note in enumerate(glob.glob(self.dir_address + '\\*.txt')):
			title = note.split('\\')
			title_name = title[-1].strip(".txt")
			print(f"{n+1}. {title_name}")

	def display_tasks(self):
		"""
			This method displays all the tasks that have been added by the user 
			under some todo note along with the task's priority and status.
		"""
		while(True):

			print("Please enter the title of the note")
			title = str(input())
			title += '.txt'
			# change to user's directory 
			os.chdir(self.dir_address)
			if not os.path.isfile(title):
				cprint(f"There is no note titled '{title}'! ", 'red', 'on_grey')
				print("Please provide a title from this list")
				# display all the notes
				self.show_notes()
				print("Press 1 to continue or 0 to exit")
				choice = str(input())
				if choice is "0":
					print("user wants to exit !")
					return
				else:
					continue

			else:
				with open(title, 'r') as f:
					tasks = f.readlines()
					for n, task in enumerate(tasks):
						print(f"{n+1}. {task}")
					break

		return len(tasks), title

	def mark_complete(self):
		"""
			This method changes the status of a task to complete!
		"""
		n_tasks, title = self.display_tasks()
		print(f"n tasks = {n_tasks}")
		if int(n_tasks) == 0:
			cprint("No tasks to mark complete! Add a task 1st!", 'red', 'on_grey') 
			return
		
		while(True):

			print("Enter the task number which you want to mark as complete")
			choice = str(input())
			print(f"choice = {choice}")
			if int(choice) > n_tasks:
				cprint("Invalid task number", 'red', 'on_grey')
			else:
				print("right choice")
				break 

		os.chdir(self.dir_address)
		with open(title, 'r+') as f:
			tasks = f.readlines()
			f.close()

		# mark the specified task from the list as complete
		line = tasks[int(choice) -1]
		s_line = line.strip('\n')
		s_line = s_line.split('\t\t\t\t')
		s_line[-1] = 'Complete'
		new_line = '\t\t\t\t'.join(s_line)
		new_line += '\n'

		with open(title, 'w+') as f:
			for n, task in enumerate(tasks):
				if n +1 == int(choice):
					f.writelines([new_line])
					continue
				f.writelines([task])
		cprint("marked the task as complete succesfully!", 'green', 'on_grey')
		

		return

	def delete_note(self):
		"""
			This method deletes the todo note that is entered by the user.
		"""
		# displat the titles of all the notes added by the user so far
		self.show_notes()
		os.chdir(self.dir_address)
		while(True):

			print("Please enter the title of the note you want to delete")
			title = str(input())
			title += '.txt'
			# change to user's directory 
			os.chdir(self.dir_address)
			if not os.path.isfile(title):
				cprint(f"There is no note titled '{title}'! ", 'red', 'on_grey')
				print("Please provide a title from this list")
				# display all the notes
				self.show_notes()
				print("Press 1 to continue or 0 to exit")
				choice = str(input())
				if choice is "0":
					print("user wants to exit !")
					return
				else:
					continue

			else:
				os.remove(title)
				cprint("To-do note deleted succesfully", 'green', 'on_grey')
				break
		return


		





# main function 
def main():
	# create a Users directory 
	path = os.path.join(os.getcwd(), 'Users')
	if not os.path.isdir(path):
		os.makedirs(path)
	# Welcome Text 
	text =  pyfiglet.figlet_format("TO-DO List", font="starwars")
	to_print = colored(text)
	colorama.init()
	cprint(text, 'cyan', 'on_grey', attrs=['bold'])
	# Load user data
	User.load_user_data()
	
	name = ''
	password = ''
	
	print("Are you a registerd user? \n  y/n")
	ans = str(input())
	# new user
	if ans is 'n':
		registered, dir_add, name = User.register_user()
		if not registered:
			print("Hope to see you again soon!")
			return
			#usr.display_options()
	# registered user 		 
	elif ans is 'y':
		# TO-DO
		is_valid_user, name = User.authenticate_user()
		if is_valid_user is False:
			print("Exiting the program")
			return 

	usr = User(name)
	usr.welcome_user()
	usr.display_options()
	while(True):
		print("Enter your choice")
		choice = str(input())
		# user wants to exit 
		if choice is "0":
			return
		# create a note
		if choice is "1":
			usr.create_note()
		# add a task in note
		if choice is "2":
			usr.add_task()
		# delete a task in the todo note 
		if choice is "3":
			usr.delete_task()
		# display a list of all the notes added by user
		if choice is "4":
			usr.show_notes()
		# display all the tasks in a given note 
		if choice is "5":
			_ = usr.display_tasks()
		# mark a task as complete
		if choice is "6":
			usr.mark_complete()



		

		

# call for main
main()