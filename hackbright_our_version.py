"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect to database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackbright.db'
    db.app = app
    db.init_app(app)


def get_student_by_github(github_name):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github_name})
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])

    return row

def get_student_info_and_project_info(github_name):
    """Given a github account name, return information of the first name, last name, 
    github, and list of all the projects completed and grade for that project."""

    QUERY = """
        SELECT first_name, last_name, github, project_title, grade FROM Students 
        as s Join Grades AS g ON github = student_github)
        WHERE github = :github
    """   

    db_cursor = db.session.execute(QUERY, {'github': github_name})
    row = db_cursor.fetchall()

    return row

def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """INSERT INTO Students VALUES (:first_name, :last_name, :github)"""
    db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name, 'github': github})
    db.session.commit() 
    print "Successfully added student: %s %s" % (first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    QUERY = """
        SELECT * FROM Projects
        WHERE title = :title
        """
    db_cursor = db.session.execute(QUERY, {'title': title}).fetchall()
    for project_details in db_cursor:
        id, title, description, max_grade = project_details
        print "id is {}, title is {}, description is {}, max grade is {}".format(id, title, description, max_grade)

    return db_cursor

def get_grade_by_github_title(github, title):
    """Print grade student received for a project given a github username and project title."""
    QUERY = """
        SELECT grade FROM Grades
        WHERE student_github = :github AND project_title = :title
    """
    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title}).fetchone()
    print "Github: {}; Project Title: {}; Project Grade: {}".format(github, title, db_cursor[0])

    return db_cursor


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    QUERY = """
    INSERT INTO Grades (student_github, project_title, grade) VALUES (:github, :title, :grade)"""
    db.session.execute(QUERY, {'github': github, 'title': title, 'grade': grade})
    db.session.commit()

    print "you have successfully added the grade {} to {}'s github for {} project".format(grade, github, title)

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            get_project_by_title(args[0])

        elif command == "get_grade_by_github_and_title":
            get_grade_by_github_title(args[0], args[1])

        elif command == "assign":
            assign_grade(args[0], args[1], args[2])

        else:
            if command != "quit":
                print "Invalid Entry. Try again."


if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db.session.close()
