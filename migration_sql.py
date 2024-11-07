import os
import django
from django.core.management import call_command
from io import StringIO

# 设置 Django 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

# 初始化 Django
django.setup()

if __name__ == '__main__':
    with open('init.sql', 'w', encoding='utf-8') as file:
        migration_plan = StringIO()
        call_command('showmigrations', '--plan', stdout=migration_plan)
        migration_plan.seek(0)
        for line in migration_plan:
            try:
                app_label, migration_name = line.split()[1].split(".")
                sql_output = StringIO()
                call_command('sqlmigrate', app_label, migration_name.split("_")[0], stdout=sql_output)
                sql_output.seek(0)
                file.write(sql_output.read())
            except Exception as e:
                print(f"Error processing {app_label}: {line}")
