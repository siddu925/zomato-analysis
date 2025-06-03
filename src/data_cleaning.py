import pandas as pd

def load_data(file_path='C:/Users/sidde/Desktop/8th sem/project/zomato-analysis/data/zomato.csv'):
    """Load the Zomato dataset from a CSV file."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Clean and preprocess the Zomato dataset."""
    # Remove rows with missing critical columns
    df = df.dropna(subset=['name', 'rate', 'votes', 'approx_cost(for two people)', 'listed_in(type)'])
    
    # Clean the 'rate' column (e.g., convert '4.1/5' to 4.1)
    def handle_rate(rate):
        if isinstance(rate, str):
            if '/' in rate:
                return float(rate.split('/')[0])
        return None
    df['rate'] = df['rate'].apply(handle_rate)
    
    # Convert 'approx_cost(for two people)' to numeric, remove commas
    df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(str).str.replace(',', '')
    df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')
    
    # Drop rows with NaN in cleaned columns
    df = df.dropna(subset=['rate', 'approx_cost(for two people)'])
    
    return df

if __name__ == "__main__":
    df = load_data('../data/zomato.csv')
    cleaned_df = clean_data(df)
    cleaned_df.to_csv('../data/cleaned_zomato.csv', index=False)
    print("Cleaned data saved to '../data/cleaned_zomato.csv'")