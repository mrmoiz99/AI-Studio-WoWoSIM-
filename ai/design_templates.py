TEMPLATES = {
    "Travel Tip": {
        "kicker": "TRAVEL TIP",
        "cta": "Explore plans at WoWoSIM",
        "subtitle": "Maps, rides, uploads, and updates without roaming stress.",
    },
    "Destination Highlight": {
        "kicker": "DESTINATION READY",
        "cta": "Get your eSIM before you fly",
        "subtitle": "Instant travel data for your next international trip.",
    },
    "Breaking Trend": {
        "kicker": "TRENDING NOW",
        "cta": "Stay connected with WoWoSIM",
        "subtitle": "Follow the moment, share the story, and stay online abroad.",
    },
    "FIFA / Event Travel": {
        "kicker": "EVENT TRAVEL",
        "cta": "Travel connected with WoWoSIM",
        "subtitle": "Share every live moment with fast travel data abroad.",
    },
    "Discount Offer": {
        "kicker": "LIMITED OFFER",
        "cta": "View eSIM deals",
        "subtitle": "Affordable travel data plans for your next trip.",
    },
}


def get_template(name: str):
    return TEMPLATES.get(name, TEMPLATES["Travel Tip"])
