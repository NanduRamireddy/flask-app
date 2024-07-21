## flask-app
In Command prompt run the following:
'docker build -t Complex_Functional_Relation.' - to build the docker container
•	‘docker run -p 5001:5001 Complex_Functional_Relation’ - to run the Code

## 1.) Steps to Use :
•	We can either use Command Prompt or terminal from the Docker Desktop application.
•	First set the directory to flask-app.
•	‘docker build -t flask-app’ Run this line to build the Docker, it will download all the essentials to run the code.
•	‘docker run -p 5001:5001 flask-app’ .This line runs the entire code.
•	Navigate to ‘http://localhost:5001’ to access the web interface.
•	Upload the ‘sample.csv’ using ‘Choose file’ option .
•	The application will generate and display the plot, table, and JSON results.
## 2.) Reproducing the Demonstration Case:
•	Create a ‘sample.csv’ file  with multiple Y_i columns corresponding to the X_i column.
•	Save ‘sample.csv’ in the ‘static’ directory of the project.
•	Run the web application and upload the ‘sample.csv’