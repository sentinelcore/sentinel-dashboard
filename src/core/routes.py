from fastapi import APIRouter, HTTPException
from utils.token_utils import create_token
from utils.blockchain_auth import verify_solana_signature
import uuid

router = APIRouter()

@router.post("/api/token")
async def generate_token(agent_id: str):
    if not agent_id:
        raise HTTPException(status_code=400, detail="❌ Agent ID is required.")
    token = create_token(agent_id)
    return {"token": token, "message": "✅ Token generated successfully."}

@router.post("/api/solana_auth")
async def solana_auth(wallet_address: str, signature: str):
    challenge = "Sentinel Agent Authentication Challenge: " + str(uuid.uuid4())
    is_valid = verify_solana_signature(challenge, signature, wallet_address)
    if not is_valid:
        raise HTTPException(status_code=400, detail="❌ Invalid signature or wallet address.")
    token = create_token(wallet_address)
    return {"token": token, "message": "✅ Wallet authenticated successfully."}
