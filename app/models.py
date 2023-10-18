from typing import Any, Dict

from database import session
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import DeclarativeBase, backref, relationship


class Base(DeclarativeBase):
    pass


followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("user.id")),
    Column("followed_id", Integer, ForeignKey("user.id")),
)


class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    note_id = Column(Integer, ForeignKey("note.id"))


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    token = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    notes = relationship(
        "Note", back_populates="user",
        cascade="all, delete-orphan", lazy="select"
    )
    followed = relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    like = relationship(
        "Like", foreign_keys="Like.user_id", backref="user", lazy="dynamic"
    )

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id)\
                   .count() > 0

    def like_note(self, note_id):
        if not self.has_liked_note(note_id):
            like = Like(user_id=self.id, note_id=note_id)
            session.add(like)
            session.commit()
            return True
        return self.unlike_note(note_id)

    def unlike_note(self, note_id):
        if self.has_liked_note(note_id):
            session.query(Like).filter(
                Like.user_id == self.id, Like.note_id == note_id
            ).delete()
            session.commit()

    def has_liked_note(self, note_id):
        return (
                session.query(Like)
                .filter(Like.user_id == self.id, Like.note_id == note_id)
                .count()
                > 0
        )

    def get_all_followers(self):
        data = (
            session.query(followers.c.follower_id)
            .filter(followers.c.followed_id == self.id)
            .all()
        )
        return_list = []
        for follower in data:
            user = session.query(User).filter(User.id == follower[0]).one()
            return_list.append({"id": user.id, "name": user.name})
        return return_list

    def get_all_following(self):
        data = (
            session.query(followers.c.followed_id)
            .filter(followers.c.follower_id == self.id)
            .all()
        )
        return_list = []
        for follow in data:
            user = session.query(User).filter(User.id == follow[0]).one()
            return_list.append({"id": user.id, "name": user.name})
        return return_list


class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True)
    tweet_data = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="notes")
    image_id = Column(Integer, ForeignKey("image.id"))
    image = relationship("Image", back_populates="note")
    like = relationship("Like", backref="note", lazy="dynamic")

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_likes(self):
        all_likes = session.query(Like).filter(Like.note_id == self.id).all()
        return [{"id": data.user_id, "name": data.user.name}
                for data in all_likes]

    def get_image(self):
        request = session.query(Image).filter(Image.id == self.image_id).all()
        return [f"static/images/{image.name}" for image in request]


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    note = relationship("Note", back_populates="image",
                        uselist=False, lazy="select")
