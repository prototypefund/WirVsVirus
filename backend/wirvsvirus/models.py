
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, HttpUrl

from wirvsvirus import db



class ProfileTypeEnum(str, Enum):
    """Capabailty a helper can have."""
    hospital = 'hospital'
    helper = 'helper'


class RoleEnum(str, Enum):
    """Capabailty a helper can have."""
    admin = 'admin'
    logistic = 'logistic'
    medical = 'medical'


class CapabilityEnum(str, Enum):
    """Capabailty a helper can have."""
    hotline = 'hotline'
    testing = 'testing'
    care_normal = 'care_normal'
    care_intensive = 'care_intensive'
    care_intensive_medical = 'care_intensive_medical'
    care_intensive_medical_ventilation = 'care_intensive_medical_ventilation'
    medical_specialist = 'medical_specialist'


class ProfileBase(db.MongoModel):
    """Basic profile with authentication info.

    The user_id is taken from the access token provided by our oauth provider
    (auth0).
    """
    email: str
    profile_type: ProfileTypeEnum


class ProfileIntermediate(ProfileBase):
    """Profile with user id."""
    user_id: str  # provided by auth0


class Profile(ProfileIntermediate):
    id: str


class AddressBase(BaseModel):
    zip_code: str
    street: str
    latitude: float
    longitude: float


class HelperBase(db.MongoModel):
    """Define helper model."""
    name: str
    email: str
    address: str  # AddressModel
    phone_number: str
    capability: CapabilityEnum
    helping_category: RoleEnum
    profile_id: Optional[str] = None

class Helper(HelperBase):
    """Define helper model."""
    id: str


class HospitalBase(db.MongoModel):
    """Hospital model."""
    name: str
    address: str
    website: Optional[str]
    phone_number: Optional[str]
    profile_id: Optional[str] = None
    helper_demand_ids: List[str] = []

class Hospital(HospitalBase):
    id: str


class HelperDemandBase(db.MongoModel):
    """Demand for help."""
    hospital_id: str
    capability: CapabilityEnum
    value: int = 1

class HelperDemand(HelperDemandBase):
    """Demand for help."""
    id: str = None


class MatchBase(db.MongoModel):
    """Match model."""
    helper_id: str
    demand_id: str
    helper_confirmed: bool = False
    hospital_confirmed: bool = False

class Match(MatchBase):
    """Match model."""
    id: str
