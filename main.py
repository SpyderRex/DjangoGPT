import openai
import subprocess
import sys
import re
import os
import webbrowser
import importlib
from commands import tasks
from commands import preliminary_commands
from commands import app_init
from response import response

openai.api_key = os.environ.get("OPENAI_API_KEY")


chat_log = []

if not os.path.exists("workplace"):
    subprocess.run(["mkdir", "workplace"], check=False)

while True:
    model = input("Hello, I am DjangoGPT, a GPT powered agent designed to automate the process of building a Django website. Choose between two models: 1) GPT3.5-turbo, or 2) GPT4. The first one produces faster responses and is less expensive than the second, but the second produces more accurate answers (select 1 or 2): ")
    print()

    if model == "1":
        model = "gpt-3.5-turbo"
        break
    elif model == "2":
        model = "gpt4"
        break
    else:
        print("You must select 1 or 2.")
        print()
    

django_site_type = input(f"Thank you. You have chosen {model}. What kind of Django website would you like me to build for you? ")
print()

project_name = input("And what would you like to name your Django project? Use a simple but memorable name like 'myproject' or 'mysite': ")
print()

pip_executable = 'pip' if os.system('pip --version') == 0 else 'pip3'

subprocess.check_call([pip_executable, 'install', 'Django'])

python_executable = 'python' if os.system('python --version') == 0 else 'python3'

#subprocess.check_call([python_executable, '-m', 'venv', 'venv'])
"""
if sys.platform == 'win32':
    activate_script = os.path.join('venv', 'Scripts', 'activate.bat')
else:
    activate_script = os.path.join('venv', 'bin', 'activate')
subprocess.check_call([activate_script])
"""

subprocess.check_call(['django-admin', 'startproject', project_name, 'workplace'])


print()
print(f"Django installed and virtual environment set up. Initializing Django project in 'workplace' directory under name {project_name}.")
print()

prime_system = openai.ChatCompletion.create(
  model=model,
  messages=[
        {"role": "system", "content": "I want you to pretend that you are an expert in Django web development."}
        ]
)

chat_log.append({"role": "system", "content": "I want you to pretend that you are an expert in Django web development."})

system_response = prime_system["choices"][0]["message"]["content"]
chat_log.append({"role": "assistant", "content": system_response.strip("\n").strip()})


chat_log.append({"role": "user", "content": f"Give me a detailed plan for building me a fully functional {django_site_type}, named {project_name}, including in this plan the apps that need to be created, as well as the separate views, urls, models, forms, templates, databases, settings, and anything else that would provide a comprehensive website of the kind I wish to build."})

print("Building plan...")
print()

system_response = (model, chat_log)


app_name_prompt = {"role": "user", "content": "What app or apps would I need to initialize in my project? Create a python list of app names for the app or apps I would need to initialize in my project, excluding the standard issued apps already contained in the settings.py file. I am referring to apps that must be initialized by the startapp command. It is important that you create the python list of these app names, with no extra text or comments, not even the command itself, as I have that part covered. I am seeking to automate the process and will need to create from the list a for loop of names. Name the list itself 'app_init_list'."}

chat_log.append(app_name_prompt)

print("Initializing apps...")
print()

system_response = response(model, chat_log)


match = re.search(r'```(.*?)```', system_response, re.DOTALL)

if match:
    code = match.group(1)
    code = re.sub(r"^(import|class|def|\s+)?([a-z]+(\.[a-z]+)*\s+)?((?!print)[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*)\s*=", r"\4 = ", code, flags=re.M)
    with open('commands/app_init.py', 'w') as f:
        f.write(code)
        
importlib.reload(app_init)

current_dir = os.getcwd()        
os.chdir("workplace/")        
for app_name in app_init.app_init_list:
    subprocess.    call(f"{python_executable} manage.py startapp {app_name}", shell=True)
os.chdir(current_dir)

    

bullet_list_tasks_prompt = {"role": "user", "content": "Take all of what I have told you so far and organize it into a python list of separate tasks, starting from the next step after initializing the project itself and the app or apps included in the project. Assume that I have already installed Django, set up a virtual environment, and initialized the project and the app or apps. From that point I want you to create a thorough and comprehensive step-by-step list, making it as detailed as possible. Make sure to name the python list 'task_list'."}

print("Compiling list of tasks...")
print()

chat_log.append(bullet_list_tasks_prompt)

system_response = response(model, chat_log)


double_list = {"role": "user", "content": "Now I want you to double the number of items in the python list you created. Double it by making the list even more comprehensive and by being more detailed in the separate tasks that go into creating a fully functioning Django web site. Remember to name the python list 'task_list'."}

print("Doubling list of tasks for greater detail...")
print()

chat_log.append(double_list)

system_response = response(model, chat_log)


match = re.search(r'```(.*?)```', system_response, re.DOTALL)

if match:
    code = match.group(1)
    code = re.sub(r"^(import|class|def|\s+)?([a-z]+(\.[a-z]+)*\s+)?((?!print)[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*)\s*=", r"\4 = ", code, flags=re.M)
    with open('commands/tasks.py', 'w') as f:
        f.write(code)

    
task_to_command_prompt = {"role": "user", "content": "Now I want you to look at the list of tasks you have compiled for me. I want you to create another python list that contains actual commands, in the order that they need to be completed, for the tasks that can be completed with a command. Provide only the preliminary setup commands for the project, such as installing basic libraries with pip and initialization of the Django project itself. Please do not provide any explanatory material or comments in the list of commands itself, as I plant to use a for loop for the list and implement each command in turn. Assume I am using Linux and bash command line. Call this python list of commands 'preliminary_command_list'."}

print("Creating list of commands...")
print()

chat_log.append(task_to_command_prompt)

system_response = response(model, chat_log)


match = re.search(r'```(.*?)```', system_response, re.DOTALL)

if match:
    code = match.group(1)
    code = re.sub(r"^(import|class|def|\s+)?([a-z]+(\.[a-z]+)*\s+)?((?!print)[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)*)\s*=", r"\4 = ", code, flags=re.M)
    with open('commands/preliminary_commands.py', 'w') as f:
        f.write(code)


os.chdir('workplace')
subprocess.check_call([python_executable, 'manage.py', 'runserver'])

server_url = 'http://localhost:8000'
webbrowser.open(server_url)






        





