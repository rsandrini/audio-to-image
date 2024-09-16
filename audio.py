import multiprocessing

from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pydub.silence import split_on_silence
from utils import check_folder, save_text, split_long_lines, increment_file_text
import speech_recognition as sr


def transcribe_audio(start_time, path, language="en-US"):
    # create a speech recognition object
    r = sr.Recognizer()

    # use the audio file as the audio source
    try:
        with sr.AudioFile(path) as source:
            audio_listened = r.record(source)
            # try converting it to text
            text = r.recognize_google(audio_listened, language=language).capitalize() + ". "
            return start_time, text
    except Exception as e:
        if str(e):
            print(f"chunk_filename: {path}  | Error: {str(e)}")
        return start_time, ""


# Function to process each audio chunk
def process_chunk(chunk, start_time, min_silence_len=500, keep_silence=500):
    segments = split_on_silence(chunk, min_silence_len=min_silence_len,
                                silence_thresh=chunk.dBFS-14, keep_silence=keep_silence)

    # Initialize a variable to keep track of the accumulated duration
    accumulated_duration = 0

    # List to store segments with their start time
    timed_segments = []

    for segment in segments:
        # Calculate the start time for the current segment
        segment_start_time = start_time + accumulated_duration

        # Add the segment and its start time to the list
        timed_segments.append((segment, segment_start_time))

        # Update the accumulated duration
        accumulated_duration += len(segment) / 1000.0  # Assuming len(segment) gives duration in milliseconds

    return timed_segments


# a function that splits the audio file into chunks on silence
# and applies speech recognition
def get_large_audio_transcription_on_silence(file, project_name, min_silence_len=500, keep_silence=100, chunk_length_ms=120000):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""

    # Load your audio file
    audio = AudioSegment.from_file(file)

    if int(chunk_length_ms) < 1000:
        chunk_length_ms = len(audio)

    # Split the audio into chunks for each thread
    chunks = [(audio[i:i + int(chunk_length_ms)], i/1000, int(min_silence_len), int(keep_silence)) for i in range(0, len(audio), int(chunk_length_ms))]

    print(f"Split original audio into {len(chunks)} chunks ...")

    cpu_cores = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=cpu_cores) as pool:
        results = pool.starmap(process_chunk, chunks)

    # Flatten and sort the results
    processed_chunks = [item for sublist in results for item in sublist]
    processed_chunks.sort(key=lambda x: x[1])

    # create a directory to store the audio chunks
    folder_name = check_folder(project_name)

    # Save each segment to a file
    chunks_processed = []
    for idx, (segment, start_time) in enumerate(processed_chunks):
        file_name = f"{folder_name}/chunk_{idx}_{start_time}.wav"
        segment.export(file_name, format="wav")
        chunks_processed.append([start_time, file_name])

    return chunks_processed


def audio_to_text(project_name, chunks, language="en-US"):
    print(f"Extracting text... Using language: {language}")

    # Determine the number of processes to use
    num_processes = min(len(chunks), multiprocessing.cpu_count()*10)
    print(f"Using {num_processes} processes to extract text from {len(chunks)} chunks...")
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Package the chunk and language into a tuple
        chunk_language_pairs = [(start_time, chunk, language) for start_time, chunk in chunks]

        # Use starmap to pass multiple arguments
        results = pool.starmap(transcribe_audio, chunk_language_pairs)

    # Sort results based on the index
    sorted_results = sorted(results, key=lambda x: x[0])

    # Concatenate the sorted results
    whole_text = ' \n'.join([f"{result[0]}:{result[1]}" if result[1] else "" for result in sorted_results])
    #remove empty lines in the file
    whole_text = "\n".join([s for s in whole_text.splitlines() if s.strip()])

    print("Checking and fixing long lines")
    # Check and fix long lines before process the GPT
    whole_text = split_long_lines(whole_text)

    save_text(whole_text, project_name, "text.txt")

    # Return the text for all chunks detected
    return whole_text


def increment_file(project_name, image_prompts, file_name):
    for img_ppt in image_prompts:
        new_line = f"{img_ppt['secs']}:{img_ppt['image_prompt']}"
        increment_file_text(project_name=project_name, content=new_line, file_name=file_name)
