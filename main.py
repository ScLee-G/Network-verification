import os
import pandas as pd
from classify import scs
from os.path import join

def main():
    # Path of related files
    xlsx_path = path_to_web_excel
    base_path = path_to_save_screenshot
    company_list_path = path_to_company_name
    address = input("请按“中国/省/市”格式输入核查公司的注册地信息：").split("/")

    company_names = []

    # Read the companies list
    with open(company_list_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            company_names.append(line.rstrip())

    # Read the websites list
    df = pd.read_excel(xlsx_path)

    # First loop: company; Second loop: address
    for company_name in company_names:
        dir_path = join(base_path, company_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        for i in range(len(address)):
            scs(company_name, dir_path, address[i], df)

if __name__ == "__main__":
    main()
