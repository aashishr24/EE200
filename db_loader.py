#!/usr/bin/env python3
"""
Deployment helper: Auto-load song database on startup
Call this at the beginning of ss.py to load pre-built database
"""
import os
import pickle
import streamlit as st
from collections import defaultdict

DATABASE_CACHE = "song_database.pkl"
SONGS_DIR = "songs_wav"

@st.cache_resource
def load_or_build_database():
    """Load pre-built database or build from scratch"""
    
    # Try to load from cache
    if os.path.exists(DATABASE_CACHE):
        try:
            with open(DATABASE_CACHE, 'rb') as f:
                database = pickle.load(f)
            st.sidebar.success(f"📦 Loaded pre-indexed database ({len(database)} songs)")
            return database
        except Exception as e:
            st.sidebar.warning(f"Could not load cache: {e}")
    
    # Build from scratch if needed
    from project import MusicFingerprinter
    
    fingerprinter = MusicFingerprinter()
    database = {}
    
    if not os.path.exists(SONGS_DIR):
        st.error(f"Songs directory '{SONGS_DIR}' not found. Please add WAV files.")
        return {}
    
    wav_files = [f for f in os.listdir(SONGS_DIR) if f.endswith('.wav')]
    
    if not wav_files:
        st.warning(f"No WAV files found in '{SONGS_DIR}'")
        return {}
    
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    for idx, filename in enumerate(wav_files):
        filepath = os.path.join(SONGS_DIR, filename)
        song_name = os.path.splitext(filename)[0]
        
        try:
            audio, sr = fingerprinter.load_audio(filepath)
            frequencies, times, magnitude = fingerprinter.compute_spectrogram(audio, sr)
            peaks = fingerprinter.find_peaks(magnitude, frequencies, threshold_db=10)
            fingerprints = fingerprinter.create_fingerprint_pairs(peaks, frequencies, times)
            
            database[song_name] = defaultdict(list)
            for fp in fingerprints:
                fp_hash = hash(fp) % (10 ** 9)
                database[song_name][fp_hash].append(0)
            
            database[song_name] = dict(database[song_name])
            
        except Exception as e:
            st.sidebar.warning(f"Error processing {song_name}: {e}")
        
        progress = (idx + 1) / len(wav_files)
        progress_bar.progress(progress)
        status_text.text(f"Indexing: {idx+1}/{len(wav_files)}")
    
    progress_bar.empty()
    status_text.empty()
    
    # Save cache for next run
    try:
        with open(DATABASE_CACHE, 'wb') as f:
            pickle.dump(database, f)
    except Exception as e:
        st.sidebar.warning(f"Could not save cache: {e}")
    
    if database:
        st.sidebar.success(f"📦 Built database ({len(database)} songs)")
    
    return database
