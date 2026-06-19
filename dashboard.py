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
    if dataset == "Fire":
        dashboard_type = st.radio(
            "Select Dashboard",
            ["Claims", "Premiums"]
        )

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

def show_claim_dashboard(df):
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
                st.subheader("Bar Chart - Count Based On Category")
                st.bar_chart(pwc.count())
            elif graph_type=="Line Chart":
                st.subheader("Line Chart - Count Based On Category")
                st.line_chart(pwc.count())
        
    st.divider()
    st.caption(
        "📊 Insurance Claims Dashboard | Built using Streamlit and Pandas"
    )




def show_premium_dashboard(df):    
    st.title("📊 Fire Premium Dashboard")
    st.markdown("### Premium Analytics and Reporting Portal")
    summary = premiumSummary(df)

    st.subheader("Overall Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Policy Count",
            f"{int(summary.iloc[0]['Value']):,}"
        )

    with col2:
        st.metric(
            "Total Premium",
            f"{summary.iloc[1]['Value']:,.2f}"
        )
    tab1, tab2, tab3 = st.tabs([
        "📦 Product Analysis",
        "🏢 RO Analysis",
        "📈 Premium vs Claims"
    ])
    with tab1:

        result = productWisePremium(df)

        st.dataframe(
            result,
            hide_index=True,
            use_container_width=True
        )
        st.subheader("📥 Export")

        download_format = st.selectbox(
            "Download Format",
            ["CSV", "Excel"],
            key="product_download"
        )

        data, file_name, mime = download_block(
            result,
            "Product Wise Premium",
            download_format
        )

        st.download_button(
            label=f"Download {download_format}",
            data=data,
            file_name=file_name,
            mime=mime
        )
        graph_type = st.selectbox(
        "Select Graph",
        ["Bar Chart", "Line Chart"],
        key="product_graph"
        )
        if graph_type == "Bar Chart":
            st.bar_chart(
                result.set_index("PRODUCT_NAME")
                ["Premium_Amount"]
            )
        else:
            st.line_chart(
                result.set_index("PRODUCT_NAME")
                ["Premium_Amount"]
            )
    with tab2:
        result = roWisePremium(df)

        st.dataframe(
            result,
            hide_index=True,
            use_container_width=True
        )
        st.subheader("📥 Export")

        download_format = st.selectbox(
            "Download Format",
            ["CSV", "Excel"],
            key="ro_download"
        )

        data, file_name, mime = download_block(
            result,
            "RO Wise Premium",
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
            key="ro_graph"
        )
        if graph_type == "Bar Chart":
            st.bar_chart(
                result.set_index("REGIONAL_OFFICE_CODE")
                ["Premium_Amount"]
            )
        else:
            st.line_chart(
                result.set_index("REGIONAL_OFFICE_CODE")
                ["Premium_Amount"]
            )
    with tab3:

        claims_df = pd.read_csv(
            "SampleClaimsFire-Export Worksheet.csv"
        )

        total_premium = premium_df["TOTAL_PREMIUM"].sum()
        total_claims = claims_df["TOTAL"].sum()

        profit_loss = total_premium - total_claims

        loss_ratio = (
            total_claims / total_premium
        ) * 100

        coverage = (
            total_premium / total_claims
        )

        st.subheader("💰 Premium vs Claims Breakdown")

        # -------------------------------
        # SECTION FUNCTION (REUSABLE)
        # -------------------------------
        def section(title, value, pie_data):

            st.markdown(f"## {title}")

            col1, col2 = st.columns([1, 2])

            with col1:
                st.metric(title, f"{value:,.2f}")

            with col2:
                st.bar_chart(pie_data)

            st.divider()


        # -------------------------------
        # SECTION 1 - TOTAL PREMIUM
        # -------------------------------
        section(
            "Total Premium",
            total_premium,
            pd.DataFrame({
                "Value": [total_premium, total_claims]
            }, index=["Premium", "Claims"])
        )

        # -------------------------------
        # SECTION 2 - TOTAL CLAIMS
        # -------------------------------
        section(
            "Total Claims",
            total_claims,
            pd.DataFrame({
                "Value": [total_claims, total_premium]
            }, index=["Claims", "Premium"])
        )

        # -------------------------------
        # SECTION 3 - PROFIT / LOSS
        # -------------------------------
        section(
            "Profit / Loss",
            profit_loss,
            pd.DataFrame({
                "Value": [
                    total_premium,
                    total_claims,
                    profit_loss
                ]
            }, index=[
                "Premium",
                "Claims",
                "Net"
            ])
        )

        # -------------------------------
        # SECTION 4 - LOSS RATIO
        # -------------------------------
        section(
            "Loss Ratio (%)",
            loss_ratio,
            pd.DataFrame({
                "Value": [
                    total_claims,
                    total_premium - total_claims
                ]
            }, index=[
                "Claims",
                "Remaining Premium"
            ])
        )

        # -------------------------------
        # SECTION 5 - COVERAGE
        # -------------------------------
        section(
            "Premium Coverage (x)",
            coverage,
            pd.DataFrame({
                "Value": [
                    total_premium,
                    total_claims
                ]
            }, index=["Premium", "Claims"])
        )




st.divider()
if dataset=="Health":
    df = pd.read_csv("SampleHealthClaims-Export Worksheet.csv")
    show_claim_dashboard(df)

elif dataset=="Fire":

    

    if dashboard_type == "Claims":

        claims_df = pd.read_csv(
            "SampleClaimsFire-Export Worksheet.csv"
        )

        show_claim_dashboard(claims_df)

    else:

        premium_df = pd.read_csv(
            "Fire_Premium_FY25_26-Export Worksheet.csv"
        )

        show_premium_dashboard(premium_df)

else:

    df = pd.read_csv(
        "SampleClaimsMotor-Export Worksheet.csv"
    )

    show_claim_dashboard(df)
