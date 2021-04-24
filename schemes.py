from validator import OneUppercase, OneLowercase, OneNumber, OneSpecial
from marshmallow import Schema, fields, validate


class UserLoginSchema(Schema):
    password = fields.String(required=True, validate=[
                             validate.Length(min=8), OneUppercase(),
                             OneLowercase(),
                             OneNumber(),
                             OneSpecial()])
    email = fields.String(
        required=True, validate=validate.Email(), )


class UserRegisterSchema(Schema):
    firstName = fields.String(required=True, validate=validate.Length(min=4))
    lastName = fields.String(required=True, validate=validate.Length(min=4))
    password = fields.String(required=True, validate=[
                             validate.Length(min=8), OneUppercase(),
                             OneLowercase(),
                             OneNumber(),
                             OneSpecial()])
    email = fields.String(
        required=True, validate=validate.Email(), )
    dob = fields.String(required=True)
    gender = fields.String(required=True, validate=validate.OneOf(
        ["Male", "Female", "Custom"]))
