import os
from src.data_cleaning import load_data, clean_data
from src.analysis import analyze_delivery, analyze_cuisine, analyze_cost
from src.generate_json import generate_json
import matplotlib.pyplot as plt
import seaborn as sns

def plot_delivery(df, output_path):
    """Plot the proportion of restaurants with online vs offline services."""
    plt.figure(figsize=(8, 6))
    sns.countplot(x='online_order', data=df)
    plt.title('Online vs Offline Order Availability')
    plt.xlabel('Online Order')
    plt.ylabel('Number of Restaurants')
    plt.savefig(output_path)
    plt.close()

def plot_cuisine(df, output_path):
    """Plot the popularity of restaurant types."""
    plt.figure(figsize=(10, 6))
    sns.countplot(y='listed_in(type)', data=df, order=df['listed_in(type)'].value_counts().index)
    plt.title('Popularity of Restaurant Types')
    plt.xlabel('Count')
    plt.ylabel('Restaurant Type')
    plt.savefig(output_path)
    plt.close()

def plot_cost_distribution(df, output_path):
    """Plot the distribution of cost for two people."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df['approx_cost(for two people)'], bins=30, kde=True)
    plt.title('Cost Distribution for Two People')
    plt.xlabel('Approx Cost (for two people)')
    plt.ylabel('Frequency')
    plt.savefig(output_path)
    plt.close()

def main():
    # Ensure output directories exist
    os.makedirs('output/figures', exist_ok=True)
    os.makedirs('output/results', exist_ok=True)
    os.makedirs('static/data', exist_ok=True)
    
    # Load and clean data
    data_path = 'data/zomato.csv'
    df = load_data(data_path)
    cleaned_df = clean_data(df)
    cleaned_df.to_csv('data/cleaned_zomato.csv', index=False)
    
    # Perform analysis
    delivery_stats = analyze_delivery(cleaned_df)
    cuisine_stats = analyze_cuisine(cleaned_df)
    cost_stats = analyze_cost(cleaned_df)
    
    # Save analysis results
    delivery_stats.to_csv('output/results/delivery_stats.csv')
    cuisine_stats.to_csv('output/results/cuisine_stats.csv')
    cost_stats.to_csv('output/results/summary_stats.csv')
    
    # Generate static visualizations
    plot_delivery(cleaned_df, 'output/figures/online_vs_offline.png')
    plot_cuisine(cleaned_df, 'output/figures/cuisine_popularity.png')
    plot_cost_distribution(cleaned_df, 'output/figures/cost_distribution.png')
    
    # Generate JSON for web
    generate_json(cleaned_df, 'static/data/zomato_data.json')
    
    print("Zomato Data Analysis Complete!")
    print("Cleaned data saved to 'data/cleaned_zomato.csv'")
    print("Results saved to 'output/results/'")
    print("Static visualizations saved to 'output/figures/'")
    print("JSON data for website saved to 'static/data/zomato_data.json'")
    print("Open 'templates/index.html' in a browser to view interactive results")

if __name__ == "__main__":
    main()