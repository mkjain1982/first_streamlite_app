import streamlit
import pandas as pd
import requests
import snowflake.connector

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text(' 🥣 Omega 3 & Blueberry oatmeal')
streamlit.text(' 🥗 Kale  Spinach & rocket Smoothy')
streamlit.text(' 🐔 Hard Boiled  Free range')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.

streamlit.dataframe(fruits_to_show)

# Display response of API
streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)

# Normalize the json data
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The Fruit Load List Contains:")
streamlit.dataframe(my_data_row)


fruit_list_choice = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thank you for adding ', fruit_list_choice)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlite');
