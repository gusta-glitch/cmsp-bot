#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

# <----- Import libraries ------------------------------------------------------------------

import argparse
import json
import random
import string
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

# End of inport libraries ----->------------------------------------------------------------


# <----- Important functions ---------------------------------------------------------------

def debug(type, message):
	if args.verbose:
		if type == "error":
			print(f"\033[91m[ERROR]\033[0m {message}")
		elif type == "info":
			print(f"\033[92m[INFO]\033[0m {message}")
		elif type == "warning":
			print(f"\033[93m[WARNING]\033[0m {message}")
		elif type == "success":
			print(f"\033[94m[SUCCESS]\033[0m {message}")
		else:
			print(f"\033[95m[DEBUG]\033[0m {message}")

# End of important functions ----->---------------------------------------------------------


# <----- Set the arguments -----------------------------------------------------------------

parser = argparse.ArgumentParser(usage="%(prog)s [opitions]" ,description="Script to autofill tasklist o CMSP, write in Python", epilog="Developed by: @gustavofreitas", formatter_class=argparse.MetavarTypeHelpFormatter)

parser.add_argument("-V", "--version", help="show version and exit", action="version", version=f"%(prog)s {__version__}")

parser_login = parser.add_argument_group("Login")

parser_login.add_argument("-u", "--ra", type=str, help="RA of the student, with digit")
parser_login.add_argument("-c", "--uf", type=str, help="UF of the student", default="sp")
parser_login.add_argument("-p", "--password", type=str, help="password of the student")
parser_login.add_argument("-t", "--team", type=str, help="team of the student")
parser_login.add_argument("-a", "--amount", type=int, help="amount of tasks to fill")

parser_login.add_argument("-l", "--list", type=str, help="list of user to fill tasks [NOT WORKING]")

parser_debug = parser.add_argument_group("Debug")

parser_debug.add_argument("-v", "--verbose", help="verbose mode", action="store_true", default=False)

args = parser.parse_args()

# End of set the arguments ----->-----------------------------------------------------------

if args.ra and args.password and args.team:
	arg_ra = args.ra
	arg_uf = args.uf
	arg_password = args.password
	arg_team = args.team
	arg_amount = args.amount

	if args.ra.find(".") or args.ra.find("-"):
		try:
			arg_ra = args.ra.replace(".", "")
		except:
			print("Invalid RA, use pattern")
			exit()
		else:
			arg_ra = arg_ra.replace("-", "")
	if args.list:
		with open(args.list, "r") as file:
			if file.name.endswith(".json"):
				arg_list = json.load(file)["users"]
else:
	debug("warning", "Not all arguments were informed")
	exit()

# <----- Set up the driver -----------------------------------------------------------------

driver = webdriver.Chrome() # Set the driver

# End of set up the driver ----->-----------------------------------------------------------


# <----- Set global variables --------------------------------------------------------------

implicit_wait = driver.implicitly_wait(1000 * 1) # Wait 1 second
wait = WebDriverWait(driver, 900)

# End of variables ----->-------------------------------------------------------------------

driver.get("https://cmspweb.ip.tv/") # Open the "CMSP" website

# <----- Set functions ---------------------------------------------------------------------

def login(ra: str, uf: str, password: str):
	debug("info", f"Logging in with RA:{ra} and UF:{uf}")

	time.sleep(0.6) # Wait 600 miliseconds

	wait.until(lambda driver: driver.find_element(By.ID, "access-student")).click() # Click on the "Student" button

	wait.until(lambda driver: driver.find_element(By.ID, "ra-student")).send_keys(ra[slice(0, -1)]) # Enter the student's RA
	wait.until(lambda driver: driver.find_element(By.ID, "digit-student")).send_keys(ra[slice(-1, -2, -1)]) # Enter the student's digit

	uf_stdent = wait.until(lambda driver: driver.find_element(By.ID, "uf-student")) # Select the student's UF
	Select(uf_stdent).select_by_value(uf) # Select the student's UF

	wait.until(lambda driver: driver.find_element(By.ID, "password-student")).send_keys(password) # Enter the student's password

	wait.until(lambda driver: driver.find_element(By.ID, "btn-login-student")).click() # Click on the "Login" button

	debug("success", f"Logged in with RA:{ra} and UF:{uf}")

	return 0
def navigate(team: str):
	debug("info", f"Navigating to team:{team}")

	time.sleep(0.6) # Wait 600 miliseconds

	implicit_wait
	wait.until(lambda driver: driver.find_element(By.ID, "chng")).click() # Click on the "Groups" button

	if team.isnumeric(): 
		implicit_wait
		wait.until(lambda driver: driver.find_elements(By.CSS_SELECTOR, "#roomList > div"))[int(team) - 1].click() # Click on the team
	else:
		implicit_wait
		wait.until(lambda driver: driver.find_element(By.NAME, team)).click() # Click on the "Room" button

	implicit_wait
	wait.until(lambda driver: driver.find_element(By.ID, "channelTaskList")).click() # Click on the "TaskList" button

	driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe")) # Switch to the "TaskList" iframe

	debug("success", f"Navigated to team:{team}")

	return 0
def count_tasks():
	debug("info", "Counting tasks")

	time.sleep(0.6) # Wait 600 miliseconds

	# tasks = driver.execute_script("return document.querySelectorAll(\"#root > div > div.homeuser > main > div.scrollable.homeuser__body--my-tasks > div > table > tbody > tr.MuiTableRow-root.row\")") # Get the tasks
	task_list = wait.until(lambda driver: driver.find_elements(By.CSS_SELECTOR, "#root > div > div.homeuser > main > div.scrollable.homeuser__body--my-tasks > div > table > tbody > tr")) # Get the tasks

	debug("success", f"Found {int(len(task_list) / 2)} tasks")

	return task_list, int(len(task_list) / 2)
def fill_tasks(amount: int):
	tasks = count_tasks()
	task_list = tasks[0] # Get the tasks
	task_amount = tasks[1] # Get the tasks amount
	first_task = 0 # Get the first task
	# fill_amount = 0 # Get the fill amount
	filled = 0 # Set the filled tasks

	if amount == 0 or amount > task_amount:
		fill_amount = task_amount
	else:
		fill_amount = amount

	debug("info", f"Filling {fill_amount} tasks")

	time.sleep(0.6) # Wait 600 miliseconds

	while fill_amount > 0:
		debug("info", f"Filling task {filled + 1} of {fill_amount}")

		task_list[first_task].click() # Click on the first task
		task_list[first_task + 1].find_element(By.TAG_NAME, "button").click() # Click on the "Perform task" button

		time.sleep(0.6) # Wait 600 miliseconds

		implicit_wait
		check_task = driver.execute_script("return document.querySelectorAll('#root > div > div.answer-task > div > div.question__body > div.question__body--multi')") # Get the check task
		radio_task = driver.execute_script("return document.querySelectorAll('div[role=\"radiogroup\"]')") # Get the radio buttons
		text_task = driver.execute_script("return document.querySelectorAll('#root > div > div.answer-task > div:nth-child(2) > div.question__body > div > div > textarea[aria-invalid=\"false\"]')") # Get the text boxes

		if len(radio_task) > 0: # If there is a radio button
			for task in radio_task:
				time.sleep(0.6) # Wait 600 miliseconds

				input = task.find_elements(By.TAG_NAME, "input") # Get the radio buttons
				input[random.randint(0, len(input) - 1)].click() # Select a random answer
		if len(text_task) > 0: # If there is a text box
			for task in text_task:
				time.sleep(0.6) # Wait 600 miliseconds

				task.send_keys(random.choice(string.ascii_letters)) # Fill the text box with a random letter
		if len(check_task) > 0: # If there is a check box
			for task in check_task:
				time.sleep(0.6) # Wait 600 miliseconds

				input = task.find_elements(By.CSS_SELECTOR, "input[type='checkbox']") # Get the check boxes
				input[random.randint(0, len(input) - 1)].click() # Select a random answer

		buttons =  wait.until(lambda driver: driver.find_elements(By.CSS_SELECTOR, "#root > div > div.answer-task > button")) # Get the buttons
		buttons[0].click() # Click on the "Submit" button

		time.sleep(0.6) # Wait 600 miliseconds

		error = driver.execute_script("return document.querySelector('div.Toastify').children.length")
		if error > 0:
			task_amount -= 1 # Decrease the tasks amount
			first_task += 2 # Go to the next task

			buttons[1].click() # Click on the "Close" button

			debug("error", "Error sending task, the task is not supported")

			break
		else:
			filled += 1
			fill_amount -= 1

			if fill_amount == 0:
				break

			time.sleep(0.6) # Wait 600 miliseconds

			tasks = count_tasks()
			task_list = tasks[0] # Get the tasks
			task_amount = tasks[1] # Get the tasks amount

			debug("success", f"Filled task {filled}")
	debug("success", f"Filled {filled} tasks")

	return 0
# End of functions ----->-------------------------------------------------------------------

# <----- Run the script --------------------------------------------------------------------

login(arg_ra, arg_uf, arg_password) # Login
navigate(arg_team) # Navigate to the "TaskList" iframe
fill_tasks(arg_amount) # Fill the tasks

driver.close() # Close the browser

# End of script ----->----------------------------------------------------------------------
