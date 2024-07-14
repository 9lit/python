from docxtpl import DocxTemplate
import pandas as pd

from docx import Document
from docxcompose.composer import Composer

import os

def merge_docx(input_file, out_file, index, lenght):
    """合并文档"""
    global master
    # 读取文件
    sub = Document(input_file)
    # 添加分页符
    sub.add_page_break()

    if index == 0 : master = Composer(sub) # 添加基底文件
    else: master.append(sub) # 合并 word 文档
 
    if index+1 == lenght: master.save(out_file)


def del_file(out_path):
    """删除合并后的文件"""
    all_file = os.listdir(out_path)
    if not all_file: exit()
    for f in all_file: os.remove(f'{out_path}/{f}')


def read_xlsx(path):

    global cps, cjhs, fdjs
    data = pd.read_excel(path, sheet_name=0)
    stu_df = pd.DataFrame(data)
    cps =stu_df['车牌号'].values # 获取当前列的全部数据
    # cjhs =stu_df['车架号'].values
    # fdjs =stu_df['发动机号'].values


def write_docx(index, input_file, filename, outpath, context):
    """将 xlsx 文件的数据写入 docx 文档"""
    global outfile, tpl
    if index == 0: tpl = DocxTemplate(input_file) # 第一次循环时 写入调用
    
    tpl.render(context)
    outfile = f"{outpath}/{filename}.docx"
    tpl.save(outfile)


def exists():

    if not ( os.path.exists(input_docx) and os.path.exists(input_xlsx) ):
        exit("输入文件不存在, 检查 docx 和 xlsx 文件是否存在")

    else:

        if os.path.splitext(input_docx)[-1] != "docx":
            exit("输入的 word 文件格式不正确, 检查扩展名是否为 docx")

        if os.path.splitext(input_xlsx)[-1] != "xlsx":
            exit("输入的 excel 文件格式不正确, 检查扩展名是否为 xlsx")

    if not os.path.exists(out_path): os.makedirs(out_path)


if __name__ == "__main__":
    
    input_docx = 'input.docx'; input_xlsx = 'input.xlsx'
    out_docx = 'out.docx'; out_path = 'word'

    exists(); read_xlsx(input_xlsx)

    for index, cp in enumerate(cps):
        context = {
            'cph': cp,
            # 'fdj': fdjs[index],
            # 'cjh': cjhs[index]
        }

        write_docx(index, input_docx, cp, out_path, context); merge_docx(outfile, out_docx, index, len(cps))

    del_file(out_path)










