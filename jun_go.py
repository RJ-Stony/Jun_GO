import pandas as pd
import streamlit as st
import requests
import json

def bunjang(word, pages):
    # file_path = "./bunjang_result/" + word + '.json'

    pid = []

    for page in range(pages):
        url = 'https://api.bunjang.co.kr/api/1/find_v2.json?order=date&n=96&page={}&req_ref=search&q={}&stat_device=w&stat_category_required=1&version=4'.format(page, word)
        response = requests.get(url)
        datas = response.json()['list']
        ids = [data['pid'] for data in datas]
        pid.extend(ids)

        items = []

        for id in pid:
            url = 'https://api.bunjang.co.kr/api/1/product/{}/detail_info.json?version=4'.format(id)
            response = requests.get(url)
            try:
                details = response.json()['item_info']
                details.pop('category_name')
                details.pop('pay_option')
                items.append(details)
            except:
                print('error')

        df = pd.DataFrame(items)

        bunjang_df = df[['name', 'price', 'num_item_view', 'pid']]
        bunjang_df = bunjang_df.rename({'name':'title', 'num_item_view':'view_counts', 'link':'url'}, axis='columns')
        bunjang_df['url'] = 'https://m.bunjang.co.kr/products/'+ bunjang_df['pid']
        bunjang_df.drop(['pid'], axis=1)

        bunjang = bunjang_df.to_dict("records")

        return bunjang_df

st.dataframe(bunjang(input(), 1))
