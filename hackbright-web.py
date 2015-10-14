from flask import Flask, request, render_template, redirect

import hackbright_our_version

app = Flask(__name__)



@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Add a student."""
    return render_template("student_add.html")


@app.route("/student-add", methods=["POST"])
def student_adding():
    """Add a student."""
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    github = request.form["github"]

    # call the function that makes the new student
    hackbright_our_version.make_new_student(first_name, last_name, github)

    # flash("New student added")

    return redirect("/student-search")


@app.route("/student")
def get_student():
    """Show information about a student."""

    #this is broken

    github = request.args.get('github','sdevelops')
    aggregate_list = hackbright_our_version.get_student_info_and_project_info(github)
    return render_template('student_info.html', aggregate_list=aggregate_list)

if __name__ == "__main__":
    hackbright_our_version.connect_to_db(app)
    app.run(debug=True)
