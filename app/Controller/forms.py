from flask_wtf import FlaskForm
from flask_wtf.recaptcha import widgets
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import  DataRequired, Length
from app.Model.models import Post, Tag

def get_tag():
    return Tag.query.all()

def get_tagLabel(tag):
    return tag.name

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=1500)])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), 
                        (2, 'Really happy'), (1,'Happy')])
    tag = QuerySelectMultipleField('Tag', query_factory=get_tag, get_label=get_tagLabel, 
                                widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    submit = SubmitField('Post')

class SortForm(FlaskForm):
    sort_by = SelectField('Sort By', choices = [(Post.timestamp, 'Date'), (Post.title, 'Title'), 
                    (Post.likes, 'Number of Likes'), (Post.happiness_level, 'Happiness Level')])
    submit = SubmitField('Refresh')