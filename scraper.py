from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def get_html(url):
	# Urlencode the URL
	url = urllib.parse.quote_plus(url)

	# Create the query URL.
	query = "https://api.scraperbox.com/scrape"
	query += "?token=%s" % "90006A2828922EEE99826CE21A338F45"
	query += "&url=%s" % url
	query += "&javascript_enabled=true"

	# Call the API.
	request = urllib.request.Request(query)
	raw_response = urllib.request.urlopen(request).read()
	html = raw_response.decode("utf-8")
	return html

# Get the amazon search page.
search_page_html = get_html("amazon.com/s?k=phone")
soup = BeautifulSoup(search_page_html, 'html.parser')

# Find all the search result links.
links = soup.select(".s-result-list div.sg-col-inner h2 > a.a-link-normal")

for link in links:
	# Get hte product detail page.
	product_page_html = get_html("https://amazon.com" + link['href'])
	soup = BeautifulSoup(product_page_html, 'html.parser')
	
	# Find the title and price elements.
	title_element = soup.select_one("#title")
	price_element = soup.select_one("#price_inside_buybox")

	# Get the text contents
	title = title_element.getText().strip()
	if price_element:
		price = price_element.getText().strip()
	else:
		price = "NA"

	print("Title=" + title)
	print("Price=" + price)
	print()
