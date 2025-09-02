ALLOWED_NICHES = [
    "ecommerce", "digital products", "legal tech", "trading", "coaching", "AI tools"
]

BANNED_NICHES = [
    "illegal drugs", "weapons", "adult content", "fake documents", "deepfakes", "hacking tools"
]

MAX_SPEND_PER_BUSINESS = 500
MIN_ROI_THRESHOLD = 1.5

def is_legal_niche(niche):
    return niche.lower() not in BANNED_NICHES

def requires_manual_review(niche, budget_estimate):
    return (
        not is_legal_niche(niche) or
        budget_estimate > MAX_SPEND_PER_BUSINESS
    )

def should_scale(profit, spend):
    roi = profit / max(spend, 1)
    return roi >= MIN_ROI_THRESHOLD