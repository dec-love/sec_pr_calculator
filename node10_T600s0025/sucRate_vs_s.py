import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ファイルパス
summary_csv = "att_result/att_n10_delay5_T600_summary.csv"
p_binomial_csv = "p_binominal_result/p_n10.csv"

# p_binominal_result/p_n10.csvを読み込む
p_df = pd.read_csv(p_binomial_csv)

# プロットするpの値のリスト
# p_values = [0.01, 0.1, 0.2, 0.25, 0.3, 0.5]
p_values = [0.1, 0.3, 0.5, 0.7, 0.9]
# p_values = [0.3]



# グラフの描画の準備
plt.figure(figsize=(10, 6))

# 各pに対してグラフを作成 (false と false2)
for p_value in p_values:
    # pに対応する行を抽出
    p_row = p_df[p_df['p'] == p_value].iloc[0, 1:].values

    # att_result/att_n10_delay5_T6_summary.csvを読み込む
    summary_df = pd.read_csv(summary_csv)

    # falseに対して期待値を計算
    summary_df['expected_false'] = 0.0
    for i in range(11):
        summary_df['expected_false'] += summary_df.apply(
            lambda row: row['false'] * p_row[i] if row['i'] == i else 0, axis=1
        )
    
    # false2に対して期待値を計算
    summary_df['expected_false2'] = 0.0
    for i in range(11):
        summary_df['expected_false2'] += summary_df.apply(
            lambda row: row['false2'] * p_row[i] if row['i'] == i else 0, axis=1
        )

    # sごとに期待値を集計
    expected_false_by_s = summary_df.groupby('s')['expected_false'].sum()
    expected_false2_by_s = summary_df.groupby('s')['expected_false2'].sum()
    # expected_false_by_sの最大値とそのときのsをprint
    print(expected_false_by_s.idxmax())
    print(expected_false_by_s.max())
    

    # # グラフをプロット (false)
    
    # plt.plot(expected_false_by_s.index, expected_false_by_s.values, linestyle='None', marker='o', label=f'With Stale Block Impact')

    # # グラフをプロット (false2)
    # plt.plot(expected_false2_by_s.index, expected_false2_by_s.values, linestyle='None', marker='x',  label=f'Without Stale Block Impact')
    
    plt.plot(expected_false_by_s.index, expected_false_by_s.values, linestyle='None', marker='o', label=f'p={p_value}')


# グラフの設定
plt.xlabel('s' , fontsize=24)
plt.ylabel('Security probability', fontsize=24)
# plt.title('Expected False and Expected False2 vs s for different p values')
plt.legend(title='', fontsize=14)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.grid(True)
# pdfファイルで保存する
# plt.savefig("/Users/nt/Documents/distributed_system_semi/css2024/sec_pr_intro.pdf")
plt.tight_layout()
plt.show()

