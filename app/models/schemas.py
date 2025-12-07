from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional
from datetime import datetime
from fastapi import Form
from inspect import signature, Parameter
from typing import Any, Type
from .enums import LeadState

def as_form(cls: Type[BaseModel]):
    """
    Add Form support to Pydantic V2 models
    """
    new_params = []
    for name, field in cls.model_fields.items():
        if field.default is None and field.default_factory is None:
            default = Form(...)  # 必填
        else:
            default = Form(field.default if field.default is not None else ...)
        new_params.append(
            Parameter(
                name=name,
                kind=Parameter.POSITIONAL_ONLY,
                default=default
            )
        )
    cls.__signature__ = signature(cls.__init__).replace(parameters=new_params)
    return cls


@as_form
class LeadForm(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=128)
    last_name: str = Field(..., min_length=1, max_length=128)
    email: EmailStr

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: EmailStr = Form(...)
    ):
        return cls(first_name=first_name, last_name=last_name, email=email)

class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class LeadOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    resume_path: Optional[str]
    state: LeadState
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StateUpdate(BaseModel):
    state: LeadState

class LeadUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=128)
    last_name: Optional[str] = Field(None, min_length=1, max_length=128)
    resume_path: Optional[str] = None
