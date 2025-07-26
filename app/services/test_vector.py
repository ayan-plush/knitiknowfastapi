# from app.utils.save_vectors import save_vectorized_article
# import requests

# def vectorizeArticle():
#     article = {
#         "_id": {"$oid": "6872cff01f83845ca8756475"},
#         "politician": {"$oid": "6853fbb2f98f065e2d59e19b"},
#         "title": "Asaduddin Owaisi, Kiren Rijiju engage in war of words on social media over minorities rights",
#         "politicianName": "Kiren Rijiju",
#         "url": "https://m.economictimes.com/news/politics-and-nation/asaduddin-owaisi-kiren-rijiju-engage-in-war-of-words-on-social-media-over-minorities-rights/articleshow/122301618.cms",
#         "description": "Asaduddin Owaisi and Kiren Rijiju had a social media exchange. Owaisi criticized Rijiju's statement on minority benefits.    5 days ago",
#         "text": "(Catch all the Business News, Breaking News, Budget 2025 Events and Latest News Updates on The Economic Times.)\nSubscribe to The Economic Times Prime and read the ET ePaper online.\n(Catch all the Business News, Breaking News, Budget 2025 Events and Latest News Updates on The Economic Times.)\nSubscribe to The Economic Times Prime and read the ET ePaper online.\nWhy this one from ‘Dirty Dozen’, now in Vedanta fold, is again in a mess\nThe deluge that’s cooling oil prices despite the Iran conflict\nCan Indian IT protect its high valuation as AI takes centre stage?\nEngine fuel switches or something else? One month on, still no word on what crashed AI 171\nAs GenAI puts traditional BPO on life support, survival demands a makeover\nStock Radar: ITC Hotels hits fresh record high in July – time to buy or book profits?",
#         "img": "https://img.etimg.com/thumb/msid-122301636,width-1200,height-630,imgsize-15740,overlay-economictimes/articleshow.jpg",
#         "scrapedAt": {"$date": {"$numberLong": "1752354800460"}},
#         "createdAt": {"$date": {"$numberLong": "1752354800461"}},
#         "updatedAt": {"$date": {"$numberLong": "1752354800461"}},
#         "__v": {"$numberInt": "0"}
#     }
#     save_vectorized_article(article)
#     return {"message": "success"}

# def vectorizeArticle(text: str):
#     response = requests.post("http://ml:8001/vectorize", json={"text": text})
#     return response.json()["embedding"]
