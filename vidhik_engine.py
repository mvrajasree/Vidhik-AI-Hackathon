# --- vidhik_engine.py (Complete Implementation) ---
import faiss
import pickle
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# --- EMBEDDING MODEL INITIALIZATION ---
# Initialize the embedding model globally
model = SentenceTransformer('all-MiniLM-L6-v2')

# --- PATH CONFIGURATION ---
# Note: Paths are set relative to the root directory where the app is executed
FAISS_INDEX_PATH = "data/vidhik_legal_db.faiss"
FAISS_METADATA_PATH = "data/vidhik_legal_db_metadata.pkl"

# Global variables to store the loaded index and metadata
loaded_index = None
loaded_metadata = None

def load_faiss_artifacts():
    """
    Loads the FAISS index and associated metadata (text chunks) from disk.
    Uses global variables to ensure artifacts are only loaded once.
    """
    global loaded_index
    global loaded_metadata
    
    if loaded_index is None:
        try:
            # Load the binary FAISS index
            loaded_index = faiss.read_index(FAISS_INDEX_PATH)
            
            # Load the corresponding metadata (document IDs/text)
            with open(FAISS_METADATA_PATH, 'rb') as f:
                loaded_metadata = pickle.load(f)
                
            print("Vidhik AI FAISS database loaded successfully.")
            return loaded_index, loaded_metadata
            
        except FileNotFoundError:
            # Handles missing files, which causes a Streamlit error if not handled
            print(f"CRITICAL ERROR: FAISS files not found at {FAISS_INDEX_PATH} and {FAISS_METADATA_PATH}. Cannot run live conflict detection.")
            return None, None
        except Exception as e:
            print(f"Error loading FAISS artifacts: {e}")
            return None, None
    else:
        # Return already loaded objects
        return loaded_index, loaded_metadata

def detect_bias_phrases(text):
    """
    Detect potentially biased language in the policy text.
    
    Args:
        text (str): Policy text to analyze for bias
        
    Returns:
        list: List of flagged phrases with their bias categories
    """
    # Bias lexicon - expand this based on your requirements
    bias_lexicons = {
        "Gender Bias": [
            "he should", "she should", "the common man", "mankind", 
            "manpower", "businessman", "waitress", "stewardess"
        ],
        "Ability Bias": [
            "handicapped", "crippled", "retarded", "lame", "insane",
            "wheelchair bound", "suffers from", "victim of"
        ],
        "Age Bias": [
            "young people", "old people", "the elderly", "senile",
            "too old to", "digital native", "millennial"
        ],
        "Racial/Cultural Bias": [
            "exotic", "oriental", "articulate", "urban", "ghetto",
            "tribal knowledge", "spirit animal"
        ]
    }
    
    flagged_phrases = []
    text_lower = text.lower()
    
    for category, phrases in bias_lexicons.items():
        for phrase in phrases:
            if phrase.lower() in text_lower:
                flagged_phrases.append({
                    "phrase": phrase,
                    "lexicon": category,
                    "recommendation": f"Consider replacing '{phrase}' with more inclusive language"
                })
    
    return flagged_phrases

def detect_pii(text):
    """
    Detect potential Personally Identifiable Information (PII) in the policy text.
    
    Args:
        text (str): Policy text to analyze for PII
        
    Returns:
        dict: PII detection results
    """
    # Simple PII patterns - expand with regex for more sophisticated detection
    pii_patterns = {
        "Email Address": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "Phone Number": r'\b(\+?91[\-\s]?)?[789]\d{9}\b',  # Indian phone numbers
        "Aadhaar Number": r'\b[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}\b',
        "PAN Number": r'[A-Z]{5}[0-9]{4}[A-Z]{1}',
        "Credit Card": r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
    }
    
    import re
    detected_pii = []
    
    for pii_type, pattern in pii_patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            detected_pii.extend([{"type": pii_type, "value": match} for match in matches])
    
    return {
        "pii_found": len(detected_pii) > 0,
        "detected_items": detected_pii,
        "status": "PII Found" if detected_pii else "Clean"
    }

def analyze_policy(new_policy_text, similarity_threshold=0.3):
    """
    Core function for policy analysis. This function:
    1. Loads the FAISS database (via load_faiss_artifacts).
    2. Embeds the new_policy_text.
    3. Searches the FAISS index for conflicts (high similarity).
    4. Compiles the comprehensive audit report (legal, ethical, PII).

    Args:
        new_policy_text (str): The text of the policy/clause to analyze.
        similarity_threshold (float): Threshold for considering matches as conflicts (lower = more strict)
        
    Returns:
        dict: A comprehensive audit report in JSON format.
    """
    # Load FAISS artifacts
    index, metadata = load_faiss_artifacts()
    
    if index is None or metadata is None:
        # Return a failure report if the database is missing
        return {
            "Actionable Recommendations": "### Recommendations for Legal Conflicts\n- **Database Error:** The legal database failed to load. Please ensure `vidhik_legal_db.faiss` and `vidhik_legal_db_metadata.pkl` are correctly pushed to the `data/` directory using Git LFS.",
            "Raw Reports": {
                "Conflict Report": {"Status": "Failed", "Conflicting Laws": []},
                "Bias Report": {"Status": "Not Run", "flagged_phrases": []},
                "PII Report": {"Status": "Not Run", "pii_found": False, "detected_items": []}
            }
        }
    
    # 1. Embed the policy text
    try:
        new_embedding = model.encode([new_policy_text])
        new_embedding = np.array(new_embedding).astype('float32')
    except Exception as e:
        return {
            "Actionable Recommendations": f"### Embedding Error\n- Failed to encode policy text: {str(e)}",
            "Raw Reports": {
                "Conflict Report": {"Status": "Failed", "Conflicting Laws": []},
                "Bias Report": {"Status": "Not Run", "flagged_phrases": []},
                "PII Report": {"Status": "Not Run", "pii_found": False, "detected_items": []}
            }
        }
    
    # 2. Search FAISS for similar legal provisions
    try:
        k = 5  # Number of similar documents to retrieve
        D, I = index.search(new_embedding, k)
        
        conflicting_laws = []
        for i, (distance, idx) in enumerate(zip(D[0], I[0])):
            # Convert cosine similarity distance to similarity score (assuming cosine similarity)
            similarity_score = 1 - distance if distance <= 2 else 0  # Simple conversion for cosine distance
            
            if similarity_score > similarity_threshold and idx < len(metadata):
                law_text = metadata[idx]
                conflicting_laws.append({
                    "Rank": i + 1,
                    "Similarity Score": f"{similarity_score:.3f}",
                    "Legal Provision": law_text,
                    "Risk Level": "HIGH" if similarity_score > 0.7 else "MEDIUM" if similarity_score > 0.5 else "LOW"
                })
    except Exception as e:
        conflicting_laws = []
        print(f"Error during FAISS search: {e}")
    
    # 3. Run bias detection
    try:
        bias_results = detect_bias_phrases(new_policy_text)
    except Exception as e:
        bias_results = []
        print(f"Error during bias detection: {e}")
    
    # 4. Run PII detection
    try:
        pii_results = detect_pii(new_policy_text)
    except Exception as e:
        pii_results = {"pii_found": False, "detected_items": [], "status": "Error"}
        print(f"Error during PII detection: {e}")
    
    # 5. Generate actionable recommendations
    recommendations = generate_recommendations(conflicting_laws, bias_results, pii_results)
    
    # 6. Compile final report
    report = {
        "Actionable Recommendations": recommendations,
        "Raw Reports": {
            "Conflict Report": {
                "Status": "Success" if index is not None else "Failed",
                "Similarity Threshold Used": similarity_threshold,
                "Conflicting Laws": conflicting_laws
            },
            "Bias Report": {
                "Status": "Success",
                "flagged_phrases": bias_results
            },
            "PII Report": pii_results
        }
    }
    
    return report

def generate_recommendations(conflicting_laws, bias_phrases, pii_results):
    """
    Generate actionable recommendations based on analysis results.
    
    Args:
        conflicting_laws (list): List of conflicting legal provisions
        bias_phrases (list): List of flagged biased phrases
        pii_results (dict): PII detection results
        
    Returns:
        str: Formatted recommendations string
    """
    recommendations = []
    
    # Legal conflict recommendations
    if conflicting_laws:
        recommendations.append("### ⚖️ Recommendations for Legal Conflicts")
        high_risk = [law for law in conflicting_laws if law["Risk Level"] == "HIGH"]
        medium_risk = [law for law in conflicting_laws if law["Risk Level"] == "MEDIUM"]
        
        if high_risk:
            recommendations.append("- **HIGH RISK CONFLICTS DETECTED**: Immediate review required")
            for law in high_risk[:2]:  # Show top 2 high-risk conflicts
                recommendations.append(f"  - Conflict with similarity {law['Similarity Score']}: {law['Legal Provision'][:100]}...")
        
        if medium_risk:
            recommendations.append("- **Medium risk conflicts found**: Consider reviewing")
            for law in medium_risk[:2]:  # Show top 2 medium-risk conflicts
                recommendations.append(f"  - Potential conflict: {law['Legal Provision'][:80]}...")
        
        recommendations.append(f"\n**Total conflicts found**: {len(conflicting_laws)}")
    else:
        recommendations.append("### ✅ Legal Conflict Analysis")
        recommendations.append("- No significant legal conflicts detected at the current threshold")
    
    # Bias recommendations
    if bias_phrases:
        recommendations.append("\n### 🌍 Recommendations for Inclusive Language")
        unique_categories = set(phrase["lexicon"] for phrase in bias_phrases)
        for category in unique_categories:
            category_phrases = [p for p in bias_phrases if p["lexicon"] == category]
            recommendations.append(f"- **{category}**: {len(category_phrases)} instances found")
            for phrase in category_phrases[:2]:  # Show first 2 examples per category
                recommendations.append(f"  - Replace '{phrase['phrase']}' with more inclusive alternative")
    else:
        recommendations.append("\n### ✅ Bias Analysis")
        recommendations.append("- No biased language detected")
    
    # PII recommendations
    if pii_results["pii_found"]:
        recommendations.append("\n### 🔒 Recommendations for PII Risk")
        recommendations.append("- **PERSONALLY IDENTIFIABLE INFORMATION DETECTED**: Immediate redaction required")
        for pii_item in pii_results["detected_items"][:3]:  # Show first 3 PII items
            recommendations.append(f"  - {pii_item['type']}: {pii_item['value']}")
    else:
        recommendations.append("\n### ✅ PII Analysis")
        recommendations.append("- No Personally Identifiable Information detected")
    
    return "\n".join(recommendations)

# Example usage and test
if __name__ == "__main__":
    # Test the function with sample policy text
    sample_policy = """
    Our company policy states that all employees must provide their personal email addresses 
    and phone numbers for emergency contacts. The common man should understand that we 
    may store Aadhaar numbers for verification purposes. He should also provide his 
    PAN card details for tax purposes.
    """
    
    print("Testing Vidhik AI Engine...")
    result = analyze_policy(sample_policy)
    print("\n" + "="*50)
    print("ANALYSIS RESULTS:")
    print("="*50)
    print(result["Actionable Recommendations"])
    print("\nRaw Reports available in result['Raw Reports']")
