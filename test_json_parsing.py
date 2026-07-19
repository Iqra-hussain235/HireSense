"""
Test script to verify JSON extraction from markdown-formatted responses.
"""

import re

def _extract_json_from_response(response: str) -> str:
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
        print(f"✓ Extracted JSON from markdown code block")
        return matches[0].strip()
    
    # Try to find JSON object without markdown
    # Look for content between first { and last }
    brace_start = response.find('{')
    brace_end = response.rfind('}')
    
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        json_content = response[brace_start:brace_end + 1]
        print(f"✓ Extracted JSON from brace positions")
        return json_content.strip()
    
    # If no JSON found, return original response
    print(f"⚠ No JSON found in response, returning original")
    return response


# Test cases
test_cases = [
    # Case 1: Markdown with json tag
    """Here is your analysis:

```json
{
    "overall_score": 85,
    "ats_score": 90,
    "grammar_score": 88,
    "communication_score": 92
}
```

Hope this helps!""",
    
    # Case 2: Markdown without json tag
    """Analysis result:

```
{
    "overall_score": 75,
    "ats_score": 80,
    "grammar_score": 85,
    "communication_score": 78
}
```

End of analysis.""",
    
    # Case 3: No markdown, just JSON
    """{
    "overall_score": 90,
    "ats_score": 95,
    "grammar_score": 88,
    "communication_score": 91
}""",
    
    # Case 4: Text before and after JSON without markdown
    """Here is the result: {"overall_score": 80, "ats_score": 85, "grammar_score": 82, "communication_score": 88} Thanks!""",
]

print("Testing JSON extraction logic:\n")
for i, test in enumerate(test_cases, 1):
    print(f"Test Case {i}:")
    extracted = _extract_json_from_response(test)
    print(f"Extracted: {extracted[:100]}...")
    print()
