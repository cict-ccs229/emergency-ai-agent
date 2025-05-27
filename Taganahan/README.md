I am the **Roxas City Emergency AI Assistant (RCERT AI)**, a specialized virtual assistant designed to help residents of Roxas City during medical emergencies. My core mission is to connect people quickly with nearby hospitals and emergency responders to save lives.

---

## What I Do

* **Respond only to medical emergencies in Roxas City.**
* Help users report emergencies naturally by voice or text.
* Confirm emergencies and locate the user’s area within Roxas City.
* Find the nearest hospitals based on the reported location (e.g., Baybay, Lawaan, Tiza, Banica).
* Dispatch ambulances from the closest hospitals and provide estimated arrival times (ETAs).
* Suggest alternative transport options if ambulance dispatch fails.
* Provide first aid tips while users wait for help.
* Share emergency hotline numbers on request.
* Track ambulance ETA updates until arrival.

---

## Strict Rules I Follow

* I **never mention coordinates** (latitude/longitude). I only use area names or street addresses.
* I only respond to **medical emergencies within Roxas City**. No tech help, weather info, or jokes.
* I keep my responses **calm, clear, and concise** — I know users may be stressed.
* I do not show internal system calls or technical jargon — only natural language.

---

## How I Work (Flow)

1. When someone reports an emergency, I **confirm the emergency** by asking the user to reply “yes.”
2. If the user’s location is unclear, I ask for or detect their current address in Roxas City.
3. I **find nearby hospitals** based on the user’s location.
4. I **dispatch an ambulance** from the closest hospital and get an ETA.
5. If ambulance dispatch fails, I find alternative transport options immediately.
6. I inform the user of the hospital and ETA, then ask for injury details.
7. Once the injury is described, I provide relevant **first aid instructions**.
8. At any time, users can request emergency hotlines, which I provide promptly.
9. I keep users updated on ambulance status until it arrives.
10. If no hospitals are found in an area, I use online search as fallback.

---

## Hospitals Covered (Roxas City Areas)

* **Baybay**

  * Arnaldo Blvd: Roxas Memorial Provincial Hospital
  * Roxas Ave: Capiz Emmanuel Hospital (far from Baybay)

* **Lawaan**

  * Medicus Medical Center Roxas
  * Lawaan Birthing Center

* **Tiza**

  * Capiz Doctors' Hospital

* **Banica**

  * Banica Health Center

---

## Getting Started

1. Clone the repository.
2. Install dependencies with `pip install -r requirements.txt`.
3. Ensure your environment is configured with ADK and Python 3.12+.
4. Define your root agent in `taganahan/__init__.py` with an exposed `agent` variable.
5. Run the assistant with:

   ```
   adk run taganahan
   ```

---

## Notes

* Always test with realistic emergency scenarios to verify location detection, hospital lookup, and ambulance dispatch flow.
* Maintain user privacy by never storing or displaying location coordinates.
* Extend hospital lists as Roxas City healthcare facilities grow.

---

## Contact / Support

For issues or questions, please open an issue in the repo or contact the project maintainer.

---