# ====================
# 人とAIの対戦
# ====================

# パッケージのインポート
from reversi_game import State
import tkinter as tk

# ゲームUIの定義
class GameUI(tk.Frame):
    # 初期化
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('リバーシ')

        # ゲーム状態の生成
        self.state = State()

        # キャンバスの生成
        self.c = tk.Canvas(self, width=480, height=480, highlightthickness=0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 描画の更新
        self.on_draw()

    # 人間のターン
    def turn_of_human(self, event):
        # ゲーム終了時
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # 先手でない時
        if not self.state.is_first_player():
            return

        # クリック位置を行動に変換
        x = int(event.x/60)
        y = int(event.y/60)
        if x < 0 or 7 < x or y < 0 or 7 < y: # 範囲外
            return
        action = x + y * 8

        # 合法手でない時
        legal_actions = self.state.legal_actions()
        if legal_actions == [64]:
            action = 64 # パス
        if action != 64 and not (action in legal_actions):
            return

        # 次の状態の取得
        self.state = self.state.next(action)
        self.on_draw()

        # AIのターン
        self.master.after(1000, self.turn_of_ai)

    # AIのターン
    def turn_of_ai(self):
        # ゲーム終了時
        if self.state.is_done():
            return

        # 行動の取得
        action = self.state.random_action(self.state)

        # 次の状態の取得
        self.state = self.state.next(action)
        self.on_draw()

    # 石の描画
    def draw_piece(self, index, first_player):
        x = (index%8)*60+5
        y = int(index/8)*60+5
        if first_player:
            self.c.create_oval(x, y, x+50, y+50, width=1.0, outline='#ffffff', fill='#000000')
        else:
            self.c.create_oval(x, y, x+50, y+50, width=1.0, outline='#000000', fill='#ffffff')

    # 描画の更新
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 480, 480, width=0.0, fill='#008000')
        for i in range(1, 8):
            self.c.create_line(0, i*60, 480, i*60, width=1.0, fill='#000000')
            self.c.create_line(i*60, 0, i*60, 480, width=1.0, fill='#000000')
        for i in range(64):
            if self.state.my_pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())

# ゲームUIの実行
f = GameUI()
f.pack()
f.mainloop()