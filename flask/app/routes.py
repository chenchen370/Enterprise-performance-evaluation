from flask import Blueprint, jsonify, request
from flask import Flask, request, jsonify
import pandas as pd
import baostock as bs
from flask_cors import CORS  # 导入 CORS
app = Flask(__name__)
CORS(app)  # 启用 CORS 支持
# 创建蓝图
api_bp = Blueprint('api', __name__)

# 示例：GET 请求
@api_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

# 示例：POST 请求
@api_bp.route('/echo', methods=['POST'])
def echo():
    data = request.json  # 获取 JSON 数据
    return jsonify({"received": data})


@app.route('/profit', methods=['POST'])
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

    # 登出 Baostock
    bs.logout()

    # 转换为 DataFrame
    if not profit_list:
        return jsonify({"success": False, "message": "未找到数据"})

    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    result_profit = result_profit.to_dict(orient='records')

    return jsonify({"success": True, "data": result_profit})