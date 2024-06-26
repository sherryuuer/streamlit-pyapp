import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve

# 创建 Streamlit 应用程序界面
st.title('Confusion Matrix Visualization')

# 用户输入 TP、FP、TN、FN
tp = st.number_input('Enter True Positive (TP):', value=85)
fp = st.number_input('Enter False Positive (FP):', value=5)
fn = st.number_input('Enter False Negative (FN):', value=5)
tn = st.number_input('Enter True Negative (TN):', value=5)

# 构建混淆矩阵
conf_matrix = np.array([[tp, fp], [fn, tn]])

# 可视化混淆矩阵
st.write('Confusion Matrix:')
st.write(conf_matrix)

# 绘制热图
fig, ax = plt.subplots()
fig.set_figwidth(8)
fig.set_figheight(6)
sns.heatmap(
    conf_matrix,
    annot=True,
    cmap='Blues',
    fmt='g',
    cbar=False,
    square=True,
    ax=ax
)
ax.set_xlabel('Predicted Label')
ax.set_ylabel('True Label')
ax.set_title('Confusion Matrix')
ax.set_xticks([0.5, 1.5])
ax.set_xticklabels(['Negative', 'Positive'])
ax.set_yticks([0.5, 1.5])
ax.set_yticklabels(['Negative', 'Positive'])
st.pyplot(fig)

# 计算评估指标
true_positive = conf_matrix[0][0]
false_positive = conf_matrix[0][1]
false_negative = conf_matrix[1][0]
true_negative = conf_matrix[1][1]

accuracy = (true_positive + true_negative) / np.sum(conf_matrix)
precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
f1_score = 2 * (precision * recall) / (precision + recall)

# 显示评估指标
st.write('Accuracy:', accuracy)
st.write('Precision:', precision)
st.write('Recall:', recall)
st.write('F1 Score:', f1_score)

# 计算 ROC 曲线和 AUC
y_true = np.array([1] * true_positive + [0] * false_positive)
y_score = np.concatenate(
    [np.random.rand(true_positive), np.random.rand(false_positive)])
fpr, tpr, _ = roc_curve(y_true, y_score)
roc_auc = auc(fpr, tpr)

# 绘制 ROC 曲线
fig, ax = plt.subplots()
fig.set_figwidth(8)
fig.set_figheight(6)
ax.plot(fpr, tpr, color='darkorange', lw=2,
        label='ROC curve (area = %0.2f)' % roc_auc)
ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.set_title('Receiver Operating Characteristic (ROC)')
ax.legend(loc="lower right")
ax.grid(True)

st.pyplot(fig)

# 计算 PR 曲线和 AUC
precision, recall, _ = precision_recall_curve(y_true, y_score)
pr_auc = auc(recall, precision)

# 绘制 PR 曲线
fig, ax = plt.subplots()
fig.set_figwidth(8)
fig.set_figheight(6)
ax.plot(recall, precision, color='blue', lw=2,
        label='Precision-Recall curve (area = %0.2f)' % pr_auc)
ax.set_xlabel('Recall')
ax.set_ylabel('Precision')
ax.set_title('Precision-Recall Curve')
ax.legend(loc="lower left")
ax.grid(True)

st.pyplot(fig)
