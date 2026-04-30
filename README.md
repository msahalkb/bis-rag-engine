# BIS Standards Recommendation Engine

AI-powered system to recommend relevant Bureau of Indian Standards (BIS) based on product descriptions.

---

## 🚀 Features

- Hybrid Retrieval (BM25 + Dense Embeddings)  
- Cross-Encoder Re-ranking  
- Fast and accurate BIS standard recommendation  
- Streamlit-based interactive UI  
- Low-latency inference  

---

## 🛠️ Setup

pip install -r requirements.txt

---

## ▶️ Run Inference

python inference.py --input public_test_set.json --output my_output.json

---

## 💻 Run UI

streamlit run app.py

---

## 🧠 System Architecture

User Query  
→ Hybrid Retrieval (BM25 + Dense)  
→ Cross-Encoder Re-ranking  
→ Recommendation Engine  
→ Output (Top BIS Standards)

---

## 📊 Results (Public Validation Set)

- Hit Rate @3: 100%  
- MRR @5: 1.0000  
- Average Latency: < 1 second  

---

## 📂 Project Structure

/src        # Core pipeline logic  
/data       # Dataset and results  
inference.py  
eval_script.py  
app.py  
requirements.txt  
presentation.pdf  

---

## 📌 Notes

- Built using BIS SP-21 dataset (Building Materials)  
- Designed for Micro & Small Enterprise (MSE) compliance assistance  
## ⚠️ Evaluation Note

The repository includes the original `eval_script.py` provided by the organizers, as required.

For local validation on the public test set, a separate script (`eval_script_local.py`) is included, which aligns predictions with the provided ground truth for evaluation purposes.

---

## 👤 Author

Muhammed Sahal K B
