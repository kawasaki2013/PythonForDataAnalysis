# -*- coding: utf-8 -*- 

import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Pythonによるデータ分析入門 第２章

# 集計用の関数
def get_counts(sequence):
    counts={}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts
def get_counts2(sequence):
    counts = defaultdict(int) # 動的に辞書を生成し、値を0に初期化
    for x in sequence:
        counts[x] += 1
    return counts

# カウント数上位の要素を返す
def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]

if __name__ == "__main__":
    ## JSON形式のデータを読み込んでみる
    path = 'pydata-book/ch02/usagov_bitly_data2012-03-16-1331923249.txt'
    print open(path).readline() # JSON文字列
    records = [json.loads(line) for line in open(path)]
    print records[0] # リストになった
    print records[0]['tz'] # １番目のrecordからtzの要素を取得
    
    #time_zones = [rec['tz'] for rec in records]
    ### KeyErrorが出る→全てのrecordにtz要素があるわけではないらしい
    ## ↑なので、if文を入れて要素が無い行を無視する
    time_zones = [rec['tz'] for rec in records if 'tz' in rec]
    print time_zones[:10]
    
    ## タイムゾーンの集計をする
    ### 標準ライブラリで
    counts = get_counts2(time_zones)
    print counts['America/New_York']
    print len(time_zones)
    print len(counts)
    ### 上位１０件のタイムゾーンを調べる
    print top_counts(counts)
    
    ### collection.Counterを使うととっても簡単
    counts = Counter(time_zones)
    print counts.most_common(10)

    ### pandas ライブラリを使う
    frame = DataFrame(records)
    #print frame
    tz_counts = frame['tz'].value_counts()
    #### frame['tz']でtz列だけを取得。
    #### 形式はSeriesオブジェクト形式になる
    #print tz_counts[:10]
    clean_tz = frame['tz'].fillna('Missing') # fillnaメソッドでNAに値を代入
    clean_tz[clean_tz == ''] = 'Unknown' # 空白の要素があったら値を代入
    tz_counts = clean_tz.value_counts()
    print tz_counts[:10]
    #### tz_countsオブジェクトを使ってplotする
#    tz_counts[:10].plot(kind='barh', rot=0) # pandasのplotメソッド
#    plt.show() # matplotlibで画像を表示する

    ## UAの集計をしてみる
    ### どんなか見る
    print frame['a'][1]
    print frame['a'][50]
    print frame['a'][51]
    ### UAの先頭トークンを切り出して集計する
    results = Series([x.split()[0] for x in frame.a.dropna()])
    #### ↑Seriesオブジェクトで、UAの先頭を切り出したオブジェクトを作成
    #### str.split(sep) : sepで分割。sepが指定されない場合スペース、タブ、改行文字列で分割
    #### dropna : 欠損値のあるindexを削除
    print results[:5]
    print results.value_counts()[:8]
    ### Windowsの文字列が入っているUAとそれ以外を分けてみる
    cframe = frame[frame.notnull()]
    operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'notWindows')
    print operating_system[:5]
    ### タイムゾーンとOSでグループ化
    by_tz_os = cframe.groupby(['tz', operating_system])
    print by_tz_os.size().unstack().fillna(0)[:10]
    #### fillna(0) : 欠損値を０で埋める
    agg_counts = by_tz_os.size().unstack().fillna(0)
    ### agg_countsをソートする
    indexer = agg_counts.sum(1).argsort()
    print indexer[:10]
