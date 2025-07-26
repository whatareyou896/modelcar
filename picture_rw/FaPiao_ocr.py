import json
from loguru import logger
import re
import api_doc_demo
'''
def FaPiao_ocr_main(url_json):
    """
    将 ocr 识别的 json 文件进行 收集所需内容输出
    双方识别号以及各类数据
    :param url_json:
    :return:
    """
    with open(
            r"../../download\[OCR]_dzfp_25442000000412007143_陈海铨_20250709104906.jsonl",
            'r', encoding='utf-8') as f:
        data = json.loads(f.read())

    items = data['data']

    result = {
        "buyer_name": None,
        "buyer_tax_id": None,
        "seller_name": None,
        "seller_tax_id": None,
        "amount": None,
        "tax_amount": None,
        "total_amount": None,
        "remark_code": None
    }

    for idx, item in enumerate(items):
        text = item.get('text', '')
        # 购买方
        if text == '名称：' and idx + 1 < len(items):
            if not result["buyer_name"]:
                result["buyer_name"] = items[idx + 1]['text']
            elif '东莞市长安瞳瞳电动自行车店' in items[idx + 1]['text']:
                result["seller_name"] = items[idx + 1]['text']
        if text.startswith('统一社会信用代码') or text.startswith('纳税人识别号'):
            if idx + 1 < len(items):
                code = items[idx + 1]['text']
                if code.startswith('92'):
                    result["seller_tax_id"] = code
                else:
                    result["buyer_tax_id"] = code
        # 金额
        if item['text'].replace(' ', '') == '金额' and idx + 1 < len(items):
            result["amount"] = items[idx + 1]['text']
        # 税额
        if item['text'].replace(' ', '') == '税额' and idx + 1 < len(items):
            result["tax_amount"] = items[idx + 1]['text']
        # 价税合计（大写）对应的阿拉伯数字
        if '价税合计（大写' in item['text']:
            # 查找后面带¥的金额
            for j in range(idx + 1, idx + 5):
                if j < len(items) and '¥' in items[j]['text']:
                    result["total_amount"] = items[j]['text'].replace('¥', '')
                    break
        # 备注区数字串
        if item['text'] in ['注', '备注']:
            for j in range(idx + 1, min(idx + 5, len(items))):
                t = items[j]['text']
                if t.isdigit():
                    result["remark_code"] = t
                    break
        if item['text'].isdigit() and len(item['text']) > 10:
            result["remark_code"] = item['text']
    logger.info(result)
    return result
    '''
def remark_code(url_json,name):
    with open(
            #r'd:\software\python\envs\py38\script\download\[OCR]_dzfp_25442000000412019647_李春莲_20250709105155.jsonl',
            url_json,
            'r', encoding='utf-8') as f:
        obj = json.loads(f.read())

    remark_code = None
    for item in obj['data']:
        match = re.fullmatch(r'\d{15}', item['text'])
        if match:
            remark_code = match.group()
            break
    name_split = name.split("_")
    bianhao = {"整车编码":remark_code,
               "发票号码":name_split[2]}
    logger.info(bianhao)
    return bianhao
url_josn,name = api_doc_demo.api_doc_demo_main(0)

remark_code(url_josn,name)