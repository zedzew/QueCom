import os
from flask import render_template, url_for, flash, request, redirect, g
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import QuestionForm, LoginForm, CommentForm
from models import Questions, Comments, User, Like
from app import app, login_manager
from database import db_session

@app.route('/')
@app.route('/index')
def questions():
    questions = Questions.query.all()
    return render_template('index.html', title='Question Test',
                           questions=questions)


@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    form = QuestionForm()
    if form.validate_on_submit():
        add_question = Questions(question=request.form['question'], user_id=g.user.id)
        db_session.add(add_question)
        db_session.commit()
        flash('Question Add!')
        return redirect(url_for('questions'))
    return render_template('add_question.html', title='Add question', form=form)



@app.route('/comment/<question_id>', methods=['GET', 'POST'])

def comment(question_id):
    form = CommentForm()
    question = Questions.query.filter_by(id=question_id).first()
    if not question:
        flash('Question no')
        return redirect(url_for('questions'))
    if form.validate_on_submit():
        comment_text = request.form['comment']
        user = g.user.id
        comment = Comments(comment_text, user, question.id)
        db_session.add(comment)
        db_session.commit()
        flash('Your comment add')
        return redirect(url_for('questions'))
    return render_template('comments.html', title='Comments', question=question, form=form)

@app.route('/like/<comment_id>')
@login_required
def like(comment_id):
    user = g.user.id
    comment = Comments.query.filter_by(id=comment_id).first()
    if Like.query.filter_by(user=user, comment=comment_id).first():
        flash('Already like')
        return redirect(url_for('questions'))
    elif comment:
        add_like = Like(comment=comment_id, user=user)
        db_session.add(add_like)
        comment.likes += 1
        db_session.commit()
        flash("You like comment")
        return redirect(url_for("questions"))
    else:
        flash('This comment not available for like')
        return redirect(url_for('questions'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if g.user.is_authenticated():
        return redirect(url_for('questions'))

    if form.validate_on_submit():
        if form.validate():
            name = request.form['name']
            password = request.form['password']
            user = User.query.filter_by(name=name, password=password).first()
            if user is None:
                flash('Not the correct data, try again')
                return redirect(url_for('login'))
            login_user(user)
            flash("Logged in successfully.")
            return redirect(url_for('questions'))
    return render_template("login_form.html", form=form, title='Log In')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if g.user.is_authenticated():
        return redirect(url_for('questions'))

    if form.validate_on_submit():
        name = request.form['name']
        password = request.form['password']
        if not User.query.filter_by(name=name).first():
            user = User(name, password)
            db_session.add(user)
            db_session.commit()
            flash("You have successfully registered. Now you can enter")
            return redirect(url_for('login'))
        else:
            flash('This name already used.')
            return render_template('login_form.html', form=form, title='Sign up')
    return render_template('login_form.html', form=form, title='Register')

@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out.')
    return redirect(url_for('questions'))


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
