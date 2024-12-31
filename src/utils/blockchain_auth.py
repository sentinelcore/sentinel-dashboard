# utils/blockchain_auth.py

from solders.pubkey import Pubkey
from solders.signature import Signature


def verify_solana_signature(challenge: str, signature: str, wallet_address: str) -> bool:
    """
    Verify a signed message against a Solana wallet address.
    """
    try:
        signature = Signature.from_string(signature)
        wallet_pubkey = Pubkey.from_string(wallet_address)
        message = challenge.encode('utf-8')

        return signature.verify(wallet_pubkey, message)
    except Exception as e:
        print(f"❌ Solana Signature Verification Failed: {e}")
        return False
