# Popularity Based Book Recommender System

A command-line program that recommends the most popular books using Python and pandas.

## Problem
Readers have thousands of books to choose from. This project helps them find
books that many people have read and rated highly.

## Questions answered
1. Which books are the most popular?
2. Why must a book have a minimum number of ratings before it is recommended?
3. Which authors have the most highly rated books?
4. How are the ratings spread between High, Medium and Low books?

## Dataset
Book-Crossing dataset (stored in `data/raw/`):

| File | Rows | Main columns |
|---|---|---|
| `Books.csv` | 271,360 | ISBN, Book-Title, Book-Author |
| `Ratings.csv` | 1,149,780 | User-ID, ISBN, Book-Rating (0 to 10) |

## Method
A book is **popular** if it has many ratings **and** a high average rating.

1. **Inspect the data** - print the shape, column names, missing values and rating range.
2. **Clean the data**
   - remove duplicate rows (none were found)
   - remove books with a missing title or author (2 books)
   - remove ratings of 0, because 0 means "not rated" (716,109 ratings, about 62%)
3. **Combine** ratings with book titles using the ISBN.
4. **Calculate** the number of ratings and the average rating of every book.
5. **Create a new column**, `Rating_Level`: High (average 8 or more), Medium (6 to 8) or Low (below 6).
6. **Filter** out books with fewer than the minimum number of ratings (default 50),
   so a book with a single 10-star rating does not rank first.
7. **Sort** the remaining books by average rating.

The cleaned book table is saved to `data/processed/popular_books.csv`.
The raw files are never changed.

## Features
- Show the top N popular books
- Show the top books by an author (partial names work, upper or lower case)
- Change the minimum number of ratings
- Input checking, so wrong input does not crash the program

## Project structure
```
cs project final/
├── data/
│   ├── raw/             Books.csv, Ratings.csv (original data)
│   └── processed/       popular_books.csv (created by the program)
├── project_code.py      the program
├── requirements.txt     libraries needed
├── .gitignore
└── README.md
```

## How to run
```bash
pip install -r requirements.txt
python3 project_code.py
```
A menu appears:
```
1. Show top popular books
2. Show top books by an author
3. Change minimum ratings (currently 50)
4. Exit
```

## Sample result (minimum 50 ratings)
| Rank | Book | Author | Ratings | Average | Level |
|---|---|---|---|---|---|
| 1 | The Two Towers (The Lord of the Rings, Part 2) | J.R.R. Tolkien | 136 | 9.33 | High |
| 2 | The Return of the King (The Lord of the Rings, Part 3) | J.R.R. Tolkien | 103 | 9.21 | High |
| 3 | Harry Potter and the Goblet of Fire (Book 4) | J. K. Rowling | 247 | 9.13 | High |

## Key findings
- **Most ratings are missing.** About 62% of the ratings are 0 ("not rated"). After
  removing them, 433,671 real ratings remain.
- **A minimum rating count is necessary.** Of the 135,565 rated books, 65% have only one
  rating, and 17,050 of them have a perfect average of 10. Without a minimum, these
  books would fill the top of the list.
- **Few books are well established.** Only 651 books have 50 or more ratings, 200 have
  100 or more, and just 27 have 250 or more.
- **Most popular books are rated High or Medium.** Among the 651 books with 50+ ratings,
  218 are High, 429 are Medium and only 4 are Low. The average rating of these books is
  about 7.8.
- **The Lord of the Rings and Harry Potter lead.** *The Two Towers* (9.33), *The Return
  of the King* (9.21) and *Harry Potter and the Goblet of Fire* (9.13) have the highest
  averages with 50+ ratings.
- **Many ratings do not mean a good rating.** *Wild Animus* has 581 ratings, the second
  highest count, but an average of only 4.39. Popularity (many ratings) and quality
  (high average) are different things.
- **Stephen King is the most represented author,** with 40 books that have 50+ ratings,
  followed by James Patterson (17) and Nora Roberts (14).

## Recommendations
- Use a minimum of at least 50 ratings before recommending a book.
- For a more reliable list, raise the minimum to 100 ratings (200 books qualify).
- Combine the number of ratings with the average rating, for example with a weighted
  score, so that very popular books are not hidden behind small, high-scoring ones.

## Limitations
- Not personalised: every user gets the same recommendations.
- New books with no ratings cannot be recommended (cold-start problem).
- Results depend on the minimum ratings value that is chosen.

## Possible improvements
- Use a weighted rating so the number of ratings also affects the rank.
- Add collaborative filtering to give personalised recommendations.
- Build a web interface.

## Tools
Python 3 · pandas

## Author
Jeswin Mammen Jacob
