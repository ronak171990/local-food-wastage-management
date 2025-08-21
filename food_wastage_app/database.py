import pandas as pd
import os

# Use correct filenames
providers_file = "providers.csv"
receivers_file = "receivers.csv"
food_listings_file = "listings.csv"
claims_file = "claims.csv"   # if you also have claims data

def load_csv(file_path):
    """Generic CSV loader with clean column names"""
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip().str.lower()
    return df

def get_providers():
    """Load providers data"""
    return load_csv(providers_file)

def get_receivers():
    """Load receivers data"""
    return load_csv(receivers_file)

def get_food_listings():
    """Load food listings data"""
    return load_csv(food_listings_file)

def get_claims():
    """Load claims data"""
    return load_csv(claims_file)
