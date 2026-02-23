from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

# from models.schemas import BrandCreate, CreativeRequest, AuditTextRequest, ApprovalRequest
# from services.groq_service import generate_brand_manual, generate_creative_asset, audit_text
# from services.vision_service import audit_image
from routes.audit import audit_image_route
from routes.brand import brand_route
from routes.asset import asset_route
from routes.login import login_route
# from services.supabase_service import (
#     create_brand,
#     save_manual,
#     get_latest_manual,
#     save_asset,
#     get_asset,
#     update_asset_status
# )

app = FastAPI(title="Brand Governance AI")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],allow_headers=["*"],allow_credentials=True)

app.include_router(audit_image_route, prefix="/api/v1.0")
app.include_router(brand_route, prefix="/api/v1.0")
app.include_router(asset_route, prefix="/api/v1.0")
app.include_router(login_route, prefix="/api/v1.0")
