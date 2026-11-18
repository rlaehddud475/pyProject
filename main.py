import random
import tkinter as tk
from tkinter import messagebox
import database


class PyPokerApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Python 기말과제 - 1:1 포커 게임")
    self.root.geometry("600x500")
    self.root.resizable(False, False)

    self.current_user = None
    self.create_login_screen()

  def clear_window(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  # ==================== [1] 로그인 화면 ====================
  def create_login_screen(self):
    self.clear_window()

    tk.Label(
        self.root, text="🃏 PyPoker 게임", font=("Arial", 20, "bold")
    ).pack(pady=40)

    frame = tk.Frame(self.root)
    frame.pack(pady=10)

    tk.Label(frame, text="아이디", font=("Arial", 12), width=10).grid(
        row=0, column=0, pady=5
    )
    self.user_entry = tk.Entry(frame, font=("Arial", 12))
    self.user_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="비밀번호", font=("Arial", 12), width=10).grid(
        row=1, column=0, pady=5
    )
    self.pass_entry = tk.Entry(frame, font=("Arial", 12), show="*")
    self.pass_entry.grid(row=1, column=1, pady=5)

    tk.Button(
        self.root,
        text="로그인",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        command=self.login_action,
    ).pack(pady=15)
    tk.Button(
        self.root,
        text="회원가입 화면으로",
        font=("Arial", 10),
        width=20,
        command=self.create_register_screen,
    ).pack()

  def login_action(self):
    u = self.user_entry.get().strip()
    p = self.pass_entry.get().strip()
    if not u or not p:
      messagebox.showwarning("경고", "아이디와 비밀번호를 모두 입력해주세요.")
      return

    user = database.login_user(u, p)
    if user:
      self.current_user = user
      messagebox.showinfo("성공", f"{user['nickname']}님 환영합니다!")
      self.create_main_lobby()
    else:
      messagebox.showerror(
          "오류", "아이디 또는 비밀번호가 일치하지 않습니다."
      )

  # ==================== [2] 회원가입 화면 ====================
  def create_register_screen(self):
    self.clear_window()

    tk.Label(
        self.root, text="📝 회원가입", font=("Arial", 20, "bold")
    ).pack(pady=40)

    frame = tk.Frame(self.root)
    frame.pack(pady=10)

    tk.Label(frame, text="아이디", font=("Arial", 12), width=10).grid(
        row=0, column=0, pady=5
    )
    reg_u = tk.Entry(frame, font=("Arial", 12))
    reg_u.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="비밀번호", font=("Arial", 12), width=10).grid(
        row=1, column=0, pady=5
    )
    reg_p = tk.Entry(frame, font=("Arial", 12), show="*")
    reg_p.grid(row=1, column=1, pady=5)

    tk.Label(frame, text="닉네임", font=("Arial", 12), width=10).grid(
        row=2, column=0, pady=5
    )
    reg_n = tk.Entry(frame, font=("Arial", 12))
    reg_n.grid(row=2, column=1, pady=5)

    def register_submit():
      u, p, n = reg_u.get().strip(), reg_p.get().strip(), reg_n.get().strip()
      if not u or not p or not n:
        messagebox.showwarning("경고", "모든 항목을 입력해주세요.")
        return
      success, msg = database.register_user(u, p, n)
      if success:
        messagebox.showinfo("성공", msg)
        self.create_login_screen()
      else:
        messagebox.showerror("오류", msg)

    tk.Button(
        self.root,
        text="가입 완료",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=20,
        height=2,
        command=register_submit,
    ).pack(pady=15)
    tk.Button(
        self.root,
        text="돌아가기",
        font=("Arial", 10),
        width=20,
        command=self.create_login_screen,
    ).pack()

  # ==================== [3] 메인 로비 (전적 확인) ====================
  def create_main_lobby(self):
    self.clear_window()

    # 최신 정보 동기화
    users = database.load_users()
    for u in users:
      if u["username"] == self.current_user["username"]:
        self.current_user = u
        break

    nickname = self.current_user["nickname"]
    wins = int(self.current_user["wins"])
    losses = int(self.current_user["losses"])
    chips = int(self.current_user["chips"])
    total = wins + losses
    win_rate = (wins / total * 100) if total > 0 else 0

    tk.Label(
        self.root, text=f"👤 {nickname} 님의 대시보드", font=("Arial", 18, "bold")
    ).pack(pady=30)

    info_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief="groove")
    info_frame.pack(pady=10, ipadx=20, ipady=15)

    tk.Label(
        info_frame,
        text=f"보유 칩: 🪙 {chips:,} 칩",
        font=("Arial", 14),
        bg="#f0f0f0",
    ).pack(anchor="w", pady=5)
    tk.Label(
        info_frame,
        text=(
            f"전적: {wins}승 {losses}패 (승률: {win_rate:.1f}%, 총 게임수:"
            f" {total})"
        ),
        font=("Arial", 12),
        bg="#f0f0f0",
    ).pack(anchor="w", pady=5)

    tk.Button(
        self.root,
        text="🎮 포커 게임 시작",
        font=("Arial", 14, "bold"),
        bg="#FF9800",
        fg="white",
        width=22,
        height=2,
        command=self.start_poker_game,
    ).pack(pady=20)
    tk.Button(
        self.root,
        text="로그아웃",
        font=("Arial", 10),
        width=15,
        command=self.create_login_screen,
    ).pack()

  # ==================== [4] 포커 게임 화면 및 로직 ====================
  def start_poker_game(self):
    if int(self.current_user["chips"]) < 1000:
      messagebox.showwarning(
          "파산", "칩이 부족합니다! (기본 10,000칩 충전해드립니다)"
      )
      database.update_record(
          self.current_user["username"], False, 10000
      )  # 충전
      self.create_main_lobby()
      return

    self.clear_window()
    self.root.geometry("700x550")

    # 게임 상태 변수
    self.deck = [
        f"{suit}{val}"
        for suit in ["♠", "♥", "◆", "♣"]
        for val in [
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "J",
            "Q",
            "K",
            "A",
        ]
    ]
    random.shuffle(self.deck)

    self.player_hand = [self.deck.pop() for _ in range(5)]
    self.ai_hand = [self.deck.pop() for _ in range(5)]
    self.pot = 2000  # (유저 1000, AI 1000)

    # 상단 정보 표시
    self.top_frame = tk.Frame(self.root)
    self.top_frame.pack(pady=15)

    self.status_label = tk.Label(
        self.top_frame,
        text="[라운드 1] 카드가 배분되었습니다. 패를 확인하세요!",
        font=("Arial", 12, "bold"),
        fg="#333",
    )
    self.status_label.pack()

    # AI 영역
    ai_frame = tk.LabelFrame(
        self.root, text=" 컴퓨터 (AI) ", font=("Arial", 11), padx=10, pady=10
    )
    ai_frame.pack(pady=10, fill="x", padx=20)
    self.ai_card_labels = []
    for _ in range(5):
      lbl = tk.Label(
          ai_frame,
          text="🂠",
          font=("Arial", 28),
          width=3,
          bg="white",
          relief="solid",
      )
      lbl.pack(side="left", padx=5)
      self.ai_card_labels.append(lbl)

    # 판돈 정보
    self.pot_label = tk.Label(
        self.root,
        text=f"현재 팟(Pot): {self.pot:,} 칩",
        font=("Arial", 13, "bold"),
        fg="#D32F2F",
    )
    self.pot_label.pack(pady=5)

    # 유저 영역
    player_frame = tk.LabelFrame(
        self.root,
        text=f" {self.current_user['nickname']} (나) ",
        font=("Arial", 11),
        padx=10,
        pady=10,
    )
    player_frame.pack(pady=10, fill="x", padx=20)
    self.player_card_labels = []
    for i in range(5):
      lbl = tk.Label(
          player_frame,
          text=self.player_hand[i],
          font=("Arial", 22, "bold"),
          width=4,
          height=2,
          bg="white",
          relief="solid",
      )
      lbl.pack(side="left", padx=5)
      self.player_card_labels.append(lbl)

    # 조작 버튼 영역
    self.btn_frame = tk.Frame(self.root)
    self.btn_frame.pack(pady=15)

    self.call_btn = tk.Button(
        self.btn_frame,
        text="콜 (승부 보기)",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=15,
        height=2,
        command=self.end_game_showdown,
    )
    self.call_btn.pack(side="left", padx=10)

    self.quit_btn = tk.Button(
        self.btn_frame,
        text="포기 (다이)",
        font=("Arial", 12, "bold"),
        bg="#F44336",
        fg="white",
        width=15,
        height=2,
        command=self.player_fold,
    )
    self.quit_btn.pack(side="left", padx=10)

  def player_fold(self):
    messagebox.showinfo("패배", "다이(Fold)를 선언하여 게임을 포기했습니다.")
    database.update_record(self.current_user["username"], False, -1000)
    self.root.geometry("600x500")
    self.create_main_lobby()

  # 간단한 족보 점수 계산 알고리즘 (숫자 기준 단순 합산 및 페어 가중치)
  def evaluate_hand(self, hand):
    values = []
    val_map = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    for card in hand:
      v_str = card[1:]
      values.append(val_map[v_str])

    values.sort(reverse=True)
    counts = {v: values.count(v) for v in values}
    sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    # 족보 판정 점수 반환 (Tier, 주요숫자...)
    max_count = sorted_counts[0][1]
    if max_count == 4:
      return (8, sorted_counts[0][0])  # 포카드
    elif max_count == 3:
      if len(sorted_counts) == 2:
        return (7, sorted_counts[0][0])  # 풀하우스
      return (4, sorted_counts[0][0])  # 트리플
    elif max_count == 2:
      if len(sorted_counts) == 3:
        return (3, sorted_counts[0][0])  # 투페어
      return (2, sorted_counts[0][0])  # 원페어
    return (1, values[0])  # 하이카드

  def end_game_showdown(self):
    # AI 카드 공개
    for i, lbl in enumerate(self.ai_card_labels):
      lbl.config(text=self.ai_hand[i])

    p_score = self.evaluate_hand(self.player_hand)
    ai_score = self.evaluate_hand(self.ai_hand)

    if p_score > ai_score:
      result_text = "🎉 플레이어 승리!"
      is_win = True
      chip_change = 1000
    elif p_score < ai_score:
      result_text = "😢 컴퓨터 승리 (패배)"
      is_win = False
      chip_change = -1000
    else:
      result_text = "🤝 무승부!"
      is_win = None
      chip_change = 0

    self.status_label.config(text=result_text, fg="blue" if is_win else "red")
    self.call_btn.pack_forget()
    self.quit_btn.pack_forget()

    # DB 업데이트 반영
    if is_win is not None:
      database.update_record(self.current_user["username"], is_win, chip_change)

    tk.Button(
        self.btn_frame,
        text="로비로 돌아가기",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=20,
        height=2,
        command=lambda: [
            setattr(self.root, "geometry", self.root.geometry("600x500")),
            self.create_main_lobby(),
        ],
    ).pack()


if __name__ == "__main__":
  database.init_db()
  root = tk.Tk()
  app = PyPokerApp(root)
  root.mainloop()