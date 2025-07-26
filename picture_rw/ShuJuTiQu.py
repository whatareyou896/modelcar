from bs4 import BeautifulSoup
import re
import json
def extract_ebike_data(html_content):
    """
    从HTML内容中提取电动自行车合格证数据
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    data = {}

    # 查找所有包含数据的表格行
    rows = soup.select('div#r1 table tr')

    # 提取特定编号的数据
    target_ids = ['0.0','0.3' ,'0.4','0.6','0.14',  '0.17.1',  '0.19']

    for row in rows:
        # 获取行中的单元格
        cells = row.find_all('td')
        if len(cells) < 3:
            continue

        # 获取编号
        row_id = cells[0].get_text(strip=True)

        # 检查是否为目标编号
        if row_id in target_ids:
            # 获取字段名称
            field_name = cells[1].get_text(strip=True).replace('：', '')
            # 获取字段值
            field_value = cells[2].get_text(strip=True)

            # 添加到结果字典
            data[field_name] = field_value

    # 提取其他关键信息
    additional_data = {
        #'申请人': extract_value(soup, '申请人'),
        '制造商': extract_value(soup, '制造商'),
        '生产厂': extract_value(soup, '生产厂'),
        '产品合格证证书编号': extract_value(soup, '产品合格证证书编号'),
        'CCC证书编号': extract_value(soup, 'CCC证书编号'),
        #'车辆制造日期': extract_value(soup, '车辆制造日期'),
    }

    # 合并数据
    result = {**data, **additional_data}

    return result


def extract_value(soup, field_name):
    """
    根据字段名称提取值
    """
    # 查找包含字段名称的单元格
    td = soup.find('td', class_='biaotifontblue', string=re.compile(field_name))
    if td:
        # 找到同一行的下一个单元格
        next_td = td.find_next_sibling('td')
        if next_td:
            return next_td.get_text(strip=True)
    return None
def ShuJutiTiQu_main():
    with open('result.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # 提取数据
    ebike_data = extract_ebike_data(html_content)

    # 打印提取结果
    print("=" * 50)
    print("电动自行车合格证数据提取结果")
    print("=" * 50)
    for key, value in ebike_data.items():
        print(f"{key}: {value}")
    print(ebike_data)
    return ebike_data
# 示例使用
if __name__ == "__main__":
    # 读取HTML文件内容
    ebike_data = ShuJutiTiQu_main()
    # 保存到JSON文件
    with open('ebike_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(ebike_data, json_file, ensure_ascii=False, indent=2)
    print("\n数据已保存到 ebike_data.json")