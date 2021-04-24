from marshmallow import validate
import typing
import re
from marshmallow.exceptions import ValidationError


class OneUppercase(validate.Validator):

    default_message = "Required one uppercase."

    def __init__(self, *, error: typing.Optional[str] = None):
        self.error = error or self.default_message  # type: str

    def __call__(self, value) -> typing.Optional[str]:
        if not any(x.isupper() for x in value):
            raise ValidationError(self.error)
        return value


class OneLowercase(validate.Validator):

    default_message = "Required one lowercase."

    def __init__(self, *, error: typing.Optional[str] = None):
        self.error = error or self.default_message  # type: str

    def __call__(self, value) -> typing.Optional[str]:
        if not any(x.islower() for x in value):
            raise ValidationError(self.error)
        return value


class Alpha(validate.Validator):

    default_message = "Required alphabets only."

    def __init__(self, *, error: typing.Optional[str] = None):
        self.error = error or self.default_message  # type: str

    def __call__(self, value) -> typing.Optional[str]:
        if not value.isalpha():
            raise ValidationError(self.error)
        return value


class OneNumber(validate.Validator):

    default_message = "Required one number."

    def __init__(self, *, error: typing.Optional[str] = None):
        self.error = error or self.default_message  # type: str

    def __call__(self, value) -> typing.Optional[str]:
        if not any(x.isdigit() for x in value):
            raise ValidationError(self.error)
        return value


class OneSpecial(validate.Validator):

    default_message = "Required one special character from !@#$%^&*()."

    def __init__(self, *, error: typing.Optional[str] = None):
        self.error = error or self.default_message  # type: str
        self.regex = re.compile('[!@#$%^&*()]')

    def __call__(self, value) -> typing.Optional[str]:
        if (self.regex.search(value) == None):
            raise ValidationError(self.error)
        return value
