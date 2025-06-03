import pandas as pd
import json

def generate_json(df, output_path):
    """Generate a JSON file with raw and summary data for the website."""
    # Summary stats
    delivery_stats = df['online_order'].value_counts(normalize=True) * 100
    delivery_data = {'labels': delivery_stats.index.tolist(), 'values': delivery_stats.values.tolist()}
    
    cuisine_stats = df['listed_in(type)'].value_counts()
    cuisine_data = {'labels': cuisine_stats.index.tolist(), 'values': cuisine_stats.values.tolist()}
    
    # Raw data for filtering (convert to list of dicts)
    raw_data = df[['online_order', 'listed_in(type)', 'approx_cost(for two people)']].to_dict('records')
    
    # Combine all data
    output = {
        'delivery': delivery_data,
        'cuisine': cuisine_data,
        'raw': raw_data
    }
    
    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(output, f)
    print(f"JSON data saved to {output_path}")

if __name__ == "__main__":
    df = pd.read_csv('../data/cleaned_zomato.csv')
    generate_json(df, '../static/data/zomato_data.json')