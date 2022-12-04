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

# # consistent pathing
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

borough = 'borough'
year = 'year'
category = 'category'
offense = 'offense'

# getting filter fields
available_boroughs = df[borough].unique()
available_years = df[year].unique()
available_ofns_desc = df[category].unique()

# Sidebar filters
slct_boro = st.sidebar.multiselect('Filter by Borough', available_boroughs, available_boroughs[1])
st.sidebar.markdown('   ---')
slct_yr = st.sidebar.multiselect('Filter by Year', available_years, available_years[-1])
st.sidebar.markdown('   ---')
slct_ofnsc = st.sidebar.multiselect('Filter by Offence Category', available_ofns_desc, available_ofns_desc[-1])

# Logic for filter selections
if not slct_boro:
    slct_boro = available_boroughs.tolist()

if not slct_yr:
    slct_yr = available_years.tolist()

if not slct_ofnsc:
    slct_ofnsc = available_ofns_desc.tolist()


# query data based on selection
df_slct = df.query(f"{borough} in @slct_boro & {year} in @slct_yr & {category} in @slct_ofnsc")


####
slct_yr.sort()

if len(slct_yr) == 1:
    # current year crime count
    temp0 = df_slct.shape[0]

    # previous year crime count
    prev_y = slct_yr[0] - 1
    temp1 = df.query(f'{year} == @prev_y & {borough} in @slct_boro & {category} in @slct_ofnsc').shape[0]
else:
    # current year crime count
    sy = slct_yr[-1]
    temp0 = df_slct.query(f'{year} == @sy').shape[0]

    #...
    sy = slct_yr[0]
    temp1 = df_slct.query(f'{year} == @sy').shape[0]

delt = 100 * ( (temp0/temp1) - 1)

reportcount = df_slct.shape[0]
# display metrics about the data
st.metric(label= 'Number of Incidents Reported', value= reportcount, delta= f'{str(int(delt))}%', delta_color= 'inverse')

# Offense Category Pie Chart
def show_ofns_cat(df_temp):
    fig = px.pie(
        df_temp,
        names= category,
        color_discrete_sequence= px.colors.sequential.RdBu
    )

    fig.update_traces(textposition= 'inside')
    fig.update_layout(uniformtext_minsize = 12, uniformtext_mode= 'hide')

    st.plotly_chart(fig)

# Offense Description
def show_ofns_desc(df_temp):

    fig = px.pie(
        df_temp.query('category in @slct_ofnsc'),
        names= offense
    )

    fig.update_traces(textposition= 'inside')
    fig.update_layout(uniformtext_minsize = 1212, uniformtext_mode= 'hide')

    st.plotly_chart(fig)

# option to see raw data
show_sample = st.sidebar.button('Sample Data')



if show_sample:
    st.write(df_slct[['category', 'offense', 'borough', 'date']].sample(10))

if not slct_ofnsc or len(slct_ofnsc) == 3:
    show_ofns_cat(df_slct)
else:
    show_ofns_desc(df_slct)

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