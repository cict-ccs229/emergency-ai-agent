# Iloilo Province Emergency Support Agent

This directory contains the implementation of an emergency support agent localized within the Iloilo Province of the Philippines. 

[Observe the demo between the agent and Keane using voice input.](https://drive.google.com/drive/folders/1y2lyIpZB3BeuzF8_ROtZhsADfh5YFBbu?usp=sharing)

## What are its functions?

An emergency support agent performs three functions:
1. Pinpoint the location of the user. 
2. Search the web for hospitals near location.
3. Call emergency services of chosen hospital.

> Despite the agent using real contact information, emergency services are not actually called.

## How can I test the agent on my local computer?

You can test the agent by invoking the command `adk web` or `adk run dalisay` at the root `/emergency-ai-agent` directory. The former allows for voice input while the latter is restricted to text prompts.

I recommend you experience talking with the agent through voice input. It is more realistic although the agent is slower than average in reading its response. It will also have difficulty grasping your words if your microphone is not great at picking up audio.