import pandas as pd
import numpy as np
import itertools
import requests
import ortools
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
dt_gx = pd.read_excel('广西.xlsx', dtype={'门店编号':str})

import pymysql
config = {
    'host': '192.168.1.227',
    'port': 4000,
    'user': 'liyufan',
    'passwd': 'Juno#2021',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor
    }
conn = pymysql.connect(**config)

# 创建距离，线路dict
distance_dict = {}
route_dict = {}
# 遍历key value的值
for key, value in dt_gx.items():
    temp_df = value
    store_info = pd.read_sql("select storeCode,mapX, mapY from xsyx_frxs_base.t_store where storeCode in " + str(
        tuple(temp_df['门店编号'].values.tolist())), conn)
    temp_df['lat'] = store_info['mapY']
    temp_df['lng'] = store_info['mapX']

    # 提取门店信息和经纬度
    st_df = temp_df[['门店编号', 'lng', 'lat']].copy()

    # 去除无经纬度的门店
    if st_df['lng'].isnull().any():
        continue

    # 添加仓库地址
    st_df.loc[-1] = ['0', 114.606, 37.9361]  # adding a row
    st_df.index = st_df.index + 1  # shifting index
    st_df.sort_index(inplace=True)
    # value to list for use itertools.combination
    lnglat = st_df.values.tolist()
    dist_combination = list(itertools.combinations(lnglat, 2))

    # 路径编码排序 for storage in database
    reordered_list = []
    for i in dist_combination:
        temp_list = []
        index = ''
        if str(i[0][0]) > str(i[1][0]):
            index = str(i[1][0]) + '-' + str(i[0][0])
            temp_list.extend(i[1] + i[0])
        else:
            index = str(i[0][0]) + '-' + str(i[1][0])
            temp_list.extend(i[0] + i[1])
        temp_list.append(index)
        reordered_list.append(temp_list)

    # apply 排序函数to dataframe
    cal_combination_df = pd.DataFrame(data=reordered_list,
                                      columns=['village_code_0', 'lon0', 'lat0', 'village_code_1', 'lon1', 'lat1',
                                               'village_distance_index'])
    # 将编码转成string
    cal_combination_df['village_code_0'] = cal_combination_df['village_code_0'].astype(str)
    cal_combination_df['village_code_1'] = cal_combination_df['village_code_1'].astype(str)
    # 高德API调导航距离
    cal_combination_df_return = sub_task(cal_combination_df)
    # 将导航距离转成integer
    cal_combination_df_return['navi_distance'] = cal_combination_df_return.apply(lambda df: int(df['navi_distance']),
                                                                                 axis=1)

    # 调用google or tools
    d, r = get_route_total_distance(st_df, cal_combination_df_return)
    #
    distance_dict[key] = d
    route_dict[key] = r

distance_df = pd.DataFrame.from_records(distance_dict, index=[0])
route_df = pd.DataFrame.from_records(route_dict, index=[0])
final_result = pd.concat([distance_df, route_df], ignore_index=True)




