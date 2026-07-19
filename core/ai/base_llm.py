"""
Base LLM Interface
Abstract base class for all LLM providers to ensure consistent interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    """Data class for AI analysis results."""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients.
    All LLM providers must implement these methods.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for the LLM provider.
            model: Model name to use.
        """
        self.api_key = api_key
        self.model = model
        self.temperature = 0.7
        self.max_tokens = 4096
    
    @abstractmethod
    def _generate_content(self, prompt: str) -> str:
        """
        Generate content using the LLM.
        
        Args:
            prompt: The prompt to send to the model.
            
        Returns:
            Generated text response.
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass
    
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
