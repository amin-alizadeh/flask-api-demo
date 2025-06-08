from typing import Union
from flask import request, jsonify, Response

from app import db, logger
from app.comments import bp
from app.models import Comments
from app.schemas import CommentsSchema, CommentsDeserializingSchema
from app.errors.handlers import bad_request
from app.helpers.api_secret_key import require_secret_key

from flask_jwt_extended import jwt_required, current_user

from marshmallow import ValidationError

import asyncio
from aiohttp import ClientSession

comment_schema = CommentsSchema()
comments_schema = CommentsSchema(many=True)
comment_deserializing_schema = CommentsDeserializingSchema()


@bp.post("/")
@require_secret_key
def submit_feedback() -> Union[tuple[Response, int], Response]:
    """
    Lets users retrieve a user profile when logged in

    Returns
    -------
    str
        A JSON object containing a success message
    """
    try:
        result = comment_schema.load(request.json)
    except ValidationError as e:
        return bad_request(e.messages[0])

    feedback = Comments(**result)

    db.session.add(feedback)
    db.session.commit()

    return jsonify({"msg": "Post succesfully submitted"}), 201


@bp.get("/<int:comment_id>")
@require_secret_key
def get_comments_by_post_id(comment_id: int) -> Response:
    """
    Endpoint for retrieving the user comments associated with a particular post

    Parameters
    ----------
    id : int
        ID of the post which comment's need to be retrieved

    Returns
    -------
    str
        A JSON object containing the comments
    """
    comments = Comments.query.filter_by(id=comment_id).all()
    return comments_schema.jsonify(comments)


@bp.get("/")
@require_secret_key
def get_comments() -> Response:
    """
    Endpoint for retrieving the user comments associated with a particular post

    Parameters
    ----------
    id : int
        ID of the post which comment's need to be retrieved

    Returns
    -------
    str
        A JSON object containing the comments
    """
    comments = Comments.query.filter_by(active=True).all()
    return comments_schema.jsonify(comments)

@bp.delete("/<int:comment_id>")
@require_secret_key
def delete_comment(comment_id: int) -> Union[tuple[Response, int], Response]:
    """
    Lets users delete one of their own comments

    Parameters
    ----------
    id : int
        ID of the post which comment's need to be retrieved

    Returns
    -------
    str
        A JSON object containing a success message
    """
    comment = Comments.query.get(comment_id)

    if not comment:
        return bad_request("Comment not found")


    comment.delete()
    db.session.commit()

    return jsonify({"msg": "Comment succesfully deleted"}), 201


@bp.delete("/")
@require_secret_key
def delete_comments() -> Union[tuple[Response, int], Response]:
    """
    Lets users delete one of their own comments

    Parameters
    ----------
    id : int
        ID of the post which comment's need to be retrieved

    Returns
    -------
    str
        A JSON object containing a success message
    """
    comments = Comments.query.filter_by(active=True).all()
    for comment in comments:
        if not comment.active:
            continue
        comment.delete()
        logger.info(f"Deleting comment {comment.id}")
    db.session.commit()

    return jsonify({"msg": "Comment succesfully deleted"}), 201

