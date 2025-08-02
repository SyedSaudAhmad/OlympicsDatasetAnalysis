import streamlit as st
import pandas as pd
import preprocess, helper
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns 
# --

df = pd.read_csv("athlete_events.csv")
region = pd.read_csv("noc_regions.csv")

df = preprocess.process(df,region)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/5/55/Olympic_rings_with_transparent_rims.svg")
user_menu = st.sidebar.radio(
    'Select as option',
    ('Medal Tally', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis')
)

# st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.year_country(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall' :
        st.title('Overall Tally')

    if selected_year != 'Overall' and selected_country == 'Overall' :
        st.title(f'Medal Tally in {str(selected_year)} Olympics')

    if selected_year == 'Overall' and selected_country != 'Overall' :
        st.title(f'{selected_country} Overall Performance')

    if selected_year != 'Overall' and selected_country != 'Overall' :
        st.title(f'{selected_country} Performance in {str(selected_year)} Olympics')
    st.dataframe(medal_tally)

    
if user_menu == 'Overall Analysis':

    st.title("Top Statistics")

    editions = df['Year'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    regions = df['region'].unique().shape[0]


    col1,col2,col3 = st.columns(3,border=True,vertical_alignment='center')

    with col1:
        st.header ('Editions')
        st.title(editions)
    with col2:
        st.header ('Hosts')
        st.title(cities)
    with col3:
        st.header ('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3,border=True,vertical_alignment='center')

    with col1:
        st.header ('Events')
        st.title(events)
    with col2:
        st.header ('Nations')
        st.title(regions)
    with col3:
        st.header ('Athletes')
        st.title(athletes)

    st.write("#")
    nationOverTime = helper.data_over_time(df,'region')
    st.title('Participating Nations over the years')
    st.line_chart(nationOverTime, x='Year', y='count', x_label='Year', y_label='Number of Participating Country')
    
    st.write("#")
    EventOverTime = helper.data_over_time(df,'Event')
    st.title('Events over the years')
    st.line_chart(EventOverTime, x='Year', y='count', x_label='Year', y_label='Total Events')

    st.write("#")
    AthleteOverTime = helper.data_over_time(df,'Name')
    st.title('Athletes Participated Over the years')
    st.line_chart(AthleteOverTime, x='Year', y='count', x_label='Year', y_label='Total Athletes Competited')

    st.write('#')
    st.title("No. of Events over time (All the sports)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(["Year",'Sport','Event'])
    sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.write('#')
    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select year', sport_list)
    x = helper.most_succesful(df,selected_sport)
    st.table(x)



if user_menu == 'Country wise Analysis':

    st.sidebar.title("Country-wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country',country_list)

    country_df  = helper.yearwise_medaltally(df,selected_country)
    fig = px.line(country_df,x='Year',y = 'Medal')
    st.title('Medal Tally over the years')
    st.plotly_chart(fig)


    st.title(selected_country + ' excels in the folowing sports')
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(f"Top 10 athletes of {selected_country}")
    top_df = helper.most_succesful_countryWise(df,selected_country)
    st.table(top_df)

if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']["Age"].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']["Age"].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']["Age"].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.write('#')
    st.title("Athlete's Prime Age")
    famous_sports = ['Basketball', 'Judo', 'Football', 'Athletics',
    'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Handball', 'Weightlifting', 
    'Wrestling','Water Polo', 'Hockey', 'Rowing', 'Fencing',
    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
    'Tennis',  'Golf', 'Softball', 'Archery',
    'Volleyball',  'Table Tennis', 'Baseball',
    'Rhythmic Gymnastics', 'Trampolining',
    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
    'Cricket', 'Ice Hockey', 'Motorboating',
    'Figure Skating','Art Competitions','Equestrianism','Tug-Of-War']
    famous_sports.sort()

    with st.container():
        col1, col2 =  st.columns(2,border=True)
        with col1:
            selected_sport = st.selectbox('Select Sport', famous_sports)
        with col2:
            selected_medal = st.selectbox('Select Medal', ["Gold","Silver","Bronze"])
    histdata = helper.athlete_prime(df,selected_sport,selected_medal)
    fig = ff.create_distplot([histdata],[selected_sport],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)

    st.write("#")
    sport_list = ['Basketball', 'Judo', 'Football', 'Athletics',
    'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Handball', 'Weightlifting', 
    'Wrestling','Water Polo', 'Hockey', 'Rowing', 'Fencing',
    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
    'Tennis',  'Golf', 'Softball', 'Archery',
    'Volleyball','Synchronized Swimming', 'Table Tennis', 'Baseball',
    'Rhythmic Gymnastics', 'Trampolining',
    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
    'Ice Hockey','Rugby Sevens',
    'Art Competitions','Tug-Of-War']
    x = []
    name = []
    for sport in sport_list:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna().values.astype(int))
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age wrt Sports")
    st.plotly_chart(fig)


    st.write('#')
    st.title('Height vs Weight')
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig = px.scatter(temp_df,x='Weight',y='Height',color='Medal',symbol='Sex')
    fig.update_layout(autosize=False,width=1000,height=600)
    st.plotly_chart(fig)


    st.write('#')
    st.title('Men and Women Participation Over the Years')
    final = helper.men_vs_women(df)
    st.line_chart(data=final, x="Year", y=['Male', 'Female'])