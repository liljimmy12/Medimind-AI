# Medimind-AI
### Mission-critical AI for deep space medical autonomy                                                                                                                 
Built using Microsoft BioGPT and a custom astronaut health data system.

## Overview

Long-duration missions don’t have real-time medical advice from Earth.                                                                                                                                                                                        
Medimind-AI acts as an onboard medical assistant powered by BioGPT, capable of:

- Managing astronaut medical profiles

- Monitoring vital signs and mission-specific health data

- Detecting anomalies (oxygen, heart rate, radiation exposure, etc.)

- Generating AI-driven medical summaries and insights

## Core Features

1. **User Management:** Add, load, update, or delete astronaut medical profiles stored as .json files
2. **Vitals & Symptoms:** Input heart rate, oxygen levels, temperature, etc.
3. **Mission Data Logging:** Store data like radiation exposure, location, exercise, and microgravity experience
4. **Alert System:** Detects when vital stats fall outside safe mission thresholds

## setup Instructions
**1. Install Dependencies**                                                                                                                                                                                                                                                                                                                                                
You’ll need Python ≥ 3.9 and torch with GPU support (because BioGPT eats VRAM for breakfast).                                                                                                                                                  
use `pip install torch transformers` to install torch

**2. Clone or Place Code**                                                                                                                                                                                                                            
Save this code in a folder 

**3. Adjust Folder Path**                                                                                                                    
Make sure the variable folder_path matches your system directory:                                                                                                                                                                                                                                                                                                
ex `folder_path = "/home/meyerj@CSGP.EDU/Medimind-AI"`

**4. Run the System**                                                                                                                                                                                                                                                                                                                                             
`python main.py`

When prompted:

`choose which system you would like to use:
1 > user management
2 > diagnosis analyzer`

### Modes of Operation
#### 1. User Management

Handles astronaut profiles stored in JSON.

Options:

- add: Create a new astronaut entry

- load: Display stored astronaut data

- update: Modify existing data fields

- delete: Remove an astronaut profile

#### 2. Diagnosis Analyzer

Runs BioGPT on all user JSON files and provides AI-generated medical insights.

Auto-checks vitals against defined thresholds

Generates contextual feedback for space environments

Flags potential anomalies for mission medical review

## Example Output


<img width="701" height="178" alt="image" src="https://github.com/user-attachments/assets/07210618-a31f-40fd-ba8e-e962528713ea" />

## Future Improvements

- Integrate with biosensor streaming APIs

- Add speech-based input for onboard assistants

- Implement offline LLM inference

- Expand dataset for radiation-specific pathology predictions
