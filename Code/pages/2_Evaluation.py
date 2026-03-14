import os

import numpy as np
import streamlit as st
import pandas as pd
from io import StringIO
from util.evaluation import statistical_tests
from util.plot import create_score_plot,create_rank_plots,create_correlation_heatmaps,create_3d_plot,calculate_distances
import plotly.express as px


def check_password():
    def password_entered():
        if password_input == os.getenv('PASSWORD'):
            st.session_state['password_correct'] = True
        else:
            st.error("Incorrect Password, please try again.")

    password_input = st.text_input("Enter Password:", type="password")
    submit_button = st.button("Submit", on_click=password_entered)

    if submit_button and not st.session_state.get('password_correct', False):
        st.error("Please enter a valid password to access the demo.")

def app():
    st.title('Result Evaluation')

    if not st.session_state.get('password_correct', False):
        check_password()
    else:
        st.sidebar.success("Password Verified. Proceed with the demo.")

        # Allow users to upload a CSV file with processed results
        uploaded_file = st.file_uploader("Upload your processed CSV file", type="csv")
        if uploaded_file is not None:
            data = StringIO(uploaded_file.getvalue().decode('utf-8'))
            df = pd.read_csv(data)

            st.write('Uploaded Data:', df)

            if st.button('Evaluate Data'):
                with st.spinner('Evaluating data...'):
                    statistical_results = statistical_tests(df)
                    #correlation_results = calculate_correlations(df)
                    #divergence_results = calculate_divergences(df)

                    flat_statistical_results = {f"{key1}": value1 for key1, value1 in statistical_results.items()}
                    #flat_correlation_results = {f"Correlation_{key1}": value1 for key1, value1 in correlation_results.items()}
                    #flat_divergence_results = {f"Divergence_{key1}": value1 for key1, value1 in divergence_results.items()}

                    results_combined = {**flat_statistical_results} #,**flat_correlation_results}#, **flat_divergence_results}

                    results_df = pd.DataFrame(list(results_combined.items()), columns=['Metric', 'Value'])

                    st.write('Test Results:', results_df)

                    fig_3d = create_3d_plot(df)

                    st.plotly_chart(fig_3d)

                    # Calculate and display average distance
                    point_A = np.array([0, 0, 0])
                    point_B = np.array([10, 10, 10])
                    distances = calculate_distances(df, point_A, point_B)
                    average_distance = distances.mean()
                    st.write(f'Average distance to the ideal line: {average_distance}')


                    score_fig = create_score_plot(df)
                    st.plotly_chart(score_fig)

                    rank_fig = create_rank_plots(df)
                    st.plotly_chart(rank_fig)


                    hist_fig = px.histogram(df.melt(id_vars=['Role'],
                                                    value_vars=['Privilege_Avg_Score', 'Protect_Avg_Score',
                                                                'Neutral_Avg_Score']),
                                            x='value', color='variable', facet_col='variable',
                                            title='Distribution of Scores')
                    st.plotly_chart(hist_fig)

                    hist_rank_fig = px.histogram(
                        df.melt(id_vars=['Role'], value_vars=['Privilege_Rank', 'Protect_Rank', 'Neutral_Rank']),
                        x='value', color='variable', facet_col='variable', title='Distribution of Ranks')
                    st.plotly_chart(hist_rank_fig)

                    box_fig = px.box(df.melt(id_vars=['Role'], value_vars=['Privilege_Avg_Score', 'Protect_Avg_Score',
                                                                           'Neutral_Avg_Score']),
                                     x='variable', y='value', color='variable', title='Spread of Scores')
                    st.plotly_chart(box_fig)

                    box_rank_fig = px.box(
                        df.melt(id_vars=['Role'], value_vars=['Privilege_Rank', 'Protect_Rank', 'Neutral_Rank']),
                        x='variable', y='value', color='variable', title='Spread of Ranks')
                    st.plotly_chart(box_rank_fig)

                    heatmaps = create_correlation_heatmaps(df)
                    for title, fig in heatmaps.items():
                        st.plotly_chart(fig)

                    st.download_button(
                        label="Download Evaluation Results",
                        data=results_df.to_csv(index=False).encode('utf-8'),
                        file_name='evaluation_results.csv',
                        mime='text/csv',
                    )

if __name__ == "__main__":
    app()
