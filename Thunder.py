from flask import Flask, render_template, redirect, Response, request, session

app = Flask(__name__)
app.secret_key = "king is great"
website_user = {}
@app.route('/thunder')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    username = session.get('user')
    if username and username in website_user:
        return render_template('login.html', logged_in=True, username=username)
    return render_template('login.html', logged_in=False)

@app.route('/submit', methods=["POST"])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    if username not in website_user:
        return render_template('submit.html', login_success=False, error="User not found")

    stored_password = website_user[username][3]

    if password == stored_password:
        session['user'] = username
        name = website_user[username][0]
        return render_template('submit.html', login_success=True, name=name)
    else:
        return render_template('submit.html', login_success=False, error="Invalid password")

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/submit1', methods=["POST"])
def submit1():
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    if username in website_user:
        return render_template('submit1.html', real_name=username, name=name, users=website_user, user_exists=True)

    website_user[username] = [name, mobile, email, password]
    return render_template('submit1.html', real_name=username, name=name, users=website_user)

@app.route('/profile')
def profile():
    username = session.get('user')
    if not username or username not in website_user:
        return render_template('login.html', logged_in=False, error="Please log in to view your profile.")

    user = website_user[username]
    return render_template(
        'profile.html',
        name=user[0],
        mobile=user[1],
        email=user[2],
        username=username,
        website_user=website_user
    )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
