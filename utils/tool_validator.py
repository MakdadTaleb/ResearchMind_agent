def validate_tool_output(result: str) -> str:
    
    # --- Step 1: Empty or error check ---
    if not result or len(result.strip()) < 10:
        return ""
    
    if result.startswith("Error:"):
        return ""
    
    # --- Step 2: Suspicious content check ---
    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all instructions", 
        "you are now",
        "act as",
        "forget your instructions",
        "new instructions",
        "disregard",
        "jailbreak"
    ] 
    
    result_lower = result.lower()
    for pattern in suspicious_patterns:
        if pattern in result_lower:
            return ""
    
    # --- Step 3: URL basic check ---
    
    lines = result.split("\n")
    cleaned_lines = []
    for line in lines:
        if "URL:" in line:
            url = line.strip().replace("URL:", "").strip()
            if url and not url.startswith("http"):
                line = ""
        cleaned_lines.append(line)
    
    return "\n".join(cleaned_lines)