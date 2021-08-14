import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import plotly.graph_objects as go
from PIL import Image
import streamlit.components.v1 as components
# import matplotlib.pyplot as plt
import pickle
# load model 
import joblib
import bz2
import pickle
import _pickle as cPickle
from extract import getBagian, extract_pasal
# [theme]
# base="light"
# primaryColor="purple"

st.set_page_config(layout='wide')

def main():
    menu = ["Verdict Prediction","Detailed File Extraction"]
    
    choice = st.sidebar.selectbox("Select Menu", menu)

        
    if choice == "Verdict Prediction":
        # st.subheader("Prediction from Model")
#         st.title("MachineLearning Analytics App")
        st.subheader("Upload Dokumen untuk Melihat Hasil Banding")
        # iris= Image.open('iris.png')

        data = st.file_uploader('Upload File PDF',type='.pdf')
        if data == None:
            st.write('Please choose pdf file to upload')
        else:
            text = getBagian(data)
            pasal = extract_pasal(text)
            df = pd.DataFrame.from_dict(pasal)
            tlist = ['pasal 13', 'pasal 4', 'pasal 16', 'pasal 1', 'pasal 5', 'pasal 9', 'pasal 19', 'pasal 17']
            v1 = 1 if tlist[0] in df['pasal'].values else 0
            v2 = 1 if tlist[1] in df['pasal'].values else 0
            v3 = 0
            v4 = 0
            v5 = 1 if tlist[2] in df['pasal'].values else 0
            v6 = 1 if tlist[3] in df['pasal'].values else 0
            v7 = 1 if tlist[4] in df['pasal'].values else 0
            v8 = 1 if tlist[5] in df['pasal'].values else 0
            v9 = 1 if tlist[6] in df['pasal'].values else 0
            v10 = 1 if tlist[7] in df['pasal'].values else 0
            if st.button('Extract Features'):
                # aDict = pickle.load(open("aDict.p","rb"))
                c1,c2= st.beta_columns((3,8))
                with c1:
                    ket = pd.read_excel('verdict_fitur.xlsx')
                    pslist = df.pasal.unique()
                    # st.write('Pasal yang disebut dalam pokok sengketa')
                    # df1 = df['pasal'].unique()
                    # st.dataframe(df1.assign(hack='').set_index('hack'))
                    # st.dataframe(df1)
                    df[['pasal','drop']] = df['pasal'].str.split(' ayat',expand=True)
                    ftlist = ['pasal 13','pasal 4','pasal 16','pasal 1','pasal 5','pasal 9','pasal 19','pasal 17']
                    ftmt = df[df['pasal'].isin(ftlist)]
                    ftmt = ftmt[['pasal']]
                    # st.write('Pasal-Pasal yang menjadi Pokok Sengketa dan menjadi Fitur untuk Prediksi')
                    ket = ket[ket['pasal'].isin(ftmt['pasal'])]
                    ketlist = ket['pasal_terkait'].unique()
                    # ketlist= ketlist.assign(hack='').set_index('hack')
                    # st.table(ketlist)
                    # tlist = pd.DataFrame(ketlist)
                    # st.dataframe(tlist)
                    fig = go.Figure(data=[go.Table(header=dict(values=['Pasal dalam Pokok Sengketa']),
                                                   cells=dict(values=[ketlist],
                                                              align='left',
                                                              height=30,
                                                              font=dict(size=14))
                                                   )
                                          ],
                                    layout=go.Layout(height=200, width=200))
                    fig.update_layout(
                        margin=dict(l=5, r=0, t=0, b=0),)
                    st.plotly_chart(fig)
                    # st.dataframe(ketlist['pasal_terkait'].unique())
                    # st.write(ftmt['pasal'].unique())

                with c2:
                    # ket = pd.read_csv('verdict_fitur.csv', sep=";")
                    my_expander = st.beta_expander(label='Keterangan dan Contoh Kasus Terkait')
                    with my_expander:
                    # st.beta_expander('Keterangan dan Contoh Kasus berdasarkan pasal')
                        ket = ket[ket['pasal'].isin(ftmt['pasal'])]
                        # ftmt = ftmt.merge(ket, on='pasal', how='inner')
                        # opsi = ket['pasal_terkait'].unique()
                        # pilihan = st.selectbox('Keterangan per pasal',list(opsi))
                        # st.write(ket)
                        # ftmt = ftmt.merge(ket, on='pasal', how='inner')
                        # ket = ket[ket['pasal_terkait'].isin([pilihan])]
                        ket = ket[['pasal_terkait','keterangan', 'contoh_kasus']]
                        ket = ket.assign(hack='').set_index('hack')
                        st.table(ket)
            if st.button("2-Classes Prediction"):
                # model= open("vmodel.pkl", "rb")
                model = open("model_verdict/ver_knn_2.pkl", "rb")
                knn = joblib.load(model)
                dfvalues = pd.DataFrame(list(zip([v1], [v2], [v3], [v4], [v5], [v6], [v7], [v8], [v9], [v10])),
                                        columns=['pasal 13', 'pasal 4', 'pasal 15', 'pasal 16A', 'pasal 16B',
                                                 'pasal 1', 'pasal 5', 'pasal 9', 'pasal 19', 'pasal 17'])
                input_variables = np.array(dfvalues[
                                               ['pasal 13', 'pasal 4', 'pasal 15', 'pasal 16A', 'pasal 16B',
                                                'pasal 1', 'pasal 5', 'pasal 9', 'pasal 19', 'pasal 17']])
                prediction = knn.predict(input_variables)
                # st.write(prediction[0])
                if prediction[0] == '0':
                    st.subheader('Prediksi Hasil Verdict')
                    st.title('Permohonan Banding Ditolak')
                else:
                    st.subheader('Prediksi Hasil Verdict')
                    st.title('Permohonan Banding Dikabulkan')
            if st.button("3-Classes Prediction"):
                # model= open("vmodel.pkl", "rb")
                model = open("model_verdict/ver_knn_3.pkl", "rb")
                knn = joblib.load(model)
                dfvalues = pd.DataFrame(list(zip([v1], [v2], [v3], [v4], [v5], [v6], [v7], [v8], [v9], [v10])),
                                        columns=['pasal 13', 'pasal 4', 'pasal 15', 'pasal 16A', 'pasal 16B',
                                                 'pasal 1', 'pasal 5', 'pasal 9', 'pasal 19', 'pasal 17'])
                input_variables = np.array(dfvalues[
                                               ['pasal 13', 'pasal 4', 'pasal 15', 'pasal 16A', 'pasal 16B',
                                                'pasal 1', 'pasal 5', 'pasal 9', 'pasal 19', 'pasal 17']])
                prediction = knn.predict(input_variables)
                # st.write(prediction[0])
                if prediction[0] == '0':
                    st.subheader('Prediksi Hasil Verdict')
                    st.title('Permohonan Banding Ditolak')
                elif prediction[0] == '2':
                    st.subheader('Prediksi Hasil Verdict')
                    st.title('Permohonan Banding Dikabulkan Sebagian')
                else:
                    st.subheader('Prediksi Hasil Verdict')
                    st.title('Permohonan Banding Dikabulkan Seluruhnya')

    
    elif choice == "Detailed File Extraction":
        st.title("Esktraksi Pasal-Pasal dari dokumen PDF")
        data = st.file_uploader('Upload File', type='.pdf')
        if data == None:
            st.write('Please upload PDF File')
        else:
            text = getBagian(data)
            pasal = extract_pasal(text)
            df = pd.DataFrame.from_dict(pasal)
            if st.button('Extract Features'):
                # aDict = pickle.load(open("aDict.p","rb"))
                c1, c2 = st.beta_columns((3, 8))
                with c1:
                    pslist = df.pasal.unique()
                    st.write('Pasal yang disebut dalam Uraian File')
                    df1 = df['pasal'].unique()
                    # st.dataframe(df1.assign(hack='').set_index('hack'))
                    st.table(df1)

if __name__=='__main__':
    main()
