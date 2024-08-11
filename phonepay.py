import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as px
import json
import requests
from PIL import Image

#Data Frame Creation

mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port = "5432",
                        database = "phonepay_data",
                        password = "John@2394")
cursor =mydb.cursor()

#Aggregated Insurance df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggregated_insurance = pd.DataFrame(table1, columns=("States", "Years", "Quarter", 
                                                     "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated transaction df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggregated_transaction = pd.DataFrame(table2, columns=("States", "Years", "Quarter", 
                                                     "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated User df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggregated_user = pd.DataFrame(table3, columns=("States", "Years", "Quarter", 
                                                     "Brands", "Transaction_count", "Percentage"))

#Map Insurance df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4 = cursor.fetchall()

Map_insurance = pd.DataFrame(table4, columns=("States", "Years", "Quarter", 
                                                     "Districts", "Transaction_count", "Transaction_amount"))

#Map transaction df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5 = cursor.fetchall()

Map_transaction = pd.DataFrame(table5, columns=("States", "Years", "Quarter", 
                                                     "Districts", "Transaction_count", "Transaction_amount"))


#Map user df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6 = cursor.fetchall()

Map_user = pd.DataFrame(table6, columns=("States", "Years", "Quarter", 
                                                     "Districts", "RegisteredUsers", "AppOpens"))

#top Insurance df

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7 = cursor.fetchall()

Top_insurance = pd.DataFrame(table7, columns=("States", "Years", "Quarter", 
                                                     "Pincodes", "Transaction_count", "Transaction_amount"))

#top transaction df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8= cursor.fetchall()

Top_transaction = pd.DataFrame(table8, columns=("States", "Years", "Quarter", 
                                                     "Pincodes", "Transaction_count", "Transaction_amount"))


#Top user df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9 = cursor.fetchall()

Top_user = pd.DataFrame(table9, columns=("States", "Years", "Quarter", 
                                                     "Pincodes", "RegisteredUsers"))





def Transaction_amount_count_Y(df,year): 
    
    tacy =df[df["Years"]==year]
    tacy.reset_index(drop=True, inplace= True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1, col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount)
    with col2:    

        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(fig_count)
        
    col1, col2 = st.columns(2)
    with col1:
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 =json.loads(response.content)
        states_name =[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()   

        fig_india_1 =px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow", 
                                range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)
        
    with col2:
        fig_india_2 =px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow", 
                                range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2) 
        
    return tacy 

def Transaction_amount_count_Y_Q(df,quarter): 
    tacy =df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True, inplace= True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2 =st.columns(2)
    
    with col1:

        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount)
    with col2:
        
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(fig_count)
    col1,col2 =st.columns(2)
    
    with col1:    
    
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 =json.loads(response.content)
        states_name =[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()
        

        fig_india_1 =px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_amount", color_continuous_scale= "Rainbow", 
                                range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                hover_name= "States", title= f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1) 
        
    with col2:
        
        fig_india_2 =px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",
                                color= "Transaction_count", color_continuous_scale= "Rainbow", 
                                range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                hover_name= "States", title= f"{tacy['Years'].unique()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height= 600, width= 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)
        
    return tacy
        

def Aggre_tran_transaction_type(df, state):
    
    tacy =df[df["States"]==state]
    tacy.reset_index(drop=True, inplace= True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2 =st.columns(2)
    
    with col1:

        fig_pie_1 = px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",
                        width= 600, title=f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)
        
    with col2:
        
        fig_pie_2 = px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",
                        width= 600, title=f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2) 
        
#Aggregated user Analysis 1

def Aggre_user_plot_1(df, year):
    
    aguy = df[df["Years"]==year]
    aguy.reset_index(drop= True, inplace= True)


    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1 = px.bar(aguyg, x= "Brands", y= "Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy 

#Aggregated user Analysis 2

def Aggre_user_plot_2(df, quarter):
    
    aguyq = df[df["Quarter"]==quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1 = px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width= 1000, color_discrete_sequence= px.colors.sequential.Bluered, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguyq 

#Aggregated user Analysis 3

def Aggre_user_plot_3(df, state):

    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1 =px.line(auyqs, x= "Brands", y= "Transaction_count", hover_data= "Percentage",
                        title= f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",
                        color_discrete_sequence=px.colors.sequential.Magenta_r, width= 1000, markers= True)
    st.plotly_chart(fig_line_1)  
    
# Map Insurance Districts

def Map_insur_Districts(df, state):
    
    tacy =df[df["States"]==state]
    tacy.reset_index(drop=True, inplace= True)

    tacyg = tacy.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 =st.columns(2)
    with col1:
        
        fig_bar_1 = px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Brwnyl_r)
        st.plotly_chart(fig_bar_1)
    
    with col2:
        fig_bar_2 = px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h", height= 600,
                        title= f"{state.upper()} DISTRICTS AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Blues_r)
        st.plotly_chart(fig_bar_2)  
        
#Map user plot 1

def map_user_plot_1(df, year):
    
    muy= df[df["Years"]==year]
    muy.reset_index(drop= True, inplace= True)


    muyg = muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1 =px.line(muyg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{year} REGISTERED USERS, APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Bluered_r, width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1) 
    
    return muy  

#Map user plot 2

def map_user_plot_2(df, quarter):
    
    muyq= df[df["Quarter"]==quarter]
    muyq.reset_index(drop= True, inplace= True)


    muyqg = muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1 =px.line(muyqg, x= "States", y= ["RegisteredUsers", "AppOpens"],
                            title= f"{df['Years'].unique()} YEAR {quarter} QUARTER, REGISTERED USERS, APPOPENS",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)
    
    return muyq 

#Map user plot 3
def map_user_plot_3(df, states):

    muyqs = df[df["States"] == states ]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2 =st.columns(2)
    
    with col1:
        
        fig_map_user_bar_1 =px.bar(muyqs, x= "RegisteredUsers", y= "Districts", orientation= "h",
                                title= f"{states.upper()} REGISTERED USERS",  color_discrete_sequence= px.colors.sequential.Rainbow, height= 800)
        st.plotly_chart(fig_map_user_bar_1)
        
    with col2:
        
        fig_map_user_bar_2 =px.bar(muyqs, x= "AppOpens", y= "Districts", orientation= "h",
                                title= f"{states.upper()} APPOPENS", color_discrete_sequence= px.colors.sequential.Rainbow_r, height= 800)
        st.plotly_chart(fig_map_user_bar_2) 
        
# Top Insurance plot 1

def Top_insurance_plot_1(df, states):
    
    tiy= df[df["States"] == states]
    tiy.reset_index(drop= True, inplace= True)
    
    col1,col2 =st.columns(2)
    
    with col1:
        fig_top_insur_bar_1 =px.bar(tiy, x= "Quarter", y= "Transaction_amount", hover_data= "Pincodes",
                                    title= "TRANSACTION AMOUNT",  color_discrete_sequence= px.colors.sequential.Mint_r, height= 650, width= 600)
        st.plotly_chart(fig_top_insur_bar_1)
          
    with col2:
        
        fig_top_insur_bar_2 =px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= "Pincodes",
                                    title= "TRANSACTION COUNT",  color_discrete_sequence= px.colors.sequential.Rainbow, height= 650, width= 600)
        st.plotly_chart(fig_top_insur_bar_2) 
        
# top user plot 1

def top_user_plot_1(df, year):
    
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)


    tuyg = pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1 = px.bar(tuyg, x= "States", y= "RegisteredUsers", color= "Quarter", height= 800, width= 1000,
                            color_discrete_sequence= px.colors.sequential.Rainbow_r, hover_name= "States",
                            title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)
    
    return tuy  

#top user plot 2

def top_user_plot_2(df, state):
    
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_2 = px.bar(tuys, x= "Quarter", y= "RegisteredUsers", title= f"{state.upper()} REGISTERED USERS, PINCODES, QUARTER",
                            color_continuous_scale= px.colors.sequential.Magenta, height= 800, width= 1000, color= "RegisteredUsers",
                            hover_data= "Pincodes")
    st.plotly_chart(fig_top_plot_2)                      
            
#sql connection
def top_chart_transaction_amount(table_name):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepay_data",
                            password = "John@2394")
    cursor =mydb.cursor()

    #plot 1

    query1 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
                
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 =pd.DataFrame(table_1, columns= ("states", "transaction_amount"))

    col1, col2 = st.columns(2)
    
    with col1:
        
        fig_amount_1 = px.bar(df_1, x="states", y="transaction_amount", title=" TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                             color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount_1)


    #plot 2

    query2 = f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount 
                LIMIT 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 =pd.DataFrame(table_2, columns= ("states", "transaction_amount"))
    
    with col2:
        
        fig_amount_2 = px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    #plot 3

    query3 = f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''
                
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 =pd.DataFrame(table_3, columns= ("states", "transaction_amount"))

    fig_amount_3 = px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
    
#sql connection

def top_chart_transaction_count(table_name):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepay_data",
                            password = "John@2394")
    cursor =mydb.cursor()

    #plot 1

    query1 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''
                
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 =pd.DataFrame(table_1, columns= ("states", "transaction_count"))
    col1,col2 = st.columns(2)
    with col1:
        
        fig_amount_1 = px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount_1)


    #plot 2

    query2 = f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count 
                LIMIT 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 =pd.DataFrame(table_2, columns= ("states", "transaction_count"))
    
    with col2:
        
        fig_amount_2 = px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    #plot 3

    query3 = f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''
                
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 =pd.DataFrame(table_3, columns= ("states", "transaction_count"))

    fig_amount_3 = px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
    
    #sql connection
    
def top_chart_registered_users(table_name, state):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepay_data",
                            password = "John@2394")
    cursor =mydb.cursor()

    #plot 1

    query1 = f'''SELECT districts, SUM(registeredusers) AS registeredusers
                 FROM {table_name}
                 WHERE states='{state}'
                 GROUP BY districts
                 ORDER BY registeredusers DESC
                 LIMIT 10;'''
                
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 =pd.DataFrame(table_1, columns= ("districts", "registeredusers"))

    col1, col2 = st.columns(2)
    
    with col1:
        
        fig_amount_1 = px.bar(df_1, x="districts", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount_1)


    #plot 2

    query2 = f'''SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registeredusers 
                LIMIT 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 =pd.DataFrame(table_2, columns= ("districts", "registeredusers"))

    with col2:
        fig_amount_2 = px.bar(df_2, x="districts", y="registeredusers", title="LAST 10 OF REGISTERED USERS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    #plot 3

    query3 = f'''SELECT districts, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeredusers;'''
                
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 =pd.DataFrame(table_3, columns= ("districts", "registeredusers"))

    fig_amount_3 = px.bar(df_3, y="districts", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "districts", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
    
#sql connection
def top_chart_appopens(table_name, state):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepay_data",
                            password = "John@2394")
    cursor =mydb.cursor()

    #plot 1

    query1 = f'''SELECT districts, SUM(appopens) AS appopens
                 FROM {table_name}
                 WHERE states='{state}'
                 GROUP BY districts
                 ORDER BY appopens DESC
                 LIMIT 10;'''
                
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 =pd.DataFrame(table_1, columns= ("districts", "appopens"))
    col1,col2 = st.columns(2)
    
    with col1:
        
        fig_amount_1 = px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount_1)


    #plot 2

    query2 = f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 =pd.DataFrame(table_2, columns= ("districts", "appopens"))
    
    with col2:
        
        fig_amount_2 = px.bar(df_2, x="districts", y="appopens", title="LAST 10 OF APPOPENS", hover_name= "districts",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    #plot 3

    query3 = f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''
                
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 =pd.DataFrame(table_3, columns= ("districts", "appopens"))

    fig_amount_3 = px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
                  
#sql connection
def top_chart_registeredusers(table_name):
    
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port = "5432",
                            database = "phonepay_data",
                            password = "John@2394")
    cursor =mydb.cursor()

    #plot 1

    query1 = f'''SELECT states, SUM(registeredusers) AS registeredusers
                 FROM {table_name}
                 GROUP BY states
                 ORDER BY registeredusers DESC
                 LIMIT 10;'''
                
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 =pd.DataFrame(table_1, columns= ("states", "registeredusers"))

    col1,col2 = st.columns(2)
    
    with col1:
        
        fig_amount_1 = px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650, width= 600)
        st.plotly_chart(fig_amount_1)


    #plot 2

    query2 = f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers 
                LIMIT 10;'''
                
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 =pd.DataFrame(table_2, columns= ("states", "registeredusers"))
    
    with col2:
        
        fig_amount_2 = px.bar(df_2, x="states", y="registeredusers", title="LAST 10 OF REGISTERED USERS", hover_name= "states",
                                color_discrete_sequence=px.colors.sequential.Bluyl_r, height= 650, width= 600)
        st.plotly_chart(fig_amount_2)


    #plot 3

    query3 = f'''SELECT states, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers;'''
                
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 =pd.DataFrame(table_3, columns= ("states", "registeredusers"))

    fig_amount_3 = px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                            color_discrete_sequence=px.colors.sequential.Blues_r, height= 800, width= 1000)
    st.plotly_chart(fig_amount_3)
                            
              
              

            
#Streamlit part

st.set_page_config(layout="wide")
st.title("PHONEPAY DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select = option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\vibin\OneDrive\Desktop\PHONEPAY\download.jpeg"), width= 600)
        
    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\vibin\OneDrive\Desktop\PHONEPAY\PhonePe-Copy.jpg"), width= 500)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****") 
        
    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\vibin\OneDrive\Desktop\PHONEPAY\images.png"), width= 600)       

elif select == "DATA EXPLORATION":
    
       tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
     
       with tab1:
            
            method1 =st.radio("Select The Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])
            
            if method1 == "Insurance Analysis":
                
               col1,col2 = st.columns(2)
               
               with col1:
                   years = st.slider("Select The Year", Aggregated_insurance["Years"].min(),Aggregated_insurance["Years"].max(),
                                 Aggregated_insurance["Years"].min()) 
               tac_Y= Transaction_amount_count_Y(Aggregated_insurance, years) 
               
               col1,col2 =st.columns(2)
               
               with col1:
                   
                    quarters = st.selectbox("Select The Quarter", tac_Y["Quarter"].unique())
               Transaction_amount_count_Y_Q(tac_Y,quarters)    
                   
                
            elif method1 =="Transaction Analysis":
                
                col1,col2 = st.columns(2)
               
                with col1:
                   years = st.slider("Select The Year", Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max(),
                                 Aggregated_transaction["Years"].min())
                    
                Aggre_tran_tac_Y= Transaction_amount_count_Y(Aggregated_transaction, years)
                
                col1,col2 = st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())
                
                Aggre_tran_transaction_type(Aggre_tran_tac_Y, states)
                
                col1,col2 =st.columns(2)
               
                with col1:
                   
                    quarters = st.selectbox("Select The Quarter", Aggre_tran_tac_Y["Quarter"].unique())
                    
                Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters) 
                
                col1,col2 = st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())
                
                Aggre_tran_transaction_type(Aggre_tran_tac_Y_Q, states)  
               
            elif method1 == "User Analysis":
                col1,col2 = st.columns(2)
               
                with col1:
                   years = st.slider("Select The Year", Aggregated_user["Years"].min(),Aggregated_user["Years"].max(),
                                 Aggregated_user["Years"].min())
                   
                Aggre_user_Y = Aggre_user_plot_1(Aggregated_user, years) 
                
                col1,col2 =st.columns(2)
               
                with col1:
                   
                    quarters = st.selectbox("Select The Quarter",Aggre_user_Y ["Quarter"].unique())
                    
                Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quarters) 
                
                col1,col2 = st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())
                
                Aggre_user_plot_3(Aggre_user_Y_Q, states)
                
                   
       with tab2: 
            
            method2 = st.radio("Select The Method", ["Map Insurance", "Map Transaction", "Map User"])
            
            if method2 == "Map Insurance":
                
                col1,col2 = st.columns(2)
               
                with col1:
                    
                   years = st.selectbox("Select The Year", Map_insurance["Years"].unique())
                    
                Map_insur_tac_Y= Transaction_amount_count_Y(Map_insurance, years)
                
                col1,col2 = st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_mi", Map_insur_tac_Y["States"].unique())
                
                Map_insur_Districts(Map_insur_tac_Y, states)
                
                col1,col2 =st.columns(2)
               
                with col1:
                   
                    quarters = st.selectbox("Select The Quarter_mi", Map_insur_tac_Y["Quarter"].unique())
                    
                Map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Map_insur_tac_Y,quarters)
                col1, col2= st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_Ty",Map_insur_tac_Y_Q["States"].unique())
                
                Map_insur_Districts(Map_insur_tac_Y_Q, states)
                
            elif method2 == "Map Transaction":
                
                col1,col2 = st.columns(2)
               
                with col1:
                    
                   years = st.selectbox("Select The Year", Map_transaction["Years"].unique())
                    
                Map_tran_tac_Y= Transaction_amount_count_Y(Map_transaction, years)
                
                col1,col2 = st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_mt", Map_tran_tac_Y["States"].unique())
                
                Map_insur_Districts(Map_tran_tac_Y, states)
                
                col1,col2 =st.columns(2)
               
                with col1:
                   
                    quarters = st.selectbox("Select The Quarter_mt", Map_tran_tac_Y["Quarter"].unique())
                    
                Map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Map_tran_tac_Y,quarters)
                
                col1, col2= st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_Ty",Map_tran_tac_Y_Q["States"].unique())
                
                Map_insur_Districts(Map_tran_tac_Y_Q, states)
                
            elif method2 == "Map User":
                
                col1,col2 = st.columns(2)
               
                with col1:
                    
                   years = st.selectbox("Select The Year", Map_user["Years"].unique())
                    
                Map_user_Y= map_user_plot_1(Map_user, years)
                
                col1,col2 =st.columns(2)
               
                with col1:
                   
                    quarters = st.selectbox("Select The Quarter_mu",  Map_user_Y["Quarter"].unique())
                    
                Map_user_Y_Q = map_user_plot_2( Map_user_Y,quarters)
                
                col1, col2= st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_mu",Map_user_Y_Q["States"].unique())
                
                map_user_plot_3(Map_user_Y_Q, states)
                
                
        
       with tab3:
           
           method3 =st.radio("Select The Method", ["Top Insurance", "Top Transaction","Top User"])
           
           if method3 == "Top Insurance":

                col1,col2 = st.columns(2)
               
                with col1:
                    
                   years = st.selectbox("Select The Year_ti", Top_insurance["Years"].unique())
                    
                Top_insur_tac_Y= Transaction_amount_count_Y(Top_insurance, years)
                
                col1, col2= st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_ti", Top_insur_tac_Y["States"].unique())
                
                Top_insurance_plot_1(Top_insur_tac_Y, states)
                
                col1,col2 =st.columns(2)
               
                with col1:
                   
                    quarters = st.selectbox("Select The Quarter_ti", Top_insur_tac_Y["Quarter"].unique())
                    
                Top_insur_tac_Y_Q = Transaction_amount_count_Y_Q(Top_insur_tac_Y , quarters)
                
                
           elif method3 == "Top Transaction":
                
                col1,col2 = st.columns(2)
               
                with col1:
                    
                   years = st.selectbox("Select The Year_tt", Top_transaction["Years"].unique())
                    
                Top_tran_tac_Y= Transaction_amount_count_Y(Top_transaction, years)
                
                col1, col2= st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_tt", Top_tran_tac_Y["States"].unique())
                
                Top_insurance_plot_1(Top_tran_tac_Y, states)
                
                col1,col2 =st.columns(2)
               
                with col1:
                   
                    quarters = st.selectbox("Select The Quarter_tt", Top_tran_tac_Y["Quarter"].unique())
                    
                Top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Top_tran_tac_Y , quarters)
                
           elif method3 == "Top User":
                
                col1,col2 = st.columns(2)
               
                with col1:
                    
                   years = st.selectbox("Select The Year_tu", Top_user["Years"].unique())
                    
                Top_user_Y = top_user_plot_1(Top_user, years)
                
                col1, col2= st.columns(2)
                
                with col1:
                    
                    states = st.selectbox("Select The State_tu", Top_user_Y["States"].unique())
                
                top_user_plot_2(Top_user_Y, states)
           
elif select =="TOP CHARTS":
    
    question = st.selectbox("Select The Question", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                   "2. Transaction Amount and Count of Map Insurance",
                                                   "3. Transaction Amount and Count of Top Insurance",
                                                   "4. Transaction Amount and Count of Aggregated Transaction",
                                                   "5. Transaction Amount and Count of Map Transaction",
                                                   "6. Transaction Amount and Count of Top Transaction",
                                                   "7. Transaction Count of Aggregated User",
                                                   "8. Registered Users of Map User",
                                                   "9. Appopens of Map User",
                                                   "10. Registered Users of Top User"
                                                   ])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Aggregated_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Aggregated_insurance") 
        
    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Map_insurance")
        
    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Top_insurance") 
        
    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Aggregated_transaction") 
        
    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Map_transaction")
        
    elif question == "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("Top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Top_transaction")  
        
    elif question == "7. Transaction Count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("Aggregated_user")
        
    elif question == "8. Registered Users of Map User":
        
        states = st.selectbox("Select The State_tc", Map_user["States"].unique())
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("map_user", states)
        
    elif question == "9. Appopens of Map User":
        
        states = st.selectbox("Select The State_tc", Map_user["States"].unique())
        
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)
        
    elif question == "10. Registered Users of Top User":
        
        st.subheader("REGISTERED USERS")
        top_chart_registeredusers("top_user")                                                                             
            
                  
          
         

