import baostock as bs
import pandas as pd

# 登录 Baostock 系统
lg = bs.login()
if lg.error_code != '0':
    print("Baostock 登录失败")
    exit()


# 定义时间范围
start_year = 2010
end_year = 2024

# 存储所有股票的数据
all_profit_data = []

# 遍历每个股票代码

for year in range(start_year, end_year + 1):
    for quarter in [1, 2, 3, 4]:  # 遍历每个季度
        # 查询季频盈利能力数据
        rs_balance = bs.query_operation_data("sh.600117", year=year, quarter=quarter)
        while (rs_balance.error_code == '0') & rs_balance.next():
            profit_data = rs_balance.get_row_data()
            all_profit_data.append(profit_data)  # 将数据添加到总列表中

# 将结果转换为 DataFrame
columns = rs_balance.fields  # 获取字段名称
result_df = pd.DataFrame(all_profit_data, columns=columns)

# 保存结果到 CSV 文件
output_file = 'all_test_balance_data.csv'
result_df.to_csv(output_file, encoding="gbk", index=False)
print(f"数据已保存到 {output_file}")

# 登出 Baostock 系统
bs.logout()