import streamlit as st
import openai
import pandas as pd
# from datetime import date
# from streamlit import caching
# import hydralit_components as hc

# st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

# ## Handling Cache to refresh after s day
# def cache_clear_dt(dummy):
#     clear_dt = date.today()
#     return clear_dt
#
# if cache_clear_dt("dummy")<date.today():
#     caching.clear_cache()

def create_action(adj_response_type, response_type):
    # for adjective in adj_response_type:
    #     prefix_adj = adjective.join(adjective).split(',')
    strList = [str(i) for i in adj_response_type]
    myString = ", ".join(strList)
    prefix_keyword = myString + " and " + str(response_type)
    st.sidebar.warning(prefix_keyword)
    return prefix_keyword

def ChatGPT(user_query):
    '''
    This function uses the OpenAI API to generate a response to the given
    user_query using the ChatGPT model
    :param user_query:
    :return:
    '''
    # Use the OpenAI API to generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=user_query,
        max_tokens=1024,
        n=1,
        temperature=0.5,
    )
    response = completion.choices[0].text
    return response

@st.cache_data
def api_call_on(query):
    '''
    This function gets the user input, pass it to ChatGPT function and
    displays the response
    '''

    response = ChatGPT(query)
    return response


# Set the model engine and your OpenAI API key
model_engine = "text-davinci-003"
openai.api_key = st.secrets["Openai_SECRET_KEY"]


st.title("Run a Query with ChatGPT")
st.sidebar.header("Instructions")
st.sidebar.info(
    '''This is a web application that allows you to interact with 
       the OpenAI API's implementation of the ChatGPT model.
       Enter a **query** in the **text box** and **press enter** to receive 
       a **response** from the ChatGPT
       '''
)
# Get user input
user_query = st.text_input("Enter query here, to exit enter :q", "what is Python?")


# os.environ["Openai_SECRET_KEY"] ==  st.secrets["Openai_SECRET_KEY"]
option = st.sidebar.selectbox("How would you like to run your query?", ("Use Keywords", "Just run"))
if option == "Use Keywords":
    st.write('You selected: ', option)
    ## Read a list of adjectives and actions
    adjs = pd.read_csv('./prefix_data/adjectives.csv')
    actions = pd.read_csv('./prefix_data/actions.csv')

    adj_response_type = st.sidebar.multiselect("Please specify keywords", adjs)
    response_type = st.sidebar.selectbox("Please specify action", actions)
    if adj_response_type != "" and response_type != "":
        prefix_keyword = create_action(adj_response_type, response_type)
        prefix_query = f'A {prefix_keyword} response to {user_query}'
        if st.sidebar.button("Run"):
            with st.spinner('Wait for it...'):
                response = api_call_on(prefix_query)
                st.success(f"{response}")
else:
    response = api_call_on(user_query)
    st.success(f"{response}")

# ## To do
# Collapse option to use keywords
# Add cache
# Add loader