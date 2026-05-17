import pandas as pd
import psycopg

# 读取数据
df = pd.read_csv("data.csv")

# 处理数据
result = df.groupby("date")["sales"].sum().reset_index()

# 显示结果
print(result)

# 连接数据库
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="222222"
)

cur = conn.cursor()

# 创建表
cur.execute("""
    CREATE TABLE IF NOT EXISTS sales_summary (
        date DATE PRIMARY KEY,
        sales INTEGER
    )
""")

# 清空旧数据
cur.execute("DELETE FROM sales_summary")

# 插入新数据
for _, row in result.iterrows():
    cur.execute(
        "INSERT INTO sales_summary (date, sales) VALUES (%s, %s)",
        (row["date"], row["sales"])
    )

conn.commit()
cur.close()
conn.close()

print("写入数据库成功！")