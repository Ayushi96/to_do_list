
'''
Package to create and maintain your personal TO-DO list 

@author: Ayushi Vishwakarma
'''
import os
import colorama
from termcolor import colored, cprint
import pyfiglet

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
	# text file mastersheet contains entries in the format:
	# [users, password, user_dir(address)]
	masterfile = "mastersheet.txt"	

	def __init__(self, name, pas):
		self.username = name
		self.password = pas 

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
		text =  pyfiglet.figlet_format(f"Welcom {self.username}", font="starwars")
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
		password = str(input())

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
			f.writelines([name, password, dir_address])
		# display success message 
		cprint("Registration succesful!!", 'green', 'on_grey')

		return True, dir_address, name

# main function 
def main():
	# create a Users directory 
	path = os.path.join(os.getcwd(), 'Users')
	if not os.path.isdir(path):
		os.makedirs(path)
		print("created dir Users")

	print("Welcome to TO-DO list ")
	print("Are you a registerd user? \n  y/n")
	ans = str(input())
	if ans is 'n':
		registered, dir_add, name = User.register_user()
		if registered:
			usr = User(name, dir_add)
			usr.welcome_user()
			#usr.display_options()
		else:
			print("Hope to see you again soon!")
	elif ans is 'y':
		# TO-DO
		pass	

# call for main
main()