1. Python and pip need to be installed.

2. Install PostgreSQL on your machine. If you choose to use any other RDM System, you will need to change the database settings in settings.py file.

3. Create a database named “task” or use another name and change the database name settings in settings.py file.

4. The virtual environment.

   a. Installation:
   
      i. open terminal/console and enter the following commands:
      
         1. pip install virtualenv
         2. pip install virtualenvwrapper
         
   b. Creation:
   
      i. navigate to directory where you want to store your virtual environments and enter the following command:
      
         1. python -m venv name_of_environment
         
5. Activate virtual environment by navigating to the directory where activate file is located and just type activate

6. Navigate to the project folder using command:

   a. cd path/to/project/folder
   
7. Commands:

   a. python manage.py run – for starting the server
   b. python manage.py run -arg mm – for making migrations
   c. python manage.py run -arg m – for migrating
   d. python manage.py run -arg csu – for creating super user
   e. python manage.py run -arg t – for running tests
   f. python manage.py run -arg ir – for installing requirements from requirements.txt
   g. multiple arguments can be passed
   
8. Application is running on  http://localhost:6767/ URL
