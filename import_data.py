import csv
import os

import django

# 设置 Django 配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tkc_project.settings')



# 初始化 Django
django.setup()

# 此时应该能够导入 hobby_clubs 模块
from hobby_clubs.models import Club

def import_clubs_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # 检查 'Unique Identifier' 是否存在，如果不存在，则跳过该行
            unique_identifier = row.get('unique_identifier', None)
            if unique_identifier is None:
                continue
            
            # 使用 unique_identifier 和其他值创建俱乐部对象
            club = Club(
                club_name=row['Club_Name'],
                postal_code=row['Postal_Code'],
                address=row['Address'],
                age=int(row['Age']),
                category=row['Category'],
                activity=row['Activity'],
                website=row['Website'],
                unique_identifier=row['unique_identifier']  # 添加唯一标识符字段
            )
            club.save()

if __name__ == "__main__":
    # 传入 CSV 文件的相对路径
    import_clubs_from_csv('databasestore/clubs-info.csv')

