import csv
import os

CSV_FILE = "poker_users.csv"
FIELDNAMES = [
    "id",
    "username",
    "password",
    "nickname",
    "wins",
    "losses",
    "chips",
]


def init_db():
  """CSV 파일이 없으면 기본 헤더와 샘플 계정을 생성합니다."""
  if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8-sig") as f:
      writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
      writer.writeheader()
      # 초기 테스트 계정 생성
      writer.writerow({
          "id": 1,
          "username": "admin",
          "password": "1234",
          "nickname": "포커고수",
          "wins": 0,
          "losses": 0,
          "chips": 10000,
      })


def load_users():
  init_db()
  with open(CSV_FILE, mode="r", newline="", encoding="utf-8-sig") as f:
    return list(csv.DictReader(f))


def save_users(users):
  with open(CSV_FILE, mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(users)


def register_user(username, password, nickname):
  users = load_users()
  if any(u["username"] == username for u in users):
    return False, "이미 존재하는 아이디입니다."

  new_id = max([int(u["id"]) for u in users], default=0) + 1
  users.append({
      "id": new_id,
      "username": username,
      "password": password,
      "nickname": nickname,
      "wins": 0,
      "losses": 0,
      "chips": 10000,
  })
  save_users(users)
  return True, "회원가입이 완료되었습니다!"


def login_user(username, password):
  users = load_users()
  for u in users:
    if u["username"] == username and u["password"] == password:
      return u
  return None


def update_record(username, is_win, chip_change):
  users = load_users()
  for u in users:
    if u["username"] == username:
      if is_win:
        u["wins"] = int(u["wins"]) + 1
      else:
        u["losses"] = int(u["losses"]) + 1
      u["chips"] = max(0, int(u["chips"]) + chip_change)
      break
  save_users(users)