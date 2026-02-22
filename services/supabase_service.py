from supabase import create_client
import os
from dotenv import load_dotenv
import math

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def create_brand(name):
    res = supabase.table("brands").insert({"name": name}).execute()
    return res.data[0]


def save_manual(brand_id, briefing, manual):
    supabase.table("brand_manuals").insert({
        "brand_id": brand_id,
        "raw_briefing": briefing,
        "manual_json": manual
    }).execute()


def get_manuals_paginated(page: int = 1, page_size: int = 10):

    if page < 1:
        page = 1

    if page_size < 1:
        page_size = 10

    offset = (page - 1) * page_size
    limit = offset + page_size - 1

    res = (
        supabase
        .table("brand_manuals")
        .select("id, raw_briefing, manual_json, created_at, brands(name), brand_id", count="exact")
        .order("created_at", desc=True)
        .range(offset, limit)
        .execute()
    )

    total = res.count or 0
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    data = []

    for record in res.data:
        data.append({
            "manual_id": record["id"],
            "brand_name": record["brands"]["name"],
            "raw_briefing": record["raw_briefing"],
            "manual": record["manual_json"],
            "created_at": record["created_at"],
            "brand_id": record["brand_id"]
        })

    return {
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "items": data
    }


def get_latest_manual(brand_id: str):

    res = (
        supabase
        .table("brand_manuals")
        .select("id, manual_json, created_at, brands(name)")
        .eq("brand_id", brand_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not res.data:
        return None

    record = res.data[0]

    return {
        "brand_name": record["brands"]["name"],
        "manual": record["manual_json"],
    }


def save_asset(brand_id, asset_type, content):
    res = supabase.table("assets").insert({
        "brand_id": brand_id,
        "type": asset_type,
        "content": content
    }).execute()
    return res.data[0]


def get_assets_paginated(
    page: int = 1,
    page_size: int = 10,
    brand_id: str | None = None,
    asset_type: str | None = None
):

    offset = (page - 1) * page_size
    limit = offset + page_size - 1

    query = (
        supabase
        .table("assets")
        .select("id, type, content, created_at, brands(name)", count="exact")
        .order("created_at", desc=True)
    )

    if brand_id:
        query = query.eq("brand_id", brand_id)

    if asset_type:
        query = query.ilike("type", f"%{asset_type}%")  # ← CAMBIO AQUÍ

    res = query.range(offset, limit).execute()

    total = res.count or 0
    total_pages = math.ceil(total / page_size) if total > 0 else 1

    items = [
        {
            "asset_id": r["id"],
            "brand_name": r["brands"]["name"],
            "type": r["type"],
            "content": r["content"],
            "created_at": r["created_at"]
        }
        for r in res.data
    ]

    return {
        "page": page,
        "page_size": page_size,
        "total_items": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "items": items
    }


def get_asset(asset_id):
    res = supabase.table("assets").select("*").eq("id", asset_id).execute()
    return res.data[0]


def update_asset_status(asset_id, status):
    supabase.table("assets")\
        .update({"status": status})\
        .eq("id", asset_id)\
        .execute()