from pydantic import validator


class PasswordValidatorMixin:
    @validator("password")
    def validate_password_length(cls, value, **kwargs):
        if len(value) < 6:
            raise ValueError("Password is too short.")
        return value

    @validator("repeat_password")
    def validate_passwords_match(cls, value, values, **kwargs):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match.")
        return value