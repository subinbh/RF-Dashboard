import pandas as pd 
import plotly.express as px
import streamlit as st
import numpy as np

st.set_page_config(page_title="WSD O&M RF  Works Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)

df = pd.read_excel(
    io='rfworkdata.xlsx',
    engine="openpyxl",
    sheet_name="RF",
    usecols='B:P',
    nrows=1000

)
logo_path="ntc_logo.jpg"
st.sidebar.image(logo_path)

st.sidebar.header("Please Filter")
task_category = st.sidebar.multiselect(
    "Select The TaskCategory",
    options=df['TaskCategory'].unique(),
    default=(df['TaskCategory'].unique())

    )

task_subcategory = st.sidebar.multiselect(
    "Select The Task Sub Category",
    options=df['TaskType'].unique(),
    default=(df['TaskType'].unique())

    )

region = st.sidebar.multiselect(
    "Select The Region",
    options=df['Region'].unique(),
    default=(df['Region'].unique())

    )


taskstatus = st.sidebar.multiselect(
    "Select The Task Status",
    options=df['TaskStatus'].unique(),
    default=(df['TaskStatus'].unique())

    )

df_selection = df.query(
    "TaskCategory == @task_category & TaskType == @task_subcategory & Region == @region"
)
df_selection['Date'] = pd.to_datetime(df_selection['Date'], format='%Y-%m-%d')

start_date = '2024-05-07'
end_date = '2024-06-10'
mask = (df_selection['Date'] > start_date) & (df_selection['Date'] <= end_date) 
  
df_selection = df_selection.loc[mask] 
print(df_selection) 






st.title("📶 WSD O&M RF  Task  Dashboard")
st.dataframe(df_selection)
st.title(":bar_chart: WSD O&M  Summary  of RF Work ")
st.markdown("##")
# Top KPIS
total_work = df_selection["TaskCategory"].count()
oss_optimization = sum(df_selection['TaskCategory']=="OSS Optimization")
rf_complain =   sum(df_selection['TaskCategory']=="Network RF Complain ")
network_coverage_expansion = sum(df_selection['TaskCategory']=="Network Coverage Expansion")
network_quality_improvement= sum(df_selection['TaskCategory']=="Network Quality Improvement")
others_work=  sum(df_selection['TaskCategory']=="Others")
network_quality_test=sum(df_selection['TaskCategory']=="Network Quality Test")

highgainantenna= sum(df_selection['TaskType']=="High Gain Antenna")
repeater = sum(df_selection['TaskType']=="Repeater")
sectorexpansion=sum(df_selection['TaskType']=="Sector Expansion")
smallcell=sum(df_selection['TaskType']=="Small Cell")
drivetest= sum(df_selection['TaskType']=="Drive Test")
rfparameteroptimization= sum(df_selection['TaskType']=="RF Parameter Optimization")
neighboraudit= sum(df_selection['TaskType']=="Neighbor Audit")
sitesurvey= sum(df_selection['TaskType']=="Site Survey")
featureimplementation= sum(df_selection['TaskType']=="Feature Implementation")
sectorexpansionsurvey= sum(df_selection['TaskType']=="Sector Expansion Survey")
drivetestoptimization= sum(df_selection['TaskType']=="Drive Test & Optimization")
gaddition= sum(df_selection['TaskType']=="2G Addition")


left_column,middle_column,right_column,last_column = st.columns(4)

with left_column:
    st.subheader("Total Tasks")
    st.subheader (f"{total_work}")
with middle_column:
    st.subheader("RF Complain")
    st.subheader (f"{rf_complain}")
with right_column:
    st.subheader("OSS Optimization")
    st.subheader (f"{oss_optimization}")
with last_column:
    st.subheader("Coverage Expansion")
    st.subheader (f"{network_coverage_expansion}")


#st.markdown("---")


data = {'TaskName':['Network RF Complain', 'OSS Optimization', 'Network Coverage Expansion','Network Quality Improvement','Network Quality Test',
'Others'], 'count':[rf_complain, oss_optimization, network_coverage_expansion,network_quality_test,network_quality_improvement,others_work]}

df_for_chart = pd.DataFrame(data)
df_for_chart.sort_values(by=['count'], ascending=False)
#print (df_for_chart )

fig_task_bar = px.bar(
    df_for_chart,
    x="count",
    y="TaskName",
    orientation="h",
    title="<b> RF Works By Category</b>",
    color_discrete_sequence=['#0083B8']*len(df_for_chart),
    template= "plotly_white",
    


)
fig_task_bar.update_layout(
plot_bgcolor="rgba(0,0,0,0)",
xaxis=(dict(showgrid=False))
)

data_task_subcat= {'TaskType':['High Gain Antenna', 'Repeater', 'Sector Expansion','Small Cell','Drive Test','RF Parameter Optimization','Neighbor Audit','Feature Implementation','Drive Test & Optimization','2G Addition','Site Survey'], 'count':[highgainantenna, repeater, sectorexpansion,smallcell,drivetest,rfparameteroptimization,neighboraudit,featureimplementation,drivetestoptimization,gaddition,sitesurvey]}
df_task_subcategory=pd.DataFrame(data_task_subcat)

fig_task_bar_subcat = px.bar(
    df_task_subcategory,
    x="count",
    y="TaskType",
    orientation="h",
    title="<b> RF Works By Sub Category</b>",
    color_discrete_sequence=['#0083B8']*len(df_task_subcategory),
    template= "plotly_white",
    


)
fig_task_bar_subcat.update_layout(
plot_bgcolor="rgba(0,0,0,0)",
xaxis=(dict(showgrid=False))
)
#st.plotly_chart(fig_task_bar)

st.markdown("---")


left_column,right_column = st.columns(2)

with left_column:
    #st.subheader("Total Tasks:")
    st.plotly_chart(fig_task_bar)

with right_column:
    #st.subheader("Network Coverage Expansion:")
    st.plotly_chart(fig_task_bar_subcat)


st.markdown("---")
left_column,right_column = st.columns(2)

fig_cat_bar = px.pie(df_for_chart, values='count', names='TaskName', title='RF Works By Category')
fig_subcat_bar = px.pie(df_task_subcategory, values='count', names='TaskType', title='RF Works By Sub Category')

with left_column:
        st.plotly_chart(fig_cat_bar)

with right_column:
        st.plotly_chart(fig_subcat_bar)

st.markdown("---")

#df_selection['Date'] = pd.to_datetime(df_selection['Date'], format='%Y-%m-%d')
#total_task_day_df = df_selection["Date"]
#print (df_selection['Date'])
#print (total_task_day_df)
#line_chart = px.line(, x='date', y=["MSFT","GOOG",'FB',"AMZN"])
#count = df_selection.groupby('Date').count()
#print(count)





# Count occurrences of each date
date_counts = df_selection['Date'].value_counts().reset_index()
date_counts.columns = ['Date', 'Count']

# Merge counts back into the original DataFrame
df1 = df_selection.merge(date_counts, on='Date')

# Drop duplicates based on 'Date'
df1 = df1.drop_duplicates(subset=['Date'])

# Reset index for a clean DataFrame
df1 = df1.reset_index(drop=True)
df1.sort_values(by=['Date'])


fig_line_chart=px.bar(df1,x='Date',y='Count',title="Day Wise Work Distribution",width=1400,height=900)
st.plotly_chart(fig_line_chart)
st.markdown("---")
#df_cordinate=df_selection.loc[df_selection['TaskCategory'] == 'Network RF Complain']
#print(df_cordinate)
fig = px.scatter_geo(df_selection,lat='Lat',lon='Lon', hover_name="TaskType",width=1400,height=900)
#px.set_mapbox_access_token("AIzaSyAlrIsXH6ZKfiUNkOyceW5dxoOCXqFqEH8")
#fig = px.scatter_mapbox(df_selection,lat='Lat',lon='Lon', hover_name="TaskType",width=1400,height=900,zoom=15,mapbox_style='satellite')
#fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(title = 'RF Work Distribution Map', title_x=0.5)

#st.plotly_chart(fig)

#map = folium.Map(location=[13.406, 80.110], tiles="CartoDB Positron", zoom_start=9)

#st.plotly_chart(fig)
#map
df_point = df_selection[['Lat','Lon','TaskType','Address']]
df_point=df_point.rename(columns={'Lat':'LATITUDE','Lon':'LONGITUDE','Address':'INFO'})
df_point=df_point.dropna()

print(df_point)
st.title("✔ Newtwork RF Complain Task Attained")
st.map(df_point)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p> <h3>Developed  by </h3> <a style='display: block; text-align: center;' href="#" target="_blank">Sr.Er Subin Bhatta <BR> WSD O&M  RF Department </a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)