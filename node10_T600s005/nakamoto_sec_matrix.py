import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import comb

# CSVファイルの読み込み
file_path = 'att_result/att_n10_delay5_T600_summary.csv'
data = pd.read_csv(file_path)

# `10Ci` の計算
data['10Ci'] = data['i'].apply(lambda x: int(comb(10, x)))

# 分子/分母を計算
data['false_normalized'] = data['false'] / data['10Ci']

# 分子と分母をフォーマットして表示
data['annot_text'] = data.apply(lambda row: f"{int(row['false'])}\n-\n{int(row['10Ci'])}", axis=1)

# ピボットテーブルの作成 (sを横軸、iを縦軸にして計算結果とカスタムアノテーションを配置)
pivot_table = data.pivot(index='i', columns='s', values='annot_text')
pivot_values = data.pivot(index='i', columns='s', values='false_normalized')

# ヒートマップの作成
plt.figure(figsize=(16, 12))  # 図のサイズを大きくする

# カスタムアノテーション付きヒートマップの作成
sns.heatmap(pivot_values, annot=pivot_table.values, fmt="", cmap=sns.color_palette("coolwarm", as_cmap=True).reversed(), 
            annot_kws={"size": 10, "va": 'center', "ha": 'center'}, cbar=True, linewidths=1.0, linecolor='black', 
            vmin=pivot_values.min().min(), vmax=pivot_values.max().max())

# plt.title('Heatmap of False values normalized by 10Ci', fontsize=20)  # タイトルのフォントサイズを調整
plt.xlabel('s', fontsize=24)  # x軸ラベルのフォントサイズを調整
plt.ylabel('k', fontsize=24)  # y軸ラベルのフォントサイズを調整
plt.xticks(fontsize=14)  # x軸の目盛りのフォントサイズを調整
plt.yticks(fontsize=14)  # y軸の目盛りのフォントサイズを調整
plt.tight_layout()  # レイアウトを自動調整して余白を最小化
plt.show()
