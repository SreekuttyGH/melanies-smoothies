# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothies :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

#option = st.selectbox(
    #"What is your favourite fruit?",
    #("Banana", "Strawberries", "peaches"))

#st.write("Your favourite fruit is:", option)

from snowflake.snowpark.functions import col
cnx=st.connection("snowflake")
#session = get_active_session()
session = cnx.session()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe,use_container_width=True)
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)

#st.stop()
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('choose upto 5 ingredients:',my_dataframe)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen+' '+'Nutrition Information')
        fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    #st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

#st.write(my_insert_stmt)

time_to_insert=st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

#if ingredients_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")
#New section to display fruityvise nutrition information
#import requests
#fruityvice_response=requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
#fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)

