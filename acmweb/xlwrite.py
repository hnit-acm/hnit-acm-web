# coding:utf-8
"""获取excel文件流"""
import pandas as pd
from io import BytesIO


def get_registerInfo(users):
    sheet = []
    for user in users:
        rows = [user.name, user.student_num, user.major, user.classes,
                user.phone_num, user.qq_num, user.group, user.reg_time]
        sheet.append(rows)
    columns = ['姓名', '学号', '专业', '班级', '电话', 'QQ', '组别', '报名时间']
    data = pd.DataFrame(data=sheet, columns=columns)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Sheet1', index=False)
    output.seek(0)
    return output
