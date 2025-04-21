import logging
import os
import tempfile
import time

def setup_logging(level=logging.INFO, 
                 *,
                 sub_folder: str = 'agents_log', 
                 log_file_prefix: str = 'agent', 
                 log_file_timestamp: str = time.strftime('%Y%m%d_%H%M%S')):
    """
    Set up logging with standardized format and location
    
    Args:
        level: Logging level (default: INFO)
        sub_folder: Subfolder in the temp directory to store logs
        log_file_prefix: Prefix for the log file name
        log_file_timestamp: Timestamp for the log file name
        
    Returns:
        str: Path to the log file
    """
    log_dir = os.path.join(tempfile.gettempdir(), sub_folder)
    log_filename = f'{log_file_prefix}.{log_file_timestamp}.log'
    log_filepath = os.path.join(log_dir, log_filename)

    os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(log_filepath, mode='w')
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = []  # Clear handles to disable logging to stderr
    root_logger.addHandler(file_handler)

    print(f'Log setup complete: {log_filepath}')

    latest_log_link = os.path.join(log_dir, f'{log_file_prefix}.latest.log')
    if os.path.islink(latest_log_link):
        os.unlink(latest_log_link)
    os.symlink(log_filepath, latest_log_link)

    print(f'To access latest log: tail -F {latest_log_link}')
    return log_filepath