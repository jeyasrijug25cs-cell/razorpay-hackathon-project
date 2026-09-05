from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# -----------------------------
# PRODUCT CATALOGUE
# -----------------------------

PRODUCTS = [

    # HEADPHONES
    {
        "name": "TunePro Lite Headphones",
        "category": "headphones",
        "price": 2499,
        "rating": 4.2,
        "store": "RazorAI Store"
    },
    {
        "name": "SoundMax Pro Wireless Headphones",
        "category": "headphones",
        "price": 3499,
        "rating": 4.4,
        "store": "RazorAI Store"
    },
    {
        "name": "AudioBeat X Bluetooth Headphones",
        "category": "headphones",
        "price": 4299,
        "rating": 4.5,
        "store": "RazorAI Store"
    },
    {
        "name": "BassFlow 500 Wireless Headphones",
        "category": "headphones",
        "price": 4799,
        "rating": 4.3,
        "store": "RazorAI Store"
    },

    # LAPTOPS
    {
        "name": "TechBook Air Laptop",
        "category": "laptop",
        "price": 45999,
        "rating": 4.4,
        "store": "RazorAI Store"
    },
    {
        "name": "CodeMaster 15 Laptop",
        "category": "laptop",
        "price": 49999,
        "rating": 4.6,
        "store": "RazorAI Store"
    },

    # SMARTPHONES
    {
        "name": "MobileMax 5G Smartphone",
        "category": "smartphone",
        "price": 15999,
        "rating": 4.3,
        "store": "RazorAI Store"
    },
    {
        "name": "SmartX Pro Smartphone",
        "category": "smartphone",
        "price": 18999,
        "rating": 4.5,
        "store": "RazorAI Store"
    },

    # SMARTWATCH
    {
        "name": "FitWatch Pro Smartwatch",
        "category": "watch",
        "price": 3999,
        "rating": 4.4,
        "store": "RazorAI Store"
    },

    # SHOES
    {
        "name": "RunFast Sports Shoes",
        "category": "shoes",
        "price": 2999,
        "rating": 4.5,
        "store": "RazorAI Store"
    }
]


# -----------------------------
# USER CONVERSATION MEMORY
# -----------------------------

user_context = {
    "product": None,
    "budget": None,
    "results": []
}


# -----------------------------
# HOME PAGE
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# CHAT
# -----------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "").strip()

    text = message.lower()


    # -------------------------
    # PRODUCT DETECTION
    # -------------------------

    if "headphone" in text or "earphone" in text:

        user_context["product"] = "headphones"

        return jsonify({
            "reply": "🎧 Great! You're looking for headphones. What is your budget?",
            "products": []
        })


    elif "laptop" in text:

        user_context["product"] = "laptop"

        return jsonify({
            "reply": "💻 Great! You're looking for a laptop. What is your budget?",
            "products": []
        })


    elif (
        "smartphone" in text
        or "phone" in text
        or "mobile" in text
    ):

        user_context["product"] = "smartphone"

        return jsonify({
            "reply": "📱 Great! You're looking for a smartphone. What is your budget?",
            "products": []
        })


    elif "watch" in text:

        user_context["product"] = "watch"

        return jsonify({
            "reply": "⌚ Great! You're looking for a smartwatch. What is your budget?",
            "products": []
        })


    elif "shoe" in text:

        user_context["product"] = "shoes"

        return jsonify({
            "reply": "👟 Great! You're looking for shoes. What is your budget?",
            "products": []
        })


    # -------------------------
    # CHEAPEST PRODUCT
    # -------------------------

    elif "cheapest" in text or "lowest price" in text:

        products = user_context["results"]

        if products:

            cheapest = min(
                products,
                key=lambda product: product["price"]
            )

            return jsonify({
                "reply": (
                    f"💰 The cheapest option is "
                    f"{cheapest['name']} at "
                    f"₹{cheapest['price']:,}."
                ),
                "products": products
            })

        return jsonify({
            "reply": "Please tell me the product and budget first.",
            "products": []
        })


    # -------------------------
    # BEST RATED PRODUCT
    # -------------------------

    elif (
        "best rating" in text
        or "highest rating" in text
        or "best rated" in text
    ):

        products = user_context["results"]

        if products:

            best = max(
                products,
                key=lambda product: product["rating"]
            )

            return jsonify({
                "reply": (
                    f"⭐ The highest-rated option is "
                    f"{best['name']} with a "
                    f"{best['rating']}⭐ rating."
                ),
                "products": products
            })

        return jsonify({
            "reply": "Please search for a product first.",
            "products": []
        })


    # -------------------------
    # BUDGET DETECTION
    # -------------------------

    numbers = []

    current_number = ""

    for char in text:

        if char.isdigit():

            current_number += char

        else:

            if current_number:

                numbers.append(
                    int(current_number)
                )

                current_number = ""


    if current_number:

        numbers.append(
            int(current_number)
        )


    if numbers:

        budget = numbers[0]

        user_context["budget"] = budget

        category = user_context["product"]


        if category:

            matching_products = [

                product

                for product in PRODUCTS

                if product["category"] == category

                and product["price"] <= budget

            ]


            matching_products.sort(
                key=lambda product: product["rating"],
                reverse=True
            )


            user_context["results"] = matching_products


            if matching_products:

                best = matching_products[0]

                return jsonify({
                    "reply": (
                        f"🎯 I found "
                        f"{len(matching_products)} "
                        f"{category} options under "
                        f"₹{budget:,}.\n\n"
                        f"My recommendation is "
                        f"{best['name']} because it has "
                        f"a {best['rating']}⭐ rating."
                    ),
                    "products": matching_products
                })


            return jsonify({
                "reply": (
                    f"😕 I couldn't find "
                    f"{category} under ₹{budget:,}. "
                    f"Try increasing your budget."
                ),
                "products": []
            })


        return jsonify({
            "reply": (
                f"💰 Your budget is ₹{budget:,}. "
                f"What product would you like to buy?"
            ),
            "products": []
        })


    # -------------------------
    # BUY / PURCHASE
    # -------------------------

    if (
        "buy" in text
        or "purchase" in text
        or "checkout" in text
    ):

        return jsonify({
            "reply": (
                "🛒 Great! Please choose a product "
                "from the options above and click Buy Now."
            ),
            "products": user_context["results"]
        })


    # -------------------------
    # DEFAULT RESPONSE
    # -------------------------

    return jsonify({
        "reply": (
            "🤖 I'm RazorAI, your AI shopping assistant. "
            "Tell me what you want to buy, "
            "for example: 'I need headphones'."
        ),
        "products": []
    })


# -----------------------------
# START APPLICATION
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)