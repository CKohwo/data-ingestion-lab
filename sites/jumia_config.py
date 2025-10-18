
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64), AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}

# Define the laptop selectors inorder to prevent hardcoding and follow the DRY principle
# Added selector for pagination  
selector = {
     "id": "article.prd._fb.col.c-prd",
     "name": "h3.name",
     "price": "div.prc",
     "ratings": "div.stars._s",  
     "page_next":"a.pg[aria-label='Next Page']"    
}  
