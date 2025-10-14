#!/usr/bin/env python3
from typing import Optional, Tuple
import sys
import requests

def resolve_username(username: str) -> Optional[int]:
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username], "excludeBannedUsers": False}
    response = requests.post(url, json=payload, timeout=8)
    response.raise_for_status()
    data = response.json()
    items = data.get("data", [])
    return items[0].get("id") if items else None

def check_presence(user_id: int) -> Optional[Tuple[int, Optional[int]]]:
    url = "https://presence.roblox.com/v1/presence/users"
    payload = {"userIds": [user_id]}
    response = requests.post(url, json=payload, timeout=8)
    response.raise_for_status()
    data = response.json()
    presences = data.get("userPresences", [])
    if not presences:
        return None
    p = presences[0]
    return p.get("userPresenceType"), p.get("placeId")

def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python3 simple_bot.py <username>")
        return
    username = sys.argv[1]
    try:
        uid = resolve_username(username)
        if uid is None:
            print(f"Usuario '{username}' no encontrado.")
            return
        result = check_presence(uid)
        if result is None:
            print("No se obtuvo información de presencia (respuesta vacía).")
            return
        status, place = result
        if status == 0:
            print(f"{username} (id={uid}) está OFFLINE.")
        else:
            place_str = place if place is not None else "placeId desconocido"
            print(f"{username} (id={uid}) está ONLINE en {place_str} (userPresenceType={status}).")
    except requests.HTTPError as e:
        print("HTTP error:", e)
    except requests.RequestException as e:
        print("Error de conexión / timeout:", e)
    except Exception as e:
        print("Error inesperado:", e)

if __name__ == "__main__":
    main()

