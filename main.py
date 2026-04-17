#!/usr/bin/env python3
import os
import streamlit as st
import asyncio
import tempfile
from pathlib import Path
from poi import import_attractions
from models import call_GPT_stream, call_TTS
from openai import AsyncOpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))


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
    output_path = tmp_dir / "attraction.wav"

    # Reset file
    if output_path.exists():
        output_path.unlink()

    total_bytes = 0
    chunk_count = 0

    status.info("Generating audio...")

    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
    #st.session_state.last_audio_path = str(output_path)

    # Final render
    with open(output_path, "rb") as audio_file:
        final_audio = audio_file.read()
    audio_slot.audio(final_audio, format="audio/wav")



if __name__ == "__main__":

    st.set_page_config(page_title="Barcelona Attractions", page_icon=":ferris_wheel:")

    st.title("Barcelona Tourist Attractions")
    st.header("Generate text and audio content for Barcelona's top tourist attractions")

    attractions = import_attractions()
    
    attraction_names = [attraction["nice_name"] for attraction in attractions]
    
    #selected_attraction = st.radio("Select an attraction:", attraction_names)
    selected_attraction = st.pills("Select an attraction:", attraction_names, selection_mode="single")

    #st.write(f"You selected: {selected_attraction}")

    generate = st.button("Generate content", type="primary")

    if generate:
        model = "gpt-4o-mini"
        prompt = "You are a local travel guide based in Barcelona. Please provide an extensive description of the tourist attraction called " + selected_attraction + ". Include information about its history, architecture, and any interesting facts. Also, describe location, opening hours, the best time to visit and any nearby attractions or food options worth exploring. This content will help you plan your visit but also to guide you through the experience when you are there. Please provide the information in a friendly and engaging tone, as if you were sharing it with a friend who is visiting Barcelona for the first time."
        #res = call_GPT(model, prompt)
        result = st.write_stream(call_GPT_stream(model, prompt))
        asyncio.run(generate_tts_progressively(result, "fable"))
        #call_TTS("gpt-4o-mini-tts",result)
        #st.audio("attraction.mp3")
        
    
    