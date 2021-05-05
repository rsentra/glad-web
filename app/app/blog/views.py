from flask import render_template, abort,flash,redirect,url_for,request
from flask_login import login_required,current_user
from datetime import datetime
from sqlalchemy import outerjoin

from . import blog
from ..models import Post,Employee
from .forms import RegistrationForm
from .. import db
from flask import current_app
# from config import POSTS_PER_PAGE

@blog.route('/blog/blogs')
def blogs():
    # posts = Post.query.order_by(Post.id.desc()).all()
    POSTS_PER_PAGE= current_app.config['POSTS_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    # posts = Post.query.order_by(Post.id.desc()).paginate(
    #     page, POSTS_PER_PAGE, False)
    
    #outer join을 하여 query()에서 Post,Employee컬럼을 추출 : username을 가져옴
    posts=db.session.query(Post.author_id,Post.title,Post.body,Post.created,Post.id,Employee.username).\
            outerjoin(Employee, Post.author_id == Employee.id).order_by(Post.id.desc()).\
            paginate(page, POSTS_PER_PAGE, False)
    # next_url = url_for('blog.blogs', page=posts.next_num) \
    #     if posts.has_next else None
    # prev_url = url_for('blog.blogs', page=posts.prev_num) \
    #     if posts.has_prev else None        
    # next_num= str(posts.next_num) + 'page'
    # prev_num= str(posts.prev_num) + 'page'
    # return render_template('blog/index.html', posts=posts.items, next_url=next_url,
    #                        prev_url=prev_url,next_num=next_num,prev_num=prev_num)
    return render_template('blog/index.html', posts=posts)


@blog.route('/blog/create', methods=('GET', 'POST'))
@login_required
def create():
    usern=current_user.username
    userid=current_user.id
    print('userid=',userid)
    now=datetime.now()
    form = RegistrationForm()
    if form.validate_on_submit():
        posts = Post(author_id=userid,
                            created=now,
                            title=form.title.data,
                            body=form.body.data)

        # add cars to the database
        db.session.add(posts)
        db.session.commit()

        flash('You have successfully registered blogs!!.')
        # redirect to the login page
        return redirect(url_for('blog.blogs'))

    # load registration template
    return render_template('blog/create.html', form=form, title='Register blog')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@blog.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = Post.query.get_or_404(id)  #from table
    form = RegistrationForm(obj=post) #if not 404
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        error = None
        if not post.title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.session.commit()
            flash('You have successfully edited the blogs.')
            return redirect(url_for('blog.blogs'))

    return render_template('blog/create.html', form=form, title='Update blog')

@blog.route('/<int:id>/detail', methods=('GET', 'POST'))
@login_required
def detail(id):
    post = Post.query.get_or_404(id)  #from table
    return render_template('blog/detail.html', post=post, title='Blog detials')

@blog.route('/<int:id>', methods=('POST','GET'))
@login_required
def delete(id):
    post = Post.query.get_or_404(id) 
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.blogs'))