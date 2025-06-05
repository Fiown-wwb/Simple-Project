import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import os

# 读取任务二的数据
result_df = pd.read_csv('output/tang_poems_tfidf.txt', sep='\t', encoding='utf-8')

# 统计每种诗类型的诗数量
type_counts = result_df['Type'].value_counts()
type_counts.to_excel(os.path.join('output', 'type_counts.xlsx'))

# 统计每个作者的诗数量
author_counts = result_df['Author'].value_counts()
author_counts.to_excel(os.path.join('output', 'author_counts.xlsx'))

# 对诗内容进行中文分词并输出词云图
all_content = ' '.join(result_df['Content'])
word_list = jieba.lcut(all_content)
word_counts = Counter(word_list)

# 绘制词云图
wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=400, background_color='white')
wordcloud.generate_from_frequencies(word_counts)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig(os.path.join('output', 'wordcloud.png'))
plt.show()
