from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    posts: Mapped[list['Post']] = relationship(back_populates='user')

    comments: Mapped[list['Comment']] = relationship(back_populates='author')

    following: Mapped[list['Follower']] = relationship(back_populates='follower_user')
    followers: Mapped[list['Follower']] = relationship(back_populates='followed_user')


class Follower(db.Model):
    __tablename__ = 'follower'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    follower_user: Mapped['User'] = relationship(back_populates='following')

    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    followed_user: Mapped['User'] = relationship(back_populates='followers')


class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    user: Mapped['User'] = relationship(back_populates='posts')

    media: Mapped[list['Media']] = relationship(back_populates='post')

    comments: Mapped[list['Comment']] = relationship(back_populates='post')


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    post: Mapped['Post'] = relationship(back_populates='media')


class Comment(db.Model):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)

    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    author: Mapped['User'] = relationship(back_populates='comments')

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    post: Mapped['Post'] = relationship(back_populates='comments')
