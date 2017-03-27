# -*- coding: utf-8 -*-

import csv #此模块用来处理CSV类型文件

#数据源
data_path = '/survey.csv'


def run_main():
    male_set = {'male', 'm'}  # “男性”可能的取值
    female_set = {'female', 'f'}  # “女性”可能的取值
    #结果存放字典
    result_dict = {}

    #打开源数据文件
    with open(data_path, 'r', newline='') as csvfile:
        # 加载数据
        rows = csv.reader(csvfile)
        for i, row in enumerate(rows):
            if i == 0:
                # 跳过第一行表头数据
                continue

            if i % 50 == 0:
                print('正在处理第{}行数据...'.format(i))
            # 性别数据
            gender_val = row[2]
            country_val = row[3]

            # 去掉可能存在的空格
            gender_val = gender_val.replace(' ', '')
            # 转换为小写
            gender_val = gender_val.lower()

            # 判断“国家”是否已经存在
            if country_val not in result_dict:
                # 如果不存在，将其加入结果字典
                result_dict[country_val] = [0, 0]

            # 如果性别为女性
            if gender_val in female_set:
                #就将对应值加一
                result_dict[country_val][0] += 1
                # 如果性别为男性
            elif gender_val in male_set:
                #就将对应值加一
                result_dict[country_val][1] += 1
            else:
                # 不男不女的就pass掉
                pass

    # 将结果写入文件
    with open('/gender_country.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        # 写入表头
        csvwriter.writerow(['国家', '男性', '女性'])

        # 写入统计结果
        for k, v in list(result_dict.items()):
            csvwriter.writerow([k, v[0], v[1]])

if __name__ == '__main__':
    run_main()
