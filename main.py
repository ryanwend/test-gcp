#%%
from doh_tools.custom_logging import set_logging, send_log_over_email
import pandas as pd
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.cloud import storage
import os
import io


#%% Set up Logging
log_email = 'ryan.wendling@state.co.us'
task_name = 'Testing Google Cloud Function'
email_flag = 'LogLabel15'

subject_success = f'Success -- {task_name} Ran -- {email_flag}'
subject_error   = f'Error -- {task_name} Failed -- {email_flag}'

logger = set_logging(log_console=False, log_email=True)


try:
    # Read token data from token.json
    logger.info(f'Reading in token.json elements to reconstruct json')
    # Read environment variables
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    refresh_token = os.environ.get("REFRESH_TOKEN")
    token_uri = os.environ.get("TOKEN_URI")
    token_expiry = os.environ.get("TOKEN_EXPIRY")

    # Construct JSON object
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "token_uri": token_uri,
        "token_expiry": token_expiry
    }

    # Create OAuth 2.0 credentials object using token data
    credentials = Credentials.from_authorized_user_info(token_data)

    # Create a GCS client using the credentials
    storage_client = storage.Client(credentials=credentials)

    # Create DataFrame
    today = datetime.today().strftime('%Y-%m-%d')
    data = {
        'Date': [today],
        'Column1': [1],
        'Column2': [2],
        'Column3': [3],
        'Column4': [4],
        'Column5': [5]
    }
    df = pd.DataFrame(data)
    logger.info(f'Created {today} df with {len(df)} rows')

    # Save DataFrame as Parquet file
    file_name = 'test-parquets/' + today + "-test.parquet"

    # Define your bucket name and file name
    bucket_name = 'rw_test_devops_pipeline_gcp'

    # Write the DataFrame to a Parquet file in memory
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer)

    # Upload the Parquet file to the bucket
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    parquet_buffer.seek(0)
    blob.upload_from_file(parquet_buffer, content_type='application/octet-stream')

    logger.info(f'Saved df as parquet to bucket')

    send_log_over_email(
            logger,
            fromaddr=log_email,
            toaddr=log_email,
            subject=subject_success
        )

except Exception as e:
    logger.info(f'Process failed with error: {e}')
    send_log_over_email(
        logger,
        fromaddr=log_email,
        toaddr=log_email,
        subject=subject_error
    )

# %%
