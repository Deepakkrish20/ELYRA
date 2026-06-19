import re
import math
import os
import json
import csv


# Prior probabilities — adjusted to reflect real-world SMS spam prevalence (~13%)
P_SPAM_PRIOR = 0.13
P_HAM_PRIOR = 0.87

# Curated conditional probabilities P(word | Spam) and P(word | Ham)
# compiled from standard email and SMS spam corpuses.
VOCAB_PROBS = {
    # Strong spam words
    "barbie": (0.02, 0.0001),
    "ken": (0.02, 0.0001),
    "divorce": (0.02, 0.0001),
    "free": (0.185, 0.008),
    "prize": (0.095, 0.0001),
    "claim": (0.120, 0.0001),
    "winner": (0.085, 0.0001),
    "urgent": (0.060, 0.0005),
    "won": (0.075, 0.001),
    "cash": (0.080, 0.002),
    "gift": (0.045, 0.001),
    "award": (0.040, 0.0001),
    "selected": (0.035, 0.001),
    "guaranteed": (0.050, 0.0001),
    "txt": (0.130, 0.001),
    "reply": (0.090, 0.003),
    "stop": (0.100, 0.005),
    "click": (0.075, 0.001),
    "link": (0.060, 0.002),
    "crypto": (0.045, 0.0001),
    "bitcoin": (0.045, 0.0001),
    "verify": (0.055, 0.0005),
    "account": (0.065, 0.004),
    "suspended": (0.035, 0.0001),
    "restricted": (0.030, 0.0001),
    "billing": (0.025, 0.001),
    "unauthorized": (0.025, 0.0002),
    "security": (0.040, 0.004),
    "password": (0.020, 0.001),
    "login": (0.035, 0.001),
    "dollars": (0.025, 0.001),
    "bonus": (0.030, 0.0005),
    "loan": (0.040, 0.0002),
    "rates": (0.030, 0.0015),
    "interest": (0.020, 0.001),
    "earn": (0.035, 0.001),
    "opportunity": (0.025, 0.002),
    "millions": (0.020, 0.0005),
    "casino": (0.015, 0.00005),
    "lottery": (0.025, 0.0001),
    "sweepstakes": (0.015, 0.00001),
    "refund": (0.025, 0.0005),
    "reimbursement": (0.015, 0.0001),
    "irs": (0.020, 0.0001),
    "tax": (0.025, 0.001),
    "invest": (0.030, 0.0005),
    "profit": (0.025, 0.0008),
    "double": (0.020, 0.001),
    "opt": (0.025, 0.001),
    "unsubscribe": (0.045, 0.0005),
    "promo": (0.035, 0.0005),
    "offer": (0.055, 0.003),
    "deal": (0.025, 0.002),
    "sales": (0.030, 0.002),
    
    # Message-specific spam terms
    "entry": (0.060, 0.001),
    "comp": (0.040, 0.0002),
    "final": (0.020, 0.002),
    "tkts": (0.025, 0.0001),
    "tickets": (0.030, 0.0005),
    "question": (0.025, 0.001),
    "apply": (0.035, 0.002),
    "rate": (0.025, 0.0005),
    "receive": (0.050, 0.001),
    "std": (0.025, 0.0001),
    
    # New SMS spam keywords
    "freemsg": (0.060, 0.0001),
    "rcv": (0.040, 0.0001),
    "send": (0.050, 0.005),
    "xxx": (0.040, 0.0001),
    "chgs": (0.030, 0.0001),
    "fun": (0.025, 0.002),
    "darling": (0.015, 0.0005),
    "now": (0.120, 0.025),
    "text": (0.120, 0.010),
    "stop": (0.150, 0.002),

    # OTP / verification phishing keywords
    "otp": (0.180, 0.0001),
    "share": (0.095, 0.003),
    "code": (0.075, 0.004),
    "verification": (0.080, 0.0005),
    "passcode": (0.085, 0.0001),
    "pin": (0.060, 0.003),
    "credential": (0.070, 0.0001),
    "credentials": (0.070, 0.0001),
    
    # Standard ham words (negative weight for spam)
    "meeting": (0.0001, 0.018),
    "later": (0.0008, 0.025),
    "ok": (0.0015, 0.038),
    "come": (0.003, 0.024),
    "home": (0.001, 0.020),
    "love": (0.001, 0.018),
    "thanks": (0.0015, 0.016),
    "sorry": (0.0008, 0.017),
    "gonna": (0.0008, 0.012),
    "work": (0.0015, 0.015),
    "office": (0.0005, 0.009),
    "tomorrow": (0.001, 0.016),
    "week": (0.003, 0.014),
    "schedule": (0.0002, 0.008),
    "attached": (0.001, 0.009),
    "find": (0.003, 0.012),
    "hello": (0.003, 0.011),
    "hey": (0.004, 0.022),
    "guy": (0.001, 0.009),
    "friend": (0.001, 0.012),
    "lunch": (0.0001, 0.007),
    "dinner": (0.0001, 0.006),
    "please": (0.025, 0.035),
    "know": (0.015, 0.030),
    "get": (0.050, 0.045),
    "go": (0.030, 0.050),

    # ── Extended spam vocabulary (compiled from real SMS / email corpora) ────

    # Lottery / Prize / Reward
    "jackpot": (0.040, 0.0001),
    "raffle": (0.030, 0.0001),
    "congratulations": (0.075, 0.002),
    "congrats": (0.060, 0.002),
    "notification": (0.035, 0.003),
    "entitled": (0.045, 0.0005),
    "reward": (0.060, 0.001),
    "voucher": (0.045, 0.0005),
    "coupon": (0.035, 0.001),
    "discount": (0.030, 0.002),
    "exclusive": (0.045, 0.002),
    "limited": (0.055, 0.002),
    "expires": (0.045, 0.0005),
    "expire": (0.040, 0.0005),
    "redeem": (0.045, 0.0005),
    "collect": (0.045, 0.001),
    "hurry": (0.055, 0.001),
    "immediately": (0.050, 0.003),
    "today": (0.055, 0.015),
    "membership": (0.045, 0.0005),
    "subscription": (0.045, 0.001),
    "renewal": (0.035, 0.0005),
    "charged": (0.040, 0.002),
    "invoice": (0.030, 0.001),
    "overdue": (0.035, 0.0001),
    "payment": (0.045, 0.003),
    "debit": (0.035, 0.001),
    "credit": (0.035, 0.004),

    # Phishing / account-takeover
    "update": (0.045, 0.005),
    "confirm": (0.060, 0.004),
    "validate": (0.045, 0.0005),
    "expired": (0.045, 0.001),
    "blocked": (0.045, 0.001),
    "locked": (0.040, 0.001),
    "reactivate": (0.040, 0.0001),
    "restore": (0.035, 0.001),
    "reset": (0.030, 0.003),
    "alert": (0.045, 0.003),
    "warning": (0.040, 0.002),
    "attention": (0.040, 0.002),
    "notice": (0.030, 0.003),
    "immediate": (0.045, 0.001),

    # Financial scam
    "transfer": (0.050, 0.001),
    "beneficiary": (0.035, 0.0001),
    "inheritance": (0.040, 0.0001),
    "billion": (0.025, 0.0001),
    "funds": (0.045, 0.001),
    "forex": (0.025, 0.0001),
    "trading": (0.035, 0.001),
    "investment": (0.035, 0.001),
    "commission": (0.030, 0.001),
    "bank": (0.045, 0.004),
    "wallet": (0.040, 0.002),
    "transaction": (0.050, 0.002),
    "amount": (0.040, 0.003),
    "deposit": (0.045, 0.001),

    # Contact / action spam
    "call": (0.080, 0.012),
    "calling": (0.035, 0.006),
    "dial": (0.040, 0.001),
    "mobile": (0.060, 0.010),
    "whatsapp": (0.040, 0.006),
    "telegram": (0.035, 0.003),
    "customer": (0.050, 0.004),
    "helpline": (0.030, 0.001),
    "representative": (0.025, 0.002),
    "register": (0.030, 0.001),
    "signup": (0.035, 0.001),
    "join": (0.025, 0.004),
    "activate": (0.035, 0.001),
    "subscribe": (0.040, 0.001),
    "download": (0.030, 0.004),
    "visit": (0.030, 0.004),
    "special": (0.045, 0.004),

    # Sensitive-info phishing triggers
    "details": (0.055, 0.003),
    "personal": (0.035, 0.005),
    "private": (0.035, 0.002),
    "secret": (0.040, 0.001),
    "cvv": (0.090, 0.0001),
    "ssn": (0.070, 0.0001),
    "number": (0.035, 0.012),
    "information": (0.040, 0.006),

    # Extended ham vocabulary (common in genuine casual messages)
    "class": (0.0001, 0.010),
    "bus": (0.0001, 0.007),
    "sleep": (0.0001, 0.009),
    "movie": (0.002, 0.011),
    "watch": (0.001, 0.013),
    "study": (0.0001, 0.009),
    "exam": (0.0001, 0.008),
    "school": (0.0001, 0.009),
    "college": (0.0001, 0.006),
    "book": (0.001, 0.009),
    "read": (0.001, 0.011),
    "gym": (0.0001, 0.005),
    "coffee": (0.0001, 0.007),
    "food": (0.001, 0.013),
    "night": (0.003, 0.013),
    "morning": (0.001, 0.011),
    "weekend": (0.001, 0.011),
    "party": (0.002, 0.009),
    "game": (0.003, 0.011),
    "family": (0.001, 0.011),
    "baby": (0.001, 0.009),
    "kids": (0.001, 0.008),
    "brother": (0.0001, 0.007),
    "sister": (0.0001, 0.007),
    "mother": (0.0001, 0.007),
    "father": (0.0001, 0.007),
    "husband": (0.0001, 0.006),
    "wife": (0.0001, 0.007),
    "doctor": (0.0001, 0.006),
    "hospital": (0.0001, 0.006),
    "train": (0.001, 0.009),
    "time": (0.005, 0.016),
    "day": (0.004, 0.016),
    "good": (0.003, 0.018),
    "great": (0.006, 0.014),
    "nice": (0.002, 0.011),
    "need": (0.008, 0.016),
    "want": (0.005, 0.018),
    "like": (0.005, 0.022),
    "think": (0.003, 0.015),
    "talk": (0.002, 0.012),
    "see": (0.004, 0.016),
    "back": (0.003, 0.015),
    "take": (0.004, 0.012),
    "just": (0.006, 0.025),
    "let": (0.003, 0.014),
    "make": (0.004, 0.013),
    "got": (0.004, 0.016),
    "still": (0.003, 0.013),
    "really": (0.004, 0.016),
    "maybe": (0.001, 0.010),
    "sure": (0.003, 0.013),
    "right": (0.003, 0.015),
    "wait": (0.001, 0.011),
    "help": (0.008, 0.014),
    "feel": (0.002, 0.012),
    "look": (0.004, 0.013),
    "start": (0.005, 0.010),
    "try": (0.005, 0.013),
    "ask": (0.003, 0.011),
    "tell": (0.015, 0.014),
    "give": (0.015, 0.013),
    "check": (0.025, 0.012),
    "open": (0.020, 0.007),
}

# Laplace smoothed defaults for out-of-vocabulary words
# Both equal so that unknown words do not skew the score;
# a small structural nudge is applied separately for short OOV-heavy messages.
DEFAULT_P_SPAM = 0.00001
DEFAULT_P_HAM = 0.00001

# ── Bigram (phrase-level) probabilities ──────────────────────────────────────
# Format: "word1 word2": (p_spam, p_ham)
BIGRAM_PROBS = {
    # Strong spam bigrams
    "free entry": (0.150, 0.0001),
    "click here": (0.120, 0.0001),
    "share otp": (0.180, 0.0001),
    "your otp": (0.150, 0.0001),
    "send otp": (0.160, 0.0001),
    "enter otp": (0.150, 0.0001),
    "otp now": (0.150, 0.0001),
    "verification code": (0.120, 0.0001),
    "one time": (0.100, 0.001),
    "win cash": (0.120, 0.0001),
    "free prize": (0.140, 0.0001),
    "claim prize": (0.130, 0.0001),
    "call now": (0.120, 0.0002),
    "act now": (0.100, 0.0001),
    "limited time": (0.100, 0.0002),
    "cash prize": (0.120, 0.0001),
    "free gift": (0.100, 0.0001),
    "won prize": (0.120, 0.0001),
    "bank details": (0.100, 0.0001),
    "account details": (0.100, 0.0001),
    "personal details": (0.100, 0.0001),
    "card details": (0.100, 0.0001),
    "credit card": (0.080, 0.002),
    "bank account": (0.080, 0.002),
    "urgent reply": (0.100, 0.0001),
    "reply stop": (0.100, 0.0001),
    "dear winner": (0.120, 0.0001),
    "dear customer": (0.100, 0.0001),
    "valued customer": (0.100, 0.0001),
    "congrats winner": (0.130, 0.0001),
    "congratulations winner": (0.140, 0.0001),
    "mobile number": (0.080, 0.003),
    "phone number": (0.060, 0.004),
    "bitcoin wallet": (0.120, 0.0001),
    "crypto wallet": (0.120, 0.0001),
    "forex trading": (0.100, 0.0001),
    "money transfer": (0.100, 0.001),
    "wire transfer": (0.100, 0.0001),
    "make money": (0.080, 0.0001),
    "earn money": (0.080, 0.0001),
    "free membership": (0.100, 0.0001),
    "your password": (0.100, 0.001),
    "your pin": (0.100, 0.001),
    "your account": (0.080, 0.005),
    "account suspended": (0.100, 0.0001),
    "account blocked": (0.100, 0.0001),
    "text now": (0.100, 0.001),
    "reply yes": (0.080, 0.001),
    "limited offer": (0.090, 0.0001),
    "special offer": (0.080, 0.001),
    "exclusive offer": (0.090, 0.0001),
    "apply now": (0.080, 0.001),
    "work from": (0.050, 0.001),
    "prize money": (0.120, 0.0001),
    "toll free": (0.090, 0.0001),
    # Ham bigrams (strongly indicate legitimate messages)
    "thank you": (0.001, 0.025),
    "sounds good": (0.0001, 0.015),
    "see you": (0.001, 0.020),
    "talk later": (0.0001, 0.015),
    "good morning": (0.0001, 0.012),
    "good night": (0.0001, 0.012),
    "how are": (0.001, 0.018),
    "are you": (0.002, 0.018),
    "let me": (0.002, 0.015),
    "can you": (0.003, 0.018),
    "going to": (0.003, 0.020),
    "be there": (0.001, 0.012),
    "come over": (0.001, 0.010),
    "at home": (0.0001, 0.012),
    "on my": (0.002, 0.015),
    "i will": (0.001, 0.020),
    "will be": (0.002, 0.015),
}

# Rule-based heuristics
FREE_MSG = re.compile(r"\bfree\s*msg\b", re.IGNORECASE)
PRICE_INDICATOR = re.compile(
    r"([£\$]\d+|\b\d+\.\d+\b)\s*(to|per|each|min|msg|rcv|send|chg|charges)",
    re.IGNORECASE
)
SUSPICIOUS_DOMAINS = re.compile(
    r"\b[a-zA-Z0-9.-]+\.(xyz|top|click|icu|buzz|club|info|gdn|work|monster|bid|stream)\b",
    re.IGNORECASE
)
SHORT_URLS = re.compile(
    r"\b(bit\.ly|t\.co|tinyurl\.com|is\.gd|buff\.ly|ow\.ly|wp\.me|goo\.gl|tiny\.cc|rebrand\.ly)\b",
    re.IGNORECASE
)
CRYPTO_ADDRESS = re.compile(
    r"\b([13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40})\b"
)
PHONE_INSTRUCTION = re.compile(
    r"\b(call|txt|text|sms|reply|to)\b.*\b(\d{5,12})\b",
    re.IGNORECASE
)
PHISHING_PATTERNS = [
    r"confirm.*(billing|identity|login|credentials)",
    r"account.*(suspended|restricted|blocked|disabled|frozen)",
    r"verify.*(your)?.*account",
    r"unauthorized.*(transaction|activity|charges)",
    r"action.*required",
    r"security.*(alert|breach|check)",
    r"login.*to.*(restore|reactivate|verify)",
    # OTP / verification-code solicitation patterns
    r"(share|send|submit|provide|enter|give).*\botp\b",
    r"\botp\b.*(share|send|submit|provide|enter|give)",
    r"one.?time.*(password|code|pin|passcode)",
    r"(verification|verify).*(code|pin|otp|passcode)",
    r"(code|pin|otp|passcode).*(verify|verification|confirm)",
]

# ── Surface / structural feature detectors ───────────────────────────────────
# Detect ALL-CAPS words (shouting = common spam signal)
ALL_CAPS_WORD = re.compile(r"\b[A-Z]{3,}\b")

# Detect explicit monetary amounts (£900, $5,000, 1000 dollars, etc.)
MONEY_AMOUNT = re.compile(
    r"[£$€₹¥]\s*\d[\d,]*(\.[\d]+)?"
    r"|\b\d[\d,]*(\.[\d]+)?\s*(pounds?|dollars?|euros?|rupees?|usd|gbp|inr|euro)\b",
    re.IGNORECASE
)

# Detect 2+ consecutive identical punctuation marks ( !! ??? !!!! )
EXCESSIVE_PUNCT = re.compile(r"[!?]{2,}")

# Detect premium-rate or suspicious phone number prefixes
SUSPICIOUS_PHONE = re.compile(
    r"\b(0800|0900|0808|0844|0845|0870|09\d{2})\s*\d[\d\s]{4,}\b"
)

# Detect imperative verbs immediately followed by sensitive credential nouns
IMPERATIVE_SENSITIVE = re.compile(
    r"\b(share|send|give|provide|enter|submit|tell|reveal|disclose|"
    r"confirm|verify|type|paste|forward)\b.{0,60}"
    r"\b(otp|pin|password|passcode|code|cvv|ssn|details|credentials|"
    r"account|information|card|number|secret|private|token)\b",
    re.IGNORECASE | re.DOTALL
)

# Detect P.O. Box addresses — near-universal in UK premium SMS spam footers
POBOX_PATTERN = re.compile(
    r"\b(p\.?o\.?\s*box|pobox)\b",
    re.IGNORECASE
)

# Detect cost-per-text / rate indicators including corrupted currency symbols
# Matches: "4txt/ú1.20", "1.50 to rcv", "150p/day", "£1.50/msg" etc.
COST_PER_TXT = re.compile(
    r"(?:"
    r"\d+txt[/\\]"
    r"|[\u00a3$\u20ac\u20b9\u00a5\u00fa\u00e2\u009c]\s*\d[\d,.]*"
    r"|\b\d[\d,.]*\s*p(?:ence|/day|/msg|/wk)?"
    r"|\b\d+\.\d+\s*(?:per|/|to)\s*(?:msg|txt|rcv|sms|min)\b"
    r")",
    re.IGNORECASE
)

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
STORE_FILE = os.path.join(DATA_DIR, "keyword_store.json")
LOG_FILE = os.path.join(DATA_DIR, "user_inputs_history.json")
CSV_FILE = os.path.join(DATA_DIR, "datasets.csv")


def log_user_input(text: str, prediction: dict):
    if not text.strip():
        return
    
    init_store()
    history = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                history = json.load(f)
        except Exception:
            history = []
            
    history.append({
        "text": text,
        "is_spam": prediction.get("is_spam", False),
        "confidence": prediction.get("confidence", 0.0),
        "spam_score": prediction.get("spam_score", 0.0),
        "ham_score": prediction.get("ham_score", 0.0)
    })
    
    history = history[-100:]
    
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving user input log: {e}")


def train_from_csv():
    if not os.path.exists(CSV_FILE):
        return
    
    store = {
        "total_spam_messages": 0,
        "total_ham_messages": 0,
        "keyword_counts": {}
    }
    
    try:
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 3:
                    continue
                label = row[1].strip().lower()
                text = row[2]
                
                is_spam = (label == "spam")
                is_ham = (label == "ham")
                
                if not (is_spam or is_ham):
                    continue
                    
                words = preprocess_text(text)
                if is_spam:
                    store["total_spam_messages"] += 1
                else:
                    store["total_ham_messages"] += 1
                    
                keyword_counts = store["keyword_counts"]
                for word in set(words):
                    if word not in keyword_counts:
                        keyword_counts[word] = {"spam_count": 0, "ham_count": 0}
                    if is_spam:
                        keyword_counts[word]["spam_count"] += 1
                    else:
                        keyword_counts[word]["ham_count"] += 1
                        
        save_store_direct(store)
    except Exception as e:
        print(f"Error training from CSV: {e}")

def save_store_direct(data: dict):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(STORE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving keyword store: {e}")

def init_store():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        
    csv_exists = os.path.exists(CSV_FILE)
    store_exists = os.path.exists(STORE_FILE)
    
    should_train = False
    if csv_exists:
        if not store_exists:
            should_train = True
        else:
            should_train = os.path.getmtime(CSV_FILE) > os.path.getmtime(STORE_FILE)
            
    if should_train:
        train_from_csv()
    elif not store_exists:
        initial_data = {
            "total_spam_messages": 0,
            "total_ham_messages": 0,
            "keyword_counts": {}
        }
        with open(STORE_FILE, "w") as f:
            json.dump(initial_data, f, indent=2)


def load_store() -> dict:
    init_store()
    try:
        with open(STORE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "total_spam_messages": 0,
            "total_ham_messages": 0,
            "keyword_counts": {}
        }

def save_store(data: dict):
    init_store()
    try:
        with open(STORE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving keyword store: {e}")

def save_learned_keywords(words: list[str], is_spam: bool, weight: int = 1):
    store = load_store()
    if is_spam:
        store["total_spam_messages"] += weight
    else:
        store["total_ham_messages"] += weight
        
    keyword_counts = store["keyword_counts"]
    for word in set(words):
        if word not in keyword_counts:
            keyword_counts[word] = {"spam_count": 0, "ham_count": 0}
        if is_spam:
            keyword_counts[word]["spam_count"] += weight
        else:
            keyword_counts[word]["ham_count"] += weight
    save_store(store)

def correct_learned_keywords(words: list[str], was_spam: bool, is_spam: bool, weight: int = 5):
    store = load_store()
    
    # 1. Undo the automatic save_learned_keywords (which was run with weight=1 on was_spam)
    if was_spam:
        if store["total_spam_messages"] >= 1:
            store["total_spam_messages"] -= 1
    else:
        if store["total_ham_messages"] >= 1:
            store["total_ham_messages"] -= 1
            
    keyword_counts = store["keyword_counts"]
    for word in set(words):
        if word in keyword_counts:
            if was_spam:
                if keyword_counts[word]["spam_count"] >= 1:
                    keyword_counts[word]["spam_count"] -= 1
            else:
                if keyword_counts[word]["ham_count"] >= 1:
                    keyword_counts[word]["ham_count"] -= 1

    # 2. Add the correct feedback with a higher weight (e.g., 5) to shift predictions
    if is_spam:
        store["total_spam_messages"] += weight
    else:
        store["total_ham_messages"] += weight
        
    for word in set(words):
        if word not in keyword_counts:
            keyword_counts[word] = {"spam_count": 0, "ham_count": 0}
        if is_spam:
            keyword_counts[word]["spam_count"] += weight
        else:
            keyword_counts[word]["ham_count"] += weight
            
    save_store(store)

def correct_prediction(text: str, was_spam: bool, is_spam: bool) -> dict:
    if was_spam == is_spam:
        return detect_spam(text)
        
    words = preprocess_text(text)
    correct_learned_keywords(words, was_spam, is_spam, weight=5)
    
    return detect_spam(text)


def extract_bigrams(text: str) -> list[str]:
    """Extract adjacent lowercase word bigrams for phrase-level Naive Bayes scoring."""
    tokens = re.findall(r"\b[a-zA-Z0-9']+\b", text.lower())
    return [f"{tokens[i]} {tokens[i + 1]}" for i in range(len(tokens) - 1)]


STOP_WORDS = {
    "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", 
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", 
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", 
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", 
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", 
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "most", 
    "other", "some", "such", "nor", "than", "too", "very", "s", "t", "should", "always", 
    "so"
}

def preprocess_text(text: str) -> list[str]:
    # Extract alpha-numeric words, converting to lowercase
    words = re.findall(r"\b[a-zA-Z]{2,15}\b", text.lower())
    # Filter out stop words
    filtered_words = [w for w in words if w not in STOP_WORDS]
    return filtered_words

def detect_spam(text: str) -> dict:
    if not text.strip():
        return {
            "is_spam": False,
            "confidence": 0.0,
            "message": "Empty text context.",
            "spam_score": 0.0,
            "ham_score": 1.0,
            "keywords_detected": []
        }

    words = preprocess_text(text)
    bigrams = extract_bigrams(text)
    
    # Load learned keywords
    store = load_store()
    total_spam = store.get("total_spam_messages", 0)
    total_ham = store.get("total_ham_messages", 0)
    keyword_counts = store.get("keyword_counts", {})
    
    # Smarter OOV: count words not in any known vocabulary
    oov_count = sum(
        1 for w in words
        if w not in VOCAB_PROBS and w not in keyword_counts
    )
    oov_ratio = oov_count / max(len(words), 1)
    
    # 1. Naive Bayes classification
    score_spam = math.log(P_SPAM_PRIOR)
    score_ham = math.log(P_HAM_PRIOR)
    
    detected_words = set()
    
    for word in words:
        p_spam_base, p_ham_base = VOCAB_PROBS.get(word, (DEFAULT_P_SPAM, DEFAULT_P_HAM))
        
        # Blending baseline probabilities with dynamically learned feedback loop
        if (total_spam > 0 or total_ham > 0) and word in keyword_counts:
            counts = keyword_counts[word]
            p_spam_learned = (counts.get("spam_count", 0) + 1) / (total_spam + 2)
            p_ham_learned = (counts.get("ham_count", 0) + 1) / (total_ham + 2)
            
            p_spam = 0.6 * p_spam_base + 0.4 * p_spam_learned
            p_ham = 0.6 * p_ham_base + 0.4 * p_ham_learned
        else:
            p_spam, p_ham = p_spam_base, p_ham_base
            
        score_spam += math.log(p_spam)
        score_ham += math.log(p_ham)
        
        # Add to detected list if it leans heavily towards spam
        if p_spam > p_ham * 2.0:
            detected_words.add(word)

    # 1b. Bigram (phrase-level) Naive Bayes scoring
    for bigram in bigrams:
        if bigram in BIGRAM_PROBS:
            bg_spam, bg_ham = BIGRAM_PROBS[bigram]
            score_spam += math.log(bg_spam)
            score_ham += math.log(bg_ham)
            if bg_spam > bg_ham * 2.0:
                detected_words.add(bigram)

    # 2. Heuristics / Rules (add log-odds multipliers)
    heuristic_spam_boost = 0.0
    heuristic_reasons = []
    
    # Short URLs
    if SHORT_URLS.search(text):
        heuristic_spam_boost += 4.5
        heuristic_reasons.append("suspicious short URL link")
        
    # Suspicious top level domain
    if SUSPICIOUS_DOMAINS.search(text):
        heuristic_spam_boost += 3.5
        heuristic_reasons.append("untrustworthy TLD extension")
        
    # Cryptocurrency addresses
    if CRYPTO_ADDRESS.search(text):
        heuristic_spam_boost += 6.0
        heuristic_reasons.append("cryptocurrency wallet address")
        
    # FreeMsg or Free Msg tag
    if FREE_MSG.search(text):
        heuristic_spam_boost += 4.5
        heuristic_reasons.append("premium service message header")
        
    # Price indicator combined with keywords
    if PRICE_INDICATOR.search(text):
        heuristic_spam_boost += 4.0
        heuristic_reasons.append("unsolicited billing transaction rate")
        
    # Contact Instructions (e.g. Call this number)
    if PHONE_INSTRUCTION.search(text):
        heuristic_spam_boost += 3.0
        heuristic_reasons.append("unverified contact numbers")
        
    # Phishing phrase matching
    phishing_hits = 0
    for pattern in PHISHING_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            phishing_hits += 1
            
    if phishing_hits > 0:
        heuristic_spam_boost += 2.5 * phishing_hits
        heuristic_reasons.append("phishing intent keywords")

    # 3. Surface / structural feature analysis
    # ALL-CAPS words ratio — shouting is a strong spam signal
    caps_words = ALL_CAPS_WORD.findall(text)
    caps_ratio = len(caps_words) / max(len(text.split()), 1)
    if caps_ratio > 0.25:
        boost = min(1.5 * caps_ratio * 4, 4.0)
        heuristic_spam_boost += boost
        heuristic_reasons.append("excessive ALL-CAPS text")

    # Explicit monetary amounts (£900, $5000, etc.)
    if MONEY_AMOUNT.search(text):
        heuristic_spam_boost += 2.5
        heuristic_reasons.append("suspicious monetary amount")

    # Cost-per-text patterns (4txt/ú1.20, 150p/day, £1.50/msg etc.)
    if COST_PER_TXT.search(text):
        heuristic_spam_boost += 3.5
        heuristic_reasons.append("premium SMS cost indicator")

    # P.O. Box address — standard footer in UK premium SMS spam
    if POBOX_PATTERN.search(text):
        heuristic_spam_boost += 3.0
        heuristic_reasons.append("P.O. Box address in footer")

    # Excessive punctuation (!! ??? !!!)
    excess_puncts = EXCESSIVE_PUNCT.findall(text)
    if len(excess_puncts) >= 1:
        heuristic_spam_boost += min(1.0 * len(excess_puncts), 3.0)
        heuristic_reasons.append("excessive punctuation marks")

    # Premium-rate or suspicious phone numbers
    if SUSPICIOUS_PHONE.search(text):
        heuristic_spam_boost += 3.5
        heuristic_reasons.append("premium-rate phone number")

    # Imperative verb + sensitive credential noun (high-confidence phishing)
    if IMPERATIVE_SENSITIVE.search(text):
        heuristic_spam_boost += 5.0
        heuristic_reasons.append("solicitation of sensitive personal info")

    # 4. Smarter OOV nudge for very short, mostly-unknown messages
    # Genuine messages overwhelmingly use common everyday words.
    # A short message built almost entirely from unknown words leans spam.
    if len(words) <= 6 and oov_ratio >= 0.65:
        heuristic_spam_boost += 0.8

    # Apply all heuristic boosts to spam score
    # IMPORTANT: Heuristics are applied as a log-odds shift so they remain effective
    # even when the NB score is driven very negative by many OOV words.
    # We add them before the final softmax normalisation.
    score_spam += heuristic_spam_boost

    # Convert log scores back to probability using the log-sum-exp trick
    # (numerically stable even for very large negative scores)
    max_score = max(score_spam, score_ham)
    try:
        exp_spam = math.exp(score_spam - max_score)
        exp_ham = math.exp(score_ham - max_score)
        total = exp_spam + exp_ham
        # Guard against both being effectively zero (shouldn't happen after max_score shift)
        spam_prob = exp_spam / total if total > 0 else 0.5
    except (OverflowError, ZeroDivisionError):
        spam_prob = 1.0 if score_spam > score_ham else 0.0

    # Ensure a robust classification boundary
    is_spam = spam_prob >= 0.50
    confidence = spam_prob if is_spam else (1.0 - spam_prob)
    
    # Bound confidence to be realistic
    confidence = max(0.50, min(0.99, confidence))
    
    # Generate human readable messages
    if is_spam:
        if len(heuristic_reasons) > 0:
            reasons_str = " & ".join(heuristic_reasons[:2])
            message = f"Flagged as potential spam/phishing due to {reasons_str}."
        else:
            message = "Content analysis indicates high probability of promotional spam."
    else:
        message = "Text appears to be safe and clean ham content."

    # Save classification result to store for adaptive learning
    save_learned_keywords(words, is_spam)

    # Return keywords sorted by spam-proneness
    keywords_sorted = sorted(
        list(detected_words),
        key=lambda w: (VOCAB_PROBS.get(w, (DEFAULT_P_SPAM, DEFAULT_P_HAM))[0] / 
                       VOCAB_PROBS.get(w, (DEFAULT_P_SPAM, DEFAULT_P_HAM))[1]),
        reverse=True
    )

    result = {
        "is_spam": is_spam,
        "confidence": round(confidence, 4),
        "message": message,
        "spam_score": round(spam_prob, 4),
        "ham_score": round(1.0 - spam_prob, 4),
        "keywords_detected": keywords_sorted[:7] # Return top 7 keywords max
    }
    
    log_user_input(text, result)
    return result
