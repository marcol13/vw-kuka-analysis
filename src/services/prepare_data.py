import threading

from ..models.connection import Connection
from ..models.recording import Recording
from ..models.file import DataFile

from concurrent.futures import ThreadPoolExecutor, as_completed
from collections.abc import Callable

def download_file(key: str, failed_files: list[str], func: Callable, con: Connection):
    try:
        func(key, con)
        print(f'Successfully downloaded {key}')
    except Exception as e:
        print(f'Failed to download {key}: {str(e)}')
        failed_files.append(key)

def download_with_timeout(key: str, timeout: int, failed_files: list[str], func: Callable, con: Connection):
    thread = threading.Thread(target=download_file, args=(key, failed_files, func, con))
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        failed_files.append(key)
        print(f'Timeout reached for {key}')
        thread.join()

def download_files(rec_list: list[str], func: Callable, con: Connection, timeout: int=180):
    failed_files = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_with_timeout, key, timeout, failed_files, func, con) for key in rec_list]
        for future in as_completed(futures):
            future.result()
    return failed_files

def save_data(key: str, con: Connection):
    name = key.replace('processinfo/', '').replace('/', '_').replace('.json', '')
    
    data = con.get_record(key)
    final_data = Recording.preprocess(data, name)

    file = DataFile(name)
    file.write(data, 'raw_data')
    file.write(final_data, 'data')


def prepare_data():
    con = Connection('credentials.json')
    recording_list = con.get_records_list()

    failed_files = download_files(recording_list, save_data, con, 180)
    print(f'Failed to download {len(failed_files)} files: {failed_files}')