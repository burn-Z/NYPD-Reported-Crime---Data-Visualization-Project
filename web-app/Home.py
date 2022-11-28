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

# filter by borough
def show_borough_line_chart(bor: list[str], years: list[int]):
    selection = q2_df[q2_df['borough'].isin(bor) | q2_df['year'].isin(years)]

    vcs = selection[['borough', 'year']].value_counts().reset_index(name= 'Count').sort_values(by= ['year'])

    ax = px.line(vcs, x= 'year', y= 'Count', color= 'borough', labels={'year': 'Year'}, )
    # st.line_chart(vcs, x= 'year', y= ['borough', 'Count'] )

    st.plotly_chart(ax)

def show_neigh_crime_pie(year):
    selection = q2_df[q2_df['year'].isin(year)]

    vcs = selection['borough'].value_counts()

    borough = pd.DataFrame(data= vcs.index, columns= ['borough'])
    borough['values'] = vcs.values

    ax = go.Figure(data= [go.Pie(labels= borough['borough'], values= borough['values'])])


    years_text = ', '.join([str(i) for i in year])
    ax.update_layout( title_text = f'Crime Count Distribution per Borough in {years_text}')

    st.plotly_chart(ax)
    # plt.show()



available_boroughs = q2_df.borough.unique()
default_years = [2022]
# should only be able to choose one option
selected_borough = st.sidebar.multiselect('Filter by Borough', available_boroughs, available_boroughs[0])


if not selected_borough:
    st.error("Must select a borough")
else:
    if len(selected_borough) == 5:
        show_borough_line_chart(selected_borough, default_years)
    else:
        st.write(''' TO BE IMPLEMENTED ''')


available_years = [i for i in range(2006, 2022)]
selected_years = st.sidebar.multiselect('Pick years', available_years, [2021])
if not selected_years:
    st.error("Must select year")
else:
    show_neigh_crime_pie(selected_years)


# year_choice = st.sidebar.selectbox('Select a year', options= available_years)

# show_neigh_crime_pie(year_choice)