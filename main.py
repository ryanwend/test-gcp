#%%
from doh_tools.custom_logging import set_logging, send_log_over_email
import os
import pandas as pd
from datetime import datetime


#%% Set up Logging
log_email = 'ryan.wendling@state.co.us' #os.environ['gmail_user']
task_name = 'Testing Google Cloud Function'
email_flag = 'LogLabel15'

subject_success = f'Success -- {task_name} Ran -- {email_flag}'
subject_error   = f'Error -- {task_name} Failed -- {email_flag}'

logger = set_logging(log_console=False, log_email=True)


try:
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
    file_name = today + "-test.parquet"

    # Not sure how to get this to bucket, assume we'll go over that then can uncomment
    # df.to_parquet(file_name)
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
