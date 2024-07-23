import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st




st.set_page_config(layout='wide',page_title="Insurance Market")
IM_2020= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2020.csv")
IM_2021= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2021.csv")
IM_2022= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2022.csv")
IM_2023= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Testingapppanc/main/IM_2023.csv")


IM=pd.concat([IM_2020,IM_2021,IM_2022,IM_2023])
IM['Started']=pd.to_datetime(IM['Started'],dayfirst=True)
IM['Expired']=pd.to_datetime(IM['Expired'],dayfirst=True)

IM['Year']=IM['Started'].dt.year
month_levels = pd.Series([
  "January", "February", "March", "April", "May", "June", 
  "July", "August", "September", "October", "November", "December"
])

IM['Year']=IM['Started'].dt.year
month_levels = pd.Series([
  "January", "February", "March", "April", "May", "June", 
  "July", "August", "September", "October", "November", "December"
])

IM['Month']=IM['Started'].dt.month_name()

IM['Month'] = pd.Categorical(IM['Month'], categories=month_levels)
IM['Year'] = pd.Categorical(IM['Year'])
IM['Month_Year']=IM["Started"].dt.strftime('%m-%Y')
def gender_groups(Gender):
    if Gender==1:
        return "Άνδρας"
    elif Gender==2:
        return "Γυναίκα"
    elif Gender==3:
        return "Συνιδιοκτισία"
    elif Gender==5:
        return "Νομικό πρόσωπο"
    
def duration_groups(duration):
    if duration==1:
        return "Μηνιαίο"
    elif duration==3:
        return "Τρίμηνο"
    elif duration==6:
        return "Εξάμηνο"
    elif duration==12:
        return "Ετήσιο"
    else:
        return "Άλλη"


IM['Gender'] = IM['Gender'].apply(gender_groups)
IM['Duration']=((IM['Expired'].dt.year-IM['Started'].dt.year)*12 +IM['Expired'].dt.month-IM['Started'].dt.month+IM['Expired'].dt.day/30-IM['Started'].dt.day/30).round(0)
IM['Duration_gr']=IM['Duration'].apply(duration_groups)
duration_levels = pd.Series(["Ετήσιο","Εξάμηνο","Τρίμηνο","Μηνιαίο","Άλλη"])

IM['Duration_gr'] = pd.Categorical(IM['Duration_gr'], categories=duration_levels)
year_filter=st.selectbox('Έτος', [2020,2021,2022,2023])
IM1=IM[IM["Year"]==year_filter]

kpi1, kpi2, kpi3,kpi4 = st.columns(4)
kpi1.metric(label="Πελάτες 👩👨",
        value=IM['id'].nunique())
kpi2.metric(label="Συμβόλαια📑",
        value=IM['N_Policy'].nunique())
kpi3.metric(label="Καθαρά Ασφάλιστρα💶",
        value=IM['Gross'].sum().round(2))
kpi4.metric(label="Προμήθειες💶",
        value=IM['Commissions'].sum().round(2))

tab1, tab2, tab3, tab4,tab5 = st.tabs(["Παραγωγή ανά εταιρεια","Παραγωγή ανά κλάδο", "Εξέλιξη Παραγωγής", "Δημογραφικά Πελατών",'Διάρκειες Συμβολαίων'])
with tab1:
    tab11, tab12, tab13 = st.tabs(["Σύνολο Συμβολαίων", "Καθαρά", "Προμήθειες"])
    with tab11:
        companies_countpol=IM1['Company'].value_counts().reset_index()
        fig_barplot=px.bar(companies_countpol,x='count',y='Company',title='',
                           labels={'count':'Σύνολο Συμβολαίων','Company':'Ασφ. Εταιρεία'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,
                        height=1000)
        fig_barplot.update_traces(textfont_size=17, textangle=0.5, textposition="outside", 
                                  cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
    with tab12:
        companies_net=IM1.groupby('Company')['Net'].sum().reset_index()
        companies_net_sorted=companies_net.sort_values('Net',ascending=True)
        fig_barplot=px.bar(companies_net_sorted,x='Net',y='Company',title='',
                           labels={'Net':'Καθαρά €','Company':'Ασφ. Εταιρεία'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,
                        text='Net',height=1000,range_x=[0,500000])
        fig_barplot.update_traces(textfont_size=17,texttemplate = '%{text:.2s} €',
                                   textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
    with tab13:
        companies_comm=IM1.groupby('Company')['Commissions'].sum().reset_index()
        companies_comm_sorted=companies_comm.sort_values('Commissions',ascending=True)
        fig_barplot=px.bar(companies_comm_sorted,x='Commissions',y='Company',title='',
                           labels={'Commissions':'Προμήθειες €','Company':'Ασφ. Εταιρεία'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,
                        text='Commissions',height=1000,range_x=[0,20000])
        fig_barplot.update_traces(textfont_size=17, texttemplate = '%{text:.2s} €',textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
with tab2:
    tab21, tab22, tab23 = st.tabs(["Σύνολο Συμβολαίων", "Καθαρά", "Προμήθειες"])
    with tab21:
        categories_countpol=IM1['Category'].value_counts().reset_index()
        fig_barplot=px.bar(categories_countpol,x='count',y='Category',title='',
                           labels={'count':'Σύνολο Συμβολαίων','Category':'Κλάδος'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,
                        text_auto=True,range_x=[0,8000])
        fig_barplot.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
    with tab22:
        categories_net=IM1.groupby('Category')['Net'].sum().reset_index()
        categories_net_sorted=categories_net.sort_values('Net',ascending=True)
        fig_barplot=px.bar(categories_net_sorted,x='Net',y='Category',title='',
                           labels={'Net':'Καθαρά €','Category':'Κλάδος'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text='Net',
                        range_x=[0,500000])
        fig_barplot.update_traces(textfont_size=17, texttemplate = '%{text:.3s} €',textangle=0, textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
    with tab23:
        categories_comm=IM1.groupby('Category')['Commissions'].sum().reset_index()
        categories_comm_sorted=categories_comm.sort_values('Commissions',ascending=True)
        fig_barplot=px.bar(categories_comm_sorted,x='Commissions',y='Category',title='',
                           labels={'Commissions':'Προμήθειες €','Category':'Κλάδος'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text='Commissions',
                        range_x=[0,30000])
        fig_barplot.update_traces(textfont_size=17, texttemplate = '%{text:.2s} €',textangle=0, 
                                  textposition="outside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
with tab3:
    prod_line_by_month=IM.groupby('Month_Year')[['Commissions',"Net"]].sum().reset_index()
    prod_line_by_month['Month_Year']=pd.to_datetime(prod_line_by_month['Month_Year'],format='mixed')
    prod_line_by_month=prod_line_by_month.sort_values('Month_Year',ascending=False)
    prod_line_by_month_count=IM['Month_Year'].value_counts().reset_index()
    prod_line_by_month_count['Month_Year']=pd.to_datetime(prod_line_by_month_count['Month_Year'],format='mixed')
    prod_line_by_month_count=prod_line_by_month_count.sort_values('Month_Year',ascending=False)
    prod_line_by_month['Year']=prod_line_by_month['Month_Year'].dt.year
    prod_line_by_month_count['Year']=prod_line_by_month_count['Month_Year'].dt.year
    prod_line_by_year=prod_line_by_month.groupby('Year')[['Commissions',"Net"]].sum().reset_index()
    prod_line_by_year_count=prod_line_by_month_count.groupby('Year')['count'].sum().reset_index()
    prod_line_by_year_count['Year']=pd.Categorical(prod_line_by_year_count['Year'],pd.Series([2020,2021,2022,2023]))
    tab31, tab32, tab33 = st.tabs(["Σύνολο Συμβολαίων", "Καθαρά", "Προμήθειες"])
    with tab31:
        fig_line_polcou = px.bar(prod_line_by_year_count, 
                        x="Year", y="count", 
                        title='Σύνολο συμβολαίων ανά έτος απο το 2020 έως 2023',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'count':'Σύνολο συμβολαίων','Year':'Έτος'},
                        range_y=[0,8000],width=500,text_auto=True)
        fig_line_polcou.update_traces(textfont_size=17, textangle=0, 
                                      textposition="outside", cliponaxis=False)
        fig_line_polcou.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_line_polcou)
        
        fig_line_polcou = px.line(prod_line_by_month_count, 
                        x="Month_Year", y="count", 
                        title='Σύνολο συμβολαίων ανά μήνα απο το 2020 έως 2023',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'count':'Σύνολο συμβολαίων','Month_Year':'Μήνας-Έτος'},
                        range_y=[0,600],markers=True)
        fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
        st.write(fig_line_polcou)
    with tab32:
        fig_line_polcou = px.bar(prod_line_by_year, 
                        x="Year", y="Net", 
                        title='Καθαρά ασφάλιστρα ανά έτος',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'Net':'Καθαρά €','Year':'Έτος'},
                        range_y=[0,230000],width=500,text='Net')
        fig_line_polcou.update_traces(textfont_size=17,texttemplate = '%{text:.3s} €', textangle=0, textposition="outside", cliponaxis=False)
        fig_line_polcou.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_line_polcou)
        fig_line_net = px.line(prod_line_by_month, 
                        x="Month_Year", y="Net", 
                        title='Κάθαρα Ασφάλιστρα ανά μήνα ',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'Net':'Καθαρά €','Month_Year':'Μήνας-Έτος'},
                        range_y=[0,35000],markers=True)
        fig_line_net.update_layout(plot_bgcolor='white',font_size=13)
        st.write(fig_line_net)
    with tab33:
        fig_line_polcou = px.bar(prod_line_by_year, 
                        x="Year", y="Commissions", 
                        title='Προμήθειες ανά έτος',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'Commissions':'Προμήθειες €','Year':'Έτος'},
                        range_y=[0,30000],width=500,text='Commissions')
        fig_line_polcou.update_traces(textfont_size=17,texttemplate = '%{text:.3s} €', textangle=0, textposition="outside", cliponaxis=False)
        fig_line_polcou.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_line_polcou)
        fig_line_com = px.line(prod_line_by_month, 
                        x="Month_Year", y="Commissions", 
                        title='Προμήθειες ανά μήνα',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'Commissions':'Προμήθειες €','Month_Year':'Μήνας-Έτος'},
                        range_y=[0,3500],markers=True)
        fig_line_com.update_layout(plot_bgcolor='white',font_size=13)
        st.write(fig_line_com)        
        
with tab4:
    st.write("# Φύλο πελατών")
    gender_data=IM.groupby(['id','Gender'])[['Gross','Net','Commissions']].sum().reset_index()
    gender_data=gender_data[gender_data['Gender']!='Συνιδιοκτισία']
    gendercount=gender_data['Gender'].value_counts().reset_index()
    fig_pie=px.pie(gendercount,values='count',names='Gender', color='Gender',
               color_discrete_sequence= px.colors.sequential.Viridis_r,labels={'count':'Σύνολο',
                                                                 'Gender':'Φύλο'}, 
               height=400,
               title='Ποσόστό φύλων',hole=0.5)
    fig_pie.update_traces(hoverinfo="value",textfont_size=17)
    fig_pie.update_layout(plot_bgcolor='white',font_size=20,legend=dict(
        yanchor="top",
        y=0.80,
        xanchor="left",
        x=0.25
    ),legend_title_text='Φύλο',title_x=0.4)
    st.write(fig_pie)
    st.write("""* Σε αρκετα συμβόλαια δεν αναγραφόταν το φύλο του πελάτη. Επίσης, σε κάποια συμβόλαια υπάρχει συνιδιοκτησία""")
    st.write("# Νομός")
    IM['District']=IM['District'].replace("ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑΣ","ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑ")
    discrict_data=IM.groupby(['id','District'])[['Gross','Net','Commissions']].sum().reset_index()
    discrict_data_total=IM.groupby(['District'])[['Gross','Net','Commissions']].sum().reset_index()
    discrictcount=discrict_data['District'].value_counts().reset_index().sort_values('count')
    tab41, tab42, tab43 = st.tabs(["Σύνολο Συμβολαίων", "Καθαρά", "Προμήθειες"])
    with tab41:
        fig_barplot_reg=px.bar(discrictcount,x='count',y='District',title='',
                           labels={'count':'Αρ. Πελατών','District':'Νομός'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,
                        text_auto=True,width=1200,height=1200,range_x=[0,1500])
        fig_barplot_reg.update_traces(textfont_size=14, textangle=0.5, textposition="outside", cliponaxis=False)
        fig_barplot_reg.update_layout(plot_bgcolor='white',font_size=25)
        st.write(fig_barplot_reg)
    with tab42:
        fig_barplot_reg=px.bar(discrict_data_total.sort_values('Net'),x='Net',y='District',title='',
                           labels={'Net':'Καθαρά €','District':'Νομός'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text='Net',width=1000,
                        height=1200,range_x=[0,600000])
        fig_barplot_reg.update_traces(textfont_size=14,texttemplate = '%{text:.2s} €', textangle=0.5, textposition="outside", cliponaxis=False)
        fig_barplot_reg.update_layout(plot_bgcolor='white',font_size=25)
        st.write(fig_barplot_reg)
    with tab43:
        fig_barplot_reg=px.bar(discrict_data_total.sort_values('Commissions'),x='Commissions',y='District',title='',
                           labels={'Commissions':'Προμήθειες €','District':'Νομός'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text='Commissions',width=1200,height=1200,
                        range_x=[0,70000] )
        fig_barplot_reg.update_traces(textfont_size=14,texttemplate = '%{text:.3s} €', textangle=0.5, textposition="outside", cliponaxis=False)
        fig_barplot_reg.update_layout(plot_bgcolor='white',font_size=25)
        fig_barplot.update_xaxes(tickprefix="€")
        st.write(fig_barplot_reg)
with tab5:
    select_durations=IM.loc[(IM['Duration']==1)|(IM['Duration']==3)|(IM['Duration']==6)|(IM['Duration']==12)]
    select_duration_total_year=(select_durations[['Duration_gr','Month','Year']].value_counts().reset_index()).groupby(['Year',"Duration_gr"])['count'].sum().round(1).reset_index()
    fig_dur_bar = px.bar(select_duration_total_year.loc[select_duration_total_year['Duration_gr']!="Άλλη"], 
                        x="Year", y="count", 
                        title='Χρονικές διάρκειες συμβολαίων ανά έτος (Συνολικά)',color='Duration_gr',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'count':'# Συμβολαίων','Year':'Έτος',"Duration_gr":'Διάρκεια συμβολαίου'},
                        range_y=[0,8000],width=700,text='count')
    fig_dur_bar.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
    fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
    st.write(fig_dur_bar)

    select_durations=IM.loc[(IM['Duration']==1)|(IM['Duration']==3)|(IM['Duration']==6)|(IM['Duration']==12)]
    select_duration_total=select_durations[['Duration_gr','Month']].value_counts().reset_index().sort_values(['Duration_gr','Month'])
    fig_dur_bar = px.bar(select_duration_total, 
                        x="Month", y="count", 
                        title='Χρονικές διάρκειες συμβολαίων ανά μήνα (Συνολικά)',color='Duration_gr',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'count':'# Συμβολαίων','Month':'Μήνας',"Duration_gr":'Διάρκεια συμβολαίου'},
                        range_y=[0,2000],width=1000,text='count')
    fig_dur_bar.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
    fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
    st.write(fig_dur_bar)
    select_duration_mean=(select_durations[['Duration_gr','Month','Year']].value_counts().reset_index()).groupby(['Month',"Duration_gr"])['count'].mean().round(1).reset_index()
    fig_dur_bar = px.line(select_duration_mean.loc[select_duration_mean['Duration_gr']!="Άλλη"], 
                        x="Month", y="count", 
                        title='Χρονικές διάρκειες συμβολαίων ανά μήνα (Μέσος όρος)',color='Duration_gr',
                        color_discrete_sequence= px.colors.sequential.Aggrnyl,
                        labels={'count':'# Συμβολαίων','Month':'Μήνας',"Duration_gr":'Διάρκεια συμβολαίου'},
                        range_y=[0,250],width=1000,height=500)
    fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
    st.write(fig_dur_bar)
