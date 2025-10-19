from pydantic import BaseModel, Field
from typing import Optional


class UserAttributes(BaseModel):
    """User attributes shared across user management and vectorization."""
    uuid: str
    name: str
    specialty: str = Field(default="", description="Primary skills or specialties (comma-separated)")
    fields: str = Field(default="", description="Fields of work or study (comma-separated)")
    interests_and_hobbies: str = Field(default="", description="Interests and hobbies (comma-separated)")

    vibe: str = Field(default="", description="User vibe or personality type")
    comfort: str = Field(default="", description="Comfort level and preferences")
    availability: str = Field(default="", description="User availability (e.g., weekdays, weekends, flexible)")
    handle: str = Field(default="", description="User handle or username")
