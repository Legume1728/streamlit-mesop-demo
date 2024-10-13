# Setup
To setup:

Setup the vm
```bash
python3 -m venv .venv
. ./.venv/bin/activate

pip install -r requirements.txt
```

## Streamlit Benchmarks Demo
To run the streamlit benchmarks demo:
```bash
cd benchmark

python3 -m streamlit run streamlit_nav.py
```

## Mesop Benchmarks Demo
To run the mesop benchmarks demo:
```bash
cd benchmark

python3 -m streamlit run mesop_benchmark.py
```

## Streamlit AWS Demo
First you need to have AWS configured locally with your credentials.
To do this, first download the AWS CLI: https://aws.amazon.com/cli/

Now configure your credentials locally (in ~/.aws/config and ~/.aws/credentials):
```bash
aws configure
```

To run the streamlit AWS demo:
```bash
cd benchmark

python3 -m streamlit run streamlit_aws_dash.py
```