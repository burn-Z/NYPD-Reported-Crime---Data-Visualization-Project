import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

q2_df = pd.read_csv("web-app\\data\\neighbh_crime_dist.csv",
                 low_memory= False,
                 nrows= 500000,
                 index_col= 'id'
                )

available_boroughs = q2_df.borough.unique()

available_years = q2_df.year.unique()
default_years = [2021]

available_category = q2_df.category.unique()


def show_borough_line_chart(bor: list[str], years: list[int]):
    selection = q2_df[q2_df['borough'].isin(bor) | q2_df['year'].isin(years)]

    vcs = selection[['borough', 'year']].value_counts().reset_index(name= 'Count').sort_values(by= ['year'])

    ax = px.line(vcs, x= 'year', y= 'Count', color= 'borough', labels={'year': 'Year'}, )
    # st.line_chart(vcs, x= 'year', y= ['borough', 'Count'] )

    st.plotly_chart(ax)

def show_borough_crime_pie(years):
    selection = q2_df[q2_df['year'].isin(years)]

    vcs = selection['borough'].value_counts()

    borough = pd.DataFrame(data= vcs.index, columns= ['borough'])
    borough['values'] = vcs.values

    ax = go.Figure(data= [go.Pie(labels= borough['borough'], values= borough['values'])])

    years_text = ', '.join([str(i) for i in years])
    ax.update_layout( title_text = f'Distribution of Crime in {years_text}')

    st.plotly_chart(ax)
    # plt.show()

def show_borough_crime_bar(years: list):
    selection = q2_df[q2_df['year'].isin(years)]

    vcs = selection[['borough']].value_counts().reset_index(name= 'Count')

    ax = px.bar(vcs, x= 'borough', y= 'Count', labels= {'borough': 'Borough', 'Count':''})

    years_text = ', '.join([str(i) for i in years])
    ax.update_layout( title_text = f'Crime Count Distribution per Borough in {years_text}')

    st.plotly_chart(ax)

def show_the_witching_hour(bor, yr, cat):
    selection = q2_df[q2_df['borough'].isin(bor) & q2_df['year'].isin(yr) & q2_df['category'].isin(cat)]

    #


# should only be able to choose one option
selected_borough = st.sidebar.multiselect('Filter by Borough', available_boroughs)
selected_years = st.sidebar.multiselect('Filter by Year', available_years, available_years[-1])
selected_crime_type = st.sidebar.multiselect('Filter by Crime Category', available_category)

selected_visual = st.sidebar.button('The Witching Hour')

if not selected_borough or not selected_years:
    show_borough_crime_pie(default_years)
else:
    show_borough_crime_bar(selected_years)
    show_borough_line_chart(selected_borough, selected_years)


# year_choice = st.sidebar.selectbox('Select a year', options= available_years)

# show_neigh_crime_pie(year_choice)