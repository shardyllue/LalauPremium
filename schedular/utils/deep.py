BASE_URL = "https://t.me/"


def link(user_id : int, username : str) -> str:
    
    path = f"{BASE_URL}{username}?start={user_id}"

    return path


