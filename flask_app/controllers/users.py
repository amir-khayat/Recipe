from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


    # Valid
@app.route('/')
def login_page():
    return render_template("user_login.html")

    # Valid
@app.route('/register', methods=['POST'])
def register():
    # Validate form data
    is_valid = User.validate(request.form)

    if is_valid:
        # Hash password
        pw_hash = bcrypt.generate_password_hash(request.form['password'])

        # Create user
        user_data = {
            'first_name': request.form['first_name'],
            'email': request.form['email'],
            'password': pw_hash,
        }

        user_id = User.save(user_data)
        print(user_id)

        # Store user ID in session
        session['user_id'] = user_id

        # Redirect to dashboard page
        return redirect('/dashboard')
    

    return redirect('/')


@app.route('/login', methods=['POST'])
def login(): 
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id

    return redirect('/dashboard')


    # Valid
@app.route('/logout_session')
def logout(): 
    session.clear()
    return redirect('/')
