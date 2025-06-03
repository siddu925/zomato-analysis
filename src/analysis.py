import pandas as pd

def analyze_delivery(df):
    """Analyze the proportion of restaurants offering online delivery."""
    online_delivery = df['online_order'].value_counts(normalize=True) * 100
    return online_delivery

def analyze_cuisine(df):
    """Analyze the most favored restaurant types (cuisines)."""
    cuisine_types = df['listed_in(type)'].value_counts()
    return cuisine_types

def analyze_cost(df):
    """Analyze the cost distribution for two people."""
    cost_summary = df['approx_cost(for two people)'].describe()
    return cost_summary

if __name__ == "__main__":
    df = pd.read_csv('../data/cleaned_zomato.csv')
    delivery_stats = analyze_delivery(df)
    cuisine_stats = analyze_cuisine(df)
    cost_stats = analyze_cost(df)
    delivery_stats.to_csv('../output/results/delivery_stats.csv')
    cuisine_stats.to_csv('../output/results/cuisine_stats.csv')
    cost_stats.to_csv('../output/results/summary_stats.csv')
    print("Delivery Stats:\n", delivery_stats)
    print("\nCuisine Popularity:\n", cuisine_stats)
    print("\nCost Summary:\n", cost_stats)