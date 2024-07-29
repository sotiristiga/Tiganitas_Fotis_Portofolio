
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters

st.set_page_config(layout='wide',page_title="Insurance Market")
ME_2015_2016= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2015_2016.csv")
ME_2017= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2017.csv")
ME_2018= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2018.csv")
ME_2019= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2019.csv")
ME_2020= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2020.csv")
ME_2021= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2021.csv")
ME_2022= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2022.csv")
ME_2023= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/ME_2023.csv")
ME=pd.concat([ME_2015_2016,ME_2017,ME_2018,ME_2019,ME_2020,ME_2021,ME_2022,ME_2023])
IM_2020= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/IM_2020.csv")
IM_2021= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/IM_2021.csv")
IM_2022= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/IM_2022.csv")
IM_2023= pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Tiganitas_Fotis_Portofolio/main/IM_2023.csv")
IM=pd.concat([IM_2020,IM_2021,IM_2022,IM_2023])
IM['Platform']="Insurance Market"
ME['Platform']="Megabroker"
ME['District']=ME['District'].replace("ΑΙΤΩΛΟΚΑΡΝΑΝΙΑ","ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑ")
ME['District']=ME['District'].replace("ΑΤΤΙΚΗ","ΑΤΤΙΚΗΣ")
ME['District']=ME['District'].replace("ΑΧΑΪΑΣ","ΑΧΑΙΑΣ")
ME['District']=ME['District'].replace("ΚΟΡΙΝΘΟΥ","ΚΟΡΙΝΘΙΑΣ")
ME['District']=ME['District'].replace("ΛΑΡΙΣΗΣ","ΛΑΡΙΣΑΣ")
IM['District']=IM['District'].replace("ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑΣ","ΑΙΤΩΛΟΑΚΑΡΝΑΝΙΑ")
IM['District']=IM['District'].replace("ΔΩΔΕΚΑΝΗΣΟΥ","ΔΩΔΕΚΑΝΗΣΩΝ")
ME['District']=ME['District'].replace("ΠΕΛΛΑΣ","ΠΕΛΛΗΣ")
IM['Category']=IM['Category'].replace("ΑΥΤΟΚΙΝΗΤΟ","ΑΥΤΟΚΙΝΗΤΩΝ")
IM['Category']=IM['Category'].replace("ΠΡΟΣΩΠΙΚΟ ΑΤΥΧΗΜΑ (ΟΧΗΜΑ)","ΠΡΟΣΩΠΙΚΩΝ ΑΤΥΧΗΜΑΤΩΝ")
IM['Category']=IM['Category'].replace("ΟΔΙΚΗ ΒΟΗΘΕΙΑ","ΟΔΙΚΗΣ ΒΟΗΘΕΙΑΣ")
IM['Category']=IM['Category'].replace("ΝΟΜΙΚΗ ΠΡΟΣΤΑΣΙΑ","ΝΟΜΙΚΗΣ ΠΡΟΣΤΑΣΙΑΣ")
IM['Category']=IM['Category'].replace("ΣΚΑΦΗ","ΣΚΑΦΩΝ")
IM_select=IM[['N_Policy', 'Company', 'Category', 'Char', 'Started', 'Expired','District', 'City', 'Gross', 'Net', 'Commissions', 'id','Platform']]

All=pd.concat([ME,IM_select])
All['District'].value_counts().reset_index().sort_values('District')
All['Started']=pd.to_datetime(All['Started'],dayfirst=True)
All['Expired']=pd.to_datetime(All['Expired'],dayfirst=True)

All['Year']=All['Started'].dt.year
month_levels = pd.Series([
  "January", "February", "March", "April", "May", "June", 
  "July", "August", "September", "October", "November", "December"
])

All['Month']=All['Started'].dt.month_name()

All['Month'] = pd.Categorical(All['Month'], categories=month_levels)

All['Month_Year']=All["Started"].dt.strftime('%m-%Y')

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
    
All['Duration']=((All['Expired'].dt.year-All['Started'].dt.year)*12 +All['Expired'].dt.month-All['Started'].dt.month+All['Expired'].dt.day/30-All['Started'].dt.day/30).round(0)

All['Duration_gr']=All['Duration'].apply(duration_groups)

duration_levels = pd.Series(["Ετήσιο","Εξάμηνο","Τρίμηνο","Μηνιαίο","Άλλη"])

All['Duration_gr'] = pd.Categorical(All['Duration_gr'], categories=duration_levels)

dynamic_filters1 = DynamicFilters(All, filters=['Company','Year','Month'])


with st.sidebar:
    dynamic_filters1.display_filters()

All2=dynamic_filters1.filter_df()

kpi1, kpi2, kpi3,kpi4 = st.columns(4)

kpi1.metric(label="Πελάτες 👩👨",
        value=All2['id'].nunique())

kpi2.metric(label="Συμβόλαια📑",
        value=All2['N_Policy'].nunique())

kpi3.metric(label="Καθαρά Ασφάλιστρα💶",
        value=All2['Net'].sum().round(2))

kpi4.metric(label="Προμήθειες💶",
        value=All2['Commissions'].sum().round(2))

pie1, pie2, pie3,pie4 = st.columns(4)
with pie1:
    pie1=px.pie(All2[['N_Policy','Platform']].value_counts().reset_index().groupby('Platform').count().reset_index(),
        values='count',names='Platform', color='Platform',
        color_discrete_sequence= px.colors.sequential.Viridis_r,labels={'count':'Σύνολο',
                                                            'Platform':'Πλατφόρμα'}, 
        height=350,
        title='Πελάτες<br>(ανά πλατφόρμα)',hole=0.5,width=150)
    pie1.update_traces(hoverinfo="value",textfont_size=17)
    pie1.update_layout(plot_bgcolor='white',font_size=20,
                       legend=dict(yanchor="top",y=0.04,xanchor="left",x=0.00005),legend_title_text='Πλατφόρμα',title_x=0.1,title_y=0.8)
    st.write(pie1)

with pie2:
    pie2=px.pie(All2[['id','Platform']].value_counts().reset_index().groupby('Platform').count().reset_index(),
        values='count',names='Platform', color='Platform',
        color_discrete_sequence= px.colors.sequential.Viridis_r,labels={'count':'Σύνολο',
                                                            'Platform':'Πλατφόρμα'}, 
        height=350,
        title='Συμβόλαια<br>(ανά πλατφόρμα)',hole=0.5,width=150)
    pie2.update_traces(hoverinfo="value",textfont_size=17)
    pie2.update_layout(plot_bgcolor='white',font_size=20,showlegend=False,title_y=0.8)
    st.write(pie2)

with pie3:
    pie3=px.pie(All2.groupby('Platform')['Net'].sum().reset_index(),
        values='Net',names='Platform', color='Platform',
        color_discrete_sequence= px.colors.sequential.Viridis_r,labels={'Net':'Καθαρά<br>ασφάλιστρα',
                                                            'Platform':'Πλατφόρμα'}, 
        height=350,
        title='Καθαρά<br>ασφάλιστρα <br>(ανά πλατφόρμα)',hole=0.5,width=150)
    pie3.update_traces(hoverinfo="value",textfont_size=17)
    pie3.update_layout(plot_bgcolor='white',font_size=20,
                       showlegend=False,title_x=0.1,title_y=0.85)
    st.write(pie3)

with pie4:
    pie4=px.pie(All2.groupby('Platform')['Commissions'].sum().reset_index(),
        values='Commissions',names='Platform', color='Platform',
        color_discrete_sequence= px.colors.sequential.Viridis_r,labels={'Commissions':'Προμήθειες',
                                                            'Platform':'Πλατφόρμα'}, 
        height=350,
        title='Προμήθειες<br>(ανά πλατφόρμα)',hole=0.5,width=150)
    pie4.update_traces(hoverinfo="value",textfont_size=17)
    pie4.update_layout(plot_bgcolor='white',font_size=20,showlegend=False,title_x=0.1,title_y=0.8)
    st.write(pie4)

tab1,tab2,tab3,tab4 = st.tabs(["Εξέλιξη Παραγωγής","Κλάδος ασφάλισης",'Δημογραφικά Πελατών','Διάρκειες Συμβολαίων'])
with tab1:
    prod_line_by_month=All2.groupby('Month_Year')[['Commissions',"Net"]].sum().reset_index()
    prod_line_by_month['Month_Year']=pd.to_datetime(prod_line_by_month['Month_Year'],format='mixed')
    prod_line_by_month=prod_line_by_month.sort_values('Month_Year',ascending=False)
    prod_line_by_month_count=All2['Month_Year'].value_counts().reset_index()
    prod_line_by_month_count['Month_Year']=pd.to_datetime(prod_line_by_month_count['Month_Year'],format='mixed')
    prod_line_by_month_count=prod_line_by_month_count.sort_values('Month_Year',ascending=False)
    prod_line_by_month['Year']=prod_line_by_month['Month_Year'].dt.year
    prod_line_by_month['Month']=prod_line_by_month['Month_Year'].dt.month_name()
    prod_line_by_month_mean=prod_line_by_month.groupby('Month')[['Commissions',"Net"]].mean().round(1).reset_index()
    prod_line_by_month_mean['Month'] = pd.Categorical(prod_line_by_month_mean['Month'], categories=month_levels)
    prod_line_by_month_count['Year']=prod_line_by_month_count['Month_Year'].dt.year
    prod_line_by_month_count['Month']=prod_line_by_month_count['Month_Year'].dt.month_name()
    prod_line_by_month_mean_count=prod_line_by_month_count.groupby('Month')['count'].mean().reset_index()
    prod_line_by_month_mean_count['Month'] = pd.Categorical(prod_line_by_month_mean_count['Month'], categories=month_levels)
    prod_line_by_year=prod_line_by_month.groupby('Year')[['Commissions',"Net"]].sum().reset_index()
    prod_line_by_year_count=prod_line_by_month_count.groupby('Year')['count'].sum().reset_index()
    prod_line_by_year_count['Year']=pd.Categorical(prod_line_by_year_count['Year'],pd.Series([2015,2016,2017,2018,2019,2020,2021,2022,2023]))
    tab11, tab12, tab13 = st.tabs(["Σύνολο Συμβολαίων", "Καθαρά", "Προμήθειες"])
    with tab11:
        tab111,tab112=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab111:
            fig_line_polcou = px.bar(prod_line_by_year_count, 
                            x="Year", y="count", 
                            title='Σύνολο συμβολαίων ανά έτος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'Σύνολο συμβολαίων','Year':'Έτος'},width=500,text_auto=True)
            fig_line_polcou.update_traces(textfont_size=17, textangle=0, 
                                        textposition="outside", cliponaxis=False)
            fig_line_polcou.update_layout(plot_bgcolor='white',font_size=15)
            st.write(fig_line_polcou)
        with tab112:
            plat_count_by_year=All2[["Year","Platform"]].value_counts().reset_index()
            plat_count_by_year_bar = px.bar(plat_count_by_year, 
                            x="Year", y="count", color="Platform",barmode="group",
                            title='Σύνολο συμβολαίων ανά έτος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'Σύνολο συμβολαίων','Year':'Έτος','Platform':'Πλατφόρμα'},width=900,text_auto=True)
            plat_count_by_year_bar.update_traces(textfont_size=17, textangle=0, 
                                        textposition="outside", cliponaxis=False)
            plat_count_by_year_bar.update_layout(plot_bgcolor='white',font_size=15)
            st.write(plat_count_by_year_bar)
        tab113,tab114=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab113:  
            fig_line_polcou = px.line(prod_line_by_month_count, 
                            x="Month_Year", y="count", 
                            title='Σύνολο συμβολαίων ανά μήνα',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'Σύνολο συμβολαίων','Month_Year':'Μήνας-Έτος'},markers=True)
            fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_polcou)
        with tab114:
            plat_count_by_year=All2[["Month_Year","Platform"]].value_counts().reset_index() 
            plat_count_by_year['Month_Year']=pd.to_datetime(plat_count_by_year['Month_Year'],format='mixed')
            plat_count_by_year=plat_count_by_year.sort_values('Month_Year')  
            fig_line_plat_count_by_year = px.line(plat_count_by_year, 
                            x="Month_Year", y="count", color='Platform',
                            title='Σύνολο συμβολαίων ανά μήνα απο την έναρξη επαγγέλματος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'Σύνολο συμβολαίων','Month_Year':'Μήνας-Έτος','Platform':'Πλατφόρμα'},markers=True)
            fig_line_plat_count_by_year.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_plat_count_by_year)
        tab115,tab116=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab115:
            fig_line_polcou = px.line(prod_line_by_month_mean_count.sort_values('Month'), 
                            x="Month", y="count", 
                            title='Σύνολο συμβολαίων ανά μήνα απο την έναρξη επαγγέλματος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'Σύνολο συμβολαίων','Month':'Μήνας'},markers=True)
            fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_polcou)

        with tab116:
            
            plat_count_by_month=All2[["Month_Year","Month","Platform"]].value_counts().reset_index().groupby(["Month","Platform"])['count'].mean().reset_index()
            plat_count_by_month=plat_count_by_month.sort_values('Month')              
            fig_line_plat_count_by_month = px.line(plat_count_by_month, 
                            x="Month", y="count", color='Platform',
                            title='Σύνολο συμβολαίων ανά μήνα',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'Σύνολο συμβολαίων','Month':'Μήνας','Platform':'Πλατφόρμα'},markers=True)
            fig_line_plat_count_by_month.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_plat_count_by_month)


    plat_sum_by_year=All2.groupby(["Year","Platform"])[['Net','Commissions']].sum().reset_index()
    plat_monthyear_sum=All2.groupby(["Month_Year","Platform"])[['Net','Commissions']].sum().reset_index()
    plat_monthyear_sum['Month_Year']=pd.to_datetime(plat_monthyear_sum['Month_Year'],format='mixed')
    plat_monthyear_sum=plat_monthyear_sum.sort_values('Month_Year')
    plat_month_mean=All2.groupby(['Month_Year',"Platform"])[['Net','Commissions']].sum().reset_index()
    plat_month_mean['Month_Year']=pd.to_datetime(plat_month_mean['Month_Year'],format='mixed')
    plat_month_mean['Month']=plat_month_mean['Month_Year'].dt.month_name()
    plat_month_mean['Month'] = pd.Categorical(plat_month_mean['Month'], categories=month_levels)
    plat_month_mean=plat_month_mean.groupby(["Month",'Platform'])[['Net','Commissions']].mean().reset_index()
    plat_month_mean=plat_month_mean.sort_values('Month')                    
    with tab12:
        tab121,tab122=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab121:
            fig_line_polcou = px.bar(prod_line_by_year, 
                            x="Year", y="Net", 
                            title='Καθαρά ασφάλιστρα ανά έτος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Net':'Καθαρά €','Year':'Έτος'},width=500,text='Net')
            fig_line_polcou.update_traces(textfont_size=17,texttemplate = '%{text:.3s} €', textangle=0, textposition="outside", cliponaxis=False)
            fig_line_polcou.update_layout(plot_bgcolor='white',font_size=15)
            st.write(fig_line_polcou)
        with tab122:
            plat_sum_by_year_net = px.bar(plat_sum_by_year, 
                            x="Year", y="Net", color='Platform',barmode='group',
                            title='Καθαρά ασφάλιστρα ανά έτος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Net':'Καθαρά €','Year':'Έτος','Platform':'Πλατφόρμα'},width=1000,text='Net')
            plat_sum_by_year_net.update_traces(textfont_size=17,texttemplate = '%{text:.3s} €', textangle=0, textposition="outside", cliponaxis=False)
            plat_sum_by_year_net.update_layout(plot_bgcolor='white',font_size=15)
            st.write(plat_sum_by_year_net)

        tab123,tab124=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab123:
            fig_line_net = px.line(prod_line_by_month, 
                            x="Month_Year", y="Net", 
                            title='Κάθαρα Ασφάλιστρα ανά μήνα ',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Net':'Καθαρά €','Month_Year':'Μήνας-Έτος'},markers=True)
            fig_line_net.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_net)
        
        with tab124:
            plat_monthyear_sum_net = px.line(plat_monthyear_sum, 
                            x="Month_Year", y="Net", color='Platform',
                            title='Κάθαρα Ασφάλιστρα ανά μήνα ',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Net':'Καθαρά €','Month_Year':'Μήνας-Έτος','Platform':'Πλατφόρμα'},markers=True)
            plat_monthyear_sum_net.update_layout(plot_bgcolor='white',font_size=13)
            st.write(plat_monthyear_sum_net)
        
        tab125,tab126=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab125:
            fig_line_polcou = px.line(prod_line_by_month_mean.sort_values('Month'), 
                            x="Month", y="Net", 
                            title='Μέσος όρος καθαρών ασφαλίστρων ανά μήνα',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Net':'Καθαρά €','Month':'Μήνας'},markers=True)
            fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_polcou)
        with tab126:
            plat_month_mean_net = px.line(plat_month_mean, 
                            x="Month", y="Net", color='Platform',
                            title='Μέσος όρος καθαρών ασφαλίστρων ανά μήνα',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Net':'Καθαρά €','Month':'Μήνας','Platform':'Πλατφόρμα'},markers=True)
            plat_month_mean_net.update_layout(plot_bgcolor='white',font_size=13)
            st.write(plat_month_mean_net)

    with tab13:
        tab131,tab132=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab131:
            fig_line_polcou = px.bar(prod_line_by_year, 
                            x="Year", y="Commissions", 
                            title='Προμήθειες ανά έτος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Commissions':'Προμήθειες €','Year':'Έτος'},width=500,text='Commissions')
            fig_line_polcou.update_traces(textfont_size=17,texttemplate = '%{text:.3s} €', textangle=0, textposition="outside", cliponaxis=False)
            fig_line_polcou.update_layout(plot_bgcolor='white',font_size=15)
            st.write(fig_line_polcou)
        with tab132:
            plat_sum_by_year_com = px.bar(plat_sum_by_year, 
                            x="Year", y="Commissions", color='Platform',barmode='group',
                            title='Προμήθειες ανά έτος',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Commissions':'Προμήθειες €','Year':'Έτος','Platform':'Πλατφόρμα'},width=1000,text='Commissions')
            plat_sum_by_year_com.update_traces(textfont_size=17,texttemplate = '%{text:.3s} €', textangle=0, textposition="outside", cliponaxis=False)
            plat_sum_by_year_com.update_layout(plot_bgcolor='white',font_size=15)
            st.write(plat_sum_by_year_com)
        tab133,tab134=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab133:        
            fig_line_com = px.line(prod_line_by_month, 
                            x="Month_Year", y="Commissions", 
                            title='Προμήθειες ανά μήνα',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Commissions':'Προμήθειες €','Month_Year':'Μήνας-Έτος'},markers=True)
            fig_line_com.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_com)

        with tab134:
            plat_monthyear_sum_com = px.line(plat_monthyear_sum, 
                            x="Month_Year", y="Commissions", color='Platform',
                            title='Προμήθειες ανά μήνα ',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Commissions':'Προμήθειες €','Month_Year':'Μήνας-Έτος','Platform':'Πλατφόρμα'},markers=True)
            plat_monthyear_sum_net.update_layout(plot_bgcolor='white',font_size=13)
            st.write(plat_monthyear_sum_com)
        tab135,tab136=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
        with tab135:
            fig_line_polcou = px.line(prod_line_by_month_mean.sort_values('Month'), 
                            x="Month", y="Commissions", 
                            title='Μέσος όρος προμηθειών ανά μήνα',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Commissions':'Προμήθειες €','Month':'Μήνας'},markers=True)
            fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
            st.write(fig_line_polcou)
        with tab136:
            plat_month_mean_net = px.line(plat_month_mean, 
                            x="Month", y="Commissions", color='Platform',
                            title='Μέσος όρος προμηθειών ανά μήνα',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'Commissions':'Προμήθειες €','Month':'Μήνας','Platform':'Πλατφόρμα'},markers=True)
            plat_month_mean_net.update_layout(plot_bgcolor='white',font_size=13)
            st.write(plat_month_mean_net)


with tab2:
    st.write("### Συνολική παραγωγή ανά κλάδο ασφάλισης")
    col1,col2,col3=st.columns(3)
    with col1:
        categories_countpol=All2['Category'].value_counts().reset_index()
        fig_barplot=px.bar(categories_countpol.sort_values("count"),x='count',y='Category',title='',
                            labels={'count':'Σύνολο Συμβολαίων','Category':'Κλάδος'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,
                        text_auto=True,width=1000,height=700)
        fig_barplot.update_traces(textfont_size=20, textangle=0, textposition="inside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
    with col2:
        categories_net=All2.groupby('Category')['Net'].sum().reset_index()
        categories_net_sorted=categories_net.sort_values('Net',ascending=True)
        fig_barplot=px.bar(categories_net_sorted,x='Net',y='Category',title='',
                            labels={'Net':'Καθαρά €','Category':'Κλάδος'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text='Net',width=1000,height=700)
        fig_barplot.update_traces(textfont_size=17, texttemplate = '%{text:.3s} €',textangle=0, textposition="inside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=40)
        st.write(fig_barplot)
    with col3:
        categories_comm=All2.groupby('Category')['Commissions'].sum().reset_index()
        categories_comm_sorted=categories_comm.sort_values('Commissions',ascending=True)
        fig_barplot=px.bar(categories_comm_sorted,x='Commissions',y='Category',title='',
                            labels={'Commissions':'Προμήθειες €','Category':'Κλάδος'},
                        color_discrete_sequence= px.colors.sequential.Blugrn,text='Commissions',width=1000,height=700)
        fig_barplot.update_traces(textfont_size=17, texttemplate = '%{text:.2s} €',textangle=0, 
                                    textposition="inside", cliponaxis=False)
        fig_barplot.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_barplot)
    st.write("### Εξέλιξη παραγώγης ανά έτος σε κάθε κλάδος ασφάλισης")
    tabs21,tabs22,tabs23=st.columns(3)
    with tabs21:
        cat_sum_year=pd.merge(All2.groupby(['Category','Year'])[['Commissions','Net']].sum().reset_index(),All2[['Category','Year']].value_counts().reset_index())
        fig_line_polcou = px.line(cat_sum_year, 
                                    x="Year", y="count", color='Category',
                                    title='Σύνολο συμβολαίων',
                                    color_discrete_sequence= px.colors.sequential.Aggrnyl,
                                    labels={'count':'Σύνολο συμβολαίων','Year':'Έτος',"Category":"Κλάδος"},markers=True)
        fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
        st.write(fig_line_polcou)

    with tabs22:
        fig_line_polcou = px.line(cat_sum_year, 
                                    x="Year", y="Net", color='Category',
                                    title='Καθαρά ασφάλιστρά',
                                    color_discrete_sequence= px.colors.sequential.Aggrnyl,
                                    labels={'Net':'Καθαρά','Year':'Έτος',"Category":"Κλάδος"},markers=True)
        fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
        st.write(fig_line_polcou)    
    with tabs23:
        fig_line_polcou = px.line(cat_sum_year, 
                                    x="Year", y="Commissions", color='Category',
                                    title='Προμήθειες',
                                    color_discrete_sequence= px.colors.sequential.Aggrnyl,
                                    labels={'Commissions':'Προμήθειες','Year':'Έτος',"Category":"Κλάδος"},markers=True)
        fig_line_polcou.update_layout(plot_bgcolor='white',font_size=13)
        st.write(fig_line_polcou)

    tabs24,tabs25,tabs26=st.tabs(['Συμβόλαια','Καθαρά Ασφάλιστρα',"Προμήθειες"])
    cat_mean_month=pd.merge(All2[['Category','Month','Month_Year']].value_counts().reset_index().groupby(['Month',"Category"])['count'].mean().reset_index().round(1), All2.groupby(['Category','Month','Month_Year'])[["Net","Commissions"]].sum().reset_index().groupby(['Month',"Category"])[["Net","Commissions"]].mean().reset_index().round(1))
    with tabs24:
        st.write("### Συνολικά συμβόλαια ανά μήνα από κάθε κλάδο ασφάλισης κατά μέσο όρο")
        cat_mean_month_cou=px.bar(cat_mean_month,x='Month',y='count',title='',
                        labels={'count':'Συνολικά συμβόλαια','Category':'Κλάδος'},color='Category',
                    color_discrete_sequence= px.colors.sequential.Blugrn,text='count',width=1000,height=700)
        cat_mean_month_cou.update_traces(textfont_size=17, texttemplate = '%{text:.2s}',textangle=0, 
                                    textposition="inside", cliponaxis=False)
        cat_mean_month_cou.update_layout(plot_bgcolor='white',font_size=15)
        st.write(cat_mean_month_cou)
    with tabs25:
        st.write("### Καθαρά ασφάλιστρα ανά μήνα από κάθε κλάδο ασφάλισης κατά μέσο όρο")
        cat_mean_month_com=px.bar(cat_mean_month,x='Month',y='Commissions',title='',
                        labels={'Net':'Καθαρά ασφάλιστρα','Category':'Κλάδος'},color='Category',
                    color_discrete_sequence= px.colors.sequential.Blugrn,text='Net',width=1000,height=700)
        cat_mean_month_com.update_traces(textfont_size=17, texttemplate = '%{text:.2s}',textangle=0, 
                                    textposition="inside", cliponaxis=False)
        cat_mean_month_com.update_layout(plot_bgcolor='white',font_size=15)
        st.write(cat_mean_month_com)
    with tabs26:
        st.write("### Προμήθειες ανά μήνα από κάθε κλάδο ασφάλισης κατά μέσο όρο")
        cat_mean_month_com=px.bar(cat_mean_month,x='Month',y='Commissions',title='',
                        labels={'Commissions':'Προμήθειες','Category':'Κλάδος'},color='Category',
                    color_discrete_sequence= px.colors.sequential.Blugrn,text='Commissions',width=1000,height=700)
        cat_mean_month_com.update_traces(textfont_size=17, texttemplate = '%{text:.2s}',textangle=0, 
                                    textposition="inside", cliponaxis=False)
        cat_mean_month_com.update_layout(plot_bgcolor='white',font_size=15)
        st.write(cat_mean_month_com)
    cat_dur_mean_month=All2[['Category','Month','Month_Year',"Duration_gr"]].value_counts().reset_index().groupby(['Month',"Category","Duration_gr"])['count'].mean().reset_index().round(1)
    st.write("### Συνολικά συμβόλαια ανά κλάδο ασφάλισης και οι διάρκειες τους")
    option1 = st.selectbox("Κλάδος Ασφάλισης",pd.unique(cat_dur_mean_month['Category']))
    cat_mean_month_com=px.bar(cat_dur_mean_month[cat_dur_mean_month['Category']==option1],x='Month',y='count',title='',
                    labels={'count':'Συνολικά συμβόλαια','Category':'Κλάδος','Month':'Μήνας',"Duration_gr":'Διάρκεια Συμβολαίων'},color='Duration_gr',
                color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,width=1000,height=700)
    cat_mean_month_com.update_traces(textfont_size=17,textangle=0, 
                                textposition="inside", cliponaxis=False)
    cat_mean_month_com.update_layout(plot_bgcolor='white',font_size=15)
    st.write(cat_mean_month_com)
with tab3:
    client_dis_count=All2[['District',"id"]].value_counts().reset_index().groupby('District').count().reset_index()
    st.write("### Νομοί πελάτων που ασφαλίζονται")
    cat_mean_month_com=px.bar(client_dis_count.sort_values('count'),y='District',x='count',title='',
                    labels={'District':'Νομός','count':'Σύνολο Πελατών'},
                color_discrete_sequence= px.colors.sequential.Blugrn,text_auto=True,width=1000,height=1500)
    cat_mean_month_com.update_traces(textfont_size=17, textangle=0, 
                                textposition="outside", cliponaxis=False)
    cat_mean_month_com.update_layout(plot_bgcolor='white',font_size=15)
    st.write(cat_mean_month_com)

with tab4:
    select_durations=All2.loc[(All2['Duration']==1)|(All2['Duration']==3)|(All2['Duration']==6)|(All2['Duration']==12)]
    select_duration_total_year=(select_durations[['Duration_gr','Month','Year']].value_counts().reset_index()).groupby(['Year',"Duration_gr"])['count'].sum().round(1).reset_index()
    tabs51,tabs52=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
    with tabs51:
        fig_dur_bar = px.bar(select_duration_total_year.loc[select_duration_total_year['Duration_gr']!="Άλλη"], 
                            x="Year", y="count", 
                            title='Χρονικές διάρκειες συμβολαίων ανά έτος (Συνολικά)',color='Duration_gr',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'# Συμβολαίων','Year':'Έτος',"Duration_gr":'Διάρκεια συμβολαίου'},
                            width=900,text='count',height=800)
        fig_dur_bar.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_dur_bar)
    with tabs52:
        select_duration_total_year_plat=select_durations[['Duration_gr','Platform','Year']].value_counts().reset_index()
        fig_dur_bar = px.bar(select_duration_total_year_plat.loc[select_duration_total_year_plat['Duration_gr']!="Άλλη"], 
                            x="Platform", y="count", facet_col='Year',facet_col_wrap=5,
                            title='Χρονικές διάρκειες συμβολαίων ανά έτος (Συνολικά)',color='Duration_gr',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'# Συμβολαίων','Year':'Έτος',"Duration_gr":'Διάρκεια συμβολαίου','Platform':'Πλατφόρμα'},
                            width=1200,text='count',height=1000)
        fig_dur_bar.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_dur_bar)       
    tabs53,tabs54=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
    with tabs53:
        select_duration_total=select_durations[['Duration_gr','Month']].value_counts().reset_index().sort_values(['Duration_gr','Month'])
        fig_dur_bar = px.bar(select_duration_total, 
                            x="Month", y="count", 
                            title='Χρονικές διάρκειες συμβολαίων ανά μήνα (Συνολικά)',color='Duration_gr',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'# Συμβολαίων','Month':'Μήνας',"Duration_gr":'Διάρκεια συμβολαίου'},
                            width=1000,text='count')
        fig_dur_bar.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_dur_bar)
    with tabs54:        
        select_duration_total_plat=select_durations[['Duration_gr','Platform','Month']].value_counts().reset_index().sort_values(['Duration_gr','Month'])
        fig_dur_bar = px.bar(select_duration_total_plat, 
                            x="Platform", y="count",facet_col='Month',facet_col_wrap=6, 
                            title='Χρονικές διάρκειες συμβολαίων ανά μήνα (Συνολικά)',color='Duration_gr',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'# Συμβολαίων','Month':'Μήνας',"Duration_gr":'Διάρκεια συμβολαίου','Platform':'Πλατφόρμα'},
                            width=1500,text='count',height=1200)
        fig_dur_bar.update_traces(textfont_size=17, textangle=0, textposition="outside", cliponaxis=False)
        fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_dur_bar)
    tabs55,tabs56=st.tabs(["Σύνολικα","Σύγκριση ανά πλατφόρμα"])
    with tabs55:
        select_duration_mean=(select_durations[['Duration_gr','Month','Year']].value_counts().reset_index()).groupby(['Month',"Duration_gr"])['count'].mean().round(1).reset_index()
        fig_dur_bar = px.line(select_duration_mean.loc[select_duration_mean['Duration_gr']!="Άλλη"], 
                            x="Month", y="count", 
                            title='Χρονικές διάρκειες συμβολαίων ανά μήνα (Μέσος όρος)',color='Duration_gr',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'# Συμβολαίων','Month':'Μήνας',"Duration_gr":'Διάρκεια συμβολαίου'},
                            width=1000,height=1000,markers=True)
        fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_dur_bar)
    with tabs56:
        select_duration_mean=(select_durations[['Duration_gr','Month','Platform']].value_counts().reset_index()).groupby(['Month',"Duration_gr",'Platform'])['count'].mean().round(1).reset_index()
        fig_dur_bar = px.line(select_duration_mean.loc[select_duration_mean['Duration_gr']!="Άλλη"], 
                            x="Month", y="count",facet_col='Platform', facet_col_wrap=2,
                            title='Χρονικές διάρκειες συμβολαίων ανά μήνα (Μέσος όρος)',color='Duration_gr',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl,
                            labels={'count':'# Συμβολαίων','Month':'Μήνας',"Duration_gr":'Διάρκεια συμβολαίου','Platform':'Πλατφόρμα'},
                            width=2000,height=1000,markers=True)
        fig_dur_bar.update_layout(plot_bgcolor='white',font_size=15)
        st.write(fig_dur_bar)



