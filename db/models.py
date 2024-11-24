from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(Text)
    profile_picture = Column(String(255))
    bio = Column(Text)
    website = Column(String(255))
    followers_count = Column(Integer)
    following_count =  Column(Integer)
    posts_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), default=func.utcnow(), on_update=func.utcnow())
    is_verified = Column(Boolean, default=False)
    is_private = Column(Boolean, default=False)
    account_status = Column(Enum("ACTIVE", "INACTIVE", "PENDING", name="status_enum"), default="active")
    last_login =  Column(DateTime(timezone=True))
    two_factor_enabled = Column(Boolean) 
    preferences = Column(JSON, default='[]') 
    device_tokens = Column(JSON, default='[]') 
    blocked_users = Column(JSON, default='[]')



class FollowersAndFollowing(Base):
    __tablename__ = "followers_and_following"

    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, index=True)
    following_id = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), default=func.utcnow())  # Default timestamp
    is_accepted = Column(Boolean, default=False)  # Default False for new follow requests
    is_blocked = Column(Boolean, default=False)  # Default False for blocking status
    last_interaction = Column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='unique_following'),
    )


class Posts(Base): 
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id =  Column(Integer, ForeignKey('users.id'), index=True) 
    caption = Column(Text)
    tags = Column(Text)
    location = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.utcnow())
    updated_at = Column(DateTime(timezone=True), default=func.utcnow(), on_update=func.utcnow())
    like_count = Column(Integer, default=0)  # Number of likes
    comment_count = Column(Integer, default=0)  # Number of comments


class PostMetaData(Base):
    __tablename__ = "post_metadata"
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'), index=True)
    media_type = Column(String(255))
    cdn_url = Column(Text)
    thumbnail_url = Column(Text)
    order = Column(Integer)


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.utcnow())
    user = relationship("User", backref="likes")
    post = relationship("Post", backref="likes")
    
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_like'),)  # Prevent duplicate likes


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), index=True, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.utcnow())
    user = relationship("User", backref="comments")
    post = relationship("Post", backref="comments")
