# --- 2. SCRIPT TO BE USED IN STREAMLIT APP (vidhik_engine.py) ---
import faiss
import pickle
import os

FAISS_INDEX_PATH = "data/vidhik_legal_db.faiss"
FAISS_METADATA_PATH = "data/vidhik_legal_db_metadata.pkl"

# Global variables to store the loaded index and metadata
loaded_index = None
loaded_metadata = None

def load_faiss_artifacts():
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
            # This handles cases where the files were not pushed to GitHub (correctly gitignored)
            print(f"CRITICAL ERROR: FAISS files not found at {FAISS_INDEX_PATH} and {FAISS_METADATA_PATH}. Cannot run live conflict detection.")
            return None, None
        except Exception as e:
            print(f"Error loading FAISS artifacts: {e}")
            return None, None
    else:
        return loaded_index, loaded_metadata
        
# Example of how you would use it in your engine's logic:
# index, metadata = load_faiss_artifacts()
# if index is not None:
#     # ... proceed to vectorize the new clause and search the index ...
