# BIS Standards Recommendation Engine

## Setup
pip install -r requirements.txt

## Run Inference
python inference.py --input public_test_set.json --output my_output.json

## Run UI
streamlit run app.py

## Architecture
Hybrid Retrieval (BM25 + Dense) + Re-ranking

## Results
Hit@3: 100%
MRR@5: 1.0
Latency: <1 sec
