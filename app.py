from flask import Flask, render_template, request
import os

from resume_parser import extract_text
from nlp_utils import clean_text
from model import text_similarity, skill_match, experience_score
from database import init_db, save_result

app = Flask(__name__)
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        role = request.form["role"]
        job_desc = clean_text(request.form["job_desc"])

        resumes, names = [], []
        files = request.files.getlist("resumes")

        for f in files:
            path = os.path.join(UPLOAD_FOLDER, f.filename)
            f.save(path)
            text = clean_text(extract_text(path))
            resumes.append(text)
            names.append(f.filename)

        sim_scores = text_similarity(resumes, job_desc)

        for i in range(len(names)):
            skill_s, matched, missing, m, t = skill_match(
                resumes[i], job_desc, role
            )
            exp_s = experience_score(resumes[i])

            final = (0.6 * skill_s) + (0.25 * sim_scores[i]) + (0.15 * exp_s)
            final_pct = round(final * 100, 2)

            # ---------- FIXED FEEDBACK LOGIC ----------
            feedback = []

            if final_pct < 40:
                feedback.append("Low match with job requirements")

            if t > 0 and m == 0:
                feedback.append("No core job skills matched")

            if missing:
                feedback.append("Consider adding: " + ", ".join(missing))

            if exp_s < 0.5:
                feedback.append("Highlight internships or projects more clearly")

            feedback_text = (
                "Strong profile for this role"
                if not feedback
                else "; ".join(feedback)
            )

            # Resume improvement tips
            tips = []
            if missing:
                tips.append("Add missing technical skills to resume")
            if exp_s < 0.7:
                tips.append("Mention project impact and duration clearly")
            if sim_scores[i] < 0.4:
                tips.append("Align resume wording with job description keywords")

            save_result(names[i], role, final_pct)

            results.append({
                "name": names[i],
                "score": final_pct,
                "coverage": f"{m}/{t}",
                "matched": matched,
                "missing": missing,
                "breakdown": {
                    "skills": round(skill_s * 100, 1),
                    "nlp": round(sim_scores[i] * 100, 1),
                    "exp": round(exp_s * 100, 1)
                },
                "feedback": feedback_text,
                "tips": tips
            })

            results.sort(key=lambda x: x["score"], reverse=True)

# ✅ Assign rank ONLY if more than one resume
            if len(results) > 1:
                for idx, r in enumerate(results):
                    r["rank"] = idx + 1
            else:
                results[0]["rank"] = None


    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
