import streamlit as st
import pandas as pd
from datetime import datetime
from SampleClaimsFunction import *
from io import BytesIO
dataset=st.selectbox("Select Dataset",["Health","Fire","Motor"])

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

st.title("Insurance Claims Dashboard")

summary=aggregation(df,"TOTAL")
st.header("Overall Summary")
col1,col2,col3=st.columns([1,2,1])
with col1:
    st.metric("Count",f"{int(summary.iloc[0]["Value"]):,}")
with col2:
    st.metric("Sum",f"{summary.iloc[1]["Value"]:,.2f}")
with col3:
    st.metric("Average",f"{summary.iloc[2]["Value"]:,.2f}")

option = st.selectbox(
    "Choose Analysis",
    [
        "Category Analysis",
        "Duplicate Policies",
        "Policy Claim Frequency"
    ]
)

if option == "Category Analysis":
    result=categoryTable(df, "PAYEE_CATEGORY", "TOTAL")
    st.dataframe(result)
    download_format = st.selectbox(
    "Download Format",
    ["CSV", "Excel"])
    
    data,file_name,mime=download_block(result,option,download_format)
    st.download_button(
    label=f"Download {download_format}",
    data=data,
    file_name=file_name,
    mime=mime)
    graph_type = st.selectbox(
    "Select Graph",
    ["Bar Chart", "Line Chart"])
    if graph_type=="Bar Chart":
        st.header("Bar Chart - Total Sum")
        st.bar_chart(result["Total_Sum"])
    elif graph_type=="Line Chart":
        st.header("Line Chart - Total Sum")
        st.line_chart(result["Total_Sum"])
elif option == "Duplicate Policies":
    dp=duplicateCount(df,"POLICY_NO")
    dp.index.name="Index"
    st.write(dp)
    download_format = st.selectbox(
    "Download Format",
    ["CSV", "Excel"])
    data,file_name,mime=download_block(dp,option,download_format)
    st.download_button(
    label=f"Download {download_format}",
    data=data,
    file_name=file_name,
    mime=mime)
    

else:
    pwc=policyWiseCount(df)
    pwc.index.name="Index"
    st.write(pwc)
    download_format = st.selectbox(
    "Download Format",
    ["CSV", "Excel"])
    data,file_name,mime=download_block(pwc,option,download_format)
    st.download_button(
    label=f"Download {download_format}",
    data=data,
    file_name=file_name,
    mime=mime)
    graph_type = st.selectbox(
    "Select Graph",
    ["Bar Chart", "Line Chart"])
    if graph_type=="Bar Chart":
        st.header("Bar Chart - Count Based On Category")
        st.bar_chart(pwc.count())
    elif graph_type=="Line Chart":
        st.header("Line Chart - Count Based On Category")
        st.line_chart(pwc.count())
    
