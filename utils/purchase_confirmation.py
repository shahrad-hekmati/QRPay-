import secrets


def generate_purchase_confirmation_token(user_id: int) -> str:
    confirmation_token = secrets.token_urlsafe(16)
    purchase_confirmation_token = f"{user_id}_{confirmation_token}"
    return purchase_confirmation_token
