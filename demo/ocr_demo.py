import json
import os

from loguru import logger
from pathlib import Path

from demo.demo_test import get_json_from_local_or_s3
from magic_pdf.dict2md.ocr_mkcontent import ocr_mk_mm_markdown_with_para, ocr_mk_nlp_markdown, ocr_mk_mm_markdown, ocr_mk_mm_standard_format
from magic_pdf.libs.commons import join_path
from magic_pdf.pdf_parse_by_ocr import parse_pdf_by_ocr


def save_markdown(markdown_text, input_filepath):
    # 获取输入文件的目录
    directory = os.path.dirname(input_filepath)
    # 获取输入文件的文件名（不带扩展名）
    base_name = os.path.basename(input_filepath)
    file_name_without_ext = os.path.splitext(base_name)[0]
    # 定义输出文件的路径
    output_filepath = os.path.join(directory, f"{file_name_without_ext}.md")

    # 将Markdown文本写入.md文件
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(markdown_text)


def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def ocr_local_parse(ocr_pdf_path, ocr_json_file_path):
    try:
        ocr_pdf_model_info = read_json_file(ocr_json_file_path)
        pth = Path(ocr_json_file_path)
        book_name = pth.name
        save_tmp_path = os.path.join(os.path.dirname(__file__), "../..", "tmp", "unittest")
        save_path = join_path(save_tmp_path, "md")
        save_path_with_bookname = os.path.join(save_path, book_name)
        text_content_save_path = f"{save_path_with_bookname}/book.md"
        pdf_info_dict = parse_pdf_by_ocr(
            ocr_pdf_path,
            None,
            ocr_pdf_model_info,
            save_path,
            book_name,
            debug_mode=True)

        parent_dir = os.path.dirname(text_content_save_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # markdown_content = mk_nlp_markdown(pdf_info_dict)
        markdown_content = ocr_mk_mm_markdown_with_para(pdf_info_dict)

        with open(text_content_save_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        standard_format = ocr_mk_mm_standard_format(pdf_info_dict)
        standard_format_save_path = f"{save_path_with_bookname}/standard_format.txt"
        with open(standard_format_save_path, "w", encoding="utf-8") as f:
            f.write(str(standard_format))

        # logger.info(markdown_content)
        # save_markdown(markdown_text, ocr_json_file_path)
    except Exception as e:
        logger.exception(e)


def ocr_online_parse(book_name, start_page_id=0, debug_mode=True):
    json_object = get_json_from_local_or_s3(book_name)
    logger.info(json_object)

if __name__ == '__main__':
    #ocr_pdf_path = r"D:\project\20231108code-clean\ocr\new\双栏\s0043-1354(02)00581-x.pdf"
    #ocr_json_file_path = r"D:\project\20231108code-clean\ocr\new\双栏\s0043-1354(02)00581-x.json"
    # ocr_pdf_path = r"D:\project\20231108code-clean\ocr\new\双栏\j.1540-627x.2006.00176.x.pdf"
    # ocr_json_file_path = r"D:\project\20231108code-clean\ocr\new\双栏\j.1540-627x.2006.00176.x.json"
    ocr_pdf_path = r"/home/cxu/workspace/Magic-PDF/ocr_demo/ocr_1.pdf"
    ocr_json_file_path = r"/home/cxu/workspace/Magic-PDF/ocr_demo/ocr_1.json"
    ocr_online_parse(book_name="数学新星网/edu_00001236")
    ocr_local_parse(ocr_pdf_path, ocr_json_file_path)
    pass