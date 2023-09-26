import pandas as pd
import os
import re


def clean_comment(comment):

    if pd.notna(comment):
        # Remove 'nan' and leading/trailing whitespaces
        comment = comment.replace('nan', '').strip()
        
        # Replace '|' with newlines
        comment = comment.replace('|', '\n')
        
        # Extract and format timestamps
        comment = re.sub(r'(\d{2}/\w{3}/\d{2} \d{2}:\d{2});[^\n]*', r'\1', comment)
    
    return comment

def main():

    downloads = f'{os.path.expanduser("~")}{os.sep}Downloads{os.sep}'
    source_csv = f"{downloads}data.csv"
    excel_report = f"{downloads}output.xlsx"

    basic_cols = ['Issue key', 'Summary', 'Description', 'Status']

    df = pd.read_csv(source_csv)

    comment_cols = [col for col in df.columns if col.startswith('Comment')]
    cols_to_keep = basic_cols + comment_cols

    # Extract the columns you want to keep
    df = df[cols_to_keep]
    df['All Comments']= df[comment_cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    df.drop(comment_cols, axis=1, inplace=True)

    df['All Comments'] = df['All Comments'].apply(clean_comment)

    # Create an Excel writer object
    excel_writer = pd.ExcelWriter(excel_report, engine='openpyxl')

    # Iterate over unique values in the 'Status' column and save each as a separate tab
    for status_value in df['Status'].unique():
        status_df = df[df['Status'] == status_value]
        status_df.to_excel(excel_writer, sheet_name=status_value, index=False)

    # Save the Excel file
    excel_writer.save()

    print(f"Data separated by 'Status' column and saved to {excel_report}")

if __name__ == "__main__":
    main()