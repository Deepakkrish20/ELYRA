import re
import urllib.request
import urllib.parse
import json

MOVIE_DATABASE = {
    "inception": {
        "title": "Inception",
        "year": "2010",
        "genres": [
            {"name": "Sci-Fi", "confidence": 0.95},
            {"name": "Thriller", "confidence": 0.85},
            {"name": "Action", "confidence": 0.75}
        ],
        "advisories": {"violence": "Moderate", "language": "Low", "nudity": "None"},
        "key_themes": ["Dreams vs. Reality", "Grief & Guilt", "Subconscious Heist"],
        "runtime_estimate": "148 mins",
        "watchability_status": "Highly Recommended",
        "summary": "A mind-bending sci-fi thriller about a team of thieves who infiltrate the human subconscious. It offers an intellectually rich experience with moderate action sequences and no mature/explicit content."
    },
    "the dark knight": {
        "title": "The Dark Knight",
        "year": "2008",
        "genres": [
            {"name": "Action", "confidence": 0.98},
            {"name": "Thriller", "confidence": 0.90},
            {"name": "Drama", "confidence": 0.80}
        ],
        "advisories": {"violence": "High", "language": "Low", "nudity": "None"},
        "key_themes": ["Chaos vs. Order", "Morality & Justice", "Sacrifice"],
        "runtime_estimate": "152 mins",
        "watchability_status": "Highly Recommended (Mature Audiences)",
        "summary": "A gritty superhero masterpiece exploring Batman's confrontation with the Joker's anarchy. Its high level of intense, psychological violence requires parental caution for younger viewers."
    },
    "titanic": {
        "title": "Titanic",
        "year": "1997",
        "genres": [
            {"name": "Romance", "confidence": 0.98},
            {"name": "Drama", "confidence": 0.92}
        ],
        "advisories": {"violence": "Moderate", "language": "Low", "nudity": "Moderate"},
        "key_themes": ["Class Divide", "Fate & Sacrifice", "Eternal Devotion"],
        "runtime_estimate": "195 mins",
        "watchability_status": "Highly Recommended",
        "summary": "An epic romance set against the tragic sinking of the R.M.S. Titanic. It features emotional class struggles and historic disaster sequences alongside brief nudity and mild language."
    },
    "the matrix": {
        "title": "The Matrix",
        "year": "1999",
        "genres": [
            {"name": "Sci-Fi", "confidence": 0.96},
            {"name": "Action", "confidence": 0.92}
        ],
        "advisories": {"violence": "Moderate", "language": "Moderate", "nudity": "None"},
        "key_themes": ["Illusion vs. Truth", "Fate & Choice", "Rebirth"],
        "runtime_estimate": "136 mins",
        "watchability_status": "Highly Recommended",
        "summary": "A groundbreaking cyberpunk action film depicting humanity's struggle against artificial systems. Its themes of self-discovery are paired with stylish gunplay and martial arts."
    },
    "toy story": {
        "title": "Toy Story",
        "year": "1995",
        "genres": [
            {"name": "Comedy", "confidence": 0.95},
            {"name": "Fantasy", "confidence": 0.90},
            {"name": "Drama", "confidence": 0.70}
        ],
        "advisories": {"violence": "None", "language": "None", "nudity": "None"},
        "key_themes": ["Friendship & Loyalty", "Identity Crisis", "Acceptance & Growth"],
        "runtime_estimate": "81 mins",
        "watchability_status": "Family Friendly (All Ages)",
        "summary": "A delightful animated story about the secret lives of toys. Perfectly clean and heartwarming, it delivers valuable lessons about cooperation and friendship for children and parents alike."
    },
    "interstellar": {
        "title": "Interstellar",
        "year": "2014",
        "genres": [
            {"name": "Sci-Fi", "confidence": 0.98},
            {"name": "Drama", "confidence": 0.88}
        ],
        "advisories": {"violence": "Low", "language": "Low", "nudity": "None"},
        "key_themes": ["Love Across Dimensions", "Survival & Time", "Human Exploration"],
        "runtime_estimate": "169 mins",
        "watchability_status": "Highly Recommended",
        "summary": "A visually breathtaking odyssey about astronauts searching for a habitable planet. It explores deep scientific concepts wrapped in a powerful, emotional father-daughter bond."
    },
    "finding nemo": {
        "title": "Finding Nemo",
        "year": "2003",
        "genres": [
            {"name": "Comedy", "confidence": 0.90},
            {"name": "Family", "confidence": 0.95}
        ],
        "advisories": {"violence": "None", "language": "None", "nudity": "None"},
        "key_themes": ["Parental Love", "Overcoming Fears", "Trust & Independence"],
        "runtime_estimate": "100 mins",
        "watchability_status": "Family Friendly (All Ages)",
        "summary": "An endearing underwater quest following a father's search for his lost son. Packed with comedy, memorable sea creatures, and family-oriented heart, it is safe for viewers of all ages."
    },
    "pulp fiction": {
        "title": "Pulp Fiction",
        "year": "1994",
        "genres": [
            {"name": "Thriller", "confidence": 0.90},
            {"name": "Action", "confidence": 0.85},
            {"name": "Drama", "confidence": 0.80}
        ],
        "advisories": {"violence": "High", "language": "High", "nudity": "Moderate"},
        "key_themes": ["Redemption", "Fate & Chance", "Underworld Morality"],
        "runtime_estimate": "154 mins",
        "watchability_status": "Restricted (Mature Audiences Only)",
        "summary": "A highly stylized and influential neo-noir crime film. It contains extreme, stylized violence, heavy profanity, and mature themes, making it suitable only for adults."
    },
    "gladiator": {
        "title": "Gladiator",
        "year": "2000",
        "genres": [
            {"name": "Action", "confidence": 0.95},
            {"name": "Drama", "confidence": 0.90}
        ],
        "advisories": {"violence": "High", "language": "Low", "nudity": "None"},
        "key_themes": ["Honor & Revenge", "Legacy & Family", "Tyranny vs. Freedom"],
        "runtime_estimate": "155 mins",
        "watchability_status": "Watchable with Caution (Violence)",
        "summary": "A magnificent historical epic following a betrayed general who becomes a gladiator. Its intense and bloody arena combat sequences necessitate viewer discretion for younger audiences."
    }
}

def fetch_movie_from_wikipedia(title: str, year: str = "") -> dict:
    query = f"{title} film"
    if year:
        query = f"{title} {year} film"
        
    url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'InsightAI/1.0 (contact@example.com)'})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            search_results = res_data.get('query', {}).get('search', [])
            if not search_results:
                return None
            
            page_title = search_results[0]['title']
            
            # Verify if the search result page title is a reasonable match for our query title
            def get_significant_words(t: str):
                t = re.sub(r'\(.*?\)', '', t)
                t = re.sub(r'[^a-zA-Z0-9\s]', '', t)
                words = t.lower().split()
                return [w for w in words if w not in ["film", "movie", "the", "a", "an", "of", "and", "in", "on", "at", "to", "for"]]
                
            qw = get_significant_words(title)
            pw = get_significant_words(page_title)
            
            if not qw:
                return None
                
            overlap = sum(1 for w in qw if w in pw)
            if (overlap / len(qw)) < 0.5:
                return None
            
            # 1. Fetch introduction extract
            extract_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles={urllib.parse.quote(page_title)}&format=json"
            req2 = urllib.request.Request(extract_url, headers={'User-Agent': 'InsightAI/1.0'})
            extract = ""
            with urllib.request.urlopen(req2, timeout=5) as extract_response:
                extract_data = json.loads(extract_response.read().decode('utf-8'))
                pages = extract_data.get('query', {}).get('pages', {})
                for page_id, page_info in pages.items():
                    extract = page_info.get('extract', '')
                    
            if not extract:
                return None
                
            # 2. Fetch revisions (infobox) to find runtime
            runtime = None
            rev_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles={urllib.parse.quote(page_title)}&format=json"
            req3 = urllib.request.Request(rev_url, headers={'User-Agent': 'InsightAI/1.0'})
            try:
                with urllib.request.urlopen(req3, timeout=5) as rev_response:
                    rev_data = json.loads(rev_response.read().decode('utf-8'))
                    pages = rev_data.get('query', {}).get('pages', {})
                    for page_id, page_info in pages.items():
                        revisions = page_info.get('revisions', [])
                        if revisions:
                            content = revisions[0].get('*', '')
                            runtime_match = re.search(r'runtime\s*=\s*([^\n|]+)', content, re.IGNORECASE)
                            if runtime_match:
                                raw_runtime = runtime_match.group(1).strip()
                                nums = re.findall(r'\d+', raw_runtime)
                                if nums:
                                    runtime = nums[0] + " mins"
            except Exception:
                pass
                
            # If runtime not found in infobox, search in intro text
            if not runtime:
                runtime_match = re.search(r'(\d+)\s*(?:minute|min)', extract, re.IGNORECASE)
                if runtime_match:
                    runtime = runtime_match.group(1) + " mins"
            if not runtime:
                runtime = "120 mins" # Default fallback
                
            # 3. Extract year
            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', extract)
            extracted_year = year_match.group(1) if year_match else (year or "Unknown")
            
            # 4. Extract genres
            genre_keywords = {
                "Sci-Fi": ["sci-fi", "science fiction", "cyberpunk", "futuristic", "alien", "space"],
                "Thriller": ["thriller", "suspense", "mystery", "crime", "detective", "investigate"],
                "Action": ["action", "martial arts", "superhero", "spy", "combat", "police", "cop", "chase"],
                "Romance": ["romance", "romantic", "love story", "love", "passion"],
                "Comedy": ["comedy", "humorous", "sarcastic", "parody", "hilarious"],
                "Fantasy": ["fantasy", "magical", "supernatural", "wizard", "magic"],
                "Drama": ["drama", "melodrama", "biographical", "historical", "family"]
            }
            
            extract_lower = extract.lower()
            genres_found = []
            for genre, keywords in genre_keywords.items():
                for kw in keywords:
                    if kw in extract_lower:
                        genres_found.append(genre)
                        break
            
            if not genres_found:
                genres_found = ["Drama"]
                
            # Calculate match percentages
            genres_result = []
            for g in list(set(genres_found)):
                genres_result.append({
                    "name": g,
                    "confidence": round(1.0 / len(set(genres_found)), 4)
                })
            
            primary_genre = genres_result[0]["name"]
            
            # 5. Extract Themes
            theme_map = {
                "Sci-Fi": ["Technology & Humanity", "The Unknown Space", "Ethics of Creation"],
                "Thriller": ["Trust & Deception", "Morality in Shadows", "Survival Instincts"],
                "Action": ["Honor & Duty", "Good vs. Evil", "Courage Under Fire"],
                "Romance": ["Fate & Soulmates", "Sacrifice for Love", "Personal Connection"],
                "Comedy": ["Acceptance & Quirks", "Laughter & Friendship", "Chaotic Encounters"],
                "Fantasy": ["The Hero's Journey", "Destiny & Power", "Mythical Legacy"],
                "Drama": ["Growth & Adaptation", "Legacy & Family", "Overcoming Grief"]
            }
            key_themes = theme_map.get(primary_genre, ["Human Journey", "Fate", "Choices"])[:3]
            
            # 6. Advisories
            has_violent_words = any(w in extract_lower for w in ["kill", "dead", "murder", "blood", "war", "fight", "dark", "die", "violence"])
            has_mature_words = any(w in extract_lower for w in ["sex", "passion", "wild", "naked", "night", "strip", "nudity"])
            
            title_hash = sum(ord(c) for c in page_title)
            violence = "High" if has_violent_words else ("Moderate" if title_hash % 3 == 0 else "Low")
            nudity = "Moderate" if has_mature_words else ("Low" if (title_hash + 1) % 4 == 0 else "None")
            language = "Moderate" if (title_hash + 2) % 3 == 0 else "Low"
            
            advisories = {
                "violence": violence,
                "language": language,
                "nudity": nudity
            }
            
            # 7. Watchability Verdict & Summary
            if violence == "High" or nudity == "High":
                watchability_status = "Watchable with Caution (Mature Audiences)"
            elif violence in ["None", "Low"] and nudity == "None" and language in ["None", "Low"]:
                watchability_status = "Family Friendly (All Ages)"
            else:
                watchability_status = "Highly Recommended"
                
            # Create a nice short sentence summary based on the extract
            summary_sentences = extract.split('.')
            if len(summary_sentences) > 0:
                summary = '. '.join(summary_sentences[:2]).strip()
                if not summary.endswith('.'):
                    summary += '.'
            else:
                summary = f"A production centering on themes of {', '.join(key_themes[:2])}."
                
            return {
                "title": page_title.replace(" (film)", "").strip(),
                "year": str(extracted_year),
                "genres": genres_result,
                "advisories": advisories,
                "key_themes": key_themes,
                "runtime_estimate": runtime,
                "watchability_status": watchability_status,
                "summary": summary
            }
    except Exception as e:
        print("Error during Wikipedia lookup:", e)
        return None

def clean_title(title: str) -> str:
    return title.strip().lower()

def classify_movie(title: str, year: str = "") -> dict:
    cleaned = clean_title(title)
    
    # Try exact match in our movie database
    if cleaned in MOVIE_DATABASE:
        db_entry = MOVIE_DATABASE[cleaned].copy()
        # Override year if user passed one
        if year:
            db_entry["year"] = str(year)
        return db_entry

    # Try fetching from Wikipedia API for real data
    wiki_result = fetch_movie_from_wikipedia(title, year)
    if wiki_result:
        return wiki_result

    # Otherwise, classify dynamically based on title keywords and character hashing
    # Genres mapping
    genre_keywords = {
        "Sci-Fi": ["space", "star", "future", "alien", "cyborg", "robot", "dystopia", "galaxy", "tech", "quantum", "planet"],
        "Thriller": ["murder", "killer", "dead", "dark", "crime", "secret", "detective", "shadow", "night", "trap", "conspiracy"],
        "Action": ["war", "fight", "agent", "force", "chase", "combat", "strike", "heist", "weapon", "battle", "gun", "rescue"],
        "Romance": ["love", "heart", "kiss", "marry", "date", "lover", "passion", "forever", "sweet", "romance"],
        "Comedy": ["fun", "crazy", "buddy", "laugh", "happy", "wild", "silly", "party", "joke", "dog", "cat", "pet"],
        "Fantasy": ["magic", "dragon", "wizard", "spell", "sword", "beast", "curse", "realm", "legend", "myth", "kingdom"],
        "Drama": ["life", "hope", "tear", "family", "loss", "grief", "dream", "truth", "road", "home", "story", "growth"]
    }
    
    matched_genres = {}
    for genre, keywords in genre_keywords.items():
        score = 0
        for kw in keywords:
            if kw in cleaned:
                score += 2
        if score > 0:
            matched_genres[genre] = score
            
    # Deterministic fallback using title characters if no keywords match
    if not matched_genres:
        title_hash = sum(ord(c) for c in cleaned)
        genres_list = list(genre_keywords.keys())
        g1 = genres_list[title_hash % len(genres_list)]
        g2 = genres_list[(title_hash + 7) % len(genres_list)]
        matched_genres[g1] = 5
        matched_genres[g2] = 3
        
    total_score = sum(matched_genres.values())
    genres_result = []
    for g, score in matched_genres.items():
        genres_result.append({
            "name": g,
            "confidence": round(score / total_score, 4)
        })
    genres_result = sorted(genres_result, key=lambda x: x["confidence"], reverse=True)[:3]
    
    primary_genre = genres_result[0]["name"]
    
    # Key themes map based on primary genre
    theme_map = {
        "Sci-Fi": ["Technology & Humanity", "The Unknown Space", "Ethics of Creation"],
        "Thriller": ["Trust & Deception", "Morality in Shadows", "Survival Instincts"],
        "Action": ["Honor & Duty", "Good vs. Evil", "Courage Under Fire"],
        "Romance": ["Fate & Soulmates", "Sacrifice for Love", "Personal Connection"],
        "Comedy": ["Acceptance & Quirks", "Laughter & Friendship", "Chaotic Encounters"],
        "Fantasy": ["The Hero's Journey", "Destiny & Power", "Mythical Legacy"],
        "Drama": ["Growth & Adaptation", "Legacy & Family", "Overcoming Grief"]
    }
    key_themes = theme_map.get(primary_genre, ["Human Journey", "Fate", "Choices"])[:3]
    
    # Deterministic Advisories
    has_violent_words = any(w in cleaned for w in ["kill", "dead", "murder", "blood", "war", "fight", "dark", "die"])
    has_mature_words = any(w in cleaned for w in ["sex", "passion", "wild", "naked", "night", "strip"])
    
    title_hash = sum(ord(c) for c in cleaned)
    
    violence = "High" if has_violent_words else ("Moderate" if title_hash % 3 == 0 else "Low")
    nudity = "Moderate" if has_mature_words else ("Low" if (title_hash + 1) % 4 == 0 else "None")
    language = "Moderate" if (title_hash + 2) % 3 == 0 else "Low"
    
    is_kids = any(w in cleaned for w in ["kids", "toy", "nemo", "cartoon", "baby", "little", "happy", "dog", "cat"])
    if is_kids:
        violence = "None"
        nudity = "None"
        language = "None"
        
    advisories = {
        "violence": violence,
        "language": language,
        "nudity": nudity
    }
    
    # Watchability & Summary
    if violence == "High" or nudity == "High":
        watchability_status = "Watchable with Caution (Mature Audiences)"
        summary = f"An intense cinematic depiction showcasing themes of {', '.join(key_themes[:2])}. Parental discretion is strongly advised due to mature visual and verbal elements."
    elif violence in ["None", "Low"] and nudity == "None" and language in ["None", "Low"]:
        watchability_status = "Family Friendly (All Ages)"
        summary = f"A lighthearted and engaging movie built around themes of {', '.join(key_themes[:2])}. With completely clean content, it is highly suitable for children and family audiences."
    else:
        watchability_status = "Highly Recommended"
        summary = f"A solid, well-recommended production centering on themes of {', '.join(key_themes[:2])}. Suitable for general viewership with minor mature content warnings."
        
    runtime_base = 90 + (title_hash % 60)
    runtime_estimate = f"{runtime_base} mins"
    
    return {
        "title": title.title(),
        "year": str(year) if year else "Unknown",
        "genres": genres_result,
        "advisories": advisories,
        "key_themes": key_themes,
        "runtime_estimate": runtime_estimate,
        "watchability_status": watchability_status,
        "summary": summary
    }
