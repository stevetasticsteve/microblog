import flask_wtf
import wtforms, wtforms.validators
from app.models import User

class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])
    remember_me = wtforms.BooleanField('Remember Me')
    submit = wtforms.SubmitField('Sign In')

    
class RegistrationForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired()])
    email = wtforms.StringField('Email', validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])
    password2 = wtforms.PasswordField(
        'Repeat Password', validators=[wtforms.validators.DataRequired(), wtforms.validators.EqualTo('password')])
    submit = wtforms.SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise wtforms.validators.ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise wtforms.validators.ValidationError('Please use a different email address.')


class editProfileForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators = [wtforms.validators.DataRequired()])
    about_me = wtforms.TextAreaField('About me', validators = [wtforms.validators.Length(min=0, max=140)])
    submit = wtforms.SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
