# 🃏 PyPoker (Python GUI 1:1 Poker Game)

> 파이썬과 Tkinter, SQLite를 활용하여 제작한 데스크톱 기반 1:1 포커(5-Card Draw) 게임 및 전적 관리 시스템입니다. 대학 기말 과제 제출용으로 개발되었습니다.

---

## 🛠️ Tech Stack & Environment
* **Language:** Python 3.11+
* **GUI Framework:** Tkinter (Python 표준 라이브러리)
* **Database:** SQLite3 (로컬 사용자 계정 및 승패/칩 데이터 영속성 관리)
* **Packaging Tool:** PyInstaller (독립 실행형 `.exe` 파일 빌드)

---

## ✨ Key Features (핵심 기능)
1. **사용자 인증 시스템**
   - 회원가입 및 로그인 기능 (비밀번호 검증 및 아이디 중복 방지)
   - SQLite 기반의 로컬 데이터베이스 연동으로 안전한 계정 관리
2. **전적 및 대시보드 관리**
   - 로그인한 유저의 **닉네임, 총 승리/패배 횟수, 승률, 보유 칩(포인트)** 실시간 조회
3. **포커 게임 플레이 (5-Card Draw)**
   - 52장 트럼프 카드 무작위 셔플 및 분배
   - 배팅 시스템 (콜, 레이즈, 다이) 및 카드 교체(Draw) 로직
   - 포커 족보 판별 알고리즘을 통한 공정한 승패 판정 및 DB 즉시 반영

---

## 📂 Project Structure (프로젝트 구조)
```text
PyPoker/
│
├── main.py            # 프로그램 진입점 및 화면 흐름 제어 (로그인/로비)
├── game.py            # 오목/포커 게임 로직 및 족보 판별 알고리즘
├── database.py        # SQLite DB 연결 및 쿼리 관리 (회원가입, 전적 업데이트)
├── poker_game.db      # 로컬 SQLite 데이터베이스 파일 (자동 생성)
└── README.md          # 프로젝트 설명서