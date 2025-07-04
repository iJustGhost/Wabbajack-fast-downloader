import webbrowser
import time
import os

download_path = ""

def read_links_in_batches(file_path, batch_size):
    """Read links from a text file in batches and yield each batch."""
    try:
        with open(file_path, 'r') as file:
            batch = []
            for line in file:
                batch.append(line.strip())
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

def count_lines(file_path):
    """Count the total number of lines in the file."""
    try:
        with open(file_path, 'r') as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return 0
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return 0

def open_links_in_batches(file_path, batch_size):
    """Open links in batches and wait for user input before proceeding to the next batch."""
    total_lines = count_lines(file_path)
    if total_lines == 0:
        return

    total_batches = (total_lines + batch_size - 1) // batch_size  # Calculate total number of batches
    current_batch = 1

    for batch_links in read_links_in_batches(file_path, batch_size):
        print(f"Opening batch {current_batch} of {total_batches}...")
        for link in batch_links:
            webbrowser.open(link)
        time.sleep(15) # Delay and wait to receive downloads
        while True: # Check if there is still .aria2 (currently) downloading files
            currently_downloading = []
            for current_file in os.listdir(download_path):
                if current_file.endswith(".aria2"):
                    currently_downloading.append(current_file)
            if len(currently_downloading) == 0: # Break when every files are done downloading
                break
        current_batch += 1

def main():
    file_path = 'output.txt'
    batch_size = 3
    open_links_in_batches(file_path, batch_size)

if __name__ == "__main__":
    main()
