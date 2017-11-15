# Logistic Regression
import pandas as pd

df = pd.read_csv('SMSSpamCollection', delimiter='\t', header=None)
df.head()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split

# 用pandas加载数据.csv文件，然后用train_test_split分成训练集（75%）和测试集（25%）：
X_train_raw, X_test_raw, y_train, y_test = train_test_split(df[1], df[0])
# 我们建一个TfidfVectorizer实例来计算TF-IDF权重：
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)
# LogisticRegression同样实现了fit()和predict()方法
classifier = LogisticRegression()
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

for i, prediction in enumerate(predictions[-5:]):
    print('预测类型：%s.信息：%s' % (prediction, X_test_raw.iloc[i]))
