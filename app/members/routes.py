from typing import Any, Union
from flask import request, jsonify, Response


from app import db, logger
from app.members import bp
from app.models import Members
from app.schemas import MembersSchema, MemberDeserializingSchema
from app.errors.handlers import bad_request
from app.helpers.api_secret_key import require_secret_key

from marshmallow import ValidationError

from aiohttp import ClientSession

member_schema = MembersSchema()
members_schema = MembersSchema(many=True)
member_deserializing_schema = MemberDeserializingSchema()


@bp.post("/")
@require_secret_key
def add_member() -> Union[tuple[Response, int], Response]:
    """
    Lets users retrieve a user profile when logged in

    Returns
    -------
    str
        A JSON object containing a success message
    """
    try:
        result = member_schema.load(request.json)
    except ValidationError as e:
        return bad_request(e.messages[0])

    if Members.query.filter_by(login=result["login"]).first():
        return bad_request("Login name already in use")

    if Members.query.filter_by(email=result["email"]).first():
        return bad_request("Email already in use")

    member: Members = Members(**result)

    db.session.add(member)
    db.session.commit()

    return jsonify({"msg": "Member succesfully added"}), 201

@bp.get("/")
@require_secret_key
def get_members() -> Response:
    """
    Endpoint for retrieving the members


    Returns
    -------
    str
        A JSON object containing the members
    """
    members = Members.query.filter_by(active=True).order_by(Members.followers.desc()).all()
    return members_schema.jsonify(members)


@bp.get("/<string:login>")
@require_secret_key
def get_member_by_login(login: str) -> Union[tuple[Response, int], Response]:
    """
    Lets users retrieve a user profile when logged in

    Parameters
    ----------
    login : str
        The login of the user who's information should be retrieved

    Returns
    -------
    str
        A JSON object containing the user profile information
    """
    logger.info(f"Retrieving user profile for {login}")
    user = Members.query.filter_by(login=login).first()

    if user is None:
        return bad_request("User not found")

    return member_schema.jsonify(user), 200


@bp.delete("/<int:member_id>")
@require_secret_key
def delete_member_by_id(member_id: int) -> Union[tuple[Response, int], Response]:
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
    member = Members.query.filter_by(id=member_id).first()

    if not member:
        return bad_request("Member not found")

    member.delete()
    db.session.commit()

    return jsonify({"msg": "Member succesfully deleted"}), 201


@bp.delete("/<string:login>")
@require_secret_key
def delete_member_by_login(login: int) -> Union[tuple[Response, int], Response]:
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
    member = Members.query.filter_by(login=login).first()

    if not member:
        return bad_request("Member not found")

    member.delete()
    db.session.commit()

    return jsonify({"msg": "Member succesfully deleted"}), 201


@bp.delete("/")
@require_secret_key
def delete_members() -> Union[tuple[Response, int], Response]:
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
    members = Members.query.all()
    for member in members:
        if not member.active:
            continue
        member.delete()
        logger.info(f"Deleting member {member.login} with ID {member.id}")
    
    db.session.commit()

    return jsonify({"msg": "All members succesfully deleted"}), 201