import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

# Adding jumia.com.eg to the base_url.
base_url = "https://www.jumia.com.eg/catalog/?"

# Getting the product name and the number of pages from the user.
search_word = input("Enter the product name: ")
pages = int(input("Enter the number of pages: "))
print_output = input("Do you want to print products details to console? (yes/no): ")


# data lists

product_names = []
prices = []
old_prices = []
discounts = []
ratings = []

try:
    # Looping through the pages.
    for page in range(1, pages + 1):
        
        
        # Sending a request to the website with user's parameters.
        req = requests.get(base_url, params={"q": search_word, "page": page})
        soup = BeautifulSoup(req.content, "html.parser")

        # Getting the parent element of the products.
        products = soup.find_all("article", {"class": "prd _fb col c-prd"})

        # Looping through products.
        for product in products:
            # Getting reuqired data: name, price, old price, discount, and rating.
            name = product.find("h3", {"class": "name"})
            price = product.find("div", {"class": "prc"})
            old_price = product.find("div", {"class": "old"})
            discount = product.find("div", {"class": "bdg _dsct _sm"})
            rating = product.find("div", {"class": "stars _s"})

            # Printing the data to console.
            if print_output.lower() == "yes":
                print(f"Product Name: {name.text if name else 'N/A'}")
                print(f"Price: {price.text if price else 'N/A'}")
                print(f"Old Price: {old_price.text if old_price else price.text}")
                print(f"Discount: {discount.text if discount else '0%'}")
                print(f"Rating: {rating.text if rating else 'N/A'}")
                print("=====================================")

            # Appending the data to the lists.
            product_names.append(name.text if name else "N/A")
            prices.append(price.text if price else "N/A")
            old_prices.append(old_price.text if old_price else price.text)
            discounts.append(discount.text if discount else "0%")
            ratings.append(rating.text if rating else "N/A")

    file_list = [product_names, prices, old_prices, discounts, ratings]
    exported = zip_longest(*file_list)

    with open("data.csv", "w", newline='', encoding='utf-8') as my_file:
        wr = csv.writer(my_file)
        wr.writerow(["Product_Name", "Price", "Old_Price", "Discount", "Rating"])
        wr.writerows(exported)
    
    print("Data has been exported successfully.")


except: 
    print("An error has occurred.")

