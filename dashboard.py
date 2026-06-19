import streamlit as st
import pandas as pd
from datetime import datetime
from SampleClaimsFunction import *
from io import BytesIO

st.markdown("""
<style>
thead tr th {
    background-color: #003366 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="Insurance Claims Dashboard",
    page_icon="📊",
    layout="wide"
)

with st.sidebar:
    st.image("logo.svg", width=250)
    st.header("⚙️ Dashboard Controls")

    dataset = st.radio(
    "Select Dataset",
    ["Health", "Fire", "Motor"])

def to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    return output.getvalue()

def download_block(df, analysis_name, download_format):
    today = datetime.today().strftime("%Y-%m-%d")
    safe_name = analysis_name.replace(" ", "_")

    if download_format == "CSV":
        data = df.to_csv(index=False)
        file_name = f"{safe_name}-{today}.csv"
        mime = "text/csv"

    else:
        data = to_excel(df)
        file_name = f"{safe_name}-{today}.xlsx"
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return data, file_name, mime


if dataset=="Health":
    df=pd.read_csv("SampleHealthClaims-Export Worksheet.csv")
elif dataset=="Fire":
    df=pd.read_csv("SampleClaimsFire-Export Worksheet.csv")
else:
    df=pd.read_csv("SampleClaimsMotor-Export Worksheet.csv")

st.title("📊 Insurance Claims Dashboard")
st.markdown(
    "### Claims Analytics and Reporting Portal"
)
st.markdown(
    "*Monitor claims, identify duplicates, and analyze policy trends across Health, Fire, and Motor portfolios.*"
)
st.divider()

summary=aggregation(df,"TOTAL")
with st.container():
    st.subheader("Overall Summary")
col1,col2,col3=st.columns([1,2,1])
with col1:
    st.metric("Count",f"{int(summary.iloc[0]["Value"]):,}")
with col2:
    st.metric("Sum",f"{summary.iloc[1]["Value"]:,.2f}")
with col3:
    st.metric("Average",f"{summary.iloc[2]["Value"]:,.2f}")
st.divider()
st.subheader("Analysis")

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Category Analysis",
        "🔍 Duplicate Policies",
        "📈 Policy Claim Frequency"
    ]
)

with tab1:
    result = categoryTable(df, "PAYEE_CATEGORY", "TOTAL")

    with st.expander("Category Analysis Results", expanded=True):

        st.dataframe(result, hide_index=True,use_container_width=True)

        st.subheader("📥 Export")

        download_format = st.selectbox(
            "Download Format",
            ["CSV", "Excel"],
            key="cat_download"
        )

        data, file_name, mime = download_block(
            result,
            "Category Analysis",
            download_format
        )

        st.download_button(
            label=f"Download {download_format}",
            data=data,
            file_name=file_name,
            mime=mime
        )

        st.subheader("📈 Visualization")

        graph_type = st.selectbox(
            "Select Graph",
            ["Bar Chart", "Line Chart"],
            key="cat_graph"
        )

        if graph_type == "Bar Chart":
            st.subheader("Bar Chart - Total Sum")
            st.bar_chart(result["Total_Sum"])

        else:
            st.subheader("Line Chart - Total Sum")
            st.line_chart(result["Total_Sum"])
with tab2:
    dp=duplicateCount(df,"POLICY_NO")
    search = st.text_input(
    "🔎 Search Policy Number",
    key="dup_search")
    dp.index.name="Index"
    if search:
        dp = dp[
            dp["POLICY_NO"]
            .astype(str)
            .str.contains(search, case=False, na=False)
        ]
    with st.expander("Duplicate Policy Results", expanded=True):
        st.dataframe(dp,hide_index=True)
        st.subheader("📥 Export")
        download_format = st.selectbox(
        "Download Format",
        ["CSV", "Excel"],
        key="dup_download")
        data,file_name,mime=download_block(dp,"Duplicate Policy Results",download_format)
        st.download_button(
        label=f"Download {download_format}",
        data=data,
        file_name=file_name,
        mime=mime)
    

with tab3:
    pwc=policyWiseCount(df)
    pwc.index.name="Index"
    with st.expander("Policy Claim Frequency Results", expanded=True):
        st.dataframe(pwc,hide_index=True)
        st.subheader("📥 Export")
        download_format = st.selectbox(
        "Download Format",
        ["CSV", "Excel"],
        key="freq_download")
        data,file_name,mime=download_block(pwc,"Policy Wise Count",download_format)
        st.download_button(
        label=f"Download {download_format}",
        data=data,
        file_name=file_name,
        mime=mime)
        st.subheader("📈 Visualization")
        graph_type = st.selectbox(
        "Select Graph",
        ["Bar Chart", "Line Chart"],
        key="freq_graph")
        if graph_type=="Bar Chart":
            st.header("Bar Chart - Count Based On Category")
            st.bar_chart(pwc.count())
        elif graph_type=="Line Chart":
            st.header("Line Chart - Count Based On Category")
            st.line_chart(pwc.count())
    
st.divider()
st.caption(
    "📊 Insurance Claims Dashboard | Built using Streamlit and Pandas"
)
