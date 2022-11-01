	Development tools: Python, Django Framework and VSCode
			
		Steps to setup and run app:

0. Open vscode terminal
1. Create your virtualenv => virtualenv environmentname
2. Activate your venv => environmentname/Scripts/activate
3. Then, cd FunOlympic-Game-Project
4. pip install -r requirements.txt
5. create superuser -> django-admin createsuperuser 
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver

9. After running the app, go towards 'settings.py' file located in project directory
   and at the end there are email_host_user and email_host_password. Please provide 
   your email and app token as password which can be generated from your google account.

10. Then during registration process, provide your email and check it out 
   for verification process.

11. Hurray!!! App works.



