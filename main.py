import itertools
import random
import tkinter as tk
from tkinter import messagebox
import database


class RealCardGamePlatform:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "Python 기말과제 - 카드 게임 & 슬롯머신 통합 플랫폼"
    )
    self.root.geometry("900x720")
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
        self.root, text="🎰 아케이드 게임 통합 플랫폼", font=("Arial", 20, "bold")
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
      self.create_game_select_lobby()
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

  # ==================== [3] 게임 선택 로비 및 랭킹 보드 ====================
  def create_game_select_lobby(self):
    self.clear_window()

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
        self.root,
        text=f"👤 {nickname} 님, 플레이할 게임을 선택하세요!",
        font=("Arial", 18, "bold"),
    ).pack(pady=20)

    info_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2, relief="groove")
    info_frame.pack(pady=5, ipadx=20, ipady=10)

    tk.Label(
        info_frame,
        text=f"보유 칩: 🪙 {chips:,} 칩",
        font=("Arial", 13),
        bg="#f0f0f0",
    ).pack(anchor="w", pady=2)
    tk.Label(
        info_frame,
        text=f"전적: {wins}승 {losses}패 (승률: {win_rate:.1f}%)",
        font=("Arial", 11),
        bg="#f0f0f0",
    ).pack(anchor="w", pady=2)

    game_btn_frame = tk.Frame(self.root)
    game_btn_frame.pack(pady=15)

    tk.Button(
        game_btn_frame,
        text="🃏 세븐 포커\n(7장 받아 최고 5장 승부)",
        font=("Arial", 11, "bold"),
        bg="#3F51B5",
        fg="white",
        width=22,
        height=4,
        command=self.start_seven_poker,
    ).pack(side="left", padx=10)

    tk.Button(
        game_btn_frame,
        text="🎲 텍사스 홀덤\n(공용카드 5장 승부)",
        font=("Arial", 11, "bold"),
        bg="#FF9800",
        fg="white",
        width=22,
        height=4,
        command=self.start_holdem_game,
    ).pack(side="left", padx=10)

    tk.Button(
        game_btn_frame,
        text="🎰 슬롯 머신\n(잭팟을 노려보세요!)",
        font=("Arial", 11, "bold"),
        bg="#E91E63",
        fg="white",
        width=22,
        height=4,
        command=self.start_slot_machine,
    ).pack(side="left", padx=10)

    sub_btn_frame = tk.Frame(self.root)
    sub_btn_frame.pack(pady=10)

    tk.Button(
        sub_btn_frame,
        text="🏆 랭킹 보드 보기",
        font=("Arial", 11, "bold"),
        bg="#9C27B0",
        fg="white",
        width=18,
        height=2,
        command=self.create_ranking_screen,
    ).pack(side="left", padx=10)

    tk.Button(
        sub_btn_frame,
        text="로그아웃",
        font=("Arial", 11),
        width=15,
        height=2,
        command=self.create_login_screen,
    ).pack(side="left", padx=10)

  def create_ranking_screen(self):
    self.clear_window()
    self.root.geometry("800x600")

    tk.Label(
        self.root, text="🏆 유저 칩 보유 랭킹 보드", font=("Arial", 20, "bold")
    ).pack(pady=20)

    # 랭킹 리스트 출력 영역 (Frame + Text / Listbox)
    rank_frame = tk.Frame(self.root)
    rank_frame.pack(pady=10, fill="both", expand=True, padx=50)

    scrollbar = tk.Scrollbar(rank_frame)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(
        rank_frame,
        font=("Arial", 13),
        yscrollcommand=scrollbar.set,
        width=60,
        height=15,
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    # 유저 데이터 로드 및 칩 기준 내림차순 정렬
    users = database.load_users()
    users.sort(key=lambda x: int(x["chips"]), reverse=True)

    for idx, u in enumerate(users, start=1):
      w = int(u["wins"])
      l = int(u["losses"])
      tot = w + l
      rate = (w / tot * 100) if tot > 0 else 0
      medal = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else f"{idx}위"))
      listbox.insert(
          tk.END,
          f" {medal} | 닉네임: {u['nickname']} ({u['username']})  |  보유 칩: 🪙"
          f" {int(u['chips']):,} 칩  |  전적: {w}승 {l}패 ({rate:.1f}%)",
      )

    tk.Button(
        self.root,
        text="🏠 게임 선택 로비로",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=20,
        height=2,
        command=self.create_game_select_lobby,
    ).pack(pady=20)

  def sync_user_data(self):
    users = database.load_users()
    for u in users:
      if u["username"] == self.current_user["username"]:
        self.current_user = u
        break

  # ==================== [4] 세븐 포커 모드 ====================
  def start_seven_poker(self):
    self.sync_user_data()
    if int(self.current_user["chips"]) < 1000:
      messagebox.showwarning(
          "파산", "칩이 부족합니다! (기본 10,000칩 충전)"
      )
      database.update_record(self.current_user["username"], False, 10000)
      self.sync_user_data()

    self.clear_window()
    self.root.geometry("900x720")

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

    self.sp_player_cards = [self.deck.pop() for _ in range(7)]
    self.sp_ai_cards = [self.deck.pop() for _ in range(7)]

    self.pot = 2000
    self.sp_step = 1

    top_info_frame = tk.Frame(self.root)
    top_info_frame.pack(pady=5)

    self.my_chips_lbl = tk.Label(
        top_info_frame,
        text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩",
        font=("Arial", 13, "bold"),
        fg="#2E7D32",
    )
    self.my_chips_lbl.pack(side="left", padx=15)

    self.sp_pot_lbl = tk.Label(
        top_info_frame,
        text=f"현재 팟(Pot): {self.pot:,} 칩",
        font=("Arial", 13, "bold"),
        fg="#D32F2F",
    )
    self.sp_pot_lbl.pack(side="left", padx=15)

    self.sp_status_lbl = tk.Label(
        self.root,
        text=(
            "[세븐 포커 1단계] 처음 3장을 받았습니다. 서로의 3번째 오픈 패를"
            " 확인하고 베팅하세요!"
        ),
        font=("Arial", 11, "bold"),
        fg="#3F51B5",
    )
    self.sp_status_lbl.pack(pady=5)

    ai_frame = tk.LabelFrame(
        self.root,
        text=" 컴퓨터 (AI) - 3번째 패 및 오픈 카드 ",
        font=("Arial", 11),
        padx=10,
        pady=5,
    )
    ai_frame.pack(pady=5, fill="x", padx=20)
    self.sp_ai_frame = ai_frame
    self.sp_ai_lbls = []

    for i in range(7):
      lbl = tk.Label(
          ai_frame,
          text="",
          font=("Arial", 16, "bold"),
          width=6,
          height=2,
          relief="solid",
      )
      lbl.pack(side="left", padx=3)
      self.sp_ai_lbls.append(lbl)

    player_frame = tk.LabelFrame(
        self.root,
        text=(
            f" {self.current_user['nickname']} (나의 패 - 3번째 카드는 상대에게도"
            " 공개됨) "
        ),
        font=("Arial", 11),
        padx=10,
        pady=5,
    )
    player_frame.pack(pady=5, fill="x", padx=20)
    self.sp_player_frame = player_frame
    self.sp_player_lbls = []

    for i in range(7):
      lbl = tk.Label(
          player_frame,
          text="",
          font=("Arial", 16, "bold"),
          width=6,
          height=2,
          relief="solid",
      )
      lbl.pack(side="left", padx=3)
      self.sp_player_lbls.append(lbl)

    self.update_seven_poker_cards_ui()

    self.sp_btn_frame = tk.Frame(self.root)
    self.sp_btn_frame.pack(pady=15)

    self.sp_action_btn = tk.Button(
        self.sp_btn_frame,
        text="콜 (4번째 카드 받기)",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=22,
        height=2,
        command=self.seven_poker_next,
    )
    self.sp_action_btn.pack(side="left", padx=10)

    self.sp_fold_btn = tk.Button(
        self.sp_btn_frame,
        text="포기 (다이)",
        font=("Arial", 12, "bold"),
        bg="#F44336",
        fg="white",
        width=15,
        height=2,
        command=self.seven_poker_fold,
    )
    self.sp_fold_btn.pack(side="left", padx=10)

  def update_seven_poker_cards_ui(self):
    max_dealt_idx = self.sp_step + 1

    for i in range(7):
      if i <= max_dealt_idx:
        if i == 6 and self.sp_step < 6:
          p_text = "🂠 (히든)"
          p_bg = "#ffecb3"
        elif i == 2:
          p_text = f"{self.sp_player_cards[i]}\n(오픈)"
          p_bg = "#e3f2fd"
        else:
          p_text = self.sp_player_cards[i]
          p_bg = "white"
      else:
        p_text = "🂠"
        p_bg = "#e0e0e0"

      self.sp_player_lbls[i].config(text=p_text, bg=p_bg)

      if i <= max_dealt_idx:
        if i in [2, 3, 4, 5] or self.sp_step == 6:
          ai_text = (
              f"{self.sp_ai_cards[i]}\n(오픈)"
              if (i == 2 and self.sp_step < 6)
              else self.sp_ai_cards[i]
          )
          ai_bg = "#e3f2fd" if (i == 2 and self.sp_step < 6) else "white"
        else:
          ai_text = "🂠 (비공개)"
          ai_bg = "#ccc"
      else:
        ai_text = "🂠"
        ai_bg = "#e0e0e0"

      self.sp_ai_lbls[i].config(text=ai_text, bg=ai_bg)

  def seven_poker_next(self):
    self.sp_step += 1
    self.pot += 500

    if self.sp_step == 2:
      self.sp_status_lbl.config(
          text=(
              "[세븐 포커 2단계] 서로 4번째 오픈 카드를 받았습니다. 베팅을"
              " 진행하세요!"
          )
      )
      self.sp_action_btn.config(text="콜 (5번째 카드 받기)")
    elif self.sp_step == 3:
      self.sp_status_lbl.config(
          text=(
              "[세븐 포커 3단계] 서로 5번째 오픈 카드를 받았습니다. 베팅을"
              " 진행하세요!"
          )
      )
      self.sp_action_btn.config(text="콜 (6번째 카드 받기)")
    elif self.sp_step == 4:
      self.sp_status_lbl.config(
          text=(
              "[세븐 포커 4단계] 서로 6번째 오픈 카드를 받았습니다. 베팅을"
              " 진행하세요!"
          )
      )
      self.sp_action_btn.config(text="콜 (마지막 7번째 히든 카드 받기)")
    elif self.sp_step == 5:
      self.sp_status_lbl.config(
          text=(
              "[세븐 포커 5단계] 마지막 7번째 카드를 히든(뒷면)으로 받았습니다."
              " 최종 베팅 후 쇼다운 하세요!"
          ),
          fg="#D32F2F",
      )
      self.sp_action_btn.config(text="쇼다운 (결과 확인 및 승부)")
    elif self.sp_step == 6:
      self.perform_seven_poker_showdown()
      return

    self.update_seven_poker_cards_ui()
    self.sp_pot_lbl.config(text=f"현재 팟(Pot): {self.pot:,} 칩")

  def perform_seven_poker_showdown(self):
    self.update_seven_poker_cards_ui()

    p_score, p_desc = self.evaluate_best_5_of_7(self.sp_player_cards)
    ai_score, ai_desc = self.evaluate_best_5_of_7(self.sp_ai_cards)

    if p_score > ai_score:
      result_text = f"🎉 플레이어 승리! (나: {p_desc} vs AI: {ai_desc})"
      is_win = True
      chip_change = self.pot // 2
    elif p_score < ai_score:
      result_text = f"😢 컴퓨터 승리 (나: {p_desc} vs AI: {ai_desc})"
      is_win = False
      chip_change = -(self.pot // 2)
    else:
      result_text = f"🤝 무승부! (족보 동일: {p_desc})"
      is_win = None
      chip_change = 0

    self.sp_status_lbl.config(text=result_text, fg="blue" if is_win else "red")
    self.sp_action_btn.pack_forget()
    self.sp_fold_btn.pack_forget()

    if is_win is not None:
      database.update_record(self.current_user["username"], is_win, chip_change)
      self.sync_user_data()
      self.my_chips_lbl.config(
          text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩"
      )

    end_btn_frame = tk.Frame(self.sp_btn_frame)
    end_btn_frame.pack()

    tk.Button(
        end_btn_frame,
        text="🔄 다시하기",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=14,
        height=2,
        command=self.start_seven_poker,
    ).pack(side="left", padx=5)

    tk.Button(
        end_btn_frame,
        text="🏠 게임 선택 로비",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=14,
        height=2,
        command=self.create_game_select_lobby,
    ).pack(side="left", padx=5)

  def seven_poker_fold(self):
    database.update_record(self.current_user["username"], False, -1000)
    self.sync_user_data()
    self.my_chips_lbl.config(
        text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩"
    )

    self.sp_status_lbl.config(
        text="😢 다이(Fold)를 선언하여 게임을 포기했습니다 (-1,000 칩)",
        fg="red",
    )
    self.sp_action_btn.pack_forget()
    self.sp_fold_btn.pack_forget()

    end_btn_frame = tk.Frame(self.sp_btn_frame)
    end_btn_frame.pack()

    tk.Button(
        end_btn_frame,
        text="🔄 다시하기",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=14,
        height=2,
        command=self.start_seven_poker,
    ).pack(side="left", padx=5)

    tk.Button(
        end_btn_frame,
        text="🏠 게임 선택 로비",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=14,
        height=2,
        command=self.create_game_select_lobby,
    ).pack(side="left", padx=5)

  # ==================== [5] 텍사스 홀덤 모드 ====================
  def start_holdem_game(self):
    self.sync_user_data()
    if int(self.current_user["chips"]) < 1000:
      messagebox.showwarning(
          "파산", "칩이 부족합니다! (기본 10,000칩 충전)"
      )
      database.update_record(self.current_user["username"], False, 10000)
      self.sync_user_data()

    self.clear_window()
    self.root.geometry("900x720")

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

    self.holdem_player_hole = [self.deck.pop(), self.deck.pop()]
    self.holdem_ai_hole = [self.deck.pop(), self.deck.pop()]

    self.deck.pop()  # Burn card
    self.holdem_community = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
    self.deck.pop()  # Burn card
    self.holdem_community.append(self.deck.pop())
    self.deck.pop()  # Burn card
    self.holdem_community.append(self.deck.pop())

    self.pot = 2000
    self.holdem_stage = 1

    top_info_frame = tk.Frame(self.root)
    top_info_frame.pack(pady=5)

    self.holdem_my_chips_lbl = tk.Label(
        top_info_frame,
        text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩",
        font=("Arial", 13, "bold"),
        fg="#2E7D32",
    )
    self.holdem_my_chips_lbl.pack(side="left", padx=15)

    self.holdem_pot_lbl = tk.Label(
        top_info_frame,
        text=f"현재 팟(Pot): {self.pot:,} 칩",
        font=("Arial", 13, "bold"),
        fg="#388E3C",
    )
    self.holdem_pot_lbl.pack(side="left", padx=15)

    self.holdem_status_lbl = tk.Label(
        self.root,
        text=(
            "[텍사스 홀덤 - ① 프리플랍] 개인 카드 2장을 받았습니다. 첫 베팅을"
            " 진행하세요!"
        ),
        font=("Arial", 11, "bold"),
        fg="#FF9800",
    )
    self.holdem_status_lbl.pack(pady=5)

    ai_frame = tk.LabelFrame(
        self.root, text=" 컴퓨터 (AI 홀 카드) ", font=("Arial", 11), padx=10, pady=5
    )
    ai_frame.pack(pady=5, fill="x", padx=20)
    self.holdem_ai_lbls = []
    for _ in range(2):
      lbl = tk.Label(
          ai_frame,
          text="🂠",
          font=("Arial", 20),
          width=4,
          height=2,
          bg="white",
          relief="solid",
      )
      lbl.pack(side="left", padx=5)
      self.holdem_ai_lbls.append(lbl)

    comm_frame = tk.LabelFrame(
        self.root,
        text=" 공용 카드 (Community Cards - 총 5장) ",
        font=("Arial", 11),
        padx=10,
        pady=5,
    )
    comm_frame.pack(pady=5, fill="x", padx=20)
    self.holdem_comm_lbls = []
    for _ in range(5):
      lbl = tk.Label(
          comm_frame,
          text="🂠",
          font=("Arial", 20),
          width=4,
          height=2,
          bg="#e0e0e0",
          relief="solid",
      )
      lbl.pack(side="left", padx=5)
      self.holdem_comm_lbls.append(lbl)

    player_frame = tk.LabelFrame(
        self.root,
        text=f" {self.current_user['nickname']} (나의 홀 카드 2장) ",
        font=("Arial", 11),
        padx=10,
        pady=5,
    )
    player_frame.pack(pady=5, fill="x", padx=20)
    for card in self.holdem_player_hole:
      tk.Label(
          player_frame,
          text=card,
          font=("Arial", 20, "bold"),
          width=4,
          height=2,
          bg="white",
          relief="solid",
      ).pack(side="left", padx=5)

    self.holdem_btn_frame = tk.Frame(self.root)
    self.holdem_btn_frame.pack(pady=15)

    self.holdem_action_btn = tk.Button(
        self.holdem_btn_frame,
        text="콜 (② 플랍 3장 공개)",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=22,
        height=2,
        command=self.holdem_next_step,
    )
    self.holdem_action_btn.pack(side="left", padx=10)

    self.holdem_fold_btn = tk.Button(
        self.holdem_btn_frame,
        text="포기 (다이)",
        font=("Arial", 12, "bold"),
        bg="#F44336",
        fg="white",
        width=15,
        height=2,
        command=self.holdem_fold,
    )
    self.holdem_fold_btn.pack(side="left", padx=10)

  def holdem_next_step(self):
    self.holdem_stage += 1
    self.pot += 1000

    if self.holdem_stage == 2:
      self.holdem_comm_lbls[0].config(
          text=self.holdem_community[0], bg="white"
      )
      self.holdem_comm_lbls[1].config(
          text=self.holdem_community[1], bg="white"
      )
      self.holdem_comm_lbls[2].config(
          text=self.holdem_community[2], bg="white"
      )
      self.holdem_status_lbl.config(
          text=(
              "[텍사스 홀덤 - ② 플랍] 공용 카드 3장이 공개되었습니다. 세 번째"
              " 베팅(턴)으로 진행하세요!"
          )
      )
      self.holdem_action_btn.config(text="콜 (③ 턴 카드 1장 추가)")
    elif self.holdem_stage == 3:
      self.holdem_comm_lbls[3].config(
          text=self.holdem_community[3], bg="white"
      )
      self.holdem_status_lbl.config(
          text=(
              "[텍사스 홀덤 - ③ 턴] 공용 카드 4장이 되었습니다. 네 번째"
              " 베팅(리버)으로 진행하세요!"
          )
      )
      self.holdem_action_btn.config(text="콜 (④ 리버 카드 1장 추가)")
    elif self.holdem_stage == 4:
      self.holdem_comm_lbls[4].config(
          text=self.holdem_community[4], bg="white"
      )
      self.holdem_status_lbl.config(
          text=(
              "[텍사스 홀덤 - ④ 리버] 마지막 공용 카드까지 5장이 모두"
              " 공개되었습니다. 최종 쇼다운 하세요!"
          ),
          fg="#D32F2F",
      )
      self.holdem_action_btn.config(text="쇼다운 (결과 확인 및 승부)")
    elif self.holdem_stage == 5:
      self.perform_holdem_showdown()
      return

    self.holdem_pot_lbl.config(text=f"현재 팟(Pot): {self.pot:,} 칩")

  def perform_holdem_showdown(self):
    for i, card in enumerate(self.holdem_ai_hole):
      self.holdem_ai_lbls[i].config(text=card, bg="white")

    p_cards = self.holdem_player_hole + self.holdem_community
    ai_cards = self.holdem_ai_hole + self.holdem_community

    p_score, p_desc = self.evaluate_best_5_of_7(p_cards)
    ai_score, ai_desc = self.evaluate_best_5_of_7(ai_cards)

    if p_score > ai_score:
      result_text = f"🎉 텍사스 홀덤 승리! (나: {p_desc} vs AI: {ai_desc})"
      is_win = True
      chip_change = self.pot // 2
    elif p_score < ai_score:
      result_text = f"😢 컴퓨터 승리 (나: {p_desc} vs AI: {ai_desc})"
      is_win = False
      chip_change = -(self.pot // 2)
    else:
      result_text = f"🤝 무승부! (족보 동일: {p_desc})"
      is_win = None
      chip_change = 0

    self.holdem_status_lbl.config(
        text=result_text, fg="blue" if is_win else "red"
    )
    self.holdem_action_btn.pack_forget()
    self.holdem_fold_btn.pack_forget()

    if is_win is not None:
      database.update_record(self.current_user["username"], is_win, chip_change)
      self.sync_user_data()
      self.holdem_my_chips_lbl.config(
          text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩"
      )

    end_btn_frame = tk.Frame(self.holdem_btn_frame)
    end_btn_frame.pack()

    tk.Button(
        end_btn_frame,
        text="🔄 다시하기",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=14,
        height=2,
        command=self.start_holdem_game,
    ).pack(side="left", padx=5)

    tk.Button(
        end_btn_frame,
        text="🏠 게임 선택 로비",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=14,
        height=2,
        command=self.create_game_select_lobby,
    ).pack(side="left", padx=5)

  def holdem_fold(self):
    database.update_record(self.current_user["username"], False, -1000)
    self.sync_user_data()
    self.holdem_my_chips_lbl.config(
        text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩"
    )

    self.holdem_status_lbl.config(
        text="😢 포기(Fold)를 선언했습니다 (-1,000 칩)", fg="red"
    )
    self.holdem_action_btn.pack_forget()
    self.holdem_fold_btn.pack_forget()

    end_btn_frame = tk.Frame(self.holdem_btn_frame)
    end_btn_frame.pack()

    tk.Button(
        end_btn_frame,
        text="🔄 다시하기",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=14,
        height=2,
        command=self.start_holdem_game,
    ).pack(side="left", padx=5)

    tk.Button(
        end_btn_frame,
        text="🏠 게임 선택 로비",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=14,
        height=2,
        command=self.create_game_select_lobby,
    ).pack(side="left", padx=5)

  # ==================== [6] 슬롯 머신 모드 ====================
  def start_slot_machine(self):
    self.sync_user_data()
    if int(self.current_user["chips"]) < 500:
      messagebox.showwarning(
          "파산", "칩이 부족합니다! (기본 10,000칩 충전)"
      )
      database.update_record(self.current_user["username"], False, 10000)
      self.sync_user_data()

    self.clear_window()
    self.root.geometry("800x600")

    top_frame = tk.Frame(self.root)
    top_frame.pack(pady=15)

    self.slot_chips_lbl = tk.Label(
        top_frame,
        text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩",
        font=("Arial", 14, "bold"),
        fg="#2E7D32",
    )
    self.slot_chips_lbl.pack()

    tk.Label(
        self.root,
        text="🎰 럭키 77 슬롯 머신",
        font=("Arial", 22, "bold"),
        fg="#E91E63",
    ).pack(pady=10)

    reel_frame = tk.Frame(self.root, bg="#222", bd=5, relief="ridge")
    reel_frame.pack(pady=20)

    self.slot_symbols = ["🍒", "🍋", "🍊", "🍇", "🔔", "💎", "7"]
    self.reel_labels = []

    for _ in range(3):
      lbl = tk.Label(
          reel_frame,
          text="🎰",
          font=("Arial", 40, "bold"),
          width=3,
          height=2,
          bg="white",
          fg="#333",
          relief="sunken",
      )
      lbl.pack(side="left", padx=10, pady=10)
      self.reel_labels.append(lbl)

    self.slot_status_lbl = tk.Label(
        self.root,
        text="배팅 금액: 500 칩 | [SPIN] 버튼을 눌러 돌리세요!",
        font=("Arial", 13, "bold"),
        fg="#333",
    )
    self.slot_status_lbl.pack(pady=15)

    btn_frame = tk.Frame(self.root)
    btn_frame.pack(pady=15)

    self.spin_btn = tk.Button(
        btn_frame,
        text="🎰 SPIN! (500칩 베팅)",
        font=("Arial", 14, "bold"),
        bg="#E91E63",
        fg="white",
        width=20,
        height=2,
        command=self.spin_slot_machine,
    )
    self.spin_btn.pack(side="left", padx=10)

    tk.Button(
        btn_frame,
        text="로비로 돌아가기",
        font=("Arial", 12, "bold"),
        bg="#2196F3",
        fg="white",
        width=15,
        height=2,
        command=self.create_game_select_lobby,
    ).pack(side="left", padx=10)

  def spin_slot_machine(self):
    bet_cost = 500
    self.sync_user_data()
    if int(self.current_user["chips"]) < bet_cost:
      messagebox.showwarning("경고", "보유 칩이 부족합니다!")
      return

    database.update_record(self.current_user["username"], False, -bet_cost)

    r1 = random.choice(self.slot_symbols)
    r2 = random.choice(self.slot_symbols)
    r3 = random.choice(self.slot_symbols)

    self.reel_labels[0].config(text=r1, fg="red" if r1 == "7" else "#333")
    self.reel_labels[1].config(text=r2, fg="red" if r2 == "7" else "#333")
    self.reel_labels[2].config(text=r3, fg="red" if r3 == "7" else "#333")

    reward = 0
    if r1 == "7" and r2 == "7" and r3 == "7":
      reward = 25000
      msg = "🔥 대박! 777 잭팟 당첨!! (+25,000 칩)"
    elif r1 == r2 == r3:
      reward = 5000
      msg = f"🎉 {r1} 트리플 당첨!! (+5,000 칩)"
    elif r1 == r2 or r2 == r3 or r1 == r3:
      reward = 1000
      msg = "✨ 투 림(더블) 당첨! (+1,000 칩)"
    else:
      msg = "😢 아쉽네요... 꽝!"

    if reward > 0:
      database.update_record(self.current_user["username"], True, reward)
      self.slot_status_lbl.config(text=msg, fg="blue")
    else:
      self.slot_status_lbl.config(text=msg, fg="red")

    self.sync_user_data()
    self.slot_chips_lbl.config(
        text=f"보유 칩: 🪙 {int(self.current_user['chips']):,} 칩"
    )

  # ==================== [7] 7장 중 가장 좋은 5장을 뽑아 족보를 판정하는 알고리즘 ====================
  def evaluate_best_5_of_7(self, cards_7):
    best_score = -1
    best_desc = ""
    best_combo_values = ()

    for combo in itertools.combinations(cards_7, 5):
      score, desc, val_tuple = self.evaluate_5_cards(list(combo))
      if score > best_score or (
          score == best_score and val_tuple > best_combo_values
      ):
        best_score = score
        best_desc = desc
        best_combo_values = val_tuple

    return best_score, best_desc

  def evaluate_5_cards(self, cards_5):
    rev_val_map = {
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "10",
        11: "J",
        12: "Q",
        13: "K",
        14: "A",
    }
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
    suits = [c[0] for c in cards_5]
    values = sorted([val_map[c[1:]] for c in cards_5], reverse=True)

    is_flush = len(set(suits)) == 1

    is_straight = False
    unique_vals = sorted(list(set(values)), reverse=True)
    if len(unique_vals) == 5:
      if unique_vals[0] - unique_vals[4] == 4:
        is_straight = True
      elif unique_vals == [14, 5, 4, 3, 2]:
        is_straight = True
        values = [5, 4, 3, 2, 1]

    counts = {v: values.count(v) for v in values}
    sorted_counts = sorted(
        counts.items(), key=lambda x: (x[1], x[0]), reverse=True
    )
    max_count = sorted_counts[0][1]

    if is_flush and is_straight:
      if max(values) == 14 and min(values) == 10:
        return (1300, "로열 스트레이트 플러시", tuple(values))
      if unique_vals == [14, 5, 4, 3, 2]:
        return (1200, "백 스트레이트 플러시", tuple(values))
      return (1100 + max(values), "스트레이트 플러시", tuple(values))

    if max_count == 4:
      four_val = sorted_counts[0][0]
      kicker = sorted_counts[1][0]
      f_name = rev_val_map[four_val]
      return (1000 + four_val, f"{f_name} 포카드", (four_val, kicker))

    if max_count == 3 and len(sorted_counts) == 2:
      tri_val = sorted_counts[0][0]
      pair_val = sorted_counts[1][0]
      t_name = rev_val_map[tri_val]
      p_name = rev_val_map[pair_val]
      return (900 + tri_val, f"{t_name} 풀하우스", (tri_val, pair_val))

    if is_flush:
      return (800 + values[0], "플러시", tuple(values))

    if is_straight:
      if unique_vals == [14, 13, 12, 11, 10]:
        return (750, "마운틴", tuple(values))
      if unique_vals == [14, 5, 4, 3, 2]:
        return (720, "백 스트레이트", tuple(values))
      return (700 + max(values), "스트레이트", tuple(values))

    if max_count == 3:
      tri_val = sorted_counts[0][0]
      t_name = rev_val_map[tri_val]
      kickers = tuple(v for v in values if v != tri_val)
      return (600 + tri_val, f"{t_name} 트리플", (tri_val,) + kickers)

    if max_count == 2 and len(sorted_counts) == 3:
      pairs = sorted(
          [item[0] for item in sorted_counts if item[1] == 2], reverse=True
      )
      p1_name = rev_val_map[pairs[0]]
      p2_name = rev_val_map[pairs[1]]
      kicker = [item[0] for item in sorted_counts if item[1] == 1][0]
      return (
          500 + pairs[0] * 10 + pairs[1],
          f"{p1_name}·{p2_name} 투페어",
          (pairs[0], pairs[1], kicker),
      )

    if max_count == 2:
      pair_val = sorted_counts[0][0]
      p_name = rev_val_map[pair_val]
      kickers = tuple(v for v in values if v != pair_val)
      return (400 + pair_val, f"{p_name} 원페어", (pair_val,) + kickers)

    highest_card = max(cards_5, key=lambda c: val_map[c[1:]])
    return (300 + values[0], f"탑 ({highest_card[1:]} 탑)", tuple(values))


if __name__ == "__main__":
  database.init_db()
  root = tk.Tk()
  app = RealCardGamePlatform(root)
  root.mainloop()