import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
import os

# 读取tang_poems.txt文件
poem_df = pd.read_csv('output/tang_poems.txt', sep=',', header=0)

# 文本特征向量化
vectorizer = TfidfVectorizer(tokenizer=jieba.lcut, max_features=100)
tfidf_matrix = vectorizer.fit_transform(poem_df['Content'])
tfidf_feature_names = vectorizer.get_feature_names_out()

# 将TF-IDF结果添加到DataFrame
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_feature_names)
result_df = pd.concat([poem_df, tfidf_df], axis=1)

# 保存为txt文件
output_file = os.path.join('output', 'tang_poems_tfidf.txt')
result_df.to_csv(output_file, sep='\t', index=False, header=True, encoding='utf-8')
print(f"数据已保存至 {output_file}")
