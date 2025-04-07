import os
import time
from flask import Flask, request, jsonify, send_from_directory
import sklearn.cluster as cluster
import pandas as pd
import baostock as bs
import pandas as pd
import matplotlib.pyplot as plt
import uuid
from datetime import datetime
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans

import tensorflow as tf
print("num GPUs available:", len(tf.config.experimental.list_physical_devices("GPU")))
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense, BatchNormalization, Activation
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib 
matplotlib.use('Agg')  # 关键设置
plt.rcParams['font.sans-serif'] = ['SimHei']  # 或者 ['Arial Unicode MS'] for Mac
plt.rcParams['axes.unicode_minus'] = False
file_path = 'stocks.xls'

app = Flask(__name__)

real_df=None
pred_df =None


# 或者手动添加路由（可选）
@app.route('/api/static/img/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

def save_matplotlib_fig(plt, output_dir, filename_prefix):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:6]  # 生成唯一 ID
    filename = f"{filename_prefix}_{timestamp}_{unique_id}.png"
    output_path = os.path.join(output_dir, filename)
    plt.savefig(output_path)
    return filename  # 返回文件名，用于前端访问

def TopsisDf():
    df = pd.read_excel(file_path)
    df = df.fillna(df.mean(numeric_only=True))
    transformed_df = smart_log_transform(df)

    # 定义需要保留的主键字段
    key_columns = ['code', 'pubDate', 'statDate']
    columns_to_check = transformed_df.columns.difference(key_columns)

    # 数据清洗
    dedup_df = transformed_df.drop_duplicates(subset=columns_to_check, keep='first')
    df['statDate'] = pd.to_datetime(df['statDate'])
    df['pubDate'] = pd.to_datetime(df['pubDate'])
    df['year'] = df['statDate'].dt.year

    cleaned_df = (
        df.sort_values(['code', 'statDate'], ascending=[True, False])
        .groupby(['code', 'year'])
        .head(1)
        .sort_index()
        .drop(columns=['year'])
    )
    df = cleaned_df

    # 定义指标列
    indicators = [
        'currentRatio', 'quickRatio', 'cashRatio', 'YOYLiability', 'liabilityToAsset',
        'assetToEquity', 'YOYEquity', 'INVTurnRatio', 'INVTurnDays', 'CATurnRatio',
        'AssetTurnRatio', 'roeAvg', 'npMargin', 'netProfit', 'epsTTM', 'totalShare', 'liqaShare'
    ]

    # TOPSIS分析
    df_normalized = (df[indicators] - df[indicators].min()) / (df[indicators].max() - df[indicators].min())
    p = df_normalized / df_normalized.sum()
    e = (-1 / np.log(len(df))) * (p * np.log(p)).sum()
    g = 1 - e
    w = g / g.sum()
    weighted_matrix = df_normalized * w
    positive_ideal = weighted_matrix.max()
    negative_ideal = weighted_matrix.min()
    d_plus = np.sqrt(((weighted_matrix - positive_ideal) ** 2).sum(axis=1))
    d_minus = np.sqrt(((weighted_matrix - negative_ideal) ** 2).sum(axis=1))
    closeness = d_minus / (d_plus + d_minus)
    df['相对贴近度'] = closeness
    return df


# 智能对数转换函数
def smart_log_transform(df):
    # 自动识别数值型列
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # 创建数据副本避免修改原始数据
    transformed_df = df.copy()
    
    # 记录转换日志
    transform_log = []
    
    for col in numeric_cols:
        # 计算列均值（自动跳过NaN）
        col_mean = round(transformed_df[col].mean(), 6)
        
        # 判断转换条件
        if col_mean > 1:
            # 处理非正值：将<=0的值替换为列最小正值/2
            min_positive = transformed_df[col][transformed_df[col] > 0].min()
            transformed_df[col] = transformed_df[col].apply(
                lambda x: np.log(x if x > 0 else min_positive/2)
            )
            transform_log.append(f"{col}: 均值{col_mean:.2f} -> 已转换")
        else:
            transform_log.append(f"{col}: 均值{col_mean:.2f} -> 未转换")
    
    # 打印转换日志
    print("列转换日志：")
    print("\n".join(transform_log))
    
    return transformed_df


@app.route('/profit', methods=['POST'])  # 确保路由正确定义
def get_profit_data():
    # 获取请求参数
    data = request.json
    print(data)
    code = data.get('code')
    start_year = int(data.get('startYear'))
    end_year = int(data.get('endYear'))
    # 登录 Baostock
    lg = bs.login()
    if lg.error_code != '0':
        return jsonify({"success": False, "message": "Baostock 登录失败"})

    # 查询盈利能力数据
    profit_list = []
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
            while (rs_profit.error_code == '0') and rs_profit.next():
                profit_list.append(rs_profit.get_row_data())
    print(profit_list)
    # 登出 Baostock
    bs.logout()

    # 转换为 DataFrame
    if not profit_list:
        return jsonify({"success": False, "message": "未找到数据"})

    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    result_profit = result_profit.to_dict(orient='records')

    return jsonify({"success": True, "data": result_profit})


@app.route('/operation', methods=['POST'])  # 修改路由名称为 /operation
def get_operation_data():
    # 获取请求参数
    data = request.json
    print(data)
    code = data.get('code')
    start_year = int(data.get('startYear'))
    end_year = int(data.get('endYear'))

    # 登录 Baostock
    lg = bs.login()
    if lg.error_code != '0':
        return jsonify({"success": False, "message": "Baostock 登录失败"})

    # 查询营运能力数据
    operation_list = []
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            rs_operation = bs.query_operation_data(code=code, year=year, quarter=quarter)
            while (rs_operation.error_code == '0') and rs_operation.next():
                operation_list.append(rs_operation.get_row_data())

    # 登出 Baostock
    bs.logout()

    # 转换为 DataFrame
    if not operation_list:
        return jsonify({"success": False, "message": "未找到数据"})

    result_operation = pd.DataFrame(operation_list, columns=rs_operation.fields)
    result_operation = result_operation.to_dict(orient='records')

    return jsonify({"success": True, "data": result_operation})



@app.route('/growth', methods=['POST'])  # 修改路由名称为 /growth
def get_growth_data():
    # 获取请求参数
    data = request.json
    print(data)
    code = data.get('code')
    start_year = int(data.get('startYear'))
    end_year = int(data.get('endYear'))

    # 登录 Baostock
    lg = bs.login()
    if lg.error_code != '0':
        return jsonify({"success": False, "message": "Baostock 登录失败"})

    # 查询成长能力数据
    growth_list = []
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            rs_growth = bs.query_growth_data(code=code, year=year, quarter=quarter)
            while (rs_growth.error_code == '0') and rs_growth.next():
                growth_list.append(rs_growth.get_row_data())

    # 登出 Baostock
    bs.logout()

    # 转换为 DataFrame
    if not growth_list:
        return jsonify({"success": False, "message": "未找到数据"})

    result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)
    result_growth = result_growth.to_dict(orient='records')

    return jsonify({"success": True, "data": result_growth})


@app.route('/balance', methods=['POST'])  # 修改路由名称为 /growth
def get_balance_data():
    # 获取请求参数
    data = request.json
    print(data)
    code = data.get('code')
    start_year = int(data.get('startYear'))
    end_year = int(data.get('endYear'))

    # 登录 Baostock
    lg = bs.login()
    if lg.error_code != '0':
        return jsonify({"success": False, "message": "Baostock 登录失败"})

    # 查询成长能力数据
    growth_list = []
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            rs_balance= bs.query_balance_data(code=code, year=year, quarter=quarter)
            while (rs_balance.error_code == '0') and rs_balance.next():
                growth_list.append(rs_balance.get_row_data())

    # 登出 Baostock
    bs.logout()

    # 转换为 DataFrame
    if not growth_list:
        return jsonify({"success": False, "message": "未找到数据"})

    result_balance = pd.DataFrame(growth_list, columns=rs_balance.fields)
    result_balance = result_balance.to_dict(orient='records')

    return jsonify({"success": True, "data": result_balance})


@app.route('/origin_data', methods=['POST'])
def origin_data():
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    print(df.head())
    # 将 DataFrame 转换为 JSON 格式
    data = df.to_dict(orient='records')
    print(type(data))
    return jsonify({"success": True, "data": data})

@app.route('/clean_data', methods=['POST'])
def clean_data():
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    df = df.fillna(df.mean(numeric_only=True))
    transformed_df = smart_log_transform(df)
    # 定义需要保留的主键字段
    key_columns = ['code', 'pubDate', 'statDate']

    # 获取需要检查重复的列（所有列排除主键）
    columns_to_check = transformed_df.columns.difference(key_columns)

    # 删除重复数据（保留第一个出现的记录）
    dedup_df = transformed_df.drop_duplicates(
        subset=columns_to_check,
        keep='first'
    )
    # 转换日期列（确保已转换为datetime类型）
    df['statDate'] = pd.to_datetime(df['statDate'])
    df['pubDate'] = pd.to_datetime(df['pubDate'])

    # 提取年份用于分组
    df['year'] = df['statDate'].dt.year

    # 按企业和年份分组，保留最新statDate的记录
    cleaned_df = (
        df.sort_values(['code', 'statDate'], ascending=[True, False])
        .groupby(['code', 'year'])
        .head(1)
        .sort_index()
        .drop(columns=['year'])  # 移除临时年份列
    )
    df = cleaned_df
    # 将 DataFrame 转换为 JSON 格式
    data = df.to_dict(orient='records')
    print(type(data))
    return jsonify({"success": True, "data": data})



os.makedirs('static', exist_ok=True)
@app.route('/AnalysisTopsis', methods=['POST'])
def AnalysisTopsis():
    try:
        # 读取 Excel 文件
        df = TopsisDf()
        # 聚类分析
        mean_closeness_by_stock = df.groupby('code')['相对贴近度'].mean()
        df2 = pd.DataFrame(mean_closeness_by_stock).reset_index()
        df2.columns = ['股票代码', '相对贴近度']

        X = df2[['相对贴近度']].values
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        kmeans.fit(X)
        labels = kmeans.labels_

        centers = kmeans.cluster_centers_.flatten()
        sorted_indices = np.argsort(centers)[::-1]

        label_dict = {
            sorted_indices[0]: "很好",
            sorted_indices[1]: "好",
            sorted_indices[2]: "良好",
            sorted_indices[3]: "差",
            sorted_indices[4]: "很差"
        }

        df2['分类'] = [label_dict[label] for label in labels]
        result = df2.sort_values(by='相对贴近度', ascending=False)

        # 生成图表
        category_counts = df2['分类'].value_counts().reindex(["很好", "好", "良好", "差", "很差"], fill_value=0)
        colors = plt.cm.rainbow(np.linspace(0, 1, 5))[::-1]

        plt.figure(figsize=(12, 6), dpi=100)
        bars = plt.bar(
            category_counts.index,
            category_counts.values,
            color=colors,
            edgecolor='black',
            width=0.7
        )

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2., height,
                     f'{height}',
                     ha='center', va='bottom',
                     fontsize=12,
                     fontweight='bold')

        plt.title('股票评级分布 (n={})'.format(len(df2)), fontsize=14, pad=20)
        plt.xlabel('评级分类', fontsize=12, labelpad=10)
        plt.ylabel('股票数量', fontsize=12, labelpad=10)
        plt.ylim(0, max(category_counts.values) * 1.15)
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.annotate('数据来源：企业财务分析\n生成时间：{}'.format(pd.Timestamp.now().strftime('%Y-%m-%d')),
                     xy=(0.95, 0.05), xycoords='axes fraction',
                     ha='right', va='bottom',
                     fontsize=10,
                     alpha=0.7)

        plt.tight_layout()
        output_dir = 'static/img'  # 图表保存目录
        os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，则创建

        # 保存图表到本地
        feature_importance_path = save_matplotlib_fig(plt, output_dir, 'feature_importance')

        # 准备返回数据
        response_data = {
            "success": True,
            "analysis_result": result.to_dict(orient='records'),
            "chart_url": f"/api/static/img/{feature_importance_path}",  # 前端可以通过这个URL访问图表
            "stats": {
                "total_stocks": len(df2),
                "category_counts": category_counts.to_dict()
            }
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/Model1', methods=['POST'])
def Model1():
    # 1. 读取数据
    df = pd.read_csv("test_df.csv")
    print(df)
    global pred_df
    global real_df
    # 2. 数据预处理
    X = df.drop(columns=['分类', 'pubDate', 'statDate', 'code', 'netProfit', 'liqaShare', 'totalShare'])
    y = df['相对贴近度']

    # 3. 划分训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    y_train_df = pd.DataFrame(data=y_train)

    # 4. 数据标准化
    scaler = RobustScaler()
    scaler2 = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    y_train_scaled = scaler2.fit_transform(y_train_df)

    x_train, x_val, y_train, y_val = train_test_split(x_train_scaled, y_train_scaled, test_size=0.2)

    # 5. 构建模型
    MSE_model = Sequential()
    MSE_model.add(Dense(256, activation='relu', input_dim=len(X.columns)))
    MSE_model.add(Dense(128))
    MSE_model.add(BatchNormalization())
    MSE_model.add(Activation('relu'))
    MSE_model.add(Dense(128))
    MSE_model.add(BatchNormalization())
    MSE_model.add(Activation('relu'))
    MSE_model.add(Dense(128))
    MSE_model.add(BatchNormalization())
    MSE_model.add(Activation('relu'))
    MSE_model.add(Dense(1, activation='linear'))
    MSE_model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_percentage_error'])
    MSE_model.summary()

    # 6. 训练模型
    history = MSE_model.fit(x_train_scaled, y_train_scaled, epochs=400, validation_data=(x_val, y_val), verbose=False)

    # 7. 创建目录保存图片
    output_dir = 'static/img'
    os.makedirs(output_dir, exist_ok=True)  # 如果目录不存在，则创建

    # 8. 保存训练历史图表
    plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Training History')
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.legend(['Training', 'Validation'])
    mse_plot_path = os.path.join(output_dir, 'training_history.png')
    plt.savefig(mse_plot_path)
    plt.close()  # 关闭图表释放内存

    # 9. 预测并计算误差
    pred = scaler2.inverse_transform(MSE_model.predict(scaler.transform(x_test)))
    real = y_test
    pred_df = pd.DataFrame(data=pred)
    real_df = pd.DataFrame(data=real)
    real_df.reset_index(inplace=True)
    real_df.drop(columns=['index'], inplace=True)
    mape = sum(abs(real_df['相对贴近度'] - pred_df[0])) / real_df['相对贴近度'].sum()
    print('The Mean Absolute Percentage Error is:', mape)

    # 10. 保存误差分布直方图
    plt.figure()
    ax = sns.histplot((real_df['相对贴近度'] - pred_df[0]) / real_df['相对贴近度'] * 100, kde=True)
    ax.lines[0].set_color('crimson')
    plt.title('Histogram of 相对贴近度 Predictions')
    plt.xlabel('Mean Percentage Error (%)')
    histogram_path = os.path.join(output_dir, 'error_histogram.png')
    plt.savefig(histogram_path)
    plt.close()  # 关闭图表释放内存
    # 检查特征列是否重复（重要！）
    features = [
        '相对贴近度',
        'currentRatio',
        'quickRatio',
        'cashRatio',
        'YOYLiability',  # 这里原代码重复了两次，已修正
        'liabilityToAsset'  # 假设这是正确的特征名
    ]

    # 初始化模型（添加n_init=10）
    kmeans = cluster.KMeans(
        n_clusters=18,
        init='k-means++',
        n_init=10  # 显式设置初始化次数
    )

    # 训练模型（只需执行一次）
    kmeans.fit(df[features])

    # 保存聚类结果
    df['cluster_label'] = kmeans.labels_
    df.to_csv('test_df.csv',sep=',',index=False,header=True)
    # 11. 返回结果给前端
    response_data = {
        "success": True,
        "mape": mape,
        "mse_plot_path": f"/api/static/img/training_history.png",  # 前端访问路径
        "histogram_path": f"/api/static/img/error_histogram.png",  # 前端访问路径
    }
    return jsonify(response_data)


@app.route('/Model2', methods=['POST'])
def Model2():
    # 设置非交互式后端
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns

    try:
        # 1. 数据准备
        df = pd.read_csv("test_df.csv")
        print(df)

        # 2. 数据预处理
        X = df.drop(columns=['分类', 'pubDate', 'statDate', 'code', 'netProfit', 'liqaShare', 'totalShare'])
        y = df['相对贴近度']

        # 3. 划分数据集
        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        y_train_df = pd.DataFrame(data=y_train)

        # 4. 数据标准化
        scaler = RobustScaler()
        scaler2 = StandardScaler()
        x_train_scaled = scaler.fit_transform(x_train)
        y_train_scaled = scaler2.fit_transform(y_train_df)
        x_train, x_val, y_train, y_val = train_test_split(x_train_scaled, y_train_scaled, test_size=0.2)

        # 5. 创建图片保存目录
        output_dir = 'static/img/model2'
        os.makedirs(output_dir, exist_ok=True)

        # 6. 构建并训练模型
        MSE_model2 = Sequential()
        MSE_model2.add(Dense(256, activation='relu', input_dim=len(X.columns)))
        MSE_model2.add(Dense(128))
        MSE_model2.add(BatchNormalization())
        MSE_model2.add(Activation('relu'))
        MSE_model2.add(Dense(128))
        MSE_model2.add(Activation('relu'))
        MSE_model2.add(Dense(128))
        MSE_model2.add(BatchNormalization())
        MSE_model2.add(Activation('relu'))
        MSE_model2.add(Dense(1, activation='linear'))
        MSE_model2.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_percentage_error'])

        history = MSE_model2.fit(x_train_scaled, y_train_scaled, epochs=400,
                                 validation_data=(x_val, y_val), verbose=False)

        # 7. 保存训练历史图表
        plt.figure(figsize=(10, 6))
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model2 Training History')
        plt.xlabel('Epoch')
        plt.ylabel('MSE')
        plt.legend(['Training', 'Validation'])
        training_history_path = os.path.join(output_dir, 'model2_training_history.png')
        plt.savefig(training_history_path)
        plt.close()

        # 8. 模型预测和评估
        pred2 = scaler2.inverse_transform(MSE_model2.predict(scaler.transform(x_test)))
        real2 = y_test
        pred_df2 = pd.DataFrame(data=pred2)
        real_df2 = pd.DataFrame(data=real2)
        real_df2.reset_index(inplace=True)
        real_df2.drop(columns=['index'], inplace=True)

        # 计算MAPE
        mape = sum(abs(real_df2['相对贴近度'] - pred_df2[0])) / real_df2['相对贴近度'].sum()
        print('The Mean Absolute Percentage Error When Trained with Cluster Labels is:', mape)

        # 9. 确保 global real_df 和 pred_df 已定义
        global real_df, pred_df
        if 'real_df' not in globals() or 'pred_df' not in globals():
            # 如果没有之前的模型结果，使用当前模型结果作为对比
            real_df = real_df2.copy()
            pred_df = pred_df2.copy()

        # 10. 保存误差分布对比图
        plt.figure(figsize=(10, 6))
        df1 = pd.DataFrame(data=(real_df['相对贴近度'] - pred_df[0]) / real_df['相对贴近度'] * 100)
        df2 = pd.DataFrame((real_df2['相对贴近度'] - pred_df2[0]) / real_df2['相对贴近度'] * 100)
        df1['label'] = 'Original Model'
        df2['label'] = 'Trained on Clustered Data'
        df_frames = pd.concat([df1, df2], ignore_index=True)

        sns.kdeplot(data=df_frames, x=0, hue='label')
        plt.title('Comparison of Prediction Errors')
        plt.xlabel('Mean Percentage Error (%)')
        error_comparison_path = os.path.join(output_dir, 'model2_error_comparison.png')
        plt.savefig(error_comparison_path)
        plt.close()

        # 11. 更新全局变量以便下次比较
        real_df = real_df2
        pred_df = pred_df2

        # 12. 返回结果
        response_data = {
            "success": True,
            "mape": float(mape),
            "training_history_path": f"/api/static/img/model2/model2_training_history.png",
            "error_comparison_path": f"/api/static/img/model2/model2_error_comparison.png"
        }
        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)