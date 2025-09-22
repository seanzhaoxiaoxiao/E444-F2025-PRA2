from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)




class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[lambda form, field: field.data or ValidationError('This field is required.')])
    email = StringField('What is your UofT email address?', validators=[
        lambda form, field: (
            (_ for _ in ()).throw(ValidationError("This field is required.")) if not field.data else None
        ),
        lambda form, field: (
            (_ for _ in ()).throw(ValidationError(f"Please include an '@' in the email address. '{field.data}' is missing an '@'")) if field.data and '@' not in field.data else None
        )
    ])
    prev_name = HiddenField()
    prev_email = HiddenField()
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    name = None
    email = None
    email_valid = False
    if form.is_submitted() and not form.validate():
        # If there are validation errors, just show the form with errors, don't process further
        return render_template('index.html', form=form, name=None, email=None, email_valid=False)

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        prev_name = form.prev_name.data
        prev_email = form.prev_email.data
        if prev_name and prev_name != name:
            flash('Looks like you have changed your name!')
        if prev_email and prev_email != email:
            flash('Looks like you have changed your email!')
        email_valid = 'utoronto' in email
        # After processing, update hidden fields for next request
        form.prev_name.data = name
        form.prev_email.data = email
        return render_template('index.html', form=form, name=name, email=email, email_valid=email_valid)

    # On GET, initialize hidden fields as empty
    form.prev_name.data = ''
    form.prev_email.data = ''
    return render_template('index.html', form=form, name=None, email=None, email_valid=False)
