import csv
import random

# 打开原始的 CSV 文件和目标 CSV 文件
with open('databasestore/clubs-info.csv', 'r', encoding='utf-8') as source_file, \
     open('databasestore/clubs-info-updated.csv', 'w', newline='', encoding='utf-8') as target_file:

    # 创建 CSV 读写对象
    reader = csv.reader(source_file)
    writer = csv.writer(target_file)

    # 处理每一行数据
    for index, row in enumerate(reader):
        if index == 0:
            # 写入标题行并添加新的列名
            writer.writerow(['unique_identifier'] + row)
        else:
            # 生成随机的三位数作为唯一标识符
            unique_identifier = random.randint(100, 999)
            # 将唯一标识符添加到行的开头
            writer.writerow([unique_identifier] + row)

