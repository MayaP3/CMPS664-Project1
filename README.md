# CMPS664-Project1: Database Normalization and SQL Integration

# Introduction

This project helps with database normalization and integrates with MySQL to generate SQL scripts that create tables and insert data. The program performs tasks like:

- Importing data from a CSV file.

- Identifying functional dependencies and primary keys.

- Checking for compliance with normalization rules (1NF, 2NF, 3NF).

- Decomposing a relation into smaller relations to meet BCNF.

- Generating SQL scripts for creating tables and inserting data into a MySQL database.

- Providing an interactive menu for inserting, updating, and deleting data.

# Features 

- CSV Data Import and Display

- Identification of Functional Dependencies

- Normalization to 1NF, 2NF, and 3NF

- SQL Table Creation and Data Insertion

- Interactive Command-Line Menu for SQL Operations

# Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.6+ (to run the Python script)

- MySQL or MariaDB database (to store the tables)

- MySQL Connector for Python (mysql-connector-python)

You also need a MySQL database setup, for which you'll need credentials (username and password) to connect to it.

# Installation

1. Clone the repository

git clone https://github.com/MayaP3/CMPS664-Project1.git

2. Navigate to the project directory

cd CMPS664-Project1

3. Install dependencies

pip install -r requirements.txt

4. Set up MySQL database

CREATE DATABASE Project1;

5. Modify the connection settings in code

Update the connection details (such as host, user, passwd, database) in the script if needed. It is located in the main() function.

# Usage 

1. Run the Python script

python main.py

2. Follow the prompts

The script will ask for the following inputs:

- Path to the CSV file: The path to your CSV file for data import.

- Functional Dependencies: Enter the functional dependencies in the form of A|B -> C, D;  D->E.

- Primary Key(s): Enter the primary keys for the relation. A, B

3. Normalization and SQL Script Generation

The program will:

- Check for 1NF, 2NF, and 3NF.

- Decompose the relation if necessary.

- Generate SQL scripts for creating tables and inserting the data into your MySQL database.

4. Interactive Menu

After completing the normalization process, you can access an interactive query interface that allows you to:

- Insert Data: Insert new records into your tables.

- Update Data: Modify existing records.

- Delete Data: Delete records from your tables.

- Run Custom SQL Query: Execute any SQL query directly against the database.

- Exit: Exit the interactive menu.

You can choose these operations by entering the corresponding number.

# Interactive Menu

Example Usage of Interactive Menu:
To insert data, choose option 1.

To update data, choose option 2 and provide the required details like which fields to update and the condition.

To run custom queries, choose option 4 and enter the SQL query directly.

ex. If you choose 4, enter: SELECT SUM(ProductPrice) FROM table3
