import os
from functools import wraps
from http import HTTPStatus

from database import session
from flask import request
from flask_restful import Resource
from models import Image, Note, User
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import secure_filename


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get("api-key", None)
        if token is None:
            return {
                       "result": False,
                       "msg": "Valid api-token token is missing",
                   }, HTTPStatus.BAD_REQUEST
        try:
            current_user = session.query(User) \
                .filter(User.token == token).one()
            return func(*args, current_user, **kwargs)
        except NoResultFound:
            return {
                       "result": False,
                       "msg": "Sorry. Wrong api-key token. This user does not exist.",
                   }, HTTPStatus.BAD_REQUEST

    return decorator


class UserView(Resource):
    @token_required
    def get(self, current_user):
        return {
            "result": "true",
            "user": {
                "id": current_user.id,
                "name": current_user.name,
                "followers": current_user.get_all_followers(),
                "following": current_user.get_all_following(),
            },
        }


class FollowView(Resource):
    @token_required
    def get(self, current_user, id):
        follow_data = session.query(User).filter(User.id == id).one()
        return {
            "result": "true",
            "user": {
                "id": follow_data.id,
                "name": follow_data.name,
                "followers": follow_data.get_all_followers(),
                "following": follow_data.get_all_following(),
            },
        }


class FollowViewAdd(Resource):
    @token_required
    def post(self, current_user, id):
        follow = session.query(User).filter(User.id == id).one()
        current_user.follow(follow)
        session.commit()
        return {"result": True}

    @token_required
    def delete(self, current_user, id):
        follow = session.query(User).filter(User.id == id).one()
        current_user.unfollow(follow)
        session.commit()
        return {"result": True}


class NoteView(Resource):
    def get(self):
        notes = session.query(Note).order_by(Note.id.desc()).all()
        return {
            "result": True,
            "tweets": [
                {
                    "id": note.id,
                    "content": note.tweet_data,
                    "attachments": note.get_image(),
                    "author": {"id": note.user.id, "name": note.user.name},
                    "likes": note.get_likes(),
                }
                for note in notes
            ],
        }

    @token_required
    def post(self, current_user):
        data = request.json
        note_rec = Note(
            tweet_data=data["tweet_data"],
            user_id=current_user.id,
            image_id=None
            if len(data["tweet_media_ids"]) == 0
            else data["tweet_media_ids"][0],
        )
        session.add(note_rec)
        session.commit()
        return {"result": True, "tweet_id": note_rec.id}


class NoneViewSelf(Resource):
    @token_required
    def delete(self, current_user, id):
        note_data = session.query(Note).filter(Note.id == id).one()
        session.delete(note_data)
        session.commit()
        return {"result": True}


class MediasView(Resource):
    @token_required
    def post(self, current_user):
        file = request.files["file"]
        filename = secure_filename(file.filename)
        image_save = Image(name=filename)
        session.add(image_save)
        file.save(os.path.join("app/static/images/", f"{filename}"))
        session.commit()
        return {"result": True, "media_id": image_save.id}


class LikeView(Resource):
    @token_required
    def post(self, current_user, id):
        current_user.like_note(id)
        return {"result": True}
