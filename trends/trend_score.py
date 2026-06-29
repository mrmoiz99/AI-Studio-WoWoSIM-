TRAVEL_WORDS = ['travel','flight','airport','visa','tourism','hotel','world cup','fifa','holiday','vacation','summer','winter','europe','usa','canada','mexico','japan','thailand','dubai','saudi','maps','roaming']
RISK_WORDS = ['death','shooting','war','attack','murder','crime','earthquake','flood']

def simple_score(title):
    t = title.lower()
    score = 40
    for w in TRAVEL_WORDS:
        if w in t:
            score += 10
    for w in RISK_WORDS:
        if w in t:
            score -= 30
    return max(0, min(100, score))
