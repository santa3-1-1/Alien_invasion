# auth.py
# 用户认证与数据管理（JSON 存储 + sha256 密码哈希）
# 注意：生产环境请使用更安全的密钥管理和 PBKDF2/scrypt/bcrypt 等哈希

import os
import json
import hashlib
import time

USERS_FILE = os.path.join(os.path.dirname(__file__), "data", "users.json")
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

def _load_users():
    try:
        if not os.path.exists(USERS_FILE):
            return {}
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Warning: failed to load users.json:", e)
        return {}

def _save_users(users: dict):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Error saving users:", e)

def register(username: str, password: str) -> (bool, str):
    username = username.strip()
    if not username or not password:
        return False, "用户名或密码不能为空"
    users = _load_users()
    if username in users:
        return False, "用户名已存在"
    salt = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()[:16]
    users[username] = {
        "salt": salt,
        "password_hash": _hash_password(password, salt),
        "best_score": 0,
        "records": []
    }
    _save_users(users)
    return True, "注册成功"

def authenticate(username: str, password: str) -> (bool, str):
    users = _load_users()
    if username not in users:
        return False, "用户不存在"
    user = users[username]
    if user.get("password_hash") == _hash_password(password, user.get("salt","")):
        return True, "登录成功"
    return False, "用户名或密码错误"

def get_user(username: str):
    users = _load_users()
    return users.get(username)

def save_score(username: str, score: int):
    if not username:
        return
    users = _load_users()
    user = users.get(username)
    if not user:
        return
    try:
        user.setdefault("records", []).append({"score": score, "time": int(time.time())})
        if score > user.get("best_score", 0):
            user["best_score"] = score
        users[username] = user
        _save_users(users)
    except Exception as e:
        print("Error saving score:", e)

def get_leaderboard(limit=10):
    users = _load_users()
    entries = []
    for name, u in users.items():
        entries.append({"username": name, "best_score": u.get("best_score", 0)})
    entries.sort(key=lambda x: x["best_score"], reverse=True)
    return entries[:limit]
