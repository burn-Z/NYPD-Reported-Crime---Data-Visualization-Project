import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.write("""
# 'Hello, *World!* :sunglasses:'
""")

q2_df = pd.read_csv('..\\data\\neighbh_crime_dist.csv',
                 low_memory= False,
                # nrows= 500000,
                # parse_dates= [1],
                # index_col= 0
                )

st.write("""
#### Crime Count Distribution Per Borough
""")

def show_neigh_crime_pie(t_df, year):
    selection = t_df[t_df['CMPLNT_FR_YR'] == year]

    vcs = selection['BORO_NM'].value_counts()

    borough = pd.DataFrame(data= vcs.index, columns= ['BORO_NM'])
    borough['values'] = vcs.values

    ax = go.Figure(data= [go.Pie(labels= borough['BORO_NM'], values= borough['values'])])

    # ax.update_layout( title_text = f'Crime Count per Borough in {year}')

    st.plotly_chart(ax)
    # plt.show()


available_years = [i for i in range(2006, 2022)]

option = st.selectbox('Choose a year', options= available_years)

show_neigh_crime_pie(q2_df, option)