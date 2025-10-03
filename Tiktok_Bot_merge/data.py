# Load the CSV data into a DataFrame from a file

import pandas as pd

df = pd.read_csv("merged_file2.csv")
import ast


# Remove the dollar sign and convert 'gmv_30d' to a numeric value
def convert_gmv(gmv_str):
    try:
        if "M" in gmv_str:
            return float(gmv_str.replace("$", "").replace("M", "")) * 1e6
        elif "K" in gmv_str:
            return float(gmv_str.replace("$", "").replace("K", "")) * 1e3
        else:
            return float(gmv_str.replace("$", ""))
    except ValueError:
        return None  # Return None for invalid entries


# def check_age_ranges(follower_ages_str):
#     try:
#         follower_ages = ast.literal_eval(follower_ages_str)
#         if '55+' in follower_ages and float(follower_ages['55+']) > 0:
#             return True
#         if '18-24' in follower_ages and float(follower_ages['18-24']) > 0:
#             return True
#         if '25-34' in follower_ages and float(follower_ages['25-34']) > 0:
#             return True
#         if '35-44' in follower_ages and float(follower_ages['35-44']) > 0:
#             return True
#         if '45-54' in follower_ages and float(follower_ages['45-54']) > 0:
#             return True
#         return False
#     except (ValueError, SyntaxError):
#         return False


def check_age_ranges(follower_ages_str, age_ranges):
    try:
        follower_ages = ast.literal_eval(follower_ages_str)
        for age_range in age_ranges:
            if age_range in follower_ages and float(follower_ages[age_range]) > 0:
                return True
        return False
    except (ValueError, SyntaxError):
        return False


# Apply the conversion function to the 'gmv_30d' column
df["gmv_30d"] = df["gmv_30d"].apply(convert_gmv)
# print(df)
# Drop rows with invalid GMV values (None)
df = df.dropna(subset=["gmv_30d"])
# print(df)
# df = df.dropna(subset=['avg_video_engagement_30d'])
# # Drop rows with NaN values in 'product_category'
df = df.dropna(subset=["follower_ages"])

# Define the category to filter by
category_to_filter = "25-34"

# Define the GMV range
gmv_min = 100
gmv_max = 1000
ave = 300
# Filter rows where the product_category column contains the specified category
filtered_data = df[df["follower_ages"].str.contains(category_to_filter)]

# Further filter rows where gmv_30d is within the specified range
filtered_data = filtered_data[
    (filtered_data["gmv_30d"] >= gmv_min) & (filtered_data["gmv_30d"] <= gmv_max)
]

# filtered_data = filtered_data[(filtered_data["gmv_30d"] >= gmv_min)]
# filtered_data = df[(df['gmv_30d'] >= gmv_min)]
print(filtered_data)
# filtered_data = filtered_data[(filtered_data['avg_video_engagement_30d'] >= ave)]
# age_ranges_to_filter = ['25-34']

# # # Apply the age range check function and filter the data
# filtered_data = filtered_data[filtered_data['follower_ages'].apply(check_age_ranges, age_ranges=age_ranges_to_filter)]
usernames = filtered_data[["handle"]]

# # Write the usernames to a new CSV file
usernames.to_csv("jeff22.csv", index=False)

# # Display the filtered data
# print(filtered_data)
