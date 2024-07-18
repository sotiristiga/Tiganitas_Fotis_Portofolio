import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(layout='wide',page_title="Plotting Demo", page_icon="📈")
IM_2020= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2020.csv")
IM_2021= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2021.csv")
IM_2022= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2022.csv")
IM_2023= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2023.csv")


IM=pd.concat([IM_2020,IM_2021,IM_2022,IM_2023])
IM['Started']=pd.to_datetime(IM['Started'],dayfirst=True)
IM['Expired']=pd.to_datetime(IM['Expired'],dayfirst=True)
IM.head(5)
IM['Year']=IM['Started'].dt.year


kpi1, kpi2, kpi3,kpi4 = st.columns(4)
kpi1.metric(label="Clients 👩👨",
        value=IM['id'].nunique())
kpi2.metric(label="Ins Contracts📑",
        value=IM['N_Policy'].nunique())
kpi3.metric(label="Net💶",
        value=IM['Gross'].sum().round(2))
kpi4.metric(label="Commissions💶",
        value=IM['Commissions'].sum().round(2))

tab1, tab2, tab3 = st.tabs(["Ins", "Mega", "Both"])
with tab1:
    
    year_filter=st.selectbox('Select', [2020,2021,2022,2023])
    IM1=IM[IM["Year"]==year_filter]
    
    col = st.columns((15,15))
    with col[0]:
        companies_countpol=IM1['Company'].value_counts().reset_index()
        fig_barplot=px.bar(companies_countpol,x='count',y='Company',title='',labels={'count':'Total'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,range_x=[0,2000])
        fig_barplot.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)

        companies_net=IM1.groupby('Company')['Net'].sum().reset_index()
        companies_net_sorted=companies_net.sort_values('Net',ascending=True)
        fig_barplot=px.bar(companies_net_sorted,x='Net',y='Company',title='',labels={'Net':'Net(euros)'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,range_x=[0,100000])
        fig_barplot.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)

        companies_comm=IM1.groupby('Company')['Commissions'].sum().reset_index()
        companies_comm_sorted=companies_comm.sort_values('Commissions',ascending=True)
        fig_barplot=px.bar(companies_comm_sorted,x='Commissions',y='Company',title='',labels={'Commissions':'Commissions<br>(euros)'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,range_x=[0,10000])
        fig_barplot.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)

    with col[1]:
        categories_countpol=IM1['Category'].value_counts().reset_index()
        fig_barplot=px.bar(categories_countpol,x='count',y='Category',title='',labels={'count':'Total'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,range_x=[0,2000])
        fig_barplot.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)

        categories_net=IM1.groupby('Category')['Net'].sum().reset_index()
        categories_net_sorted=categories_net.sort_values('Net',ascending=True)
        fig_barplot=px.bar(categories_net_sorted,x='Net',y='Category',title='',labels={'Net':'Net(euros)'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,range_x=[0,100000])
        fig_barplot.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)

        categories_comm=IM1.groupby('Category')['Commissions'].sum().reset_index()
        categories_comm_sorted=categories_comm.sort_values('Commissions',ascending=True)
        fig_barplot=px.bar(categories_comm_sorted,x='Commissions',y='Category',title='',labels={'Commissions':'Commissions<br>(euros)'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,range_x=[0,10000])
        fig_barplot.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
