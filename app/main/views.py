from flask import render_template, redirect, url_for, flash, request
from . import main
from app.models import Question, Answer, Upvote
from .forms import QuestionForm, AnswerForm
from app import db
from flask_login import login_required, current_user
from flask import current_app


@main.route('/')
def index():

    page = request.args.get('page', 1, type=int)
    order_by = request.args.get('order_by', "date")

    if(order_by=="upvotes"):
        pagination = Question.query.outerjoin(Upvote).group_by(Question.id).order_by(db.func.count(Upvote.id).desc(),
                                                    Question.timestamp.desc()).paginate(page, per_page=current_app.config["QUESTIONS_PER_PAGE"], error_out=False)
    else:
        pagination = Question.query.order_by(Question.timestamp.desc()).paginate(page, per_page=current_app.config["QUESTIONS_PER_PAGE"], error_out=False)

    questions = pagination.items
    return render_template('index.html',  questions=questions, pagination=pagination, order_by=order_by)


@main.route('/new_question', methods=['GET', 'POST'])
@login_required
def new_question():

    form = QuestionForm()

    if form.validate_on_submit():
        question = Question(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template('new_question.html', form=form)


@main.route('/question/<int:id>', methods=['GET', 'POST'])
def view_question(id):
    page = request.args.get('page', 1, type=int)
    question = Question.query.get(id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(body=form.body.data,
                          question=question,
                          author=current_user._get_current_object())
        db.session.add(answer)
        db.session.commit()
        flash('Your answer has been published.')
        return redirect(url_for('.view_question', id=question.id))

    pagination = question.answers.order_by(Answer.timestamp.desc()).paginate(page, per_page=current_app.config["ANSWERS_PER_PAGE"],error_out=False)
    answers = pagination.items

    return render_template('question.html', question=question, answers=answers, correct_answer=question.correct_answer, form=form, pagination=pagination)


@main.route('/delete_question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def delete_question(question_id):

    question = Question.query.filter_by(id=question_id).first_or_404()
    if question.author_id == current_user.id or current_user.is_admin:
        db.session.delete(question)
        db.session.commit()
        flash('The question has been deleted.')
        return redirect(url_for("main.index"))
    else:
        flash("You don't have permission to perform this action")
    return redirect(request.referrer)


@main.route('/delete_answer/<int:answer_id>', methods=['GET', 'POST'])
@login_required
def delete_answer(answer_id):
    answer = Answer.query.filter_by(id=answer_id).first_or_404()
    if answer.author_id == current_user.id or current_user.is_admin:
        question = answer.question
        if question.correct_answer is not None and question.correct_answer.id == answer.id:
            question.correct_answer = None
            db.session.commit()
        db.session.delete(answer)
        db.session.commit()
        flash('The answer has been deleted.')
    else:
        flash("You don't have permission to perform this action")
    return redirect(request.referrer)


@main.route('/correct/<int:question_id>/<int:answer_id>')
@login_required
def correct(question_id, answer_id):
    question = Question.query.filter_by(id=question_id).first_or_404()
    if(current_user.id == question.author_id):
        answer = Answer.query.filter_by(id=answer_id).first_or_404()
        question.correct_answer = answer
        db.session.commit()
    return redirect(request.referrer)


@main.route('/upvote/<int:question_id>/<action>')
@login_required
def upvote(question_id, action):
    question = Question.query.filter_by(id=question_id).first_or_404()
    if action == 'upvote':
        current_user.upvote(question)
        db.session.commit()
    if action == 'downvote':
        current_user.downvote(question)
        db.session.commit()
    return redirect(request.referrer)
