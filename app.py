import pandas as pd  # pandas use for import data in project
import streamlit as st # steamlit use for localhost
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import preprocessor,helper
df=pd.read_csv("athlete_events.csv")
region=pd.read_csv("noc_regions.csv")

st.sidebar.image('https://www.pngall.com/wp-content/uploads/10/Olympics-PNG-Clipart.png',use_column_width=True)
df=preprocessor.preprocessor(df,region)
st.sidebar.title("OLYMPICS DATA ANALYSIS")
user_menu=st.sidebar.radio("Select a Option",("Medal Tally",'Overall Analysis','Country-wise Analysis','Athlete wise Analysis'))

if user_menu=='Medal Tally':
    st.sidebar.header('Medal Tally')

    years,country=helper.country_year_list(df)
    # sidebar.selectbox()this function create a select box to select a option
    select_year=st.sidebar.selectbox('select year',years) # this is for select a year
    select_country=st.sidebar.selectbox('select country',country) # this is for select a country name
    medal_tally=helper.fetch_medal_tally(df,select_year,select_country)
    if select_year=='overall'and select_country=='overall':
        st.title('Overall Tally')
    if select_year!='overall'and select_country=='overall':
        st.title("Medal Tally in  " + str(select_year) + "  Olympics")
    if select_year=='overall' and select_country!='overall':
        st.title(select_country + "  overall performance")
    if select_year!='overall'and select_country!='overall':
        st.title(select_country  +  "  performance in  "  +  str(select_year)+"  Olympics")

    st.table(medal_tally)
if user_menu=="Overall Analysis":
    st.header('Top Statistics')
    # number of Year
    Edition = df['Year'].unique().shape[0] - 1
    # number of City
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    # number of Event
    events = df['Event'].unique().shape[0]
    # number of Athletes
    athletes = df['Name'].unique().shape[0]
    # number of participating nations
    nations = df['region'].unique().shape[0]
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(Edition)
    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)

    nations_over_timer=helper.data_over_time(df,'region')
    fig=px.line(nations_over_timer,x="Edition",y="region")
    title_text="<h1 style='color: orange;'>Participating Nations Over The Year<h1>"
    st.markdown(title_text,unsafe_allow_html=True)
    st.plotly_chart(fig)

    events_over_timer=helper.data_over_time(df,'Event')
    fig=px.line(events_over_timer,x="Edition",y="Event")
    title_text="<h1 style='color: orange;'>Event Over The Year<h1>"
    st.markdown(title_text,unsafe_allow_html=True)
    st.plotly_chart(fig)

    athletes_over_timer = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_timer, x="Edition", y="Name")
    title_text = "<h1 style='color: orange;'>Athletes Over The Year<h1>"
    st.markdown(title_text, unsafe_allow_html=True)
    st.plotly_chart(fig)

    text="<h1 style='color: orange ;'>No. of Events over time (Every Sport)<h1>"
    st.markdown(text,unsafe_allow_html=True)
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(['Year','Sport','Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    # most successful atheletes
    text_successful = "<h1 style='color: red;'>MOST SUCCESS ATHELETS<h1>"
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Select a Sport')
    st.title('Select a Sport')
    selected_sport = st.selectbox("Select a Sport", sport_list)
    if selected_sport != 'Select a Sport':
        st.markdown(text_successful, unsafe_allow_html=True)
        x = helper.most_successful(df, selected_sport)
        st.table(x)
    #
if user_menu=='Country-wise Analysis':
        # yearwise medal tally
        text_yearwise = "<h1 style='color: Slate Blue ;'>Country Wise Analysis<h1>"
        st.sidebar.markdown(text_yearwise,unsafe_allow_html=True)
        country = df['region'].dropna().unique().tolist()
        country.sort()
        country.insert(0,'Select a Country')

        selected_country = st.sidebar.selectbox('Select a Country', country)
        yearwise_medaltally = helper.yearwise_medal_tally(df, selected_country)
        plot = px.line(yearwise_medaltally, x='Year', y='Medal')
        st.title(selected_country +' '+ "Medal Tally Over The Years")
        st.plotly_chart(plot)

        # heatmap by selected_country
        text_color=f"<h1 style='color: green;'>{selected_country}   excels in the following sports<h1> "
        st.markdown(text_color,unsafe_allow_html=True)
        pt=helper.country_heatmap(df,selected_country)
        fig,ax=plt.subplots(figsize=(20,20))
        ax=sns.heatmap(pt,annot=True)
        st.pyplot(fig)

        st.title('Top 10 '+'  ' +selected_country + '  ' +" Successful Athelets ")
        top10df=helper.most_athelets(df,selected_country)
        st.table(top10df)
if user_menu=='Athlete wise Analysis':
   athletes_df=df.drop_duplicates(subset=['Name','region'])

   x1=athletes_df['Age'].dropna()
   x2=athletes_df[athletes_df['Medal']=='Gold']['Age'].dropna()
   x3=athletes_df[athletes_df['Medal']=='Silver']['Age'].dropna()
   x4=athletes_df[athletes_df['Medal']=='Bronze']['Age'].dropna()
   fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
   fig.update_layout(autosize=False,width=1000,height=600)
   t1=("<h1><span style='color: orange;'> Distrubution </span><span style='color: green;'> Of </span><span style='color: red;'> Age </span></h1>")


   st.markdown(t1,unsafe_allow_html=True)
   st.plotly_chart(fig)

   # age disturibution by sports

   x = []
   name = []
   famous_sport = ["Basketball", "Judo", "Football", "Tug-Of-War", "Athletics", "Swimming", "Badminton", "Sailing",
                   "Gymnastics", "Art Competitions", "Handball", "Weightlifting", "Wrestling", "Water Polo", "Hockey",
                   "Rowing", "Fencing", "Shooting", "Boxing", "Taekwondo", "Cycling", "Diving", "Canoeing", "Tennis",
                   "Golf", "Softball", "Archery", "Volleyball", "Synchronized Swimming", "Table Tennis", "Baseball",
                   "Rhythmic Gymnastics", "Rugby Sevens", "Beach Volleyball", "Triathlon", "Rugby", "Polo",
                   "Ice Hockey"]
   for sport in famous_sport:
       temp_df = athletes_df[athletes_df['Sport'] == sport]
       x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
       name.append(sport)
   fig1 = ff.create_distplot(x, name, show_hist=False, show_rug=False)
   fig1.update_layout(autosize=False, width=1000, height=700)
   t2 = "<h1><b><span style='color:Gray;'> Distrubution Of Age w.r.t Sport(Gold Medalist)</span></b></h1>"
   st.markdown(t2, unsafe_allow_html=True)
   st.plotly_chart(fig1)


   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0, 'Overall')
   st.title('Height Vs Weight')
   selected_sport = st.selectbox("Select a Sport", sport_list)
   temp_df= helper.weight_height(df,selected_sport)
   fig,ax = plt.subplots()


   # Plot the scatter plot
   ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'], hue=temp_df["Medal"], style=temp_df['Sex'], s=60)
   st.pyplot(fig)


   # Men vs Women
   st.title('Men Vs Women')
   final=helper.men_women_athletes(df)
   fig=px.line(final,x="Year",y=['Male','Female'])
   st.plotly_chart(fig)













































