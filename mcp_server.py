import os
from typing import Optional
from fastmcp import FastMCP
from auth import verify_bearer_token, get_my_number
from llm import llm_service
from image_processor import image_processor
import json

# Initialize MCP server
mcp = FastMCP("Dating Wingman")

# --- Tool: validate (required by Puch) ---
@mcp.tool()
async def validate() -> str:
    """Validation tool required by Puch"""
    return get_my_number()

# --- Tool: analyze_profile_screenshot ---
@mcp.tool()
async def analyze_profile_screenshot(
    image_base64: str,
    analysis_type: str = "comprehensive"
) -> str:
    """
    Analyze dating profile screenshot and provide detailed feedback
    
    Args:
        image_base64: Base64 encoded image of the dating profile
        analysis_type: Type of analysis (comprehensive, quick, strengths_only)
    """
    try:
        # Process the image
        image_data = image_processor.process_base64_image(image_base64)
        if not image_data:
            return "❌ Could not process the image. Please ensure it's a valid image format."
        
        if not image_processor.validate_image_size(image_data):
            return "❌ Image is too large. Please upload an image smaller than 10MB."
        
        # Analyze with LLM
        analysis = await llm_service.analyze_profile_image(image_data)
        
        return f"""
🔍 **Dating Profile Analysis**

{analysis}

💡 **Next Steps:**
- Use `/improve_bio` to enhance your bio
- Try `/generate_opener` for conversation starters
- Use `/roast_profile` for honest feedback with humor
"""
        
    except Exception as e:
        return f"❌ Error analyzing profile: {str(e)}"

# --- Tool: generate_conversation_replies ---
@mcp.tool()
async def generate_conversation_replies(
    conversation_context: str,
    goal: str = "continue conversation"
) -> str:
    """
    Generate smart replies for dating conversations
    
    Args:
        conversation_context: The conversation history or current message
        goal: Your goal (continue_conversation, ask_for_date, be_flirty, be_funny)
    """
    try:
        response = await llm_service.generate_conversation_reply(conversation_context, goal)
        
        return f"""
💬 **Smart Reply Suggestions**

{response}

🎯 **Tips:**
- Personalize the reply to match your voice
- Ask follow-up questions to keep conversation flowing
- Show genuine interest in their responses
"""
        
    except Exception as e:
        return f"❌ Error generating replies: {str(e)}"

# --- Tool: improve_bio ---
@mcp.tool()
async def improve_bio(
    current_bio: str,
    additional_info: str = ""
) -> str:
    """
    Improve your dating app bio to be more attractive
    
    Args:
        current_bio: Your current dating app bio
        additional_info: Additional details about yourself (hobbies, job, etc.)
    """
    try:
        response = await llm_service.improve_bio(current_bio, additional_info)
        
        return f"""
✨ **Bio Improvement Suggestions**

{response}

📝 **Pro Tips:**
- Keep it authentic to who you are
- Include conversation starters
- Show, don't just tell your qualities
- Update regularly to keep it fresh
"""
        
    except Exception as e:
        return f"❌ Error improving bio: {str(e)}"

# --- Tool: generate_opener ---
@mcp.tool()
async def generate_opener(
    match_info: str
) -> str:
    """
    Generate personalized conversation openers based on match's profile
    
    Args:
        match_info: Information about your match (bio, photos, interests, etc.)
    """
    try:
        response = await llm_service.generate_opener(match_info)
        
        return f"""
🚀 **Conversation Starters**

{response}

💡 **Opening Message Tips:**
- Reference something specific from their profile
- Ask open-ended questions
- Show genuine curiosity
- Avoid generic compliments
- Keep it light and fun
"""
        
    except Exception as e:
        return f"❌ Error generating openers: {str(e)}"

# --- Tool: roast_profile ---
@mcp.tool()
async def roast_profile(
    profile_description: str,
    humor_level: str = "medium"
) -> str:
    """
    Get your dating profile roasted with constructive feedback
    
    Args:
        profile_description: Description of your dating profile
        humor_level: How brutal to be (mild, medium, savage)
    """
    try:
        response = await llm_service.roast_profile(profile_description, humor_level)
        
        return f"""
🔥 **Profile Roast ({humor_level.title()} Level)**

{response}

😅 **Remember:**
- It's all in good fun!
- Use the feedback to improve
- Confidence is attractive
- Every roast comes with love ❤️
"""
        
    except Exception as e:
        return f"❌ Error roasting profile: {str(e)}"

# --- Tool: detect_red_flags ---
@mcp.tool()
async def detect_red_flags(
    conversation_or_profile: str,
    context_type: str = "conversation"
) -> str:
    """
    Detect potential red flags in conversations or profiles
    
    Args:
        conversation_or_profile: The text to analyze
        context_type: Whether it's a 'conversation' or 'profile'
    """
    try:
        prompt = f"""
Analyze this dating {context_type} for potential red flags:

{conversation_or_profile}

Look for:
- Manipulative behavior
- Disrespectful language
- Inconsistencies
- Pushy behavior
- Inappropriate requests
- Signs of dishonesty
- Controlling tendencies

Provide a safety assessment and advice.
"""
        
        response = await llm_service.client.chat.completions.create(
            model=llm_service.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.3  # Lower temperature for safety analysis
        )
        
        analysis = response.choices[0].message.content
        
        return f"""
🚨 **Red Flag Analysis**

{analysis}

⚠️ **Safety Reminders:**
- Trust your instincts
- Take things slow
- Meet in public places
- Tell friends about your dates
- Block if you feel uncomfortable
"""
        
    except Exception as e:
        return f"❌ Error analyzing for red flags: {str(e)}"

# --- Tool: plan_date ---
@mcp.tool()
async def plan_date(
    location: str,
    budget: str = "medium",
    interests: str = "",
    date_type: str = "first_date"
) -> str:
    """
    Get date planning suggestions based on preferences
    
    Args:
        location: City or area for the date
        budget: Budget level (low, medium, high)
        interests: Shared interests or activities you both like
        date_type: Type of date (first_date, second_date, romantic, fun)
    """
    try:
        prompt = f"""
Plan a {date_type} in {location} with a {budget} budget.

Shared interests: {interests}

Provide:
1. 3-5 specific date ideas with locations
2. Estimated costs
3. What to wear suggestions
4. Conversation topics
5. How to suggest the date
6. Backup plans if needed

Make it memorable but appropriate for the relationship stage.
"""
        
        response = await llm_service.client.chat.completions.create(
            model=llm_service.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        
        plan = response.choices[0].message.content
        
        return f"""
💕 **Date Planning Assistant**

{plan}

🎯 **Date Success Tips:**
- Confirm plans the day before
- Arrive on time
- Put phone away and be present
- Ask questions and listen actively
- Have fun and be yourself!
"""
        
    except Exception as e:
        return f"❌ Error planning date: {str(e)}"

# --- Tool: help ---
@mcp.tool()
async def help() -> str:
    """Get help and see all available Dating Wingman tools"""
    return """
🎯 **Dating Wingman - Your AI Dating Assistant**

**Available Tools:**

📸 **analyze_profile_screenshot** - Upload dating profile screenshots for AI analysis
💬 **generate_conversation_replies** - Get smart reply suggestions for conversations  
✨ **improve_bio** - Make your dating bio more attractive
🚀 **generate_opener** - Create personalized conversation starters
🔥 **roast_profile** - Get honest feedback with humor
🚨 **detect_red_flags** - Safety analysis for conversations/profiles
💕 **plan_date** - Get date planning suggestions
❓ **help** - Show this help message

**How to Use:**
1. Connect via WhatsApp: Message "Dating Wingman" on Puch AI
2. Upload screenshots directly in chat
3. Ask for specific help: "Generate openers for this match"
4. Get instant AI-powered dating advice!

**Example Commands:**
- "Analyze this profile screenshot"
- "Help me reply to this message"
- "Improve my bio"
- "Generate conversation starters"

💡 **Pro Tip:** The more context you provide, the better the advice!

Built with ❤️ for #BuildWithPuch hackathon
"""

# Export the mcp server
__all__ = ["mcp"]
