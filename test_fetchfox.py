from fetchfox_sdk import FetchFox
fox = FetchFox(api_key="")

items = fox.extract(
    "https://dantri.com.vn/phap-luat/bo-cong-an-ly-giai-ve-de-xuat-bo-co-quan-dieu-tra-vksnd-toi-cao-20250419134102132.htm",
    {
        'title': 'What is the article title?', 
        'description': 'What is the meta description?', 
        'content': 'What is the full article content?'
    })

# Stream results as they become available
for item in items.limit(10):
    print(item)

# The resulting items look like this:
# {
#   'name': 'Bulbasaur',
#   'url': 'https://pokemondb.net/pokedex/bulbasaur',
# }
