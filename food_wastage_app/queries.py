# queries.py

queries = {
    1: {
        "question": "How many food providers are there in each city?",
        "query": """
            SELECT city, COUNT(provider_id) AS total_providers
            FROM providers_data
            GROUP BY city
            ORDER BY total_providers DESC;
        """
    },

    2: {
        "question": "How many food receivers are there in each city?",
        "query": """
            SELECT city, COUNT(receiver_id) AS total_receivers
            FROM receivers_data
            GROUP BY city
            ORDER BY total_receivers DESC;
        """
    },

    3: {
        "question": "Which type of food provider contributes the most food?",
        "query": """
            SELECT provider_type, SUM(quantity) AS total_food_quantity
            FROM food_listings_data
            GROUP BY provider_type
            ORDER BY total_food_quantity DESC
            LIMIT 1;
        """
    },

        4: {
        "question": "What is the contact information of food providers in a specific city?",
        "query": """
            SELECT Name, Contact, Type
            FROM providers_data
            WHERE LOWER(City) = LOWER(%s);
        """
    },

    5: {
        "question": "Which receivers have claimed the most food?",
        "query": """
            SELECT r.name AS receiver_name, COUNT(c.claim_id) AS total_claims
            FROM claims_data c
            JOIN receivers_data r ON c.receiver_id = r.receiver_id
            GROUP BY r.name
            ORDER BY total_claims DESC
            LIMIT 10;
        """
    },

    6: {
        "question": "What is the total quantity of food available from all providers?",
        "query": """
            SELECT SUM(quantity) AS total_food_available 
            FROM food_listings_data;
        """
    },

    7: {
        "question": "Which city has the highest number of food listings?",
        "query": """
            SELECT location AS city, COUNT(food_id) AS total_listings
            FROM food_listings_data
            GROUP BY location
            ORDER BY total_listings DESC
            LIMIT 1;
        """
    },

    8: {
        "question": "What are the most commonly available food types?",
        "query": """
            SELECT food_type, COUNT(food_id) AS total
            FROM food_listings_data
            GROUP BY food_type
            ORDER BY total DESC
            LIMIT 10;
        """
    },

    9: {
        "question": "Which providers have provided the largest total food quantity?",
        "query": """
            SELECT p.name AS provider_name, SUM(f.quantity) AS total_food
            FROM food_listings_data f
            JOIN providers_data p ON f.provider_id = p.provider_id
            GROUP BY p.name
            ORDER BY total_food DESC
            LIMIT 10;
        """
    },

    10: {
        "question": "What is the monthly trend of food claims?",
        "query": """
            SELECT DATE_TRUNC('month', "timestamp"::timestamp) AS month, 
            COUNT(claim_id) AS total_claims
            FROM claims_data
            GROUP BY month
            ORDER BY month;
        """
    },

    11: {
        "question": "What percentage of food listings are successfully claimed?",
        "query": """
            SELECT 
                (COUNT(DISTINCT c.food_id)::DECIMAL / COUNT(DISTINCT f.food_id) * 100) AS claim_percentage
            FROM food_listings_data f
            LEFT JOIN claims_data c ON f.food_id = c.food_id;
        """
    },

    12: {
        "question": "Which city has the highest food wastage (unclaimed food)?",
        "query": """
            SELECT f.location AS city, COUNT(f.food_id) - COUNT(c.food_id) AS unclaimed_food
            FROM food_listings_data f
            LEFT JOIN claims_data c ON f.food_id = c.food_id
            GROUP BY f.location
            ORDER BY unclaimed_food DESC
            LIMIT 1;
        """
    },

    13: {
        "question": "What is the average quantity of food provided per provider?",
        "query": """
            SELECT p.name, AVG(f.quantity) AS avg_quantity
            FROM food_listings_data f
            JOIN providers_data p ON f.provider_id = p.provider_id
            GROUP BY p.name
            ORDER BY avg_quantity DESC
            LIMIT 10;
        """
    },

    14: {
        "question": "Which food type has the highest wastage?",
        "query": """
            SELECT f.food_type, COUNT(f.food_id) - COUNT(c.food_id) AS unclaimed
            FROM food_listings_data f
            LEFT JOIN claims_data c ON f.food_id = c.food_id
            GROUP BY f.food_type
            ORDER BY unclaimed DESC
            LIMIT 1;
        """
    },

    15: {
        "question": "Which receiver organizations claim the widest variety of food?",
        "query": """
            SELECT r.name, COUNT(DISTINCT f.food_type) AS variety
            FROM claims_data c
            JOIN receivers_data r ON c.receiver_id = r.receiver_id
            JOIN food_listings_data f ON c.food_id = f.food_id
            GROUP BY r.name
            ORDER BY variety DESC
            LIMIT 10;
        """
    },

    16: {
        "question": "What is the distribution of food listings by provider type?",
        "query": """
            SELECT provider_type, COUNT(food_id) AS total
            FROM food_listings_data
            GROUP BY provider_type
            ORDER BY total DESC;
        """
    },

    17: {
        "question": "Which providers have the highest average claim success rate?",
        "query": """
            SELECT p.name,
                   (COUNT(c.claim_id)::DECIMAL / COUNT(f.food_id) * 100) AS success_rate
            FROM providers_data p
            JOIN food_listings_data f ON p.provider_id = f.provider_id
            LEFT JOIN claims_data c ON f.food_id = c.food_id
            GROUP BY p.name
            HAVING COUNT(f.food_id) > 5
            ORDER BY success_rate DESC
            LIMIT 10;
        """
    },

    18: {
        "question": "What is the trend of total food quantity listed over time?",
        "query": """
            SELECT DATE_TRUNC('month', listing_date) AS month, SUM(quantity) AS total_quantity
            FROM food_listings_data
            GROUP BY month
            ORDER BY month;
        """
    },

    19: {
        "question": "Which cities have the most active receivers?",
        "query": """
            SELECT r.city, COUNT(DISTINCT c.receiver_id) AS active_receivers
            FROM claims_data c
            JOIN receivers_data r ON c.receiver_id = r.receiver_id
            GROUP BY r.city
            ORDER BY active_receivers DESC
            LIMIT 10;
        """
    },

    20: {
        "question": "What is the ratio of perishable to non-perishable food listed?",
        "query": """
            SELECT food_type,
                   COUNT(food_id) AS total
            FROM food_listings_data
            WHERE food_type IN ('Perishable', 'Non-Perishable')
            GROUP BY food_type;
        """
    },

    21: {
        "question": "Which providers are the most consistent in listing food each month?",
        "query": """
            SELECT 
                p.name, 
                COUNT(DISTINCT DATE_TRUNC('month', COALESCE(f.expiry_date::date, CURRENT_DATE))) AS active_months
            FROM providers_data p
            JOIN food_listings_data f 
                ON p.provider_id = f.provider_id
            GROUP BY p.name
            ORDER BY active_months DESC
            LIMIT 10;
        """
    },

    22: {
        "question": "Which day of the week sees the highest food claims?",
        "query": """
            SELECT 
                TO_CHAR(timestamp::timestamp, 'Day') AS day, 
                COUNT(claim_id) AS total_claims
            FROM claims_data
            GROUP BY day
            ORDER BY total_claims DESC
            LIMIT 1;
        """
    },

    23: {
        "question": "Which receivers have the highest claim-to-listing ratio?",
        "query": """
            SELECT r.name,
                   (COUNT(c.claim_id)::DECIMAL / COUNT(DISTINCT f.food_id)) AS claim_ratio
            FROM receivers_data r
            JOIN claims_data c ON r.receiver_id = c.receiver_id
            JOIN food_listings_data f ON c.food_id = f.food_id
            GROUP BY r.name
            ORDER BY claim_ratio DESC
            LIMIT 10;
        """
    },

    24: {
        "question": "What is the overall wastage percentage (unclaimed vs listed)?",
        "query": """
            SELECT 
                ((COUNT(f.food_id) - COUNT(c.claim_id))::DECIMAL / COUNT(f.food_id) * 100) AS wastage_percentage
            FROM food_listings_data f
            LEFT JOIN claims_data c ON f.food_id = c.food_id;
        """
    },

    25: {
        "question": "Which receivers are the fastest to claim food after listing?",
        "query": """
            SELECT 
                r.name,
                AVG(EXTRACT(EPOCH FROM (c.timestamp::timestamp - f.timestamp::timestamp)) / 3600) AS avg_hours_to_claim
            FROM claims_data c
            JOIN food_listings_data f 
                ON c.food_id = f.food_id
            JOIN receivers_data r 
                ON c.receiver_id = r.receiver_id
            GROUP BY r.name
            ORDER BY avg_hours_to_claim ASC
            LIMIT 10;
        """
    }
}
