import os
import pandas as pd
from classify_pdf import scs
from os.path import join

def main():
    # Path of related files
    xlsx_path = r"D:\Git_Clone\Network_Verification\web_sources_base.xlsx"
    base_path = r"D:\Git_Clone\Network_Verification"
    company_list_path = r"D:\Git_Clone\Network_Verification\Vendor_List_1.xlsx"
    address = input("请按“中国/省/市”格式输入核查公司的注册地信息：").split("/")

    company_names = []

    # Read the companies list
    df_companies = pd.read_excel(company_list_path)
    # Assuming the first column contains company names
    company_names = df_companies.iloc[:, 0].dropna().tolist()

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
