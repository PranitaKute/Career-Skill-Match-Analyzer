import streamlit as st
import PyPDF2
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title = "Career Skill Match Analyzer",
    page_icon = "💼",
    layout = "wide"
)

st.title("💼 Career Skill Match Analyzer")
st.write("Upload your resume or paste your text below to find your best career domain matches based on your skills!")


# Input Section
st.subheader("Step 1 : Upload or Paste Resume")
uploaded_file = st.file_uploader("Upload your Resume (PDF format)", type=["pdf"])
resume_text = ""

if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
    except Exception as e:
        st.error(f"Error reading PDF: {e}")

st.write("Or paste your resume text manually below")
manual_text = st.text_area("Paste your text here:", height = 200)


# Combine uploaded + pasted text
if manual_text.strip():
    resume_text += "\n" + manual_text

if resume_text:
    st.success("Resume text loaded successfully!")
    with st.expander("Preview Resume Text"):
        st.write(resume_text[:1500] + "..." if len(resume_text) > 1500 else resume_text)
else:
    st.info("Please upload or paste your resume to continue.")



# Next phase - 2 (Skill Extraction)
st.markdown("---")
st.subheader("Step 2 : Skill Extraction & Career Match")
st.write("We'll now analyze your resume text to extract key skills.")
# We'll now analyze your resume text to extract key skills using NLP
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# dict of skills for different domains
career_skills = {
    "Web Developer" : ["html", "css", "tailwind css", "javascript", "react", "node", "frontend", "backend", "api", "bootstrap", "typescript", "php", 'responsive design', "git"],
    "Data Analyst" : ["excel", "sql", "python", "r", "data", "visualization", "manipulation", "powerbi", "tableau", "statistics", "numpy", "pandas", "critical thinking", "data preprocessing"],
    "AI Engineer" : ["machine learning", "deep learning", "tensorflow", "pytorch", "nlp", "computer vision", "data preprocessing", "statistics", "python", "r", "scikit-learn"],
    "Cybersecurity" : ["network", "security", "firewall", "encryption", "penetration", "vulnerability", "malware", "risk", "forensics", "python", "javascript", "php", "nmap", "metasploit", "burp suite"],
    "UI/UX Designer" : ["figma", "wireframe", "prototype", "user experience","design thinking", "adobe", "sketch", "illustrator", "visual design", "information architechture"],
    "Content Writing" : ["research", "storytelling", "seo", "communication", "technical writing", "documentation"],
    "Project Manager" : ["communication", "problem solving", "leadership", "time management"],
}

# skill extraction and cleaning
if resume_text:
    # st.subheader("Step 2 : Skill Extraction & Career Match")

    # tokenize and clean text
    tokens = word_tokenize(resume_text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in tokens if word.isalpha() and word not in stop_words]

    # calculate skill match score
    domain_scores = {}
    for domain, skills in career_skills.items():
        matches = [skill for skill in skills if skill in filtered_words]
        score = len(matches) / len(skills) * 100
        domain_scores[domain] = round(score, 2)
    
    # convert to dataframe for display
    df_scores = pd.DataFrame(list(domain_scores.items()), columns=['Career Domain', 'Match Percentage'])
    df_scores = df_scores.sort_values(by = "Match Percentage", ascending = False)

    st.write("Your Skill Match Summary")
    st.dataframe(df_scores, use_container_width = True)

    # Visualization
    
    # df_scores["Match Percentage"] = pd.to_numeric(df_scores["Match Percentage"], errors='coerce').fillna(0)
    # fig = px.bar(df_scores, 
    #              x = 'Career Domain', 
    #              y = 'Match Percentage', 
    #              color = 'Career Domain', 
    #              title = "Career Match Based on Your Skills", 
    #              text = df_scores["Match Percentage"].round(1).astype(str) + "%",
    #              color_discrete_sequence=px.colors.qualitative.Set2,
    #             )
    
    # fig.update_traces(textposition = 'outside',
    #                   marker_line_color = 'white',
    #                   marker_line_width = 1.5,
    #                 #   marker=dict(line=dict(color='black', width=1.2)),
    #                   width = 0.6,
    #                   opacity = 0.9
    #                   )
    
    # fig.update_layout(
    #     title = "Career Match Based on Your Skills",
    #     yaxis_range = [0, max(100, df_scores["Match Percentage"].max() + 10)],
    #     xaxis_title = "Career Domain",
    #     yaxis_title = "Match Percentage",
    #     title_x = 0.5,
    #     # yaxis= dict(
    #     #     range=[0,max(df_scores["Match Percentage"].max() + 5, 25)],
    #     #     dtick = 5,
    #     #     gridcolor = 'rgba(200, 200, 200, 0.3)'
    #     #     ),
    #     # xaxis = dict(showgrid = False),
    #     bargap = 0.25,
    #     plot_bgcolor = 'rgba(0,0,0,0)',
    #     paper_bgcolor = 'rgba(0,0,0,0)',
    #     # font_color = 'white',
    #     font = dict(color='white'),
    #     height = 500
    #     )
    # st.plotly_chart(fig, use_container_width = True, theme = None)
    

    # Visualization (Fixed bar visibility issue)
    st.write("### Career Match Visualization")

    plt.style.use("dark_background")

    plt.figure(figsize=(10, 6))
    bar_colors = sns.color_palette("husl", len(df_scores))

    bars = plt.bar(
        df_scores['Career Domain'],
        df_scores['Match Percentage'],
        color=bar_colors,
        edgecolor='white',
        width=0.6,
        alpha=0.9
    )

    for bar, score in zip(bars, df_scores['Match Percentage']):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1,
            f"{score:.1f}%",
            ha='center',
            va='bottom',
            fontsize=10,
            color='white'
        )

    plt.xlabel("Career Domain", fontsize=12, color='white')
    plt.ylabel("Match Percentage", fontsize=12, color='white')
    plt.title("Career Match Based on Your Skills", fontsize=14, color='white')
    plt.ylim(0, max(df_scores['Match Percentage'].max() + 10, 100))
    plt.grid(axis='y', linestyle='--', alpha=0.5, color='gray')
    st.pyplot(plt)

    # debugging - bar chart not visible
    st.write("Debug - df_scores:", df_scores)
    st.write("Max match percentage:", df_scores["Match Percentage"].max())

    # Top Match
    top_domain = df_scores.iloc[0]
    st.success(f"Your top matching domain is **{top_domain['Career Domain']}** with a {top_domain['Match Percentage']}% match!")



# Phase 3 Enhanced Visualisation + suggestion
st.markdown("---")
st.subheader("Step 3 : Deeper Insights")

if 'df_scores' in locals() and not df_scores.empty:
    df_scores["Match Percentage"] = df_scores["Match Percentage"].astype(float)

    # Radar chart for domain comparison
    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r = df_scores["Match Percentage"],
        theta = df_scores["Career Domain"],
        fill = 'toself',
        name = 'Skill Match'
    ))

    fig_radar.update_layout(
        polar = dict(radialaxis = dict(visible = True, range = [0,100])),
        showlegend = False,
        title = "Career Domain Match Radar Chart"
    )
    st.plotly_chart(fig_radar, use_container_width = True)

    # Suggest skills to improve top 2 domains
    top_two = df_scores.sort_values(by = "Match Percentage", ascending = False).head(2)
    st.subheader("Skill Improvement Suggestions")

    for _, row in top_two.iterrows():
        domain = row['Career Domain']
        match_percent = row['Match Percentage']
        st.markdown(f" **{domain} ({match_percent}% match)**")

        # Find missing skills for that domain
        all_skills = set(career_skills[domain])
        present_skills = {skill for skill in all_skills if skill in resume_text.lower()}
        missing_skills = all_skills - present_skills

        if missing_skills:
            st.write("You could improve by learning:")
            for skill in missing_skills:
                st.write(f"- {skill.capitalize()}")
            # st.write(",".join(f" {skill}" for skill in missing_skills))
        else:
            st.success("Perfect! You already have all the key skills for this domain.")

    st.markdown("---")
    st.info("Tip: Try uploading different resumes or adding new skills to see how your match changes!")

    csv = df_scores.to_csv(index = False).encode('utf-8')
    st.download_button("Download Results as CSV", data = csv, file_name = "career_match_results.csv", mime = "text/csv")

else:
    st.warning("Please upload your resume and run analysis first!")



# Phase 4 : AI powered Career Insights
st.markdown("---")
st.subheader("Step 4 : AI-Powered Career Insights")

if 'df_scores' in locals() and not df_scores.empty:
    top_domain = df_scores.iloc[0]['Career Domain']
    top_score = df_scores.iloc[0]['Match Percentage']

    # identify overall skill strength
    if top_score > 75:
        strength = "Excellent skill alignment! You're career-ready"
    elif top_score > 50:
        strength = "Great foundation - keep strengthening your skills!"
    elif top_score > 25:
        strength = "Decent start, you're on the right path!"
    else:
        strength = "You're just starting out - explore and experiment more."
    
    st.write(f"Top Career Match: {top_domain}")
    st.write(f"Your skills align **{top_score}%** with this domain.")
    st.success(strength)

    # career suggestion
    suggestions = {
        "Web Developer": [
            "Explore full-stack frameworks like **Next.js**, **Express.js**, or **Django**",
            "Build hands-on projects - portfolio sites, blogs, or e-commerce app."
        ],
        "Data Analyst": [
            "Master **data storytelling** using Power BI or Tableau.",
            "Work on datasets to improve data cleaning, visualization, and SQL querying"
        ],
        "AI Engineer": [
            "Pracitice on **Kaggle** or **Google Colab** with real-world datasets.",
            "Deepen your understanding of **NLP**, **TensorFlow**, and **Model Optimization**."        
        ],
        "Cybersecurity": [
            "Try platforms like **TryHackMe** or **HackTheBox** for practical experience.",
            "Learn about **OWASP Top 10** vulnerabilities and basic cryptography."
        ],
        "UI/UX Designer": [
            "Create interactive prototypes on **Figma** or **Adobe XD**.",
            "Study color theory, typography, and **usability testing** principles."
        ],
        "Project Manager": [
            "Develop **leadership** and **strategic planning** skills.",
            "Learn tools like **Jira**, **Trello**, and agile frameworks such as **Scrum**."
        ]
    }

    if top_domain in suggestions:
        st.write("Recommended Next Steps")
        for tip in suggestions[top_domain]:
            st.markdown(f"- {tip}")
    
    keyword_count = len(filtered_words)
    unique_words = len(set(filtered_words))
    keyword_density = round(unique_words / keyword_count * 100, 2) if keyword_count > 0 else 0

    st.markdown("Resume Keyword Analysis")
    st.write(f"- **Total words analyzed:** {keyword_count}")
    st.write(f"- **Unique skill keywords:** {unique_words}")
    st.write(f"- **Keyword diversity:** {keyword_density}%")

    if keyword_density < 20:
        st.warning("Your resume might lack strong keywords - try adding technical or role-specific terms.")
    else:
        st.info("Your resume shows good keyword diversity and skill representation!")

    st.markdown("---")
    st.caption("*These insights are rule-based for now. Later we'll integrate AI/ML models for personalized predictions.")



# Phase 5 : Resume Optimization Recommendations
# skills coverage = (matched skills / total career skills) * 100
# st.markdown("---")
# st.subheader("Step 5 : Resume Optimization and Feedback")

# if not df_scores.empty and resume_text:
#     top_domain = df_scores.iloc[0]['Career Domain']
#     st.write(f"Analyzing your resume for deeper insights in the domain of **{top_domain}***...")

#     # relevant skills for top domain
#     domain_skills = set(career_skills[top_domain])
#     present_skills = {skill for skill in domain_skills if skill in resume_text.lower()}
#     missing_skills = domain_skills - present_skills
#     skill_coverage = round(len(present_skills) / len(domain_skills) * 100, 2)

#     st.markdown(f"Skill Coverage Analysis for {top_domain}")
#     st.write(f"Matched Skills:**{len(present_skills)} / {len(domain_skills)} ({skill_coverage}%)")

#     # skill coverage bar
#     coverage_data = pd.DataFrame({
#         "Skill Type": ["Matched", "Missing"],
#         "Count" : [len(present_skills), len(missing_skills)]
#     })

#     fig_coverage = px.bar(
#         coverage_data,
#         x = "Skill Type",
#         y = "Count",
#         color = "Skill Type",
#         title = "Skill Match Overview",
#         color_discrete_map = {"Matched": "#2ecc71", "Missing": "#e74c3c"},
#         text = "Count"
#     )

#     fig_coverage.update_traces(textposition = 'outside')
#     fig_coverage.update_layout(yaxis_title = "Number of Skills", xaxis_title = "", title_x = 0.5)
#     st.plotly_chart(fig_coverage, use_container_width = True)

#     # Display matched, missing
#     with st.expander("🔍 Matched Skills"):
#         if present_skills:
#             st.write(", ".join(sorted(present_skills)))
#         else:
#             st.write("No major skill matches found.")

#     with st.expander("🚀 Missing / Suggested Skills"):
#         if missing_skills:
#             st.write(", ".join(sorted(missing_skills)))
#         else:
#             st.success("You already have all the key skills for this domain!")