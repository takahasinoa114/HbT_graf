import pandas as pd
import matplotlib.pyplot as plt

# 1. データの読み込み
filename = 'HOTLog_20260619_154721.csv'
df = pd.read_csv(filename, skiprows=13)

# 列名の余白削除とインデックス設定
df.columns = df.columns.str.strip()
df['# Device time'] = pd.to_datetime(df['# Device time'])
df.set_index('# Device time', inplace=True)

# 2. ベースのグラフを描画
fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.plot(df.index, df['HbT change(left subtracted)'], label='HbT change(left subtracted)', alpha=0.8)
ax1.plot(df.index, df['HbT change(right subtracted)'], label='HbT change(right subtracted)', alpha=0.8)

# 下軸（時間軸）の設定
ax1.set_xlabel('Device time')
ax1.set_ylabel('HbT change')

# 3. スタート時間から8秒ごとの縦線とカウント（目盛りラベル）の計算
start_time = pd.to_datetime('2026-06-19 15:45:07.163119')
end_time = df.index.max()

current_time = start_time
count = 0

lines_time = []   # 縦線を引く時間（X軸の位置）
lines_count = []  # その時のカウント数（ラベル）

while current_time <= end_time:
    # データが存在する時間枠（グラフ内）に入っている場合のみリストに追加
    if current_time >= df.index.min():
        lines_time.append(current_time)
        lines_count.append(str(count))
        
        # 縦線を描画
        ax1.axvline(x=current_time, color='red', linestyle='--', linewidth=1, alpha=0.4)
        
    current_time += pd.Timedelta(seconds=8)
    count += 1

# 4. 上部に新しい横軸（カウント用の軸）を作成して連動させる
ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())  # 下の軸と範囲を完全に一致させる

# カウント位置に目盛りを打ち、数字を表示
ax2.set_xticks(lines_time)
ax2.set_xticklabels(lines_count, rotation=90, fontsize=8)
ax2.set_xlabel('Line Count (0 at Start Time)')

# 5. 全体の調整と出力
ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
plt.tight_layout()

# 画像として保存、または表示
plt.savefig('hotlog_with_line_counts.png')
plt.show()