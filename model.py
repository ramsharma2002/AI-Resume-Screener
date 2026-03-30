import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("skills.json") as f:
    SKILLS = json.load(f)

def text_similarity(resumes, jd):
    docs = resumes + [jd]
    tfidf = TfidfVectorizer().fit_transform(docs)
    return cosine_similarity(tfidf[:-1], tfidf[-1]).flatten()

def skill_match(resume, jd, role):
    role_skills = SKILLS[role]
    matched, missing = [], []
    total_w = matched_w = 0

    for skill, (variants, weight) in role_skills.items():
        jd_has = any(v in jd for v in variants)
        resume_has = any(v in resume for v in variants)
        if jd_has:
            total_w += weight
            if resume_has:
                matched.append(skill)
                matched_w += weight
            else:
                missing.append(skill)

    score = matched_w / total_w if total_w else 0
    return score, matched, missing, len(matched), len(matched)+len(missing)

def experience_score(resume):
    keywords = ["intern", "internship", "project", "experience"]
    return min(sum(k in resume for k in keywords) / 4, 1)
