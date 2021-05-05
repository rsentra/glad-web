from flask import render_template, abort,flash,redirect,url_for,request
from flask_login import login_required,current_user
from datetime import datetime
from sqlalchemy import outerjoin

from . import blog
from ..models import Post,Employee
from .forms import RegistrationForm
from .. import db
from config import POSTS_PER_PAGE

def _get_blogging_engine(app):
    return app.extensions["FLASK_BLOGGING_ENGINE"]


@blog.route('/blog/openblogs')
def openblogs(count=0, page=0):
    """
    Serves the page with a list of blog posts

    :param count:
    :param offset:
    :return:
    """
    blogging_engine = _get_blogging_engine(current_app)
    storage = blogging_engine.storage
    config = blogging_engine.config
    count = count or config.get("BLOGGING_POSTS_PER_PAGE", 10)

    meta = _get_meta(storage, count, page)
    offset = meta["offset"]
    meta["is_user_blogger"] = _is_blogger(blogging_engine.blogger_permission)
    meta["count"] = count
    meta["page"] = page

    render = config.get("BLOGGING_RENDER_TEXT", True)
    posts = storage.get_posts(count=count, offset=offset, include_draft=False,
                              tag=None, user_id=None, recent=True)
    index_posts_fetched.send(blogging_engine.app, engine=blogging_engine,
                             posts=posts, meta=meta)
    for post in posts:
        blogging_engine.process_post(post, render=render)
    index_posts_processed.send(blogging_engine.app, engine=blogging_engine,
                               posts=posts, meta=meta)
    return render_template("blogging/index.html", posts=posts, meta=meta,
                           config=config)

