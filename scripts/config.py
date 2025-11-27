
headers = {
  'Content-Type': 'application/json',
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64), AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
  'Origin': 'https://www.konga.com',
  'Referer': 'https://www.konga.com/'
  }

# Define the laptop selectors inorder to prevent hardcoding and follow the DRY principle
# Added selector for pagination  
selector = {
     "id": "article.prd._fb.col.c-prd",
     "name": "h3.name",
     "price": "div.prc",
     "ratings": "div.stars._s",  
     "page_next":"a.pg[aria-label='Next Page']"    
}  


# GraphQL query payload, used for the API ingestion engine   
payload = {
  "query": """
    {
      searchByStore(
        search_term: [["category.category_id:5237"]],
        numericFilters: [],
        sortBy: "",
        paginate: {page: 0, limit: 40},
        store_id: 1
      ) {
        pagination {
          limit
          page
          total
        }
        products {
          name
          brand
          price
          deal_price
          final_price
          description
          image_thumbnail
          sku
          seller {
            name
          }
          stock {
            in_stock
            quantity
          }
          product_rating {
            quality {
              average
              number_of_ratings
            }
          }
        }
      }
    }
  """
}
  