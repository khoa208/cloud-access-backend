from pydantic import BaseModel
from typing import List, Optional, Dict

# Plan Schemas
class PlanCreate(BaseModel):
    name: str
    description: str
    api_permissions: List[str]
    limits: Dict[str, int]

class PlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    api_permissions: Optional[List[str]] = None
    limits: Optional[Dict[str, int]] = None

# Permission Schemas
class PermissionCreate(BaseModel):
    api_endpoint: str
    description: str

class PermissionUpdate(BaseModel):
    api_endpoint: Optional[str] = None
    description: Optional[str] = None

# Subscription Schemas
class SubscriptionCreate(BaseModel):
    user_id: int
    plan_id: int
