import pandas as pd


def update_csv(data, file_path):
    new_data_df = pd.DataFrame(data)
    try:
        existing_df = pd.read_csv(file_path)
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=["title", "champion", "href"])

    updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
    updated_df.to_csv(file_path, index=False)
