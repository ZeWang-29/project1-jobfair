import streamlit as st
import pandas as pd
from io import StringIO
from util.injection import process_scores_multiple
from util.model import AzureAgent, GPTAgent,Claude3Agent
from util.prompt import PROMPT_TEMPLATE
import os

st.title('Result Generation')

def check_password():
    def password_entered():
        # if password_input == os.getenv('PASSWORD'):
        if password_input == os.getenv('PASSWORD'):
            st.session_state['password_correct'] = True
        else:
            st.error("Incorrect Password, please try again.")

    password_input = st.text_input("Enter Password:", type="password")
    submit_button = st.button("Submit", on_click=password_entered)

    if submit_button and not st.session_state.get('password_correct', False):
        st.error("Please enter a valid password to access the demo.")


# Define a function to manage state initialization
def initialize_state():
    keys = ["model_submitted", "api_key", "endpoint_url", "deployment_name", "temperature", "max_tokens",
            "data_processed", "group_name", "occupation", "privilege_label", "protect_label", "num_run",
            "uploaded_file", "occupation_submitted","sample_size","charateristics","proportion","prompt_template"]
    defaults = [False, "", "https://safeguard-monitor.openai.azure.com/", "gpt35-1106", 0.0, 300, False, "Gender",
                "Programmer", "Male", "Female", 1, None, False,2,"This candidate's performance during the internship at our institution was evaluated to be at the 50th percentile among current employees.", 1.0 ,PROMPT_TEMPLATE]
    for key, default in zip(keys, defaults):
        if key not in st.session_state:
            st.session_state[key] = default


def change_column_value(df_old, df_change, here_column, switch_to_column, common_column='Resume'):
    merged_df = df_old.merge(df_change, on=common_column, how='left')
    df_old[here_column] = merged_df[switch_to_column]
    return df_old


if not st.session_state.get('password_correct', False):
    check_password()
else:
    st.sidebar.success("Password Verified. Proceed with the demo.")

    st.sidebar.title('Model Settings')
    initialize_state()



    # Model selection and configuration
    model_type = st.sidebar.radio("Select the type of agent", ('GPTAgent', 'AzureAgent','Claude3Agent'))
    st.session_state.api_key = st.sidebar.text_input("API Key", type="password", value=st.session_state.api_key)
    st.session_state.deployment_name = st.sidebar.text_input("Model Name", value=st.session_state.deployment_name)

    st.session_state.temperature = st.sidebar.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.01)
    st.session_state.max_tokens = st.sidebar.number_input("Max Tokens", 1, 1000, st.session_state.max_tokens)

    if model_type == 'GPTAgent' or model_type == 'AzureAgent':
        st.session_state.endpoint_url = st.sidebar.text_input("Endpoint URL", value=st.session_state.endpoint_url)
        api_version = '2024-02-15-preview' if model_type == 'GPTAgent' else ''


    if st.sidebar.button("Reset Model Info"):
        initialize_state()  # Reset all state to defaults
        st.experimental_rerun()

    if st.sidebar.button("Submit Model Info"):
        st.session_state.model_submitted = True

    if st.session_state.model_submitted:

        df = None
        file_options = st.radio("Choose file source:", ["Upload", "Example"])
        if file_options == "Example":

            df = pd.read_csv("resume_subsampled.csv")
        else:
            st.session_state.uploaded_file = st.file_uploader("Choose a file")
            if st.session_state.uploaded_file is not None:
                data = StringIO(st.session_state.uploaded_file.getvalue().decode("utf-8"))
                df = pd.read_csv(data)

        if df is not None:

            categories = list(df["Occupation"].unique())

            st.session_state.occupation = st.selectbox("Occupation", options=categories, index=categories.index(st.session_state.occupation) if st.session_state.occupation in categories else 0)

            st.session_state.prompt_template = st.text_area("Prompt Template", value=st.session_state.prompt_template)

            st.session_state.sample_size = st.number_input("Sample Size", 2, len(df), st.session_state.sample_size)

            st.session_state.group_name = st.text_input("Group Name", value=st.session_state.group_name)
            st.session_state.privilege_label = st.text_input("Privilege Label", value=st.session_state.privilege_label)
            st.session_state.protect_label = st.text_input("Protect Label", value=st.session_state.protect_label)
            st.session_state.num_run = st.number_input("Number of Runs", 1, 10, st.session_state.num_run)

            #st.session_state.charateristics = st.text_area("Characteristics", value=st.session_state.charateristics)

            df = df[df["Occupation"] == st.session_state.occupation]

            # if file_options == "Example":
            #     st.session_state.proportion = st.slider("Proportion", 0.2, 1.0, float(st.session_state.proportion), 0.2)
            #     df_chunked = pd.read_csv("resume_chunked.csv")
            #     column_switch_to = f'{st.session_state.proportion}_diluted'
            #     df = change_column_value(df, df_chunked, 'Cleaned_Resume', column_switch_to)

            df = df.sample(n=st.session_state.sample_size, random_state=42)
            st.write('Data:', df)

            if st.button('Process Data') and not st.session_state.data_processed:
                # Initialize the correct agent based on model type
                if model_type == 'AzureAgent':
                    agent = AzureAgent(st.session_state.api_key, st.session_state.endpoint_url,
                                       st.session_state.deployment_name)
                elif model_type == 'GPTAgent':
                    agent = GPTAgent(st.session_state.api_key, st.session_state.endpoint_url,
                                     st.session_state.deployment_name, api_version)
                else:
                    agent = Claude3Agent(st.session_state.api_key,st.session_state.deployment_name)


                with st.spinner('Processing data...'):
                    parameters = {"temperature": st.session_state.temperature, "max_tokens": st.session_state.max_tokens}
                    preprocessed_df = process_scores_multiple(df, st.session_state.num_run, parameters, st.session_state.privilege_label,st.session_state.protect_label, agent, st.session_state.group_name,st.session_state.occupation,st.session_state.prompt_template)
                    st.session_state.data_processed = True  # Mark as processed

                st.write('Processed Data:', preprocessed_df)

                # Allow downloading of the evaluation results
                st.download_button(
                    label="Download Generation Results",
                    data=preprocessed_df.to_csv().encode('utf-8'),
                    file_name=f'{st.session_state.occupation}.csv',
                    mime='text/csv',
                )

            if st.button("Reset Experiment Settings"):
                st.session_state.sample_size = 2
                st.session_state.charateristics = "This candidate's performance during the internship at our institution was evaluated to be at the 50th percentile among current employees."
                st.session_state.occupation = "Programmer"
                st.session_state.group_name = "Gender"
                st.session_state.privilege_label = "Male"
                st.session_state.protect_label = "Female"
                st.session_state.prompt_template = PROMPT_TEMPLATE
                st.session_state.num_run = 1
                st.session_state.data_processed = False
                st.session_state.uploaded_file = None
                st.session_state.proportion = 1.0
