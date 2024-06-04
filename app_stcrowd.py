import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Googleスプレッドシートの設定
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
   
# Streamlit secretsからcredentialsとSPREADSHEET_KEYを取得
credentials_info = st.secrets["gcp_service_account"]
spreadsheet_key = st.secrets["spreadsheet_key"]["spreadsheet_key"]
credentials = Credentials.from_service_account_info(credentials_info, scopes=scope)
gc = gspread.authorize(credentials)
workbook = gc.open_by_key(spreadsheet_key)
sheet = workbook.sheet1

def update_sheet(username, question_num, answer):
    # スプレッドシートにデータを書き込む関数
    cell = sheet.find(username)
    if cell:
        # ユーザー名が既に存在する場合、その行を更新
        row_number = cell.row
        sheet.update_cell(row_number, question_num + 1, answer)
    else:
        # 新しいユーザーの場合、新しい行を追加
        new_row = [username] + [''] * (sheet.col_count - 1)
        sheet.append_row(new_row)
        row_number = sheet.find(username).row
        sheet.update_cell(row_number, question_num + 1, answer)

# Streamlit UI
with st.form("user_input"):
    username = st.text_input("ユーザー名")
    question_num = st.selectbox("質問番号", [i for i in range(1, 11)])
    answer = st.text_area("回答")
    submitted = st.form_submit_button("送信")
    if submitted:
        update_sheet(username, question_num, answer)
        st.success("データをスプレッドシートに送信しました。")
