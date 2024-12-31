import jwt
from datetime import datetime, timedelta
from typing import Optional

# Configuration
SECRET_KEY = "your_super_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_token(agent_id: str) -> str:
    """
    Generate a JWT token for the agent.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": agent_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)



def verify_token(token: str) -> Optional[str]:
    """
    Verify and decode a JWT token.
    
    Args:
        token (str): The JWT token to verify.
    
    Returns:
        Optional[str]: The agent_id if the token is valid, None otherwise.
    
    Raises:
        ValueError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Returns the agent_id
    except jwt.ExpiredSignatureError:
        raise ValueError("❌ Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("❌ Invalid token")


# Example Usage (for debugging)
if __name__ == "__main__":
    agent_id = "agent-001"
    token = create_token(agent_id)
    print(f"🔑 Generated Token: {token}")

    try:
        decoded_agent_id = verify_token(token)
        print(f"✅ Token is valid. Agent ID: {decoded_agent_id}")
    except ValueError as e:
        print(f"❌ Token verification failed: {e}")
