import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.special import comb

# CSVファイルの読み込み
file_path = 'att_result/att_n10_delay5_T600_summary.csv'
data = pd.read_csv(file_path)

# 10Ci の計算
data['10Ci'] = data['i'].apply(lambda x: int(comb(10, x)))

# 分子/分母を計算
data['false_normalized'] = data['false'] / data['10Ci']

# 分子と分母をフォーマットして表示
data['annot_text'] = data.apply(lambda row: f"{int(row['false'])}\n-\n{int(row['10Ci'])}", axis=1)

# ヒートマップを個別に描画
unique_i_values = data['i'].unique()  # ユニークなiの値を取得

plt.figure(figsize=(10, 1.2 * len(unique_i_values)))  # 図のサイズを調整

for idx, i_value in enumerate(unique_i_values):
    # 各iに対するデータのフィルタリング
    filtered_data = data[data['i'] == i_value]
    
    # ピボットテーブルの作成
    pivot_table = filtered_data.pivot(index='i', columns='s', values='annot_text')
    pivot_values = filtered_data.pivot(index='i', columns='s', values='false_normalized')
    
    # ヒートマップの作成
    plt.subplot(len(unique_i_values), 1, idx + 1)  # 行数をiのユニーク数に設定
    sns.heatmap(pivot_values, annot=pivot_table.values, fmt="", 
                cmap=sns.color_palette("coolwarm", as_cmap=True).reversed(), 
                annot_kws={"size": 10, "va": 'center', "ha": 'center'}, 
                cbar=True, linewidths=0.5, linecolor='black', 
                vmin=pivot_values.min().min(), vmax=pivot_values.max().max())

    # x軸ラベルの表示設定
    if i_value == 10:
        plt.xlabel('s', fontsize=18)  # x軸ラベル
    else:
        plt.xlabel('')  # 他のヒートマップのx軸ラベルを非表示にする

    # y軸ラベルの表示設定
    if i_value == 5:
        plt.ylabel('k', fontsize=18)  # y軸ラベル
    else:
        plt.ylabel('')  # 他のヒートマップのy軸ラベルを非表示にする

    # x軸目盛りの表示設定
    if i_value == 10:
        plt.xticks(fontsize=12)  # x軸の目盛りのフォントサイズ
    else:
        plt.xticks([])  # 他のヒートマップのx軸目盛りを非表示にする

    plt.yticks(fontsize=12)  # y軸の目盛りのフォントサイズ

plt.tight_layout()  # レイアウトを自動調整して余白を最小化
plt.show()
