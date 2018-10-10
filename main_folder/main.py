import numpy as np
from config_folder import config
import csv
import os
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']

def load_data(data_file,usecols):
   """
   :param data_file: 读取的文件的路径
   :param usecols: 需要取的列
   :return: data_arr:  数据的多维数组,形式[[2013    3  117  166  140]]
   """
   data = []
   # === 读取数据 ===
   with open(data_file,'r') as csvfile:
       data_reader = csv.DictReader(csvfile)

       # === 数据处理 ===
       for row in data_reader:
           #取出每行数据，组合为一个列表放入数据列表中
           row_data = []
           # 注意csv模块读入的数据全部为字符串类型
           for col in usecols:
               str_val = row[col]
               #数据类型转换为float，如果是'NA'，则返回nan
               row_data.append(float(str_val) if str_val !='NA' else np.nan)
           #如果数据中不包含nan才保存改行记录
           if not any(np.isnan(row_data)):
               data.append(row_data)
   #将data转换为ndarray
   data_arr = np.array(data).astype(int)
   return data_arr

def get_polluted_perc(data_arr):
    """
    获取污染占比小时数
    规则：
            重度污染(heavy)     PM2.5 > 150
            中度污染(medium)    75 < PM2.5 <= 150
            轻度污染(light)     35 < PM2.5 <= 75
            优良空气(good)      PM2.5 <= 35
    :param data_arr:  数据的多维数组,形式[[2013    3  117  166  140]]
    :return: polluted_perc_list: 污染小时数百分比列表
    """
    # 将每个区的PM值平均后作为该城市小时的PM值
    # 按行取平均值
    hour_val = np.mean(data_arr[:,2:-1],axis=1)
    # us_hour_val = data_arr[:,-1]
    # 总小时数
    n_hours = hour_val.shape[0]
    # usn_hours = us_hour_val.shape[0]
    # 重度污染小时数
    n_heavy_hours = hour_val[hour_val > 150].shape[0]
    # usn_heavy_hours = us_hour_val[us_hour_val > 150].shape[0]
    # print(usn_heavy_hours / usn_hours)
    # 中度污染小时数
    n_medium_hours = hour_val[(hour_val > 75)&(hour_val <= 150)].shape[0]
    # 轻度污染小时数
    n_light_hours = hour_val[(hour_val > 35) & (hour_val <= 75)].shape[0]
    # 优良空气小时数
    n_good_hours = hour_val[hour_val <= 35].shape[0]
    polluted_prc_list = [n_heavy_hours / n_hours, n_medium_hours/ n_hours, n_light_hours / n_hours, n_good_hours / n_hours]
    return polluted_prc_list


def get_us_polluted_perc(data_arr):
    """
    获取污染占比小时数
    规则：
            重度污染(heavy)     PM2.5 > 150
            中度污染(medium)    75 < PM2.5 <= 150
            轻度污染(light)     35 < PM2.5 <= 75
            优良空气(good)      PM2.5 <= 35
    :param data_arr: 数据的多维数组,形式[[2013    3  117  166  140]]
    :return: us_polluted_perc_list:污染小时数百分比列表
    """
    # 取到us给出的数据
    us_hours = data_arr[:,-1]

    # 取到总小时数
    usn_hours = us_hours.shape[0]

    # 重度污染小时数
    usn_heavy_hours = us_hours[us_hours > 150].shape[0]

    # 中度污染小时数
    usn_medium_hours = us_hours[(us_hours > 75) & (us_hours <= 150)].shape[0]

    # 轻度污染小时数
    usn_light_hours = us_hours[(us_hours > 35) & (us_hours <= 75)].shape[0]

    # 优良空气小时数
    usn_good_hours = us_hours[us_hours <= 35].shape[0]
    us_polluted_perc_list = [usn_heavy_hours / usn_hours, usn_medium_hours / usn_hours, usn_light_hours / usn_hours, usn_good_hours / usn_hours]
    return us_polluted_perc_list

def get_avg_pm_per_month(data_arr):
    """
    获取每个区每月的平均PM值
    :param data_arr: 数据的数组表示
    :return: results_arr: 多维数组结果
    """
    results = []
    # 获取年份
    years = np.unique(data_arr[:, 0])
    for year in years:
        # 获取当前年份数据
        year_data_arr = data_arr[data_arr[:,0] == year]
        # 获取数据的月份
        month_list = np.unique(year_data_arr[:, 1])

        for month in month_list:
            # 获取月份的所有数据
            month_data_arr = year_data_arr[year_data_arr[:, 1] == month]
            # 计算当前月份PM的均值,并转换为列表
            mean_vals = np.mean(month_data_arr[:, 2:-1],axis=0).tolist()

            # 格式化字符串
            row_data = ['{:.0f}-{:02.0f}'.format(year, month)] + mean_vals
            results.append(row_data)
    results_arr = np.array(results)
    return results_arr


def save_stats_to_csv(results_arr, save_file, headers):
    """
    将统计结果保存至csv文件中
    :param results_arr: 多维数组结果
    :param save_file: 文件保存路径
    :param headers: csv表头
    :return:
    """
    with open(save_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in results_arr.tolist():
            writer.writerow(row)

def draw_hist(polluted_perc_list,us_polluted_perc_list,city_name):
    plt.figure()
    labels = ['重度污染','中度污染','轻度污染','优良空气']
    explode = [0.05,0,0,0]
    colors = ['#FF0000', 'orange', '#0099CC', 'lime']
    plt.subplot(121)
    plt.pie(polluted_perc_list,explode=explode,colors=colors,labels=labels,autopct='%1.1f%%',shadow=True,labeldistance=1.1,pctdistance=0.6)
    plt.title(city_name + '污染情况,数据来自中国')
    plt.axis('equal')
    plt.subplot(122)
    plt.pie(us_polluted_perc_list, explode=explode, colors=colors,labels=labels, autopct='%1.1f%%', shadow=True, labeldistance=1.1,pctdistance=0.6)
    plt.title(city_name + '污染情况,数据来自美国')
    plt.axis('equal')
    plt.legend()
    plt.show()


def main():
    """
        主函数
    """
    polluted_state_list = []

    for city_name,(filename, cols) in config.data_config_dict.items():
        #  Step 1+2 数据获取 + 数据处理
        data_file = os.path.join(config.dataset_path, filename)
        usecols = config.common_cols + [col for col in cols]
        data_arr = load_data(data_file, usecols)

        # print('{}共有{}行有效数据'.format(city_name, data_arr.shape[0]))
        # # 预览前10行数据
        # print('{}的前10行数据：'.format(city_name))
        # print(data_arr[:10])
        #
        # # === Step 3. 数据分析 ===
        # # 五城市的污染状态，统计污染小时数的占比
        polluted_perc_list = get_polluted_perc(data_arr)
        # polluted_state_list.append([city_name] + polluted_perc_list)
        # print('{}的污染小时数百分比{}'.format(city_name, polluted_perc_list))
        #
        # # 五城市每个区空气质量的月度差异，分析计算每个月，每个区的平均PM值
        # results_arr = get_avg_pm_per_month(data_arr)
        # print('{}的每月平均PM值预览：'.format(city_name))
        # print(results_arr[:10])
        # === Step 4. 结果展示 ===
        # 4.1 保存月度统计结果至csv文件
        # save_filename = city_name + '_month_stats.csv'
        # save_file = os.path.join(config.output_path, save_filename)
        # save_stats_to_csv(results_arr, save_file, headers=['month'] + cols)
        # print('月度统计结果已保存至{}'.format(save_file))
        # print()
    # 4.2 污染状态结果保存
    # save_file = os.path.join(config.output_path, 'polluted_percentage.csv')
    # with open(save_file, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['city', 'heavy', 'medium', 'light', 'good'])
    #     for row in polluted_state_list:
    #         writer.writerow(row)
    # print('污染状态结果已保存至{}'.format(save_file))
        us_polluted_perc_list = get_us_polluted_perc(data_arr)
        draw_hist(polluted_perc_list, us_polluted_perc_list, city_name)
if __name__ == '__main__':
    main()
