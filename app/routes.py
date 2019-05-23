import flask, flask_login, werkzeug.urls
from app import app, db
from app.forms import LoginForm, RegistrationForm, editProfileForm
from app.models import User
from datetime import datetime

@app.before_request
def before_request():
    if flask_login.current_user.is_authenticated:
        flask_login.current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@flask_login.login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return flask.render_template('index.html',
                                 title='Home y\'all', posts=posts)

@app.route('/about')
def about():
    return flask.render_template('about.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flask.flash('Invalid username or password')
            return flask.redirect(flask.url_for('login'))
        flask_login.login_user(user, remember = form.remember_me.data)
        next_page = flask.request.args.get('next')
        if not next_page or werkzeug.urls.url_parse(next_page).netloc != '':
            next_page = flask.url_for('index')
        return flask.redirect(flask.url_for('index'))
    return flask.render_template('login.html', title = 'Sign in', form=form)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flask.flash('Congratulations, you are now a registered user!')
        return flask.redirect(flask.url_for('login'))
    return flask.render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@flask_login.login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return flask.render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods = ['GET', 'POST'])
@flask_login.login_required
def edit_profile():
    form = editProfileForm()
    if form.validate_on_submit():
        flask_login.current_user.username = form.username.data
        flask_login.current_user.about_me = form.about_me.data
        db.session.commit()
        flask.flash('Your changes have been saved.')
        return flask.redirect(flask.url_for(('edit_profile')))
    elif flask.request.method == 'GET':
        form.username.data = flask_login.current_user.username
        form.about_me.data = flask_login.current_user.about_me
    return flask.render_template('edit_profile.html', title='Edit profile',
                                 form = form)
