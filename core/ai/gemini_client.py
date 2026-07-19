"""
Gemini AI Client Module
Handles all AI interactions using Google Gemini API for resume analysis and recruitment.
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AnalysisResult:
    """Data class for AI analysis results."""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None


class GeminiClient:
    """
    Client for interacting with Google Gemini API.
    Provides methods for resume analysis, job matching, and recruitment insights.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client with API key.
        
        Args:
            api_key: Gemini API key. If not provided, reads from environment variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Initialize client with new SDK
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
    
    def _generate_content(self, prompt: str) -> str:
        """
        Generate content using Gemini model with new SDK.
        
        Args:
            prompt: The prompt to send to the model.
            
        Returns:
            Generated text response.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg.lower() or "invalid" in error_msg.lower():
                raise Exception(f"Invalid API Key: {error_msg}")
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                raise Exception(f"Network Error: {error_msg}")
            elif "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
                raise Exception(f"Rate Limit Exceeded: {error_msg}")
            else:
                raise Exception(f"Error generating content: {error_msg}")
    
    def analyze_resume(
        self,
        resume_text: str,
        job_description: Optional[str] = None,
        job_role: Optional[str] = None
    ) -> AnalysisResult:
        """
        Analyze resume and provide comprehensive insights.
        
        Args:
            resume_text: Extracted text from resume.
            job_description: Optional job description for matching.
            job_role: Optional job role for matching.
            
        Returns:
            AnalysisResult containing resume analysis data.
        """
        try:
            prompt = self._build_resume_analysis_prompt(
                resume_text, job_description, job_role
            )
            response = self._generate_content(prompt)
            
            # Parse JSON response
            try:
                data = json.loads(response)
                return AnalysisResult(success=True, data=data)
            except json.JSONDecodeError:
                # Fallback: return raw text if JSON parsing fails
                return AnalysisResult(
                    success=True,
                    data={"raw_response": response}
                )
                
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def calculate_ats_score(
        self,
        resume_text: str,
        job_description: str
    ) -> AnalysisResult:
        """
        Calculate ATS (Applicant Tracking System) compatibility score.
        
        Args:
            resume_text: Extracted text from resume.
            job_description: Job description to match against.
            
        Returns:
            AnalysisResult containing ATS score and details.
        """
        try:
            prompt = f"""
            Analyze the ATS compatibility of this resume against the job description.
            
            Resume:
            {resume_text}
            
            Job Description:
            {job_description}
            
            Provide a JSON response with the following structure:
            {{
                "ats_score": <number 0-100>,
                "keyword_matches": [<list of matched keywords>],
                "missing_keywords": [<list of missing keywords>],
                "format_score": <number 0-100>,
                "content_score": <number 0-100>,
                "suggestions": [<list of specific improvements>]
            }}
            """
            response = self._generate_content(prompt)
            data = json.loads(response)
            return AnalysisResult(success=True, data=data)
            
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def generate_interview_questions(
        self,
        resume_text: str,
        job_description: str,
        question_count: int = 10
    ) -> AnalysisResult:
        """
        Generate interview questions based on resume and job description.
        
        Args:
            resume_text: Extracted text from resume.
            job_description: Job description.
            question_count: Number of questions to generate.
            
        Returns:
            AnalysisResult containing interview questions.
        """
        try:
            prompt = f"""
            Generate {question_count} interview questions based on this resume and job description.
            
            Resume:
            {resume_text}
            
            Job Description:
            {job_description}
            
            Provide a JSON response with the following structure:
            {{
                "technical_questions": [
                    {{"question": "...", "difficulty": "easy/medium/hard", "category": "..."}}
                ],
                "behavioral_questions": [
                    {{"question": "...", "focus": "..."}}
                ],
                "hr_questions": [
                    {{"question": "...", "purpose": "..."}}
                ],
                "project_specific_questions": [
                    {{"question": "...", "related_project": "..."}}
                ]
            }}
            """
            response = self._generate_content(prompt)
            data = json.loads(response)
            return AnalysisResult(success=True, data=data)
            
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def generate_career_roadmap(
        self,
        resume_text: str,
        target_role: str
    ) -> AnalysisResult:
        """
        Generate career roadmap based on current skills and target role.
        
        Args:
            resume_text: Extracted text from resume.
            target_role: Target job role.
            
        Returns:
            AnalysisResult containing career roadmap.
        """
        try:
            prompt = f"""
            Generate a career roadmap to reach the target role based on current skills.
            
            Resume:
            {resume_text}
            
            Target Role:
            {target_role}
            
            Provide a JSON response with the following structure:
            {{
                "current_level": "...",
                "target_level": "...",
                "skill_gaps": [<list of missing skills>],
                "learning_path": [
                    {{"phase": "...", "skills": [...], "timeline": "...", "resources": [...]}}
                ],
                "recommended_certifications": [...],
                "project_suggestions": [...],
                "estimated_time_to_target": "..."
            }}
            """
            response = self._generate_content(prompt)
            data = json.loads(response)
            return AnalysisResult(success=True, data=data)
            
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def predict_salary(
        self,
        resume_text: str,
        job_role: str,
        location: str = "Remote"
    ) -> AnalysisResult:
        """
        Predict salary range based on resume and job role.
        
        Args:
            resume_text: Extracted text from resume.
            job_role: Job role.
            location: Job location.
            
        Returns:
            AnalysisResult containing salary prediction.
        """
        try:
            prompt = f"""
            Predict salary range based on this resume and job role.
            
            Resume:
            {resume_text}
            
            Job Role:
            {job_role}
            
            Location:
            {location}
            
            Provide a JSON response with the following structure:
            {{
                "min_salary": <number>,
                "max_salary": <number>,
                "average_salary": <number>,
                "currency": "USD",
                "factors": [<list of factors affecting the prediction>],
                "market_comparison": "above/below/at market rate",
                "negotiation_tips": [...]
            }}
            """
            response = self._generate_content(prompt)
            data = json.loads(response)
            return AnalysisResult(success=True, data=data)
            
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def rewrite_resume(
        self,
        resume_text: str,
        job_description: str,
        language: str = "english"
    ) -> AnalysisResult:
        """
        Rewrite and improve resume for better ATS compatibility.
        
        Args:
            resume_text: Extracted text from resume.
            job_description: Target job description.
            language: Language for output (english/hinglish).
            
        Returns:
            AnalysisResult containing rewritten resume.
        """
        try:
            lang_instruction = "Use professional English" if language == "english" else "Use Hinglish (mix of Hindi and English)"
            
            prompt = f"""
            Rewrite this resume to better match the job description and improve ATS compatibility.
            {lang_instruction}.
            
            Original Resume:
            {resume_text}
            
            Job Description:
            {job_description}
            
            Provide a JSON response with the following structure:
            {{
                "rewritten_resume": "...",
                "improvements_made": [<list of changes>],
                "added_keywords": [...],
                "removed_sections": [...],
                "formatting_suggestions": [...]
            }}
            """
            response = self._generate_content(prompt)
            data = json.loads(response)
            return AnalysisResult(success=True, data=data)
            
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def analyze_certificate(
        self,
        certificate_text: str,
        resume_text: Optional[str] = None
    ) -> AnalysisResult:
        """
        Analyze certificate and estimate its industry value.
        
        Args:
            certificate_text: Extracted text from certificate.
            resume_text: Optional resume text for context.
            
        Returns:
            AnalysisResult containing certificate analysis.
        """
        try:
            context = f"\nResume Context:\n{resume_text}" if resume_text else ""
            
            prompt = f"""
            Analyze this certificate and estimate its industry value.
            
            Certificate Text:
            {certificate_text}
            {context}
            
            Provide a JSON response with the following structure:
            {{
                "certificate_name": "...",
                "issuing_organization": "...",
                "industry_value": "high/medium/low",
                "relevance_score": <number 0-100>,
                "skills_covered": [...],
                "recognition_level": "industry/organization/regional",
                "suggested_usage": "...",
                "complementary_certifications": [...]
            }}
            """
            response = self._generate_content(prompt)
            data = json.loads(response)
            return AnalysisResult(success=True, data=data)
            
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def compare_candidates(
        self,
        candidate_data: List[Dict[str, Any]],
        job_description: str
    ) -> AnalysisResult:
        """
        Compare multiple candidates for a job position.
        
        Args:
            candidate_data: List of candidate data including resume text.
            job_description: Job description.
            
        Returns:
            AnalysisResult containing candidate comparison.
        """
        try:
            candidates_json = json.dumps(candidate_data, indent=2)
            
            prompt = f"""
            Compare these candidates for the job position.
            
            Candidates:
            {candidates_json}
            
            Job Description:
            {job_description}
            
            Provide a JSON response with the following structure:
            {{
                "ranked_candidates": [
                    {{
                        "rank": <number>,
                        "candidate_id": "...",
                        "score": <number>,
                        "strengths": [...],
                        "weaknesses": [...],
                        "recommendation": "..."
                    }}
                ],
                "best_fit": "...",
                "skill_comparison": {{
                    "candidate_1": {{...}},
                    "candidate_2": {{...}}
                }},
                "hiring_recommendation": "..."
            }}
            """
            response = self._generate_content(prompt)
            data = json.loads(response)
            return AnalysisResult(success=True, data=data)
            
        except Exception as e:
            return AnalysisResult(success=False, data={}, error=str(e))
    
    def _build_resume_analysis_prompt(
        self,
        resume_text: str,
        job_description: Optional[str],
        job_role: Optional[str]
    ) -> str:
        """
        Build comprehensive prompt for resume analysis.
        
        Args:
            resume_text: Extracted text from resume.
            job_description: Optional job description.
            job_role: Optional job role.
            
        Returns:
            Formatted prompt string.
        """
        job_context = ""
        if job_description:
            job_context += f"\nJob Description:\n{job_description}"
        if job_role:
            job_context += f"\nTarget Role: {job_role}"
        
        prompt = f"""
        Analyze this resume comprehensively. {job_context}
        
        Resume Text:
        {resume_text}
        
        Provide a detailed JSON analysis with the following structure:
        {{
            "overall_score": <number 0-100>,
            "ats_score": <number 0-100>,
            "grammar_score": <number 0-100>,
            "communication_score": <number 0-100>,
            "design_score": <number 0-100>,
            "sections": {{
                "summary": {{"score": <number>, "content": "...", "suggestions": [...] }},
                "experience": {{"score": <number>, "years": <number>, "suggestions": [...] }},
                "education": {{"score": <number>, "details": [...], "suggestions": [...] }},
                "skills": {{"score": <number>, "technical": [...], "soft": [...], "missing": [...] }},
                "projects": {{"score": <number>, "count": <number>, "suggestions": [...] }},
                "certificates": {{"score": <number>, "list": [...], "suggestions": [...] }}
            }},
            "strengths": [<detailed list with explanations>],
            "weaknesses": [<detailed list with explanations and how to fix>],
            "missing_skills": [<skills to add with why they matter>],
            "improvement_suggestions": [<specific actionable improvements>],
            "recommended_projects": [<project ideas to add>],
            "recommended_certifications": [<certifications to pursue>],
            "resume_summary": "<executive summary>"
        }}
        
        For each weakness, explain:
        - WHY it's a problem
        - HOW to fix it
        - WHAT impact it has on the application
        
        Be specific and actionable in all suggestions.
        """
        return prompt


class TranslationService:
    """
    Service for translating AI responses between English and Hinglish.
    """
    
    def __init__(self, gemini_client: GeminiClient):
        """
        Initialize translation service.
        
        Args:
            gemini_client: GeminiClient instance for translation.
        """
        self.client = gemini_client
    
    def translate_to_hinglish(self, text: str) -> str:
        """
        Translate English text to Hinglish.
        
        Args:
            text: English text to translate.
            
        Returns:
            Hinglish translation.
        """
        prompt = f"""
        Translate the following text to Hinglish (natural mix of Hindi and English as spoken in India).
        Keep technical terms in English. Make it conversational and natural.
        
        Text to translate:
        {text}
        """
        return self.client._generate_content(prompt)
    
    def translate_to_english(self, text: str) -> str:
        """
        Translate Hinglish text to English.
        
        Args:
            text: Hinglish text to translate.
            
        Returns:
            English translation.
        """
        prompt = f"""
        Translate the following Hinglish text to professional English.
        Maintain the technical accuracy and professional tone.
        
        Text to translate:
        {text}
        """
        return self.client._generate_content(prompt)
