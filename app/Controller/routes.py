from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from config import Config

from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET', 'POST'])
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sort_form = SortForm()
    posts = Post.query.order_by(Post.timestamp.desc())
    if sort_form.checkbox.data:
        posts = current_user.get_user_posts()
    
    if sort_form.validate_on_submit():
        posts = posts.order_by(eval('Post.' + sort_form.sort_by.data).desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all(), form = sort_form)

@bp_routes.route('/postsmile', methods=['GET', 'POST'])
@login_required
def postsmile():
    post_form = PostForm()
    if post_form.validate_on_submit():           
        new_post = Post(title=post_form.title.data, body=post_form.body.data, 
                        happiness_level=post_form.happiness_level.data, user_id = current_user.id)
        for tag in post_form.tag.data:
            new_post.tags.append(tag)
        
        db.session.add(new_post)
        db.session.commit()
        flash('Your Post "' + new_post.title + '" has been successfully created!')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form = post_form)

@bp_routes.route('/like/<post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id = post_id).first()
    post.likes += 1
    db.session.commit()
    return redirect(url_for('routes.index'))

@bp_routes.route('/delete/<post_id>', methods=['POST', 'DELETE'])
def delete(post_id):
    post = Post.query.filter_by(id = post_id).first()
    if post:
        for tag in post.tags:
            post.tags.remove(tag)
            db.session.commit()
    db.session.delete(post)
    db.session.commit()
    flash('Your Post "' + post.title + '" has been successfully deleted')
    return redirect(url_for('routes.index'))


