# Determine the scope of websites
# Determine if screenshots are allowed on the corresponding site based on the keyword
from os.path import exists
from os.path import join
# from print_html import print_html
from save_pdf import print_html_time

def scs(company, dir_path, address, df):
    for idx in df.iterrows():
        save_path = dir_path
        save_file_name = company + '_' + idx[1]['网站'] + '.pdf'
        # if exists(save_path) == True:
        #     continue
        # else:
        web_name = idx[1]['网站']
        input_box_name = idx[1]['input_box_name']
        url = idx[1]['url']
        key_word = idx[1]['备注']
        if idx[1]["地区"] != address:
            continue
        else:
            if key_word != "name" and key_word != "id":
                print("{} {}: {}".format(company, web_name, idx[1]['备注']))
            else:
                print_html_time(save_path=save_path,
                           save_file_name=save_file_name,
                           company_name=company,
                           web_name=web_name,
                           input_box_name=input_box_name,
                           url=url,
                           key_word=key_word)