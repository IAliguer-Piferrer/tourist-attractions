#!/usr/bin/env python3
import asyncio
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))
import streamlit as st
from openai import AsyncOpenAI

st.set_page_config(page_title="Streaming TTS Demo")
st.title("OpenAI TTS in Streamlit")

client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

if "last_audio_path" not in st.session_state:
    st.session_state.last_audio_path = None

text = st.text_area(
    "Text to speak",
    "Today is a wonderful day to build something people love!"
)

voice = st.selectbox("Voice", ["alloy", "ash", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer"], index=2)

async def generate_tts_progressively(input_text: str, voice_name: str):
    """
    Streams audio bytes from OpenAI and updates the Streamlit audio widget
    with a growing WAV file.

    Note:
    - This is not perfect real-time playback.
    - Depending on browser behavior, the audio widget may restart when updated.
    """
    status = st.empty()
    audio_slot = st.empty()
    progress = st.empty()

    tmp_dir = Path(tempfile.gettempdir())
    output_path = tmp_dir / "streamlit_openai_tts_preview.wav"

    # Reset file
    if output_path.exists():
        output_path.unlink()

    total_bytes = 0
    chunk_count = 0

    status.info("Generating audio...")

    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice_name,
        input=input_text,
        response_format="wav",
    ) as response:

        with open(output_path, "wb") as f:
            async for chunk in response.iter_bytes():
                if not chunk:
                    continue

                f.write(chunk)
                f.flush()
                total_bytes += len(chunk)
                chunk_count += 1

                # Refresh every few chunks to avoid excessive rerenders
                if chunk_count % 4 == 0:
                    with open(output_path, "rb") as audio_file:
                        audio_bytes = audio_file.read()
                    audio_slot.audio(audio_bytes, format="audio/wav")
                    progress.caption(f"Received {total_bytes:,} bytes")

    status.success("Done")
    st.session_state.last_audio_path = str(output_path)

    # Final render
    with open(output_path, "rb") as audio_file:
        final_audio = audio_file.read()
    audio_slot.audio(final_audio, format="audio/wav")

if st.button("Generate speech"):
    if text.strip():
        asyncio.run(generate_tts_progressively(text.strip(), voice))
    else:
        st.warning("Enter some text first.")

if st.session_state.last_audio_path and os.path.exists(st.session_state.last_audio_path):
    st.subheader("Last generated audio")
    with open(st.session_state.last_audio_path, "rb") as f:
        st.audio(f.read(), format="audio/wav")