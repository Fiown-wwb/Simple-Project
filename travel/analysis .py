import os
import jieba
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
from wordcloud import WordCloud

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
file_path = 'Chengdu_Sights.xlsx'
data = pd.read_excel(file_path)
data['Heat'] = data['Heat'].fillna(data['Heat'].mean())
data['Score'] = data['Score'].fillna(data['Score'].mean())
data['Price'] = data['Price'].fillna(data['Price'].mode()[0])
data['Location'] = data['Location'].fillna(data['Location'].mode()[0])
data['Reviews'] = data['Reviews'].fillna(data['Reviews'].mode()[0])
data['Diszance'] = data['Distance'].fillna(data['Distance'].mode()[0])

scaler = MinMaxScaler()
data[['Heat', 'Score']] = scaler.fit_transform(data[['Heat', 'Score']])
preprocessed_file_path = 'Preprocessed_Chengdu_Sights.xlsx'
data.to_excel(preprocessed_file_path, index=False)

top_10_heat = data.nlargest(10, 'Heat')
plt.figure(figsize=(10, 6))
plt.bar(top_10_heat['Name'], top_10_heat['Heat'], color='skyblue')
plt.xlabel('景区名称')
plt.ylabel('热度')
plt.title('热度前十的景区')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

location_counts = Counter(data['Location'])
top_10_locations = location_counts.most_common(10)
G = nx.DiGraph()
for location, count in top_10_locations:
    G.add_node(location, size=count*100)
for i in range(len(top_10_locations) - 1):
    G.add_edge(top_10_locations[i][0], top_10_locations[i + 1][0])
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
sizes = [G.nodes[node]['size'] for node in G]
nx.draw(G, pos, with_labels=True, node_size=sizes, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
plt.title('共同位置出现次数最多的前十个景区')
plt.show()

# 对Name进行中文分词并输出词云图
all_content = ' '.join(data['Name'])
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




