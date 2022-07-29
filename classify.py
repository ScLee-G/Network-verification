# Determine the scope of websites
# Determine if screenshots are allowed on the corresponding site based on the keyword
from os.path import join
from screenshot_excel import screenshot

def scs(company, dir_path, address, df):
    for idx in df.iterrows():
        save_path = join(dir_path, company+'_'+idx[1]['网站']+'.png')
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
                screenshot(save_path=save_path,
                           company_name=company,
                           web_name=web_name,
                           input_box_name=input_box_name,
                           url=url,
                           key_word=key_word)