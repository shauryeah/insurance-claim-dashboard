import pandas as pd
pd.set_option('display.float_format', '{:.2f}'.format)
hi= pd.read_csv("SampleHealthClaims-Export Worksheet.csv")
fi=pd.read_csv("SampleClaimsFire-Export Worksheet.csv")
mi=pd.read_csv("SampleClaimsMotor-Export Worksheet.csv")

def categoryTable(df, group_col, value_col):
    return (
        df.groupby(group_col)[value_col]
        .agg(
            Count="count",
            Total_Sum="sum",
            Average="mean"
        )
        .round(2)
        
    )
def aggregation(df,value_col):
    return pd.DataFrame({
            "Metric":["Count","Sum","Mean"],
            "Value":[df[value_col].count(),df[value_col].sum(),df[value_col].mean()]}).round(2)
def duplicateCount(df,policy_col):
    return (
        df[policy_col].value_counts().reset_index().query("count > 1"))
def policyWiseCount(df):
    counts=df["POLICY_NO"].value_counts()
    return pd.DataFrame({"2 to 5 Claims: ": pd.Series(counts[(counts>=2) & (counts<=5)].index),
                         "5 to 10 Claims: ": pd.Series(counts[(counts>=6) & (counts<=10)].index),
                         "Greater than 10 Claims: ": pd.Series(counts[(counts>10)].index)})
def premiumSummary(df):
    return pd.DataFrame({
        "Metric":["Policy Count","Total Premium"],
        "Value":[df["POLICY_NUMBER"].count(),df["TOTAL_PREMIUM"].sum()]}).round(2)
#pf=pd.read_csv("Fire_Premium_FY25_26-Export Worksheet.csv")
def productWisePremium(df):

    result = (
        df.groupby("PRODUCT_NAME")
        .agg(
            Policy_Count=("POLICY_NUMBER", "nunique"),
            Premium_Amount=("TOTAL_PREMIUM", "sum")
        )
        .reset_index()
    )

    return result

def roWisePremium(df):

    result = (
        df.groupby("REGIONAL_OFFICE_CODE")
        .agg(
            Policy_Count=("POLICY_NUMBER", "nunique"),
            Premium_Amount=("TOTAL_PREMIUM", "sum")
        )
        .reset_index()
    )

    return result
def premiumClaimSummary(premium_df, claims_df):

    total_premium = premium_df["TOTAL_PREMIUM"].sum()

    total_claims = claims_df["TOTAL"].sum()

    profit_loss = total_premium - total_claims

    loss_ratio = (
        total_claims / total_premium
    ) * 100

    premium_coverage = (
        total_premium / total_claims
    )

    return {
        "total_premium": total_premium,
        "total_claims": total_claims,
        "profit_loss": profit_loss,
        "loss_ratio": loss_ratio,
        "premium_coverage": premium_coverage
    }

