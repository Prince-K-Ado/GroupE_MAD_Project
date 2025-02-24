from flask import Blueprint, render_template, request, redirect, url_for, session, flash

main = Blueprint('main', __name__)

# For demonstration, using a simple in-memory user "database"
users = {
    "user@example.com": "password123"
}

@main.route('/')
def index():
    # Redirect to login if not logged in
    if not session.get('user'):
        return redirect(url_for('main.login'))
    return f"Hello, {session.get('user')}! Welcome back."

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Simple credential check
        if email in users and users[email] == password:
            session['user'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return render_template('login.html')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))
