# Q3 Submission Guide

## Overview
This submission contains:
- **Q3(A)**: Music fingerprinting algorithm with analysis and visualizations
- **Q3(B)**: Interactive Streamlit application (deployed + source code)

---

## Q3(A): Report Requirements

### Included Visualizations
The generated `Q3A_*.png` files demonstrate:

1. **Q3A_spectrograms.png** - Spectral analysis
   - Two songs ("Hey Jude" and "Yesterday")
   - FFT size: 4096 samples
   - Shows frequency-time representation

2. **Q3A_constellation.png** - Peak detection
   - Red X marks show detected spectral peaks
   - ~400 peaks detected per 30-second segment
   - Demonstrates fingerprinting foundation

3. **Q3A_analysis_metrics.png** - Comprehensive analysis
   - Frame energy over time
   - Average frequency content
   - Waveform comparison
   - Crest factor and RMS statistics

4. **Q3A_noise_robustness.png** - Robustness testing
   - Signal at various SNR levels: 20dB, 10dB, 5dB, 0dB
   - Shows degradation of spectrogram quality
   - Demonstrates noise immunity limits

5. **Q3A_pitch_robustness.png** - Pitch shift testing
   - Pitch shifts: ±5 semitones, ±2 semitones, 0 (original)
   - Shows frequency shifts in spectrograms
   - Highlights algorithm vulnerability to pitch changes

### Experiments Documented

| Experiment | Finding | Significance |
|-----------|---------|--------------|
| Window Length (FFT 4096) | Excellent frequency resolution, adequate time resolution | Chosen for best balance |
| Single Peaks | Too generic, high false positives | Not used in final system |
| Peak Pairs | Unique (f₁, f₂, Δt) combinations | Core fingerprinting strategy |
| Noise (SNR 20/10/5dB) | Robust up to ~10dB noise | Real-world applicability |
| Pitch Shifts (±5/2%) | Complete failure - frequencies shift | Major limitation identified |
| Time Stretch | Small changes tolerable | System has some flexibility |

---

## Q3(B): Application Deployment

### Two Modes Required

#### 1. Single-Clip Mode ✅
- Upload one WAV file
- Display: Spectrogram, Peak Constellation, Offset Histogram
- Output: Best match and confidence score

**To use:**
1. Go to "🔍 Query & Identify" tab
2. Upload a query WAV file
3. Click "🔎 Identify Song"
4. View spectrogram, peaks, and matching results

#### 2. Batch Mode ✅
- Upload multiple WAV files
- Process all in sequence
- Output: `results.csv` with exact format:
  ```
  filename,prediction
  query1,Song Name 1
  query2,Song Name 2
  ...
  ```

**To use:**
1. Go to "🎵 Batch Mode" tab
2. Upload multiple WAV files
3. Click "🎵 Process Batch"
4. Download `results.csv`

### Database
- Pre-indexed song database ships with deployed app
- Songs indexed from provided library (51 songs)
- Database loads on startup (cached)
- Uses peak-pair fingerprints with quantization:
  - Frequency bins: 25 Hz
  - Time bins: 1 frame (23 ms @ 22050 Hz SR)

---

## Deployment on Streamlit Community Cloud

### Step-by-Step

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Q3 submission ready"
   git push origin main
   ```

2. **Visit Streamlit Cloud**
   - Go to: https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"

3. **Configure**
   - Repository: `aashishr24/EE200`
   - Branch: `main`
   - Main file path: `ss.py`

4. **Deploy**
   - Click "Deploy!"
   - Streamlit builds and deploys automatically
   - App will be live in 2-3 minutes

5. **Test**
   - Single-clip mode: Upload a query file
   - Batch mode: Upload multiple files, download results.csv
   - Verify spectrogram, constellation, and offset histogram display

### Example Deployment URL
```
https://share.streamlit.io/aashishr24/EE200/main/ss.py
```

---

## File Structure

```
/workspaces/EE200/
├── ss.py                           # Main Streamlit app (Q3B)
├── project.py                      # Core MusicFingerprinter class
├── .streamlit/config.toml          # Streamlit configuration
├── requirements.txt                # Python dependencies
├── Q3A_*.png                       # Q3A visualizations (5 files)
├── ASSIGNMENT_GUIDE.md             # Detailed technical guide
├── QUICK_REFERENCE.md              # Quick API reference
├── ultra_fast_analysis.py          # Fast analysis script
└── README.md                       # Project overview
```

---

## Key Implementation Details

### Fingerprinting Algorithm
- **Type**: Hash-based spectral peaks
- **Features**: (frequency1, frequency2, time_gap) tuples
- **Quantization**: 25 Hz freq bins, 1 frame time bins
- **Matching**: Histogram voting on time offsets

### Robustness
- ✅ Handles background noise up to SNR ~10dB
- ✅ Tolerates small volume changes
- ✅ Works with slight time compressions
- ❌ Fails on pitch shifts (even ±5%)
- ❌ Fails on significant time stretching

### Why Single-Clip and Batch Modes Work

**Single-Clip Mode:**
- One query file uploaded
- Full analysis (spectrogram, peaks, matching)
- Visual intermediate steps shown
- Perfect for interactive testing

**Batch Mode:**
- Multiple query files uploaded
- Fast processing (fingerprint extraction + matching)
- Results written to results.csv
- Format: `filename,prediction` (exactly as required)
- Perfect for evaluation automation

---

## Troubleshooting

### App won't start
- Check requirements.txt is installed
- Verify Python 3.8+ environment
- Ensure .streamlit/config.toml is in place

### Database not loading
- Pre-built database should cache on first run
- Takes ~30 seconds for first load
- Subsequent runs use cached version

### Batch mode results missing
- Ensure all query files are valid WAV format
- Check filename encoding (no special characters)
- Download button appears after processing

### Spectrogram/constellation not displaying
- Verify matplotlib installation
- Check streamlit version (1.0+)
- Reload page if plots don't appear

---

## Submission Checklist

- [ ] PDF report with Q3A visualizations and explanations
- [ ] Link to live Streamlit app (working single-clip + batch modes)
- [ ] Link to GitHub source code
- [ ] All code in zip file
- [ ] Database indexed and included with app
- [ ] results.csv format verified (exactly: filename,prediction)
- [ ] Both modes tested and working

---

## Questions?

Refer to:
- `ASSIGNMENT_GUIDE.md` - Full technical details
- `QUICK_REFERENCE.md` - API and function reference
- `project.py` docstrings - Implementation details
- `ss.py` comments - App logic
