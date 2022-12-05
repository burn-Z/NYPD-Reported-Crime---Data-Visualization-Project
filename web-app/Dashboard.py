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
def load_data():
    df = pd.read_csv("web-app\\data\\neighbh_crime_dist.csv",
                    low_memory= False,
                    # nrows= 1000000,
                    index_col= 'id',
                    ).drop(labels= ['Unnamed: 0'], axis= 1)

    return df

# @st.cache
def query_data(df_temp, boro, yr, cat):
    # df_slct = df_temp.query(f"{boro} in @slct_boro & {yr} in @slct_yr & {cat} in @slct_ofnsc")
    # return df_slct
    pass

# Offense Category Pie Chart
@st.cache
def show_ofns_cat(df_temp, name):
    fig = px.pie(
        df_temp,
        names= name,
        color_discrete_sequence= px.colors.sequential.RdBu
    )

    fig.update_traces(textposition= 'inside')
    fig.update_layout(uniformtext_minsize = 12, uniformtext_mode= 'hide')

    # st.plotly_chart(fig)
    return fig

# Offense Description
@st.cache
def show_ofns_desc(df_temp, name):

    fig = px.pie(
        df_temp.query('category in @slct_ofnsc'),
        names= name,
        color_discrete_sequence= px.colors.sequential.RdBu
    )

    fig.update_traces(textposition= 'inside')
    fig.update_layout(uniformtext_minsize = 12, uniformtext_mode= 'hide')

    # st.plotly_chart(fig)
    return fig

def show_ofns_bar(df_temp, x, color, width=None, height= None):
    # fig = px.bar(
    #     df_temp.value_counts([x, color]).reset_index(name= 'Count'),
    #     x = x,
    #     y= 'Count',
    #     color= color,
    #     log_y= True,
    #     # text_auto= '.2s',
    #     width= width,
    #     height= height,
    # )

    fig = px.bar(
        df_temp.value_counts([x, color]).reset_index(name= 'Count'),
        x = 'Count',
        y= x,
        color= color,
        log_x= True,
        text_auto= '.2s',
        width= width,
        height= height,
        orientation= 'h',
    )

    fig.update_traces(textposition= 'inside')
    fig.update_layout(
        uniformtext_minsize = 8,
        uniformtext_mode= 'hide'
        )

    return fig

def show_borough_line_chart(df_temp, bor: list[str], years):
    # vcs = df_temp[['borough', 'year']].value_counts().reset_index(name= 'Count').sort_values(by= ['year'])

    fig = px.line(
        df_temp.value_counts().reset_index(name= 'Count').sort_values(by= ['year']),
        x= years,
        y= 'Count',
        color= bor,
        )
    # st.line_chart(vcs, x= 'year', y= ['borough', 'Count'] )

    return fig

# load data into memory
df = load_data()

## columns
borough = 'borough'
year = 'year'
category = 'category'
offense = 'offense'


# Sidebar filters
## getting filter fields
available_boroughs = df[borough].unique()
available_years = sorted(df[year].unique(), reverse= True)
available_ofns_desc = df[category].unique()


slct_boro = st.sidebar.multiselect('Filter by Borough', available_boroughs, available_boroughs[1])
st.sidebar.markdown('   ---')
slct_yr = st.sidebar.multiselect('Filter by Year', available_years, available_years[0])
st.sidebar.markdown('   ---')
slct_ofnsc = st.sidebar.multiselect('Filter by Offense Category', available_ofns_desc, available_ofns_desc[-1])

## option to see raw data
show_sample = st.sidebar.button('Sample Data')

## Logic for filter selections
if not slct_boro:
    slct_boro = available_boroughs.tolist()

if not slct_yr:
    slct_yr = available_years.tolist()

if not slct_ofnsc:
    slct_ofnsc = available_ofns_desc.tolist()


# query data based on selection
# df_slct = query_data(df, borough, year, category)
df_slct = df.query(f"{borough} in @slct_boro & {year} in @slct_yr & {category} in @slct_ofnsc")


####
slct_yr.sort(reverse= True)

if len(slct_yr) == 1:
    # most recent year crime count
    temp0 = df_slct.shape[0]

    # previous year crime count
    prev_y = slct_yr[0] - 1
    temp1 = df.query(f'{year} == @prev_y & {borough} in @slct_boro & {category} in @slct_ofnsc').shape[0]
else:
    # most recent year crime count
    sy = slct_yr[-1]
    temp0 = df_slct.query(f'{year} == @sy').shape[0]

    # least recent year crime count
    sy = slct_yr[0]
    temp1 = df_slct.query(f'{year} == @sy').shape[0]

try:
    delt = 100 * ( (temp0/temp1) - 1)
except ZeroDivisionError:
    delt = 0

reportcount = df_slct.shape[0]


# display metrics about the data
st.metric(label= 'Number of Incidents Reported', value= reportcount, delta= f'{str(int(delt))}%', delta_color= 'inverse')


c1, c2 = st.columns([3,7])

with c1:
    st.plotly_chart(show_ofns_cat(df_slct, category), use_container_width= True)

with c2:
    st.plotly_chart(
        # show_ofns_desc(df_slct, offense),
        show_ofns_bar(df_slct, offense, category, 1200),
        use_container_width= True
        )

if show_sample:
    st.write(df_slct[['category', 'offense', 'borough', 'date']].sample(10))