from pydantic import BaseModel

class BrandCreate(BaseModel):
    name: str
    briefing: str


class CreativeRequest(BaseModel):
    brand_id: str
    asset_type: str
    instructions: str


class AuditTextRequest(BaseModel):
    asset_id: str


class ApprovalRequest(BaseModel):
    asset_id: str
    approve: bool