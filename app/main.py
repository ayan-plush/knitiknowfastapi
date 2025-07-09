from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from curl_cffi import requests
from rich import print
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend origin(s)
    allow_credentials=True,
    allow_methods=["*"],  # or ["GET", "POST", ...]
    allow_headers=["*"],
)


my_posts = [{"title": "title of post 1","content": "content of post 1","id": 1},{"title": "opps list","content": "1 pheobe bridgers","id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            print('reached')
            return p
        
def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # optional field
    rating: Optional[int] = None
    
class ItemList(BaseModel):
    ministers: list[str]

@app.get("/")
def root():
    return {"message": "Hell00o"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    thepost = find_post(id)
    if not thepost:
        # response.status_code = 404 still works
        ##response.status_code = status.HTTP_404_NOT_FOUND
        ##return {"message": f"post with id:{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    # always convert to int 
    return {"data": thepost}

@app.get("/posts/latest")
def get_latest_post():
    thepost = my_posts[len(my_posts)-1]
    # always convert to int 
    return {"data": thepost}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if not index:
        # response.status_code = 404 still works
        ##response.status_code = status.HTTP_404_NOT_FOUND
        ##return {"message": f"post with id:{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    my_posts.pop(index)    
    # always convert to int 
    return Response(status_code = status.HTTP_204_NO_CONTENT)



@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    #new post is stored as a pydantic model so you can convert it 
    post_dict = new_post.model_dump()
    size = len(my_posts)
    post_dict['id'] = size+1
    my_posts.append(post_dict)
    return {"new_posts": my_posts}
# title str, content str
@app.post("/scrape", status_code=status.HTTP_201_CREATED)
def scrape_news(data: ItemList):
    cookies = {
        '_grx': '127dbe24-5fce-4f9d-8f96-275c78809a45',
        'deviceid': 'bxh0ebf7inb73ikfluyolhnhf',
        '__eoi': 'ID=3a8a18f55c011394:T=1741165632:RT=1741165632:S=AA-AfjZuyV0pu0a2ZE5nVUwtEdaR',
        '_scor_uid': 'ad3ed1eb8cb04057ac331060a7362a80',
        '_gcl_au': '1.1.2078873441.1747843597',
        '_ga': 'GA1.1.879350451.1747843597',
        '_ga_9T90YDGX9D': 'GS2.2.s1747843598$o1$g0$t1747843598$j0$l0$h0',
        '_uetvid': '892ad7501b9d11f08f356d3b64efd163',
        '_cc_id': '26ef26fc536ecb3bdebd760ac7ba0b97',
        'FCNEC': '%5B%5B%22AKsRol8SmNyy-ko_3yTlJOwCnAE5WbJtHfv0WAwJoZ0iBcLvtUOg-3TjYutMdnAZs0B8eoksgawdJsKVheNPC4qzYxbWWjT05i3SWTp5Qz24cYTH0rvGhKC8PWk90jfB41EMEXw9WcDMFeJFkdfAdfEZ1lpG54kGhw%3D%3D%22%5D%5D',
        '_clck': '1mmlkm5%7C2%7Cfw3%7C0%7C1967',
        'cto_bundle': 'sy_bFl94bkVwTWo2dzlZcE41ZjJ0JTJGeWRPVDc1TFNSUHRuZDZIbmhrWlZnSzRtRW04ZXphN01qNkdicTFHNW5LQ0dJTDBGSTRZWCUyQkFsazdqaEd6RjlSUmZVYVlpdGNIdGpiSGR3cmRUZHBPb2YlMkZBY1p5Y01GVXViRWN4dWM1RHJTU0N5YQ',
        '_ga_WZ3Z4GGVRC': 'GS2.1.s1747843598$o1$g0$t1747843606$j52$l0$h0$ddnPOXqG6dqm5cHUKVZKy0_ozLLB29-RjNQ',
        'geo_continent': 'AS',
        'geo_country': 'IN',
        'geolocation': 'Faridabad',
        'grxgeostate': 'Haryana',
        'geostate': 'DL',
        'geo_region': 'HR',
        'ak_bmsc': 'C482BD304A5062143B7573088EECA03A~000000000000000000000000000000~YAAQzbYRYH2vNFmXAQAARSKmjRwqTx/iPApZyIAcwXiF63QrAJeibarQKTWoevUYnRYSIkJyeqpQvc2r5xNDTLc4vubz3BmJlsJr+PZvUodP87D+uBlOpzkSNdrYlTI13AFwZ8nUoilUwDJPVUjIrEkYQRR+KvC1YXUuGWwXTFFQeuc2k0Cc4yU9bCrGoT4L3yTFA7XrboCtt/AJXReaesFNyjySuq2oS7XykSAN848RK2jTMzlK9U8XIR9K8Ddgo6o/EhHbsE+/NZ6QYUTxhATIgj7dBe9+b6XUXFG6YpiW8c68kegm3IVoSPCuJ0VMUUe+C3WvLl+FEqFJc7+o9qkOY5Spbb76RVmdffjRdnJB3tMzRJGFBtZYPdkIuixs3H8idD4q',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"4d5e2-kbGXbidvlGb4Md+bYyZSMhiNQY4"',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # 'cookie': '_grx=127dbe24-5fce-4f9d-8f96-275c78809a45; deviceid=bxh0ebf7inb73ikfluyolhnhf; __eoi=ID=3a8a18f55c011394:T=1741165632:RT=1741165632:S=AA-AfjZuyV0pu0a2ZE5nVUwtEdaR; _scor_uid=ad3ed1eb8cb04057ac331060a7362a80; _gcl_au=1.1.2078873441.1747843597; _ga=GA1.1.879350451.1747843597; _ga_9T90YDGX9D=GS2.2.s1747843598$o1$g0$t1747843598$j0$l0$h0; _uetvid=892ad7501b9d11f08f356d3b64efd163; _cc_id=26ef26fc536ecb3bdebd760ac7ba0b97; FCNEC=%5B%5B%22AKsRol8SmNyy-ko_3yTlJOwCnAE5WbJtHfv0WAwJoZ0iBcLvtUOg-3TjYutMdnAZs0B8eoksgawdJsKVheNPC4qzYxbWWjT05i3SWTp5Qz24cYTH0rvGhKC8PWk90jfB41EMEXw9WcDMFeJFkdfAdfEZ1lpG54kGhw%3D%3D%22%5D%5D; _clck=1mmlkm5%7C2%7Cfw3%7C0%7C1967; cto_bundle=sy_bFl94bkVwTWo2dzlZcE41ZjJ0JTJGeWRPVDc1TFNSUHRuZDZIbmhrWlZnSzRtRW04ZXphN01qNkdicTFHNW5LQ0dJTDBGSTRZWCUyQkFsazdqaEd6RjlSUmZVYVlpdGNIdGpiSGR3cmRUZHBPb2YlMkZBY1p5Y01GVXViRWN4dWM1RHJTU0N5YQ; _ga_WZ3Z4GGVRC=GS2.1.s1747843598$o1$g0$t1747843606$j52$l0$h0$ddnPOXqG6dqm5cHUKVZKy0_ozLLB29-RjNQ; geo_continent=AS; geo_country=IN; geolocation=Faridabad; grxgeostate=Haryana; geostate=DL; geo_region=HR; ak_bmsc=C482BD304A5062143B7573088EECA03A~000000000000000000000000000000~YAAQzbYRYH2vNFmXAQAARSKmjRwqTx/iPApZyIAcwXiF63QrAJeibarQKTWoevUYnRYSIkJyeqpQvc2r5xNDTLc4vubz3BmJlsJr+PZvUodP87D+uBlOpzkSNdrYlTI13AFwZ8nUoilUwDJPVUjIrEkYQRR+KvC1YXUuGWwXTFFQeuc2k0Cc4yU9bCrGoT4L3yTFA7XrboCtt/AJXReaesFNyjySuq2oS7XykSAN848RK2jTMzlK9U8XIR9K8Ddgo6o/EhHbsE+/NZ6QYUTxhATIgj7dBe9+b6XUXFG6YpiW8c68kegm3IVoSPCuJ0VMUUe+C3WvLl+FEqFJc7+o9qkOY5Spbb76RVmdffjRdnJB3tMzRJGFBtZYPdkIuixs3H8idD4q',
    }

    ministers = [
        "bhupathiraju-srinivasa-varma",
        "rao-inderjit-singh",
        "nirmala-sitharaman"
    ]
    
    result = []

    for minister in data.ministers:
        response = requests.get('https://timesofindia.indiatimes.com/topic/'+ minister, cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        for div in soup.select("div.uwU81"):
            
            link = div.select_one("a")
            img = div.select_one("div.cOu80 img")
            # print(div.select_one("div.cOu80 img"))
            title = div.select_one("div.fHv_i.o58kM span")

            resultantText = {
                "minister": minister,
                "articlelink": link["href"] if link else None,
                "img": img["src"] if img else None,
                "title": title.get_text(strip=True) if title else None
            }
            
            result.append(resultantText)
            
            
            
    return {"scraped": result}
            
            
