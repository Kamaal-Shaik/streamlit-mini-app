import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from setuptools.command.rotate import rotate

# Title and description
st.title("Interactive Sales Dashboard")
st.write("Upload a CSV file with sales and profit data to analyze and visualize results.")

# File uploader (only CSV allowed)
uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)
    st.write("Preview the Data:")
    st.dataframe(df.head())

    metric = st.selectbox("Choose a metric", ["sales", "profit"])

    # Calculate total
    total_value = df[metric].sum()
    st.write(f"**Total {metric.capitalize()}:** {round(total_value, 3)}")

    # Aggregate by region
    agg_by_region = df.groupby("region")[metric].sum()
    st.write(f"**{metric.capitalize()} by Region:**")
    st.write(agg_by_region)

    # Dropdown for the chart type
    chart_type = st.selectbox("Choose a chart type:", ["Bar", "Line", "Pie"])

    fig, ax = plt.subplots()

    if chart_type == 'Bar':
        agg_by_region.plot(kind="bar", ax=ax, color="skyblue", edgecolor="black")
        ax.set_ylabel(metric.capitalize())
        ax.set_title(f"{metric.capitalize()} by Region")
    elif chart_type == "Line":
        agg_by_region.plot(kind="line", marker="o", ax=ax, color="green")
        ax.set_ylabel(metric.capitalize())
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_title(f"{metric.capitalize()} by Region (Line Chart)")
    elif chart_type == "Pie":
        agg_by_region.plot(kind="pie", autopct="%1.1f%%", ax=ax, textprops={'fontsize': 6})

        ax.set_ylabel("")  # Hide Y-axis for pie chart
        ax.set_title(f"{metric.capitalize()} Distribution by Region")

    # Show chart in Streamlit
    st.pyplot(fig)

    # Prepare processed results
    processed_df = agg_by_region.reset_index()
    processed_df.columns = ["Region", metric.capitalize()]

    # Download button
    csv = processed_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Processed Data as CSV",
        data=csv, file_name=f"{metric}_by_region.csv", mime="text/csv"
    )
