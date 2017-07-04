# Log_Analysis
To build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like. This project won't take any input from the user. Instead, it will connect to the database, use SQL queries to analyze the log data, and print out the answers to some questions.
# Instructions
## Prerequisites
* VirtualBox
* Vagrant
* Python 2.7
## Setup
* Install VirtualBox
* Install Vagrant
* Download or Clone [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.
* Change the working directory to vagrant directory within newly created FSND-Virtual-Machine directory.
* Download the [data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) from here and unzip it and copy the file newsdata.sql into the  vagrant directory.
* Run the command vagrant up.
* Run command vagrant ssh to log in to the installed Linux VM.
* Load the data, using the command psql -d news -f newsdata.sql.
* Use psql -d news to connect to database.
### View
Create view tops using:
```
create view tops as select path, count(case status when '200 OK' then 1 else null end) as 
num from log group by path having count(case status when '200 OK' then 1 else null end)>0;
```

## To Run
* Clone or download this repository.
* Run log_analysis.py in the Linux-based virtual machine (VM) using the command:$ python log_analysis.py
