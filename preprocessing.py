import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# =========================================================
# ML PREPROCESSING FUNCTION
# =========================================================
def preprocess_fitness_data(df):

    steps = []
    report = {}

    # Before cleaning
    report["nulls_before"] = df.isnull().sum()

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    steps.append("Converted Date column to datetime.")

    # Sort for time-series correctness
    df = df.sort_values(by=["User_ID", "Date"])
    steps.append("Sorted dataset by User_ID and Date.")

    numeric_cols = [
        "Hours_Slept",
        "Water_Intake (Liters)",
        "Active_Minutes",
        "Heart_Rate (bpm)"
    ]

    # Interpolation
    df[numeric_cols] = df.groupby("User_ID")[numeric_cols].transform(
        lambda x: x.interpolate(method="linear")
    )
    steps.append("Applied user-wise linear interpolation.")

    # Forward/Backward fill
    df[numeric_cols] = df.groupby("User_ID")[numeric_cols].transform(
        lambda x: x.ffill().bfill()
    )
    steps.append("Handled boundary nulls using forward/backward fill.")

    # Categorical fill
    df["Workout_Type"] = df["Workout_Type"].fillna("No Workout")
    steps.append("Filled missing Workout_Type with 'No Workout'.")

    # After cleaning
    report["nulls_after"] = df.isnull().sum()

    return df, steps, report


# =========================================================
# EDA FUNCTION
# =========================================================
def run_eda(df):

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_cols = [
        "Steps_Taken",
        "Calories_Burned",
        "Hours_Slept",
        "Active_Minutes",
        "Heart_Rate (bpm)",
        "Stress_Level (1-10)"
    ]

    results = {}

    results["date_range"] = (df["Date"].min(), df["Date"].max())
    results["correlation"] = df[numeric_cols].corr()
    results["user_summary"] = df.groupby("User_ID")[numeric_cols].mean()
    results["workout_counts"] = df["Workout_Type"].value_counts()

    sample_user = df["User_ID"].iloc[0]
    results["sample_user"] = df[df["User_ID"] == sample_user].sort_values("Date")

    results["numeric_cols"] = numeric_cols

    return results   # 🔥 THIS LINE MUST EXIST

   