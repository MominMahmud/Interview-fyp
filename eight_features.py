from pydub import AudioSegment
from pydub import silence as si
import numpy as np
import speech_recognition as sr
from textblob import TextBlob


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0  # ms

    assert chunk_size > 0  # to avoid infinite loopp
    while sound[
        trim_ms : trim_ms + chunk_size
    ].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def audio_text_anlysis(address):
    sound = AudioSegment.from_file("Audios//test2.wav", format="wav")

    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)
    myaudio = sound[start_trim : duration - end_trim]
    silence = si.detect_silence(myaudio, min_silence_len=1000, silence_thresh=-40)

    silence = [
        ((start / 1000), (stop / 1000)) for start, stop in silence
    ]  # convert to sec

    print(silence)
    gaps = []
    for gap in silence:
        gaps.append(gap[1] - gap[0])
    total_silence_duration = sum(gaps)
    total_speach_duration = sound.duration_seconds - total_silence_duration
    speech_to_silence_ratio = total_speach_duration / total_silence_duration
    audio_length_in_minutes = sound.duration_seconds / 60

    # print("Speech-to-silence ratio:", speech_to_silence_ratio)
    avg_silence_duration = np.mean(gaps)
    # print("Average_silence duration:",avg_silence_duration)
    Avg_silence_dur_per_minute = total_silence_duration / audio_length_in_minutes
    # print("Average_silence duration per minute :",Avg_silence_dur_per_minute)
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile("Audios//test2.wav") as source:
        audio_data = recognizer.record(source)

    # Convert speech to text
    text = recognizer.recognize_google(audio_data, language="en-US")
    speaker_text = text
    blob = TextBlob(text)
    words = text.split()
    unique_words = set(words)
    num_unique_words = len(unique_words)
    blob = TextBlob(text)

    polarity = blob.sentiment.polarity
    # subjectivity = blob.sentiment.subjectivity
    sentiment = ""
    if polarity > 0:
        sentiment = "Positive"
    elif polarity == 0:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"
    # print("Number of unique words:", num_unique_words)
    unique_words_to_total_no_of_words_ratio = num_unique_words / len(words)
    # print("unque words to total number of words ratio:",unique_words_to_total_no_of_words_ratio)
    rate_of_words_per_minute = len(words) / audio_length_in_minutes
    # print("rate of words per minute:",rate_of_words_per_minute)
    return (
        speaker_text,
        silence,
        speech_to_silence_ratio,
        avg_silence_duration,
        Avg_silence_dur_per_minute,
        num_unique_words,
        unique_words_to_total_no_of_words_ratio,
        rate_of_words_per_minute,
        sentiment,
    )
