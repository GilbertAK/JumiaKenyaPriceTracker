# 🛒 Project: Jumia Kenya Price Intelligence Tracker

## 📖 Project Overview
This tool is a professional E-commerce monitoring system designed for the **Kenyan smartphone market**. It automates the collection of pricing data, discounts, and customer sentiment (ratings) from Jumia Kenya to provide competitive market insights.

## 🎯 Key Features
* **Large Scale Extraction:** Targets **3,000+ unique products** across the smartphone category.
* **Smart Price Cleaning:** Automatically converts currency strings (KSh) into integers for direct mathematical analysis.
* **Sentiment Analysis:** Captures star ratings and review counts to identify top-performing brands.
* **Anti-Detection Logic:** Implements randomized request headers and human-like browsing delays.

## ⚙️ Engineering Highlights
1. **Deduplication:** Ensures no duplicate listings using Pandas unique-constraint logic.
2. **Resilience:** Built-in error handling for network timeouts and 403 Forbidden errors.
3. **Data Quality:** Filters out incomplete listings to maintain a 99% data fill rate.

## 📊 Business Application
Retailers can use this dataset to:
- Monitor competitors' discount strategies in real-time.
- Identify the most popular smartphone brands in the Nairobi region.
- Optimize their own pricing based on market averages.
