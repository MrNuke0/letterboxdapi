from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
import uvicorn

app = FastAPI(title="Letterboxd API", version="0.1")

version = "0.1"


@app.get('/')
async def root():
    return f"Letterboxd Scraper v{version}"

@app.get('/latest/{user}')
async def get_latest_entry(user: str):
    return latest_entry(user)


# function to scrape the latest diary entry of a letterboxd user
def latest_entry(username: str):
    url = f"https://letterboxd.com/{username}/rss/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")

    user_link = f"https://letterboxd.com/{username}/"
    link = soup.find('link').text

    if soup.find('link') is None:
        return "could not find user"

    if user_link == link:
        item = soup.find('item')
        if item is None:
            return "could not find any new entries"
        if item.watchedDate is not None:
            title = item.title.text
            entry_link = item.link.text
            movie_name = item.filmTitle.text
            movie_year = item.filmYear.text
            user_rating = item.memberRating.text
            description = item.description.text
            pubdate = item.pubDate.text

            dictionary = {"title": title,
                    "film-title": movie_name,
                    "film-year": movie_year,
                    "link": entry_link,
                    "rating": user_rating,
                    "date": pubdate
                    }

            return dictionary



if __name__ == "__main__":
    print(latest_entry("mrnuke"))
    uvicorn.run(app, host="127.0.0.1", port=8000)








