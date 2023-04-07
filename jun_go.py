import pandas as pd
import streamlit as st
import requests
import altair as alt

#def activate_sidebar(df):
#    with st.sidebar:
#        uploaded_files = st.file_uploader('CSV 파일 혹은 ZIP 파일을 업로드해주세요.', accept_multiple_files=True)
    # Check if files were uploaded
#    if len(uploaded_files) > 0:
#        for uploaded_file in uploaded_files:
#            if uploaded_file.type == 'text/csv':
#                uploaded_df = pd.read_csv(uploaded_file)
#                st.write(uploaded_df)

#df = dict()
#activate_sidebar(df)

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

        bunjang_df = bunjang_df.astype({'price':'int', 'view_counts':'int'})

        # with open(file_path, 'w', encoding='UTF-8-sig') as file:
        #        file.write(json.dumps(bunjang, ensure_ascii=False, indent="\t"))

        return bunjang_df

# if __name__ == "__main__":
word = st.text_input('Keyword', '아이폰')
bunjang_df = bunjang(word, 1)
st.write(bunjang_df)

st.write(alt.Chart(bunjang_df).mark_bar().encode(
    x = alt.X('view_counts', sort=None),
    y = 'price',
))
