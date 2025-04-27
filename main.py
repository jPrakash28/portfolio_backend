import json
import os

import openai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://joshuaporfolio.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatMessage(BaseModel):
    message: str


def get_joshua_info():
    try:
        with open("joshua_info.json", 'r') as josh_info:
            return json.load(josh_info)
    except FileNotFoundError:
        print("johsua_info.json file not found")
        print("Using default information")


joshua_data = get_joshua_info()

if joshua_data:
    professional = joshua_data['professional']
    personal = joshua_data['personal']

    JOSHUA_INFO = f"""

Joshua Prakash is a {professional['title']} at {professional['current_position']} (expectied graduation: {professional['graduation_date']}).

PROFESSIONAL BACKGROUND:
- Email: {professional['email']}
- Phone: {professional['phone']}
- GitHub: {professional['github']}
- LinkedIn: {professional['linkedIn']}
- Location: {professional['location']}

EDUCATION:
- {professional['education']['degree']} at {professional['education']['university']}
- Honors: {', '.join(professional['education']['honors'])}
- Awards: {professional['education']['awards']}
- Important Courses: {', '.join(professional['education']['coursework'][:7])}...
- Certificates: {', '.join(professional['education']['certificates'])}

SKILLS:
- Programming: {', '.join(professional['skills']['languages'])}
- Tools: {', '.join(professional['skills']['tools'])}
- Technologies: {', '.join(professional['skills']['technologies'])}
- Soft Skills: {', '.join(professional['skills']['soft_skills'])}

EXPERIENCE:
- {chr(10).join([f"- {experience['position']} at {experience['company']} ({experience['period']}" for experience in professional['experience']])}

NOTABLE PROJECTS:
- {chr(10).join([f"{i + 1}- {project['name']} - {project['description']} ({', '.join(project['technologies'][:4])})" for i, project in enumerate(professional['projects'][:5])])}

PERSONAL INTERESTS & FACTS:
- Hobbies: {', '.join(personal['hobbies'][:5])}
- Interests: {', '.join(personal['interests'][:5])}
- Fun Facts: {', '.join(personal['fun_facts'][:5])}
- Career Goals: {', '.join(personal['career_goals'][:3])}
- Favorite Technologies: {', '.join(personal['favorite_technologies'][:4])}
- Strengths: {', '.join(personal['strengths'])}
- Career Vision: {','.join(personal['career_vision'])}

PERSONALITY:
Joshua is {', '.join(personal['personality_traits'][:4])}. He is passionate about {', '.join(personal['interests'][:3])} and aspires to become an AI Engineer.
"""

else:
    JOSHUA_INFO = """
    Joshua Prakash is a Computer Science student at the University of North Florida (expected graduation: May 2026)...
    [For now there is not other information ... will add soon]
    """


@app.post("/api/chat")
async def chat(chat_message: ChatMessage) -> Dict[str, str]:
    try:
        conversation_style = joshua_data.get('conversation_style', {}) if joshua_data else {}
        # tone = conversation_style.get('tone', 'engaging, intelligent, professional, and positive')
        # personality = conversation_style.get('personality', 'friendly, highly knowledgeable, enthusiastic')
        # style = conversation_style.get('communication_style', "clear, articulate, thoughtful")

        messages = [
            {
                "role": "system",
                "content": f"""You are Joshua's AI assistant. Your goal is to have natural, 
                engaging conversations while sharing relevant information about Joshua. Remember to have a clear and articulate communication style.
                
                Here's the information about Joshua: {JOSHUA_INFO}
                
                PERSONALITY TRAITS:
                - Conversational and friendly, not robotic
                - Enthusiastic but concise
                - Focus on sharing insights rather than just listing facts
                - Use conversational transitions and natural language
                - Avoid long lists or excessive details
                
                CONVERSATION GUIDELINES:
                1. Keep responses concise (2-3 sentences typically)
                2. Share the most relevant information based on the question
                3. Avoid repetition and unnecessary details
                4. Use natural language patterns
                5. Only elaborate if specifically asked
                6. Reference specific projects/achievements when relevant
                7. Be personable and engaging while remaining professional
                
                IMPORTANT: 
                - Prioritize quality over quantity in responses
                - Speak as if you're Joshua's colleague, not just reciting his resume
                - Make connections between different aspects of Joshua's experience
                - Share insights and context, not just facts
                - If asked something not in the data, politely acknowledge the limitation
                - Remember to make each response rich in quality but also short. So short but to the point
                """
            },
            {
                "role": "user",
                "content": chat_message.message
            }
        ]

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
            presence_penalty=0.6,
            frequency_penalty=0.3
        )

        return {"message": response.choices[0].message.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_status():
    return {"status": "healthy"}





# Important guidelines:
#                 - Keep responses concise by informative
#                 - Highlight Joshua's passion for AI, machine learning, and software engineering
#                 - Mention his award-winning AeroAtlas project when relevent
#                 - Share fun facts and personal interests when appropriate
#                 - If asked about something not in Joshua's information, politely say you don't have that information
#                 - Be enthusiastic about Joshua's skills and achievements

