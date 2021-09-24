from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET', 'POST'])
def index():
    sort_form = SortForm()
    posts = Post.query.order_by(Post.timestamp.desc())
    if sort_form.validate_on_submit():
        posts = Post.query.order_by(eval(sort_form.sort_by.data).desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all(), form = sort_form)

@bp_routes.route('/postsmile', methods=['GET', 'POST'])
def postsmile():
    post_form = PostForm()
    if post_form.validate_on_submit():
        def get_tagList():
            selected_tag = []
            for tag in post_form.tag.data:
                selected_tag.append(tag)
            return selected_tag
            
        new_post = Post(title=post_form.title.data, body=post_form.body.data, 
                        happiness_level=post_form.happiness_level.data, tags=get_tagList())
        db.session.add(new_post)
        db.session.commit()
        flash('Your Post "' + new_post.title + '" has been successfully created!')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form = post_form)

@bp_routes.route('/like/<post_id>', methods=['POST'])
def like(post_id):
    post = Post.query.filter_by(id = post_id).first()
    post.likes += 1
    db.session.commit()
    return redirect(url_for('routes.index'))

