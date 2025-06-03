import pandas as pd
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

if __name__ == "__main__":
    # Load cleaned data
    df = pd.read_csv('../data/cleaned_zomato.csv')
    
    # Generate plots
    plot_delivery(df, '../output/figures/online_vs_offline.png')
    plot_cuisine(df, '../output/figures/cuisine_popularity.png')
    plot_cost_distribution(df, '../output/figures/cost_distribution.png')
    print("Visualizations saved to '../output/figures/'")