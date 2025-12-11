import os
import dlt
from gmail_source import fetch_emails

def gmail_source(max_emails=100):
    df = fetch_emails(max_emails)
    for row in df.to_dict(orient="records"):
        yield row

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(
    '..', 'credentials', 'service_account.json'
)

pipeline = dlt.pipeline(
    pipeline_name="gmail_to_bigquery",
    destination="bigquery",
    dataset_name="gmail_dataset"
)

if __name__ == "__main__":
    info = pipeline.run(gmail_source(60))
    print("Pipeline info:", info)