# Password Reset Example Application written in Flask 

This is a simple and very basic application written in Python (Flask framework) that is meant
to show how to implement the password reset via email feature that is commonly used 
across web applications.

It is heavily influenced by Miguel Grinberg's [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).
If you are working with Flask and haven't stumbled across Miguel's blog go ahead and check it out
right away. He has a lot of stuff on Flask and his Mega-Tutorial is definitely one of the best
places to learn Flask.


## Features of the app
As already mentioned, this is a very basic app with no fancy frontend, just Python (Flask) and some 
HTML. Its sole purpose is to showcase one idea how to implement password reset flow in Flask.
You can register, log-in and reset your password while logged out.
It uses email to send out URL that redirects user to a page for creating new password.

### Pages in the app:
- Home page - empty page with list of links to other pages
- Registration page
- Login page
- Protected page - page that is only visible to logged-in users
- Password reset (and create new password) page

### Some screenshots of the app:

<img src="/docs_screenshots/login.jpg" alt="Login page" width="200">

<img src="/docs_screenshots/reset_password_request.jpg" alt="Reset password request" width="200">

<img src="/docs_screenshots/reset_password_success.jpg" alt="Successful password reset" width="200">

I said it is very basic :)

## Running the app

### Requirements
I have used Python 3.11.5 while I was writing this app, however it should work 
on few lower versions too (you will only maybe have issues in regard to typing with
lower versions of Python).

Other requirements are listed in `requirements.txt` file.

I suggest using Python's [virtual environments](https://docs.python.org/3/library/venv.html) to isolate your Python packages.

Also, instructions bellow were written for macOS, so they will also probably work on Linux.
However, on Windows commands might need some changes.

### Installing the requirements
Clone this repository and enter the directory. Then, create new virtual environment there
and activate it. This is not necessary but is recommended.

```shell
python -m venv venv
source venv/bin/activate
```

Then install the requirements:
```shell
pip install -r requirements.txt
```

### Setting up the database

You now need to set up your database and run your (only) migration. If you don't do anything
the migration will create SQLite database and store the data in the file in the repository
(called `app.db`). 

If you want to use for example PostgreSQL database you will need to set up your database
and export the connection string as a environment variable called `DATABASE_URL`, for example:
```shell
export DATABASE_URL=postgresql://user:secret@localhost
```

By the way, other configuration is set up in the file [config.py](config.py).

After you have set up (or not) the database you can run the migrations. 
Migrations are handled using [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) 
that uses [Alembic](https://alembic.sqlalchemy.org/en/latest/) in the background but 
makes it a bit easier to use in Flask applications. 

To run the migration and create the necessary table to run the app you run the following
command:

```shell
flask db upgrade
```

### Setting up the email manager

Only thing to do left is to set up email manager. To have the full email sending 
functionality you need to either set up an SMTP server or have some third party service
for email delivery, like Mailtrap or Sendgrid. Some services also provide sandboxes
where you can use the actual service but instead the mails end up
in your sandbox. That way you can test your application without actually sending emails.
[Mailtrap](https://mailtrap.io/email-sandbox/) provides that service for free with one inbox.

When you have your email delivery service set up you will need to export environment 
variables with connection details, something like this:

```shell
export MAIL_SERVER=server
export MAIL_USERNAME=user
export MAIL_PASSWORD=pass
export MAIL_PORT=port
```

You also have one other option, in the [config.py](config.py) you can add this line inside the
`Config` class:
```python
MAIL_BACKEND = "console"
```

That way the emails won't be sent anywhere, but will be printed out in your terminal, 
and you don't actually need a working SMTP server.

### Running the actual app
We should now be ready to run the Flask application. To run the app use the following command:

```shell
flask --app password_reset_example_app run --debug
```

If everything worked as expected you should see something like:

```
 * Serving Flask app 'password_reset_example_app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: ****
```

Go ahead and open http://127.0.0.1:5000 in your browser.

Hopefully you can see the home page!

You can now try out the app - register some users, log in, log out, reset your password and so on.
Well, to be honest, that are the only things that you can do actually :D 

## Final notes
This application is written only for educational purposes and is not meant to be 
deployed to production without changes. Feel free to use it on your own risk since there
might be some issues and bugs that I am not aware of. 