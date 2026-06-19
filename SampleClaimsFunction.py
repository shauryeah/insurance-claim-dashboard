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
print(categoryTable(hi,"PRODUCT_CODE","TOTAL"))
print(aggregation(mi,"TOTAL"))
print(duplicateCount(fi,"POLICY_NO"))
print(policyWiseCount(hi))

