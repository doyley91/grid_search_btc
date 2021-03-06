#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:23:18 2019

@author: pascal-baur
"""

import stock_scraper as scraper
import pandas as pd
import sqlite3


def createList():
    #df = pd.read_csv("sp500-constituents.csv")
    #stock_list = df['Symbol'].values
    stock_list = ['AAPL', 'TSLA', 'MSFT', 'AMZN', 'NFLX', 'GOOG'] # TODO: import file with ticker list to download
    return stock_list

def main():
    conn = sqlite3.connect('/Users/pascal-baur/Desktop/grid_search_/main.db')
    stock_list = createList()
    interested = ['Market Cap (intraday)', 'Return on Equity', 'Revenue', 'Quarterly Revenue Growth', 
    'Operating Cash Flow', 'Total Cash', 'Total Debt', 'Current Ratio', '52-Week Change',
    'Avg Vol (3 month)', 'Avg Vol (10 day)', '% Held by Insiders']
    #technicals = {}
    df = pd.DataFrame(columns=interested)
    for ticker in stock_list:
        tech = scraper.scrape_yahoo(ticker)
        for ind in interested:    
            try:
                df.at[ticker, ind] = tech[ind]
            except Exception as e:
                print('Failed, exception: ', str(e))
        print("DONE- " + ticker)
    #Correct column name
    df.rename(index=str, columns={df.columns[0]: "Symbol"}, inplace=True)
    
    # Merge symbols with data df to get name of company and industry
    #df = df.join(df_symbols.set_index('Symbol'), on="Symbol")

    # Drop rows with excessive NaN values
    df.dropna(thresh=10, inplace=True)
    # Save as CSV
    #df.to_csv("data.csv")
    
    #Save to DB
    df.to_sql('Fundamentals', conn, if_exists='replace', index=True)


if __name__ == "__main__":
    main()