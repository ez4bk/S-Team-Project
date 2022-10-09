# coding=utf-8
import encodings
import re

import chardet
import html2text as ht


def get_html_buf(file_name):
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as f:
        html_buf = f.read()
    return html_buf


def html_buf_2_md_buf(html_buf):
    text_maker = ht.HTML2Text()
    text = text_maker.handle(html_buf)
    return text


def filter_md_buf(md_buf):
    tmp = ""
    for a in md_buf.split("\n"):  # 过滤无用的url地址
        result = re.findall("](\(.*#*\s*\)*)", a)
        if len(result) != 0:
            tmp += str(a.replace(str(result[0]), "") + "\n")
        else:
            tmp += str(a + "\n")
    return tmp


def write_md_file(md_file_name, md_buf):
    with open(md_file_name, 'w', encoding='utf-8') as f:
        f.write(md_buf)


def html_2_md(html_file_name, md_file_name):
    print("html_2_md(" + str(html_file_name) + "," + str(md_file_name) + ")")
    html_buf = get_html_buf(html_file_name)
    if html_buf is None or html_buf == "":
        return
    md_buf = html_buf_2_md_buf(html_buf)
    tmp_md_buf = filter_md_buf(md_buf)
    write_md_file(md_file_name, tmp_md_buf)


if __name__ == '__main__':
    file_path = r"C:\Users\R10707\Desktop\接口文档1.html"
    with open(file_path, 'r', encoding="utf-8", errors='ignore') as f:
        html_buf = f.read()
        # print(chardet.detect(html_buf))
    # print(html_buf)
    print(html_buf_2_md_buf(html_buf))
