import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

# Dataframe Creation

#sql connection
mydb= psycopg2.connect(host= "localhost",
                       user= "postgres",
                       port= "5432",
                       database= "phonepe_data",
                       password= "2112")
cursor= mydb.cursor()

#aggre_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1= cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2= cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_type",
                                               "Transaction_count", "Transaction_amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3= cursor.fetchall()

Aggre_user= pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands",
                                               "Transaction_count", "Percentage"))

#map_insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4= cursor.fetchall()

map_insurance= pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts",
                                               "Transaction_count", "Transaction_amount"))

#map_transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5= cursor.fetchall()

map_transaction= pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Districts",
                                               "Transaction_count", "Transaction_amount"))

#map_user
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6= cursor.fetchall()

map_user= pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Districts",
                                               "RegisteredUser", "AppOpens"))

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7= cursor.fetchall()

top_insurance= pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

top_transaction= pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincodes",
                                               "Transaction_count", "Transaction_amount"))

#top_user
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9= cursor.fetchall()

top_user= pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincodes",
                                               "RegisteredUser"))

# Function Definition:
def Transaction_amount_count_Y(df, year):
    #Filtering Data by Year
    tacy= df[df["Years"] == year]
    #Resetting Index
    tacy.reset_index(drop = True, inplace= True)
    #Grouping Data by States and Aggregating
    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    #Resetting Index for the Grouped DataFrame
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year}-TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Plasma, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year}-TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Viridis, height= 650, width= 600)
        st.plotly_chart(fig_count)


    col1,col2= st.columns(2)
    with col1:

        # Fetching GeoJSON Data
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        # fetches the data from the URL.
        response= requests.get(url)
        data1= json.loads(response.content)
        # Extracting State Names
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()
        # Creating Choropleth Map
        fig_india_1= px.choropleth(
                                   tacyg, # tacyg is the DataFrame containing transaction data grouped by states.
                                   geojson= data1, # specifies the GeoJSON data for the map.
                                   locations= "States", #  indicates the column in tacyg that matches the states in the GeoJSON data.
                                   featureidkey= "properties.ST_NM", # tells Plotly Express how to match the states in the GeoJSON data with the states in the DataFrame.
                                   color= "Transaction_amount", # sets the color of each state on the map based on its transaction amount.
                                   color_continuous_scale= "Rainbow",# specifies the color scale to use for the map.
                                   range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()), # sets the range of values for the color scale.
                                   hover_name= "States", # determines what information appears when hovering over each state on the map
                                   title= f"{year}-TRANSACTION AMOUNT", #  sets the title of the map.
                                   fitbounds= "locations",# adjusts the zoom level to fit all state boundaries within the map.
                                   height= 600,width= 600) # sets the dimensions of the map.
        fig_india_1.update_geos(visible= False) # adjusts the zoom level to fit all state boundaries within the map.
        st.plotly_chart(fig_india_1) #  displays the choropleth map 

    with col2:

        fig_india_2= px.choropleth(tacyg, # tacyg is the DataFrame containing transaction data grouped by states.
                                   geojson= data1, # specifies the GeoJSON data for the map.
                                   locations= "States", #  indicates the column in tacyg that matches the states in the GeoJSON data.
                                   featureidkey= "properties.ST_NM",# tells Plotly Express how to match the states in the GeoJSON data with the states in the DataFrame.
                                   color= "Transaction_count",# sets the color of each state on the map based on its transaction count.
                                   color_continuous_scale= "Rainbow",# specifies the color scale to use for the map.
                                   range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),# sets the range of values for the color scale.
                                   hover_name= "States", # determines what information appears when hovering over each state on the map
                                   title= f"{year} TRANSACTION COUNT",  #  sets the title of the map.
                                   fitbounds= "locations",# adjusts the zoom level to fit all state boundaries within the map.
                                   height= 600,width= 600)
        fig_india_2.update_geos(visible= False) # adjusts the zoom level to fit all state boundaries within the map.
        st.plotly_chart(fig_india_2)  #  displays the choropleth map 

    return tacy

# Function Definition
def Transaction_amount_count_Y_Q(df, quarter):
    # Filtering Data by Quarter:
    tacy= df[df["Quarter"] == quarter]
    # Resetting Index:
    tacy.reset_index(drop = True, inplace= True)
    # Grouping Data by States and Aggregating:
    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    #Resetting Index for the Grouped DataFrame:
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)   
    with col1:

        fig_amount= px.sunburst(tacyg, 
                               path=["States","Transaction_amount"],
                               values='Transaction_amount',height= 650,width= 600)
        fig_amount.update_layout(title=f"{quarter} QUARTER TRANSACTION AMOUNT",title_x=0.35)
        st.plotly_chart(fig_amount)

    
        fig_count= px.sunburst(tacyg, 
                               path=["States","Transaction_amount"],
                               values='Transaction_count',height= 650,width= 600)
        fig_count.update_layout(title=f"{quarter} QUARTER TRANSACTION COUNT",title_x=0.35)
        st.plotly_chart(fig_count)


    return tacy

            
def Aggre_Tran_Transaction_type(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_pie_1= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                            width= 600, title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2= px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                            width= 600, title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)


# Aggre_User_analysis_1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg,
                       x= "Brands",
                         y= "Transaction_count", 
                         title= f"{year} BRANDS AND TRANSACTION COUNT",
                         width= 1000, 
                         color="Transaction_count",
                         barmode='stack',
                         hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy
#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, 
                      x= "Brands",
                      y= "Transaction_count", 
                      title=  f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                      width= 1000, 
                      color_discrete_sequence= px.colors.sequential.Magenta_r, 
                      hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


#Aggre_user_alalysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1= px.line(auyqs, 
                        x= "Brands",
                        y= "Transaction_count", 
                        hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",
                        width= 1000, markers= True)
    st.plotly_chart(fig_line_1)


#Map_insurance_districts
def Map_insur_Districts(df, state):

    tacy= df[df["States"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:

        fig_bar_2= px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

# map_user_plot_1
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{year} REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

# map_user_plot_2
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",width= 1000, height= 800, markers= True,
                        color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

# top_insurance_plot_1
def Top_insurance_plot_1(df, state):
    tiy= df[df["States"]== state]
    tiy.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_top_insur_bar_1= px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:

        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", color= "Quarter", width= 1000, height= 800,
                        color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_pot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUser", title= "REGISTEREDUSER, PINCODES, QUARTER",
                        width= 1000, height= 800, color= "RegisteredUser", hover_data= "Pincodes",
                        color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_pot_2)

#sql connection
def top_chart_transaction_amount(table_name):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "2112")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) AS Transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


#sql connection
def top_chart_transaction_count(table_name):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "2112")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



#sql connection
def top_chart_registered_user(table_name, state):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "2112")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(Registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_appopens(table_name, state):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "2112")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))


    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:

        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_users(table_name):
    mydb= psycopg2.connect(host= "localhost",
                        user= "postgres",
                        port= "5432",
                        database= "phonepe_data",
                        password= "2112")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registereduser"))
    
    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="registereduser", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registereduser"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states", y="registereduser", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registereduser"))

    fig_amount_3= px.bar(df_3, y="states", x="registereduser", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


# Streamlit Part

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


with st.sidebar:
    
    select= option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])
if select == "HOME":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    
    col1,col2= st.columns(2)
    with col1:
            st.write(" ")
            st.write(" ")
            st.markdown("### :violet[Domain :] Fintech")
            st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, postgres,Streamlit, and Plotly.")
            st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    with col2:
        st.image(Image.open("download1.png"),width=600)



elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",int(Aggre_insurance["Years"].min()), int(Aggre_insurance["Years"].max()),int(Aggre_insurance["Years"].min()))
            tac_Y= Transaction_amount_count_Y(Aggre_insurance, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",int(tac_Y["Quarter"].min()), int(tac_Y["Quarter"].max()),int(tac_Y["Quarter"].min()))
            Transaction_amount_count_Y_Q(tac_Y, quarters)

        elif method == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",int(Aggre_transaction["Years"].min()), int(Aggre_transaction["Years"].max()),int(Aggre_transaction["Years"].min()))
            Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

        

        elif method == "User Analysis":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year",int(Aggre_user["Years"].min()),int(Aggre_user["Years"].max()),int(Aggre_user["Years"].min()))
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter",int(Aggre_user_Y["Quarter"].min()), int(Aggre_user_Y["Quarter"].max()),int(Aggre_user_Y["Quarter"].min()))
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)




    with tab2:

        method_2= st.radio("Select The Method",["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_for Map Insurance Analysis",int(map_insurance["Years"].min()), int(map_insurance["Years"].max()),int(map_insurance["Years"].min()))
            map_insur_tac_Y= Transaction_amount_count_Y(map_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_for Map Insurance Analysis", map_insur_tac_Y["States"].unique())

            Map_insur_Districts(map_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_for Map Insurance Analysis",int(map_insur_tac_Y["Quarter"].min()), int(map_insur_tac_Y["Quarter"].max()),int(map_insur_tac_Y["Quarter"].min()))
            map_insur_tac_Y_Q= Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_for Map Insurance Analysis", map_insur_tac_Y_Q["States"].unique())

            Map_insur_Districts(map_insur_tac_Y_Q, states)

        elif method_2 == "Map Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year For Map Transaction Analysis",int(map_transaction["Years"].min()), int(map_transaction["Years"].max()),int(map_transaction["Years"].min()))
            map_tran_tac_Y= Transaction_amount_count_Y(map_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State For Map Transaction Analysis", map_tran_tac_Y["States"].unique())

            Map_insur_Districts(map_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_For Map Transaction Analysis",int(map_tran_tac_Y["Quarter"].min()), int(map_tran_tac_Y["Quarter"].max()),int(map_tran_tac_Y["Quarter"].min()))
            map_tran_tac_Y_Q= Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_For Map Transaction Analysis", map_tran_tac_Y_Q["States"].unique())

            Map_insur_Districts(map_tran_tac_Y_Q, states)


        elif method_2 == "Map User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_mu",int(map_user["Years"].min()), int(map_user["Years"].max()),int(map_user["Years"].min()))
            map_user_Y= map_user_plot_1(map_user, years)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_mu",int(map_user_Y["Quarter"].min()), int(map_user_Y["Quarter"].max()),int(map_user_Y["Quarter"].min()))
            map_user_Y_Q= map_user_plot_2(map_user_Y, quarters)


    with tab3:

        method_3= st.radio("Select The Method",["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_For Top Insurance Analysis",int(top_insurance["Years"].min()), int(top_insurance["Years"].max()),int(top_insurance["Years"].min()))
            top_insur_tac_Y= Transaction_amount_count_Y(top_insurance, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_For Top Insurance Analysis", top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_For Top Insurance Analysis",int(top_insur_tac_Y["Quarter"].min()), int(top_insur_tac_Y["Quarter"].max()),int(top_insur_tac_Y["Quarter"].min()))
            top_insur_tac_Y_Q= Transaction_amount_count_Y_Q(top_insur_tac_Y, quarters)

            

        elif method_3 == "Top Transaction":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_For Top Transaction Analysis",int(top_transaction["Years"].min()),int(top_transaction["Years"].max()),int(top_transaction["Years"].min()))
            top_tran_tac_Y= Transaction_amount_count_Y(top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_For Top Transaction Analysis", top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:

                quarters= st.slider("Select The Quarter_For Top Transaction Analysis",int(top_tran_tac_Y["Quarter"].min()),int(top_tran_tac_Y["Quarter"].max()),int(top_tran_tac_Y["Quarter"].min()))
            top_tran_tac_Y_Q= Transaction_amount_count_Y_Q(top_tran_tac_Y, quarters)


        elif method_3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:

                years= st.slider("Select The Year_For Top User Analysis",int(top_user["Years"].min()), int(top_user["Years"].max()),int(top_user["Years"].min()))
            top_user_Y= top_user_plot_1(top_user, years)

            col1,col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State_For Top User Analysi", top_user_Y["States"].unique())

            top_user_plot_2(top_user_Y, states)

elif select == "TOP CHARTS":
    
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User",
                                                    ])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered users of Map User":
        
        states= st.selectbox("Select the State", map_user["States"].unique())   
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":
        
        states= st.selectbox("Select the State", map_user["States"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "10. Registered users of Top User":
          
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")