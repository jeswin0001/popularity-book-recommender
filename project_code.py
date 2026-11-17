# -*- coding: utf-8 -*-
"""Popularity Based Book Recommender System (command-line menu)

Dataset: Book-Crossing (data/raw/Books.csv, data/raw/Ratings.csv)
Method : a book is popular if it has many ratings AND a high average rating.
         Books with fewer than the minimum number of ratings are ignored,
         then the rest are sorted by average rating.
"""

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')


def inspect_data(books, ratings):
    """Print a quick look at the raw data (shape, columns, missing values)."""
    print("\n--- Data Inspection ---")
    print(f"Books   : {books.shape[0]} rows, {books.shape[1]} columns")
    print(f"Columns : {list(books.columns)}")
    print(f"Ratings : {ratings.shape[0]} rows, {ratings.shape[1]} columns")
    print(f"Columns : {list(ratings.columns)}")

    print("Missing values in Books:")
    missing = books.isnull().sum()
    print(missing[missing > 0].to_string() if missing.sum() > 0 else "  none")
    print("Missing values in Ratings:")
    missing = ratings.isnull().sum()
    print(missing[missing > 0].to_string() if missing.sum() > 0 else "  none")

    print(f"Rating range: {ratings['Book-Rating'].min()} to {ratings['Book-Rating'].max()}")


def rating_level(avg):
    """Group an average rating into High, Medium or Low."""
    if avg >= 8:
        return 'High'
    elif avg >= 6:
        return 'Medium'
    else:
        return 'Low'


def clean_data(books, ratings):
    """Clean the raw data and print what was removed."""
    print("\n--- Data Cleaning ---")
    print(f"Books before cleaning   : {len(books)}")
    print(f"Ratings before cleaning : {len(ratings)}")

    # 1. remove duplicate rows
    dup_books = books.duplicated().sum()
    dup_ratings = ratings.duplicated().sum()
    books = books.drop_duplicates()
    ratings = ratings.drop_duplicates()
    print(f"Duplicate rows removed  : {dup_books} books, {dup_ratings} ratings")

    # 2. remove books with missing title or author
    missing_books = books[['Book-Title', 'Book-Author']].isnull().any(axis=1).sum()
    books = books.dropna(subset=['Book-Title', 'Book-Author'])
    print(f"Missing title/author    : {missing_books} books removed")

    # 3. a rating of 0 means "not rated" in this dataset, so remove it
    zero_ratings = (ratings['Book-Rating'] == 0).sum()
    ratings = ratings[ratings['Book-Rating'] > 0]
    print(f"Zero ratings removed    : {zero_ratings}")

    print(f"Ratings after cleaning  : {len(ratings)}")
    return books, ratings


def load_data():
    """Load the CSV files, clean them and calculate the number of ratings and average rating of each book."""
    books = pd.read_csv(os.path.join(RAW_DIR, 'Books.csv'), low_memory=False)
    ratings = pd.read_csv(os.path.join(RAW_DIR, 'Ratings.csv'))

    inspect_data(books, ratings)
    books, ratings = clean_data(books, ratings)

    ratings_with_name = ratings.merge(books, on='ISBN')

    # number of ratings of each book
    num_rating_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
    num_rating_df.rename(columns={'Book-Rating': 'num_ratings'}, inplace=True)

    # average rating of each book
    avg_rating_df = ratings_with_name.groupby('Book-Title')['Book-Rating'].mean().reset_index()
    avg_rating_df.rename(columns={'Book-Rating': 'avg_rating'}, inplace=True)

    # join both tables and add the author name
    popular_df = num_rating_df.merge(avg_rating_df, on='Book-Title')
    popular_df = popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')
    popular_df = popular_df[['Book-Title', 'Book-Author', 'num_ratings', 'avg_rating']]

    # new column: High (8 and above), Medium (6 to 8) or Low (below 6)
    popular_df['Rating_Level'] = popular_df['avg_rating'].apply(rating_level)

    # save the cleaned result so the raw data is never changed
    popular_df.to_csv(os.path.join(PROCESSED_DIR, 'popular_books.csv'), index=False)

    return popular_df


def get_popular_books(popular_df, n, min_ratings, author=None):
    """Return the top n books that have at least min_ratings ratings."""
    result = popular_df[popular_df['num_ratings'] >= min_ratings]

    if author:
        result = result[result['Book-Author'].str.contains(author, case=False, na=False)]

    return result.sort_values('avg_rating', ascending=False).head(n)


def show_books(df):
    """Print the books one by one."""
    if df.empty:
        print("\nNo books found. Try a lower minimum ratings value.")
        return

    print("\n--- Recommended Books ---")
    rank = 1
    for index, row in df.iterrows():
        print(f"{rank}. {row['Book-Title']}")
        print(f"   Author  : {row['Book-Author']}")
        print(f"   Ratings : {row['num_ratings']}   Average: {row['avg_rating']:.2f} ({row['Rating_Level']})")
        rank = rank + 1


def ask_number(message, default):
    """Ask the user for a number. Use the default if the input is not valid."""
    text = input(message).strip()
    if text.isdigit() and int(text) > 0:
        return int(text)
    print(f"Invalid number, using {default}.")
    return default


def main():
    print("Loading data, please wait...")
    popular_df = load_data()
    min_ratings = 50

    while True:
        print("\n===== Popular Book Recommender =====")
        print("1. Show top popular books")
        print("2. Show top books by an author")
        print(f"3. Change minimum ratings (currently {min_ratings})")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            n = ask_number("How many books do you want? ", 10)
            show_books(get_popular_books(popular_df, n, min_ratings))

        elif choice == '2':
            author = input("Enter author name (e.g. Stephen King): ").strip()
            if author == '':
                print("Author name cannot be empty.")
            else:
                n = ask_number("How many books do you want? ", 10)
                show_books(get_popular_books(popular_df, n, min_ratings, author))

        elif choice == '3':
            min_ratings = ask_number("Enter minimum ratings (e.g. 50): ", min_ratings)
            print(f"Minimum ratings set to {min_ratings}.")

        elif choice == '4':
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please enter 1, 2, 3 or 4.")


main()
