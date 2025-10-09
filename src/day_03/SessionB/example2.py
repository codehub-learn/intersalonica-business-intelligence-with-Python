"""
Create hierarchies in dimension tables:
- Product Category → Product Subcategory → Product Name
- Date → Month → Quarter → Year 
- Customer Region → Customer Country → Customer City    

"""

# Product hierarchy: Category → Subcategory → Product
product_hierarchy = {
    "Electronics": {
        "Mobile Phones": ["iPhone 15", "Samsung Galaxy S24"],
        "Laptops": ["MacBook Pro", "Dell XPS"]
    },
    "Clothing": {
        "Men Shirts": ["Formal Shirt", "Casual Shirt"],
        "Women Dresses": ["Summer Dress", "Evening Gown"]
    }
}

# Print full hierarchy
print("=== Product Hierarchy ===")
for category, subcats in product_hierarchy.items():
    print(f"Category: {category}")
    for subcat, products in subcats.items():
        print(f"  Subcategory: {subcat}")
        for product in products:
            print(f"    Product: {product}")


#Let’s query all products under "Electronics":

electronics_products = []
for subcat, products in product_hierarchy["Electronics"].items():
    electronics_products.extend(products)

print("Products under Electronics:", electronics_products)