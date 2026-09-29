
import os, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

p=os.path.join(os.path.dirname(__file__),"data","tickets.csv")
t=pd.read_csv(p)
t["created_dt"]=pd.to_datetime(t["created_at"],errors="coerce")
t=t[(t.created_dt>="2025-01-01")&(t.created_dt<"2026-07-01")].copy()
X=(t.customer_message.fillna("")+" "+t.agent_notes.fillna("")).values
y=t.category.values
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
vec=FeatureUnion([
 ("word",TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=50000,sublinear_tf=True)),
 ("char",TfidfVectorizer(analyzer="char_wb",ngram_range=(3,5),min_df=2,max_features=50000,sublinear_tf=True))
])
A=vec.fit_transform(Xtr); B=vec.transform(Xte)
clf=LogisticRegression(max_iter=1000,C=3,class_weight="balanced")
clf.fit(A,ytr); pred=clf.predict(B)
print(f"Holdout agreement with historical tags: {accuracy_score(yte,pred):.1%}")
print("Holdout disagreement/error rate: {:.1%}".format(1-accuracy_score(yte,pred)))
print(classification_report(yte,pred,digits=3))
