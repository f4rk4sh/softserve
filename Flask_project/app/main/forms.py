from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField,\
    DateField, TimeField, FieldList, FormField, SelectField, Form
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, length, NumberRange, ValidationError
from wtforms.widgets import DateInput, TimeInput
from datetime import datetime


class QuestionForm(FlaskForm):
    area = StringField('Area', validators=[DataRequired(), length(max=100)])
    question = TextAreaField('Question', validators=[DataRequired(), length(max=200)])
    answer = TextAreaField('Answer', validators=[DataRequired(), length(max=400)])
    max_grade = IntegerField('Max grade', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Confirm')


class QuestionSetForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), length(max=50)])
    area = StringField('Area', validators=[DataRequired(), length(max=100)])
    level = SelectField('Level',
                        choices=['junior', 'middle', 'senior'],
                        validators=[DataRequired()])
    questions = QuerySelectMultipleField('Questions',
                                         get_label='question',
                                         allow_blank=False,
                                         blank_text='Select one or more questions',
                                         render_kw={'size': 10},)
    submit = SubmitField('Confirm')


class RecruiterInterviewForm(FlaskForm):
    interviewee = StringField('Interviewee', validators=[DataRequired(), length(max=50)])
    brief = TextAreaField('Brief info', validators=[DataRequired(), length(max=200)])
    date = DateField('Date', widget=DateInput(), validators=[DataRequired()])
    time = TimeField('Time', widget=TimeInput(), validators=[DataRequired()])
    users = QuerySelectMultipleField('Interviewers',
                                     get_label='name',
                                     allow_blank=False,
                                     blank_text='Select one or more interviewers',
                                     render_kw={'size': 10},)
    submit = SubmitField('Confirm')

    def validate_date(self, *args):
        if datetime.combine(self.date.data, self.time.data) < datetime.now():
            raise ValidationError('Interview datetime cannot be in the past.')

    def validate_time(self, *args):
        if datetime.combine(self.date.data, self.time.data) < datetime.now():
            raise ValidationError('Interview datetime cannot be in the past.')


class ManageQuestionsForm(FlaskForm):
    sets = QuerySelectMultipleField('Question sets',
                                    get_label='title',
                                    render_kw={'size': 10},)
    questions = QuerySelectMultipleField('Questions',
                                         get_label='question',
                                         render_kw={'size': 10},)
    submit = SubmitField('Confirm')

    def validate_sets(self, *args):
        if len(self.questions.data) == 0 and len(self.sets.data) == 0:
            raise ValidationError('Select one or more sets.')

    def validate_questions(self, *args):
        if len(self.questions.data) == 0 and len(self.sets.data) == 0:
            raise ValidationError('Select one or more questions.')


class GradeForm(Form):
    grade = SelectField(validators=[DataRequired()])


class GradeFormSet(FlaskForm):
    grade_set = FieldList(FormField(GradeForm), min_entries=1)
    submit = SubmitField('Confirm')
