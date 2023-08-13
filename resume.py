import pdfplumber
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_contact_info(text):
    phone_numbers = re.findall(r'\b(?:\d{3}-\d{2}-\d{4}|\d{10})\b', text)
    emails = re.findall(r'\S+@\S+', text)
    return phone_numbers, emails

def extract_name(doc):
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break
    return name

def extract_education(doc):
    education_levels = []
    qualifications = []

    for ent in doc.ents:
        if ent.label_ == "EDUCATION":
            education_levels.append(ent.text)
        elif ent.label_ == "QUALIFICATION":
            qualifications.append(ent.text)

    highest_education = education_levels[0] if education_levels else None

    return highest_education, qualifications

def extract_skills(doc, skills_list):
    skills = []
    for token in doc:
        if token.text.lower() in skills_list:
            skills.append(token.text)
    return skills

def extract_achievements_and_community(doc):
    achievements = []
    community_experience = []

    for sent in doc.sents:
        if "achievement" in sent.text.lower():
            achievements.append(sent.text)
        if "community" in sent.text.lower():
            community_experience.append(sent.text)

    return achievements, community_experience

def main():
    with pdfplumber.open("C V.pdf") as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    doc = nlp(text)

    phone_numbers, emails = extract_contact_info(text)
    name = extract_name(doc)
    highest_education, qualifications = extract_education(doc)

    skills_list = ["python", "java", "communication", "teamwork", "problem solving", "leadership"]
    skills = extract_skills(doc, skills_list)

    achievements, community_experience = extract_achievements_and_community(doc)

    print("Name:", name)
    print("Phone Numbers:", phone_numbers)
    print("Emails:", emails)
    print("Highest Education:", highest_education)
    print("Qualifications:", qualifications)
    print("Skills:", skills)
    print("Achievements:", achievements)
    print("Community Experience:", community_experience)

if __name__ == "__main__":
    main()
