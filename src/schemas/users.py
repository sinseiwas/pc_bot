from pydantic import BaseModel, field_validator
import re


class UserIdSchema(BaseModel):
    id: int


class AddUserSchema(BaseModel):
    tg_id: int
    tg_username: str
    tg_fullname: str
    fullname: str
    phone_number: str  # = Field(pattern=r'^\+7\d{10}$')
    vk_link: str

    @field_validator('phone_number')
    def validate_phone(cls, value):
        if not re.match(r'^\+7\d{10}$', value) and len(value) != 12:
            raise ValueError(f"Неверный формат номера. Ожидается 12 чисел, введено {len(value)}.\nВведите номер в формате +7XXXXXXXXXX")
        return value

class UserFullSchema(AddUserSchema, UserIdSchema):
    pass