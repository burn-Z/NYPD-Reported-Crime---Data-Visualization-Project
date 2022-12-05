# import os
import streamlit as st
import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
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
    df = pd.read_csv("web-app\\data\\data_subset.csv",
                    low_memory= False,
                    # nrows= 1000000,
                    index_col= 'id',
                    )
    # .drop(labels= ['Unnamed: 0'], axis= 1)

    return df

# @st.cache
def query_data(df_temp, boro, yr, cat):
    # df_slct = df_temp.query(f"{borough} in @slct_boro & {category} in @slct_ofnsc & {year} >= @slct_fr_yr & {year} <= @slct_to_yr")
    # return df_slct
    pass

# Offense Category Pie Chart
@st.cache
def show_ofns_cat(df_temp, name):
    fig = px.pie(
        df_temp,
        names= name,
        # color_discrete_sequence= px.colors.sequential.RdBu
    )

    fig.update_traces(
        textposition= 'inside'
        )

    fig.update_layout(
        uniformtext_minsize = 12,
        uniformtext_mode= 'hide'
        )

    # st.plotly_chart(fig)
    return fig

@st.cache
def show_ofns_desc(df_temp, x, color):
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

    vcs = df_temp.value_counts([x, color]).reset_index(name= 'Count').sort_values(by= 'Count')
    fig = px.bar(
        vcs,
        x = 'Count',
        y= x,
        color= color,
        log_x= True,
        text_auto= '.2s',
        # width= width,
        # height= height,
        orientation= 'h',
    )

    fig.update_traces(textposition= 'inside')
    fig.update_layout(
        xaxis={'visible': False, 'showticklabels': False},
        uniformtext_minsize = 8,
        uniformtext_mode= 'hide'
        )

    return fig

@st.cache
def show_yr_ovr_yr(df_temp, filter, x, color):
    vcs = df_temp[filter].value_counts().reset_index(name= 'Count').sort_values(by= [x])

    fig = px.line(
        vcs,
        x= x,
        y= 'Count',
        color= color,
        )

    fig.update_layout(
        xaxis= {
            # 'visible': False,
            'showgrid': False,
            # 'dtick': "M1",
        },
        yaxis= {
            # 'visible': False,
            'showgrid': False
        }
    )
    # fig.update_xaxes(
    # dtick="M1",
    # tickformat="%b\n%Y")
    return fig

@st.cache
def show_per(df_temp, names):
    fig = px.pie(
        df_temp,
        names = names
    )

    vcs = df_temp.value_counts([names]).reset_index(name= 'Count').sort_values(by= names)
    fig = px.bar(
        vcs,
        x = names,
        y = 'Count',
        color= names
    )

    return fig


# load data into memory
with st.spinner('Loading dataset...'):
    df = load_data()

## columns names
borough = 'borough'
year = 'year'
month = 'month'
category = 'category'
offense = 'offense'
date = 'date'
day = 'day'

# SIDEBAR FILTERS
## getting filter fields
available_boroughs = df[borough].unique()
available_years = sorted(df[year].unique())
available_ofns_desc = df[category].unique()


slct_boro = st.sidebar.multiselect('Filter by Borough', available_boroughs, available_boroughs)
st.sidebar.markdown('   ---')

slct_ofnsc = st.sidebar.multiselect('Filter by Offense Category', available_ofns_desc, available_ofns_desc)
st.sidebar.markdown('   ---')

# slct_yr = st.sidebar.multiselect('Filter by Year', available_years, available_years)
slct_fr_yr = st.sidebar.number_input('From', available_years[0], available_years[-1], available_years[0], 1)
slct_to_yr = st.sidebar.number_input('To', slct_fr_yr, available_years[-1], available_years[-1], 1,)
st.sidebar.markdown('   ---')
#


## option to see raw data
show_sample = st.sidebar.button('Sample Data')

## Logic for filter selections
if not slct_boro:
    slct_boro = available_boroughs.tolist()

if not slct_ofnsc:
    slct_ofnsc = available_ofns_desc.tolist()



# query data based on selection
# df_slct = query_data(df, borough, year, category)
df_slct = df.query(f"{borough} in @slct_boro & {category} in @slct_ofnsc & {year} >= @slct_fr_yr & {year} <= @slct_to_yr")

# print(df_slct['month'].unique())
# PAGE CONTENTS

c1, c2, c3 = st.columns([2,4,4])

with c1:
    try:
        temp0 = df_slct.query(f'{year} == @slct_fr_yr').shape[0]
        temp1 = df_slct.query(f'{year} == @slct_to_yr').shape[0]
        delta = 100 * ( (temp0/temp1) - 1)
    except ZeroDivisionError:
        delta = 0
    incident_count = df_slct.shape[0]

    label = 'Number of Incidents Reported '
    label += f'in {slct_fr_yr}' if slct_fr_yr == slct_to_yr else f'from {slct_fr_yr} to {slct_to_yr}'
    st.metric(label= label, value= incident_count, delta= f'{str(int(delta))}%', delta_color= 'inverse')

with c2:
    st.plotly_chart(show_ofns_cat(df_slct, category), use_container_width= True)

with c3:
    st.plotly_chart(show_per(df_slct, day))


st.plotly_chart(
    show_ofns_desc(df_slct, offense, category),
    use_container_width= True
    )


filt_by = month if slct_to_yr - slct_fr_yr <=2 else year
st.plotly_chart(
    show_yr_ovr_yr(df_slct,[borough, filt_by], filt_by, borough),
    use_container_width= True,
)

if show_sample:
    st.write(df_slct[['category', 'offense', 'borough', 'date']].sample(10))