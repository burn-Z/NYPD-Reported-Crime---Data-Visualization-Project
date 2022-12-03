import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# Page setting
st.set_page_config(
    page_title="NYPD Crime Dashboard",
    page_icon=":shark:",
    layout="wide",
    initial_sidebar_state= "auto",
)

# # consitent pathing
# cur_path = os.path.join(os.getcwd(), 'style.css')
# print('------', cur_path)

# applying style sheet
with open('web-app\\style.css') as s:
    st.markdown(f'<style>{s.read()}</style>', unsafe_allow_html= True)

# loading in data
@st.cache
def get_data_csv():
    df = pd.read_csv("web-app\\data\\neighbh_crime_dist.csv",
                    low_memory= False,
                    nrows= 1000000,
                    index_col= 'id',
                    ).drop(labels= ['Unnamed: 0'], axis= 1)

    return df

df = get_data_csv()

# getting filter fields
available_boroughs = df.borough.unique()
available_years = df.year.unique()
available_category = df.category.unique()

# UI for filters
slct_boro = st.sidebar.multiselect('Filter by Borough', available_boroughs, available_boroughs)
st.sidebar.markdown('   ---')
slct_yr = st.sidebar.multiselect('Filter by Year', available_years, available_years[-1])
# crime_cats = st.sidebar.multiselect('Filter by Crime Category', available_category)

# Logic for filter selections
if not (slct_boro or slct_yr):
    df_slct = df
elif not slct_boro and slct_yr:
    df_slct = df.query("year == @slct_yr")
elif slct_boro and not slct_yr:
    df_slct = df.query("borough in @slct_boro")
else:
    df_slct = df.query("borough in @slct_boro & year in @slct_yr")

# option to see raw data
c1, c2 = st.columns(2)

with c1:
    show_sample = st.sidebar.button('Sample Data')
with c2:
    extra = st.sidebar.button('extra')

if show_sample:
    st.write(df_slct[['category', 'offense', 'borough', 'date']].sample(10))

# def show_borough_line_chart(bor: list[str], years: list[int]):
#     vcs = df_slct[['borough', 'year']].value_counts().reset_index(name= 'Count').sort_values(by= ['year'])

#     ax = px.line(vcs, x= 'year', y= 'Count', color= 'borough', labels={'year': 'Year'}, )
#     # st.line_chart(vcs, x= 'year', y= ['borough', 'Count'] )

#     st.plotly_chart(ax)

# def show_borough_crime_pie(years):

#     vcs = df_slct['borough'].value_counts()

#     borough = pd.DataFrame(data= vcs.index, columns= ['borough'])
#     borough['values'] = vcs.values

#     ax = go.Figure(data= [go.Pie(labels= borough['borough'], values= borough['values'])])

#     years_text = ', '.join([str(i) for i in years])
#     ax.update_layout( title_text = f'Distribution of Crime in {years_text}')

#     st.plotly_chart(ax)
#     # plt.show()

# def show_borough_crime_bar(years: list):
#     vcs = df_slct[['borough']].value_counts().reset_index(name= 'Count')

#     ax = px.bar(vcs, x= 'borough', y= 'Count', labels= {'borough': 'Borough', 'Count':''})

#     years_text = ', '.join([str(i) for i in years])
#     ax.update_layout( title_text = f'Crime Count Distribution per Borough in {years_text}')

#     st.plotly_chart(ax)

# def show_the_witching_hour(bor, yr, cat):
#     pass

#     #

# selected_visual = st.sidebar.button('The Witching Hour')

# if not slct_boro or not slct_yr:
#     show_borough_crime_pie(available_years)
# else:
#     show_borough_crime_bar(slct_yr)
#     show_borough_line_chart(slct_boro, slct_yr)