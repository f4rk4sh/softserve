from app.main import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Question, Set, Interview, Grade, User
from app.main.forms import QuestionForm, QuestionSetForm, RecruiterInterviewForm, ManageQuestionsForm, GradeFormSet
from app import db
from datetime import date
from app.decorators import admin_or_recruiter_required, admin_or_expert_required, expert_required


@bp.route('/')
def index():
    return render_template('main/index.html')


@bp.route('/questions')
@login_required
@admin_or_expert_required
def question_list():
    page = request.args.get('page', 1, type=int)
    questions = Question.query.paginate(page, 8, False)
    next_url = url_for('main.question_list', page=questions.next_num) if questions.has_next else None
    prev_url = url_for('main.question_list', page=questions.prev_num) if questions.has_prev else None
    return render_template('main/question_list.html',
                           title='Questions',
                           questions=questions.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/questions/add', methods=['GET', 'POST'])
@login_required
@admin_or_expert_required
def question_add():
    question = Question()
    form = QuestionForm()
    if form.validate_on_submit():
        form.populate_obj(question)
        db.session.add(question)
        db.session.commit()
        flash('Question has been successfully added.')
        return redirect(url_for('main.question_list'))
    return render_template('form.html', title='Add question', form=form)


@bp.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_or_expert_required
def question_edit(question_id):
    question = Question.query.filter_by(id=question_id).first_or_404()
    form = QuestionForm()
    if form.validate_on_submit():
        form.populate_obj(question)
        db.session.commit()
        flash('Question has been successfully edited.')
        return redirect(url_for('main.question_list'))
    elif request.method == 'GET':
        form.area.data = question.area
        form.question.data = question.question
        form.answer.data = question.answer
        form.max_grade.data = question.max_grade
    return render_template('form.html', title='Edit question', form=form)


@bp.route('/question/<int:question_id>/delete', methods=['GET', 'POST'])
@login_required
@admin_or_expert_required
def question_delete(question_id):
    question = Question.query.filter_by(id=question_id).first_or_404()
    db.session.delete(question)
    db.session.commit()
    flash('Question has been successfully deleted.')
    return redirect(url_for('main.question_list'))


@bp.route('/sets')
@login_required
@admin_or_expert_required
def set_list():
    page = request.args.get('page', 1, type=int)
    sets = Set.query.paginate(page, 4, False)
    next_url = url_for('main.set_list', page=sets.next_num) if sets.has_next else None
    prev_url = url_for('main.set_list', page=sets.prev_num) if sets.has_prev else None
    return render_template('main/set_list.html',
                           title='Question sets',
                           sets=sets.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/set/add', methods=['GET', 'POST'])
@login_required
@admin_or_expert_required
def set_add():
    question_set = Set()
    form = QuestionSetForm()
    form.questions.query = db.session.query(Question)
    if form.validate_on_submit():
        form.populate_obj(question_set)
        db.session.add(question_set)
        db.session.commit()
        flash('Question set has been successfully added.')
        return redirect(url_for('main.set_list'))
    return render_template('form.html', title='Add question set', form=form)


@bp.route('/set/<int:set_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_or_expert_required
def set_edit(set_id):
    question_set = Set.query.filter_by(id=set_id).first_or_404()
    form = QuestionSetForm()
    form.questions.query = db.session.query(Question)
    if form.validate_on_submit():
        form.populate_obj(question_set)
        db.session.commit()
        flash('Set has been successfully edited.')
        return redirect(url_for('main.set_list'))
    elif request.method == 'GET':
        form.title.data = question_set.title
        form.area.data = question_set.area
        form.level.data = question_set.level
        form.questions.data = question_set.questions
    return render_template('form.html', title='Edit question set', form=form)


@bp.route('/set/<int:set_id>/delete', methods=['GET', 'POST'])
@login_required
@admin_or_expert_required
def set_delete(set_id):
    question_set = Set.query.filter_by(id=set_id).first_or_404()
    db.session.delete(question_set)
    db.session.commit()
    flash('Set has been successfully deleted.')
    return redirect(url_for('main.set_list'))


@bp.route('/interviews')
@login_required
@admin_or_recruiter_required
def interview_list():
    page = request.args.get('page', 1, type=int)
    interviews = Interview.query.filter(
        Interview.date >= date.today()
    ).order_by('date').paginate(page, 8, False)
    next_url = url_for('main.interview_list', page=interviews.next_num) if interviews.has_next else None
    prev_url = url_for('main.interview_list', page=interviews.prev_num) if interviews.has_prev else None
    return render_template('main/interview_list.html',
                           title='Interviews',
                           interviews=interviews.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/interviews/archive')
@login_required
@admin_or_recruiter_required
def interview_list_archive():
    page = request.args.get('page', 1, type=int)
    interviews = Interview.query.filter(
        Interview.date < date.today()
    ).order_by('date').paginate(page, 8, False)
    next_url = url_for('main.interview_list_archive', page=interviews.next_num) if interviews.has_next else None
    prev_url = url_for('main.interview_list_archive', page=interviews.prev_num) if interviews.has_prev else None
    return render_template('main/interview_list_archive.html',
                           title='Archive',
                           interviews=interviews.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/interview/add', methods=['GET', 'POST'])
@login_required
@admin_or_recruiter_required
def interview_add():
    item = Interview()
    form = RecruiterInterviewForm()
    form.users.query = db.session.query(User).filter_by(is_admin=False, is_recruiter=False)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Interview has been successfully established.')
        return redirect(url_for('main.interview_list'))
    return render_template('form.html', title='Add interview', form=form)


@bp.route('/interview/<int:interview_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_or_recruiter_required
def interview_edit(interview_id):
    interview = Interview.query.filter_by(id=interview_id).first_or_404()
    if Grade.query.filter_by(interview_id=interview.id).first():
        flash('You can not edit already rated interview.')
        return redirect(url_for('main.interview_list'))
    form = RecruiterInterviewForm()
    form.users.query = db.session.query(User).filter_by(is_admin=False, is_recruiter=False)
    if form.validate_on_submit():
        form.populate_obj(interview)
        db.session.commit()
        flash('Interview has been successfully edited.')
        return redirect(url_for('main.interview_list'))
    elif request.method == 'GET':
        form.interviewee.data = interview.interviewee
        form.brief.data = interview.brief
        form.date.data = interview.date
        form.time.data = interview.time
        form.users.data = interview.users
    return render_template('form.html', title='Edit interview', form=form)


@bp.route('/interview/<int:interview_id>/delete', methods=['GET', 'POST'])
@login_required
@admin_or_recruiter_required
def interview_delete(interview_id):
    interview = Interview.query.filter_by(id=interview_id).first_or_404()
    db.session.delete(interview)
    db.session.commit()
    flash('Interview has been successfully deleted.')
    return redirect(url_for('main.interview_list'))


@bp.route('/interview/<int:interview_id>/detail')
@login_required
@expert_required
def interview_detail(interview_id):
    interview = Interview.query.filter_by(id=interview_id).first_or_404()
    rated = True if Grade.query.filter_by(user_id=current_user.id, interview_id=interview.id).first() else False
    return render_template('main/interview_detail.html', title='Interview detail', interview=interview, rated=rated)


@bp.route('/interview/<int:interview_id>/questions', methods=['GET', 'POST'])
@login_required
@expert_required
def interview_question(interview_id):
    interview = Interview.query.filter_by(id=interview_id).first_or_404()
    if Grade.query.filter_by(interview_id=interview.id).first():
        flash('You can not manage questions in already rated interview.')
        return redirect(url_for('main.interview_detail', interview_id=interview.id))
    form = ManageQuestionsForm()
    form.sets.query = db.session.query(Set).order_by('level', 'area')
    form.questions.query = db.session.query(Question).order_by('area', 'id')
    if form.validate_on_submit():
        interview.questions = form.questions.data
        for question_set in form.sets.data:
            for question in question_set.questions:
                if question not in form.questions.data:
                    interview.questions.append(question)
        db.session.commit()
        flash('Interview questions have been successfully updated.')
        return redirect(url_for('main.interview_detail', interview_id=interview.id))
    elif request.method == 'GET':
        form.questions.data = interview.questions
    return render_template('form.html', title='Add interview questions', form=form)


@bp.route('/activities')
@login_required
@expert_required
def activities():
    page = request.args.get('page', 1, type=int)
    interviews = Interview.query.filter(
        Interview.users.contains(current_user),
        Interview.date >= date.today()
    ).order_by('date').paginate(page, 8, False)
    next_url = url_for('main.activities', page=interviews.next_num) if interviews.has_next else None
    prev_url = url_for('main.activities', page=interviews.prev_num) if interviews.has_prev else None
    return render_template('main/activities.html',
                           title='Activities',
                           interviews=interviews.items,
                           next_url=next_url,
                           prev_url=prev_url)


@bp.route('/interview/<int:interview_id>/', methods=['GET', 'POST'])
@login_required
def interview(interview_id):
    interview = Interview.query.filter_by(id=interview_id).first_or_404()
    if current_user not in interview.users:
        flash('You are not assigned as interviewer in this interview.')
        return redirect(url_for('main.index'))
    if Grade.query.filter_by(user_id=current_user.id, interview_id=interview.id).first():
        flash('You have already taken part in this interview.')
        return redirect(url_for('main.interview_detail', interview_id=interview.id))
    grades = [dict(grade=None) for _ in interview.questions]
    grade_set_form = GradeFormSet(grade_set=grades)
    score = 0
    max_score = 0
    for form, question in zip(grade_set_form.grade_set, interview.questions):
        form.grade.choices = [i for i in range(1, (question.max_grade + 1))]
        max_score += question.max_grade
    if grade_set_form.validate_on_submit():
        for grade_form, question in zip(grade_set_form.grade_set, interview.questions):
            grade = Grade(user_id=current_user.id,
                          interview_id=interview.id,
                          question_id=question.id,
                          grade=grade_form.grade.data)
            db.session.add(grade)
            score += int(grade_form.grade.data)
        interview.score = ((interview.score / 100 * max_score * len(interview.users)) + score) / len(interview.users) / max_score * 100
        db.session.commit()
        flash('You have successfully rated interview.')
        return redirect(url_for('main.activities'))
    return render_template('main/interview.html', title='Interview', interview=interview, form=grade_set_form)
