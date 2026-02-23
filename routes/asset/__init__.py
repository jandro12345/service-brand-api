from fastapi import Request, APIRouter, Query, Depends
from models.schemas import CreativeRequest
from services.groq_service import generate_creative_asset
from services.supabase_service import (
    get_latest_manual,
    save_asset,
    get_assets_paginated,
    require_roles,
    get_current_user
)

asset_route = APIRouter(prefix="/asset")

@asset_route.post("/creative")
def create_asset(data: CreativeRequest, user=Depends(require_roles(["admin", "user"]))):

    data_manual = get_latest_manual(data.brand_id)
    brand_name = data_manual["brand_name"]
    manual = data_manual["manual"]
    content = generate_creative_asset(
        manual,
        data.instructions,
        data.asset_type,
        brand_name
    )

    asset = save_asset(data.brand_id, data.asset_type, content)
    return asset


@asset_route.get("/")
def list_assets(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    brand_id: str | None = None,
    asset_type: str | None = None,
    user=Depends(get_current_user)
):
    return get_assets_paginated(page, page_size, brand_id, asset_type)
