import requests
import io
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import scipy.stats
sns.set(font_scale=2)
sns.set_style("whitegrid")

# データ取得
url = 'https://ckan.pf-sapporo.jp/dataset/c89f65e7-45a8-4ab2-b94d-494ae192c70f/resource/b83606f6-3aa2-4e0c-8a1a-509dd36be2ae/download/patientssummary.csv'

res = requests.get(url).content
df = pd.read_csv(io.StringIO(res.decode('utf-8')))

df['日付'] = pd.to_datetime(df['日付'].str[:10])
df['小計'] = df['小計'].astype(int)

# サイドバー実装
min_date = df['日付'][0]
max_date = df['日付'][len(df)-1]

sidebar_date = st.sidebar.date_input(
    "表示する期間を選択してください",
    [min_date, max_date],
    min_value = min_date,
    max_value = max_date
)

sidebar_min_date = np.datetime64(sidebar_date[0])
sidebar_max_date = np.datetime64(sidebar_date[1]) if len(sidebar_date)==2 else max_date

'''
# 新型コロナ感染症の札幌市内発生状況
'''

now_patients = df['小計'][len(df)-1]
now_date = str(max_date)[:10]

f'本日 {now_date} の陽性者数は {now_patients} 人です.'

'''
## 陽性患者数（表）

'''
if sidebar_max_date==None:
    sidebar_max_date = sidebar_min_date
df_selected = df[ (df['日付'] >= sidebar_min_date) & (df['日付'] <= sidebar_max_date) ]
st.write(df_selected)


'''
## 陽性患者数（グラフ）

'''

# figure,axisオブジェクトの作成
fig = plt.figure(figsize=(16,8))
ax = fig.add_subplot(111)

plt.xlabel('day')
plt.ylabel('numbers of patients')
ax.plot(df_selected['日付'], df_selected['小計'], color='red')

# xラベルの目盛りを調整
ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
plt.setp(ax.get_xticklabels(), rotation=0)

# レイアウト？をいい感じに
plt.tight_layout()

# 描画
st.write(fig)