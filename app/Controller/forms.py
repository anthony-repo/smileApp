from flask_wtf import FlaskForm
from flask_wtf.recaptcha import widgets
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import  DataRequired, Length
from app.Model.models import Post, Tag


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), 
                        (2, 'Really happy'), (1,'Happy')])
    tag = QuerySelectMultipleField('Tag', query_factory=(lambda : Tag.query.all()), get_label=(lambda tag : tag.name), 
                            widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    sort_by = SelectField('Sort By', choices = [('timestamp', 'Date'), ('title', 'Title'), 
                    ('likes', 'Number of Likes'), ('happiness_level', 'Happiness Level')])
    submit = SubmitField('Refresh')