import os
from openai import AsyncOpenAI
from typing import List, Optional
import base64
from PIL import Image
import io

class LLMService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️ WARNING: OPENAI_API_KEY not found in environment variables!")
            print("Please set your OpenAI API key in the .env file")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=api_key)
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    def _check_client(self):
        """Check if client is initialized"""
        if not self.client:
            raise Exception("OpenAI client not initialized. Please check your API key.")
    
    async def analyze_profile_image(self, image_data: bytes) -> str:
        """Analyze dating profile image using vision model"""
        try:
            self._check_client()
            
            # Convert bytes to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Analyze this dating profile image and provide:
1. Attractiveness score (1-10)
2. 3-5 strengths of the profile
3. 3-5 areas for improvement
4. Any red flags you notice
5. Overall assessment

Be honest but constructive. Focus on photo quality, presentation, and dating appeal."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
    
    async def generate_conversation_reply(self, conversation_context: str, user_goal: str = "continue conversation") -> str:
        """Generate conversation replies based on context"""
        try:
            self._check_client()
            
            prompt = f"""
Based on this dating conversation context:
{conversation_context}

User goal: {user_goal}

Provide 3-5 potential reply options that are:
1. Engaging and show interest
2. Ask follow-up questions
3. Keep the conversation flowing
4. Match the tone of the conversation
5. Move toward meeting/date if appropriate

Also assess if there are any red flags in the conversation.
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.8
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating replies: {str(e)}"
    
    async def improve_bio(self, current_bio: str, user_details: str = "") -> str:
        """Improve dating app bio"""
        try:
            self._check_client()
            
            prompt = f"""
Improve this dating app bio:
Current bio: "{current_bio}"

Additional details about user: {user_details}

Create an improved version that is:
1. More engaging and attractive
2. Shows personality
3. Includes conversation starters
4. Avoids common clichés
5. Appropriate length (not too long)

Explain what changes were made and why.
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error improving bio: {str(e)}"
    
    async def roast_profile(self, profile_description: str, humor_level: str = "medium") -> str:
        """Provide constructive roasting of dating profile"""
        try:
            self._check_client()
            
            humor_instructions = {
                "mild": "Be gentle and mostly constructive with light humor",
                "medium": "Balance humor and constructive feedback equally",
                "savage": "Be brutally honest with sharp humor, but still helpful"
            }
            
            prompt = f"""
Roast this dating profile with {humor_level} humor level:
{profile_description}

{humor_instructions.get(humor_level, humor_instructions["medium"])}

Provide:
1. Humorous roasting points
2. Constructive feedback mixed in
3. Specific suggestions for improvement
4. End on a positive/encouraging note

Keep it fun but ultimately helpful for improving their dating success.
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.9
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating roast: {str(e)}"
    
    async def generate_opener(self, match_info: str) -> str:
        """Generate conversation openers based on match information"""
        try:
            self._check_client()
            
            prompt = f"""
Based on this information about a dating match:
{match_info}

Generate 5 creative conversation starters that:
1. Reference something specific from their profile
2. Ask engaging questions
3. Show genuine interest
4. Avoid generic "hey" messages
5. Have potential for good responses

Make them feel personalized and thoughtful.
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.8
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating openers: {str(e)}"

# Global LLM service instance
llm_service = LLMService()
