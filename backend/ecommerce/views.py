from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .serializers import ProductSerializer
import json
import re

# Simulated chatbot responses
CHATBOT_RESPONSES = {
    "hello": "Hi! How can I assist you today?",
    "hi": "Hi! How can I assist you today?",
    "products": "You can search for products by categories like Electronics, Books, Clothing, Furniture, and Appliances.",
    "discount": "We have great discounts available on various items. Please use the product filter to find them.",
    "help": "You can search for products by categories like Electronics, Books, Clothing, Furniture, and Appliances. You can also decide minimum/maximum price and also minimum rating for your product.",
}

@csrf_exempt
def chat(request):
    """
    Handle chatbot interactions.
    Responds to user queries with predefined or dynamic responses, including product filtering.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').lower()

            # Attempt to extract filtering criteria from the query
            filters = extract_filters_from_query(query)
            if filters:
                # Perform product filtering using the extracted criteria
                products = Product.objects.all()
                if filters.get("category"):
                    products = products.filter(category__icontains=filters["category"])
                if filters.get("min_price"):
                    products = products.filter(price__gte=filters["min_price"])
                if filters.get("max_price"):
                    products = products.filter(price__lte=filters["max_price"])
                if filters.get("min_rating"):
                    products = products.filter(rating__gte=filters["min_rating"])

                # Serialize and return the filtered products
                serialized_products = ProductSerializer(products, many=True)
                return JsonResponse(
                    {
                        "reply": f"Here are the filtered products based on your query: {query}",
                        "products": serialized_products.data,
                    },
                    status=200,
                )

            # Default to predefined responses if no filters are found
            response = CHATBOT_RESPONSES.get(query, "I'm sorry, I didn't understand that. Can you please rephrase?")
            return JsonResponse({'reply': response}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    elif request.method == 'GET':
        # Add a simple GET response for testing
        return JsonResponse({'message': 'Chatbot API is running. Use POST to interact.'}, status=200)
    return JsonResponse({'error': 'Invalid request method. Use POST or GET for testing.'}, status=405)


@csrf_exempt
def filter_products(request):
    """
    Handle product filtering based on criteria sent in the request body.
    Filters by category, price range, and minimum rating.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            filters = data.get('filters', {})

            # Extract filter criteria
            category = filters.get('category')
            min_price = filters.get('min_price')
            max_price = filters.get('max_price')
            min_rating = filters.get('min_rating')

            # Build the query dynamically
            products = Product.objects.all()
            if category:
                products = products.filter(category__icontains=category)
            if min_price:
                products = products.filter(price__gte=min_price)
            if max_price:
                products = products.filter(price__lte=max_price)
            if min_rating:
                products = products.filter(rating__gte=min_rating)

            # Serialize and return the products
            serialized_products = ProductSerializer(products, many=True)
            return JsonResponse(serialized_products.data, safe=False, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    elif request.method == 'GET':
        # Add a simple GET response for testing
        return JsonResponse({'message': 'Filter Products API is running. Use POST to filter products.'}, status=200)
    return JsonResponse({'error': 'Invalid request method. Use POST or GET for testing.'}, status=405)


def extract_filters_from_query(query):
    """
    Extract filtering criteria (category, min/max price, rating) from the user's query.
    """
    filters = {}
    
    # Extract category
    categories = ["electronics", "books", "clothing", "furniture", "appliances"]
    for category in categories:
        if category in query:
            filters["category"] = category
            break

    # Extract price range
    price_match = re.search(r"\bbelow\s*\$?(\d+)", query)
    if price_match:
        filters["max_price"] = int(price_match.group(1))
    min_price_match = re.search(r"\babove\s*\$?(\d+)", query)
    if min_price_match:
        filters["min_price"] = int(min_price_match.group(1))

    # Extract minimum rating
    rating_match = re.search(r"\brating\s*above\s*(\d+)", query)
    if rating_match:
        filters["min_rating"] = int(rating_match.group(1))

    return filters
