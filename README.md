To setup:

Setup the vm
```bash
python3 -m venv .venv
. ./.venv/bin/activate

pip install -r requirements.txt
```

To run the streamlit benchmarks demo:
```bash
cd benchmark

python3 -m streamlit run streamlit_nav.py
```

To run the mesop benchmarks demo:
```bash
cd benchmark

python3 -m streamlit run mesop_benchmark.py
```

To run the streamlit AWS demo:
```bash
cd benchmark

python3 -m streamlit run streamlit_aws_dash.py
```