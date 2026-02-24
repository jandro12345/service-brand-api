from fastapi import Request, APIRouter, Query, Depends
from services.groq_service import generate_brand_manual
from models.schemas import BrandCreate
from services.supabase_service import (
    create_brand,
    save_manual,
    get_manuals_paginated,
    require_roles,
    get_current_user
)
from tool import logger

brand_route = APIRouter(prefix="/brand")


@brand_route.post("/brands")
def create_brand_and_manual(data: BrandCreate, user=Depends(require_roles(["admin", "user"]))):

    brand = create_brand(data.name)
    manual = generate_brand_manual(data.briefing)
    save_manual(brand["id"], data.briefing, manual)

    return {"brand_id": brand["id"], "manual": manual}


@brand_route.get("/")
def list_manuals(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    user=Depends(get_current_user)
):
    # logger.info(f"Listing manuals - Page: {page}, Page Size: {page_size}")
    return get_manuals_paginated(page, page_size)
