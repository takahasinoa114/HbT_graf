import pandas as pd
import matplotlib.pyplot as plt

pilot_filename = 'pilot_untitled_2026-06-19_15h44.56.308.csv'   # Psychopyのデータファイル名を指定する
df_pilot = pd.read_csv(pilot_filename)

raw_start_time = df_pilot.iloc[2, 39]
cleaned_start_time = raw_start_time.replace('h', ':').replace('.', ':', 1)
start_time = pd.to_datetime(cleaned_start_time)

log_filename = 'HOTLog_20260619_154721.csv'     # NIRSのデータファイル名を指定する
df = pd.read_csv(log_filename, skiprows=13)

df.columns = df.columns.str.strip()
df['# Device time'] = pd.to_datetime(df['# Device time'])

if df['# Device time'].dt.tz is None and start_time.tz is not None:
    start_time = start_time.tz_localize(None)

df.set_index('# Device time', inplace=True)

fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.plot(df.index, df['HbT change(left subtracted)'], label='HbT change(left subtracted)', alpha=0.8)
ax1.plot(df.index, df['HbT change(right subtracted)'], label='HbT change(right subtracted)', alpha=0.8)

ax1.set_xlabel('Device time')
ax1.set_ylabel('HbT change')

end_time = df.index.max()
current_time = start_time
count = 0

lines_time = []
lines_count = []

while current_time <= end_time:
    if current_time >= df.index.min():
        lines_time.append(current_time)
        lines_count.append(str(count))
        ax1.axvline(x=current_time, color='red', linestyle='--', linewidth=1, alpha=0.4)
        count += 1
    current_time += pd.Timedelta(seconds=8)

ax2 = ax1.twiny()
ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(lines_time)
ax2.set_xticklabels(lines_count, rotation=0, fontsize=8)
ax2.set_xlabel('Line Count')

ax1.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig('HbT_0.png')   # グラフを保存するファイル名を指定する
plt.show()