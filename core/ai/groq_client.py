"""
Groq AI Client Module
Handles all AI interactions using Groq API for resume analysis and recruitment.
"""

import os
import json
import re
import logging
from typing import Dict, List, Optional, Any
from groq import Groq
from dotenv import load_dotenv
from .base_llm import BaseLLMClient, AnalysisResult

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqClient(BaseLLMClient):
    """
    Client for interacting with Groq API.
    Provides methods for resume analysis, job matching, and recruitment insights.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Groq client with API key.
        
        Args:
            api_key: Groq API key. If not provided, reads from environment variable.
            model: Model name. If not provided, reads from environment variable.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.temperature = float(os.getenv("GROQ_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "4096"))
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        logger.info(f"GroqClient initialized with model: {self.model}")
    
    def _extract_json_from_response(self, response: str) -> str:
        """
        Extract JSON from a response that may contain markdown formatting.
        
        Args:
            response: Raw response text from LLM.
            
        Returns:
            Extracted JSON string.
        """
        # Try to find JSON between markdown code blocks
        json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        matches = re.findall(json_pattern, response)
        
        if matches:
            # Return the first JSON block found
            logger.info(f"Extracted JSON from markdown code block")
            return matches[0].strip()
        
        # Try to find JSON object without markdown
        # Look for content between first { and last }
        brace_start = response.find('{')
        brace_end = response.rfind('}')
        
        if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
            json_content = response[brace_start:brace_end + 1]
            logger.info(f"Extracted JSON from brace positions")
            return json_content.strip()
        
        # If no JSON found, return original response
        logger.warning("No JSON found in response, returning original")
        return response
    
    def _generate_content(self, prompt: str) -> str:
        """
        Generate content using Groq model.
        
        Args:
            prompt: The prompt to send to the model.
            
        Returns:
            Generated text response.
        """
        try:
            logger.info(f"Generating content with prompt length: {len(prompt)}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            content = response.choices[0].message.content
            logger.info(f"Generated response length: {len(content)}")
            return content
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating content: {error_msg}")
            if "API key" in error_msg.lower() or "invalid" in error_msg.lower():
                raise Exception(f"Invalid API Key: {error_msg}")
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                raise Exception(f"Network Error: {error_msg}")
            elif "rate limit" in error_msg.lower() or "429" in error_msg:
                raise Exception(f"Rate Limit Exceeded: {error_msg}")
            elif "timeout" in error_msg.lower():
                raise Exception(f"Timeout Error: {error_msg}")
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
            logger.info("Starting resume analysis")
            
            job_context = ""
            if job_description:
                job_context += f"\nJob Description:\n{job_description}"
            if job_role:
                job_context += f"\nJob Role:\n{job_role}"
            
            prompt = f"""
            Analyze this resume comprehensively and provide detailed feedback.
            
            Resume:
            {resume_text}
            {job_context}
            
            IMPORTANT: Return ONLY valid JSON. No markdown. No code blocks. No explanations.
            
            Return this exact JSON structure:
            {{
                "overall_score": <number 0-100>,
                "ats_score": <number 0-100>,
                "grammar_score": <number 0-100>,
                "communication_score": <number 0-100>,
                
                "strengths": [
                    {{
                        "title": "Strength title",
                        "why_good": "Explanation of why this is good",
                        "recruiter_impact": "How this impacts recruiters"
                    }}
                ],
                
                "weaknesses": [
                    {{
                        "title": "Weakness title",
                        "why_hurting": "Why this is hurting the resume",
                        "ats_impact": "Low/Medium/High",
                        "recruiter_impact": "Impact on recruiters"
                    }}
                ],
                
                "improvement_suggestions": [
                    {{
                        "suggestion": "Actionable suggestion",
                        "how_to_implement": "Step-by-step implementation",
                        "expected_impact": "Expected result"
                    }}
                ],
                
                "missing_skills": [
                    {{
                        "skill": "Required skill name",
                        "importance": "High/Medium/Low",
                        "reason": "Why this skill is needed",
                        "learning_resources": ["Resource 1", "Resource 2"]
                    }}
                ],
                
                "missing_resume_sections": [
                    {{
                        "section": "Section name (e.g., Professional Summary, Achievements, Certifications, Projects, Open Source, Publications, Languages, Volunteer Experience, Leadership, Hackathons, GitHub, LinkedIn, Portfolio)",
                        "why_matters": "Why this section is important",
                        "how_to_write": "How to write this section effectively"
                    }}
                ],
                
                "ats_analysis": {{
                    "matched_keywords": ["keyword1", "keyword2"],
                    "missing_keywords": ["keyword1", "keyword2"],
                    "keyword_density": "percentage",
                    "formatting_issues": ["issue1", "issue2"],
                    "ats_compatibility": "Low/Medium/High",
                    "action_plan": ["action1", "action2"]
                }},
                
                "rewrite_suggestions": [
                    {{
                        "current_text": "Original text",
                        "suggested_text": "Improved version",
                        "reason": "Why this is better"
                    }}
                ],
                
                "interview_questions": {{
                    "technical_questions": [
                        {{
                            "question": "Question text",
                            "why_asked": "Why interviewer asks this",
                            "ideal_answer": "What the ideal answer should contain",
                            "difficulty": "Easy/Medium/Hard"
                        }}
                    ],
                    "behavioral_questions": [
                        {{
                            "question": "Question text",
                            "why_asked": "Why interviewer asks this",
                            "ideal_answer": "What the ideal answer should contain",
                            "difficulty": "Easy/Medium/Hard"
                        }}
                    ],
                    "hr_questions": [
                        {{
                            "question": "Question text",
                            "why_asked": "Why interviewer asks this",
                            "ideal_answer": "What the ideal answer should contain",
                            "difficulty": "Easy/Medium/Hard"
                        }}
                    ],
                    "coding_questions": [
                        {{
                            "question": "Question text",
                            "why_asked": "Why interviewer asks this",
                            "ideal_answer": "What the ideal answer should contain",
                            "difficulty": "Easy/Medium/Hard"
                        }}
                    ]
                }},
                
                "recruiter_verdict": {{
                    "overall_recommendation": "Recommendation text",
                    "hire_confidence": <number 0-100>,
                    "resume_readiness": "Not Ready/Needs Work/Ready/Excellent",
                    "critical_improvements": ["improvement1", "improvement2", "improvement3"],
                    "one_line_summary": "Brief summary"
                }}
            }}
            """
            response = self._generate_content(prompt)
            
            # Extract JSON from response (handles markdown formatting)
            json_str = self._extract_json_from_response(response)
            
            # Parse JSON response with retry
            try:
                data = json.loads(json_str)
                logger.info(f"Successfully parsed JSON with keys: {list(data.keys())}")
                return AnalysisResult(success=True, data=data)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                logger.error(f"JSON string that failed: {json_str[:500]}...")
                
                # Retry once with explicit JSON instruction
                retry_prompt = prompt + "\n\nCRITICAL: Respond with RAW JSON ONLY. No markdown. No code blocks. No text before or after. Just the JSON object."
                logger.info("Retrying with explicit JSON instruction")
                retry_response = self._generate_content(retry_prompt)
                retry_json_str = self._extract_json_from_response(retry_response)
                
                try:
                    data = json.loads(retry_json_str)
                    logger.info(f"Successfully parsed JSON on retry with keys: {list(data.keys())}")
                    return AnalysisResult(success=True, data=data)
                except json.JSONDecodeError as retry_e:
                    logger.error(f"Retry JSON parsing also failed: {retry_e}")
                    # Fallback: return raw text if JSON parsing fails
                    return AnalysisResult(
                        success=False,
                        data={},
                        error=f"Failed to parse JSON response: {str(e)}. Response: {response[:200]}..."
                    )
                
        except Exception as e:
            logger.error(f"Resume analysis failed: {str(e)}")
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
            logger.info("Starting ATS score calculation")
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
            json_str = self._extract_json_from_response(response)
            data = json.loads(json_str)
            logger.info(f"Successfully parsed ATS score JSON")
            return AnalysisResult(success=True, data=data)
            
        except json.JSONDecodeError as e:
            logger.error(f"ATS score JSON parsing error: {e}")
            return AnalysisResult(success=False, data={}, error=f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"ATS score calculation failed: {str(e)}")
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
            logger.info("Starting interview question generation")
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
            json_str = self._extract_json_from_response(response)
            data = json.loads(json_str)
            logger.info(f"Successfully parsed interview questions JSON")
            return AnalysisResult(success=True, data=data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Interview questions JSON parsing error: {e}")
            return AnalysisResult(success=False, data={}, error=f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Interview question generation failed: {str(e)}")
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
            logger.info("Starting career roadmap generation")
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
            json_str = self._extract_json_from_response(response)
            data = json.loads(json_str)
            logger.info(f"Successfully parsed career roadmap JSON")
            return AnalysisResult(success=True, data=data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Career roadmap JSON parsing error: {e}")
            return AnalysisResult(success=False, data={}, error=f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Career roadmap generation failed: {str(e)}")
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
            logger.info("Starting salary prediction")
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
            json_str = self._extract_json_from_response(response)
            data = json.loads(json_str)
            logger.info(f"Successfully parsed salary prediction JSON")
            return AnalysisResult(success=True, data=data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Salary prediction JSON parsing error: {e}")
            return AnalysisResult(success=False, data={}, error=f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Salary prediction failed: {str(e)}")
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
            logger.info("Starting resume rewrite")
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
            json_str = self._extract_json_from_response(response)
            data = json.loads(json_str)
            logger.info(f"Successfully parsed resume rewrite JSON")
            return AnalysisResult(success=True, data=data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Resume rewrite JSON parsing error: {e}")
            return AnalysisResult(success=False, data={}, error=f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Resume rewrite failed: {str(e)}")
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
            logger.info("Starting certificate analysis")
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
            json_str = self._extract_json_from_response(response)
            data = json.loads(json_str)
            logger.info(f"Successfully parsed certificate analysis JSON")
            return AnalysisResult(success=True, data=data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Certificate analysis JSON parsing error: {e}")
            return AnalysisResult(success=False, data={}, error=f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Certificate analysis failed: {str(e)}")
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
            logger.info("Starting candidate comparison")
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
            json_str = self._extract_json_from_response(response)
            data = json.loads(json_str)
            logger.info(f"Successfully parsed candidate comparison JSON")
            return AnalysisResult(success=True, data=data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Candidate comparison JSON parsing error: {e}")
            return AnalysisResult(success=False, data={}, error=f"Failed to parse JSON: {str(e)}")
        except Exception as e:
            logger.error(f"Candidate comparison failed: {str(e)}")
            return AnalysisResult(success=False, data={}, error=str(e))


class TranslationService:
    """
    Service for translating AI responses between English and Hinglish.
    """
    
    def __init__(self, llm_client: BaseLLMClient):
        """
        Initialize translation service.
        
        Args:
            llm_client: LLM client instance for translation.
        """
        self.client = llm_client
    
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
