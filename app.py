from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def simplify_product_name(name):
    # Remove any text in parentheses
    name = re.sub(r'\([^)]*\)', '', name)
    # Remove specific common words and extra spaces
    name = re.sub(r'\b(Inc\.|Corporation|Corp\.|Ltd\.|Limited|LLC)\b', '', name)
    # Remove multiple spaces and trim
    name = ' '.join(name.split())
    # Limit to first 30 characters if too long, but keep whole words
    if len(name) > 30:
        words = name[:30].split()
        name = ' '.join(words[:-1]) + '...'
    return name

# Load and process data
def load_data():
    df = pd.read_csv("superstore_data.csv", encoding="ISO-8859-1")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Profit Margin (%)'] = (df['Profit'] / df['Sales']) * 100
    # Simplify product names
    df['Simple Product Name'] = df['Product Name'].apply(simplify_product_name)
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard_data')
def dashboard_data():
    df = load_data()
    
    # Calculate key metrics
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    avg_profit_margin = df['Profit Margin (%)'].mean()
    
    # Sales by region
    sales_by_region = df.groupby('Region')['Sales'].sum().to_dict()
    
    # Monthly sales trend
    monthly_sales = df.groupby(df['Order Date'].dt.strftime('%Y-%m'))['Sales'].sum().tail(12).to_dict()
    
    # Top products with detailed metrics
    top_products_df = df.groupby('Simple Product Name').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    
    top_products_df['Profit Margin (%)'] = (top_products_df['Profit'] / top_products_df['Sales']) * 100
    top_products_df = top_products_df.nlargest(5, 'Sales')
    
    top_products = {
        product: {
            'sales': float(row['Sales']),
            'profit': float(row['Profit']),
            'profit_margin': float(row['Profit Margin (%)']),
            'quantity': int(row['Quantity'])
        }
        for product, row in top_products_df.set_index('Simple Product Name').iterrows()
    }
    
    return jsonify({
        'metrics': {
            'total_sales': float(total_sales),
            'total_profit': float(total_profit),
            'avg_profit_margin': float(avg_profit_margin)
        },
        'sales_by_region': sales_by_region,
        'monthly_sales': monthly_sales,
        'top_products': top_products
    })

if __name__ == '__main__':
    app.run(debug=True) 