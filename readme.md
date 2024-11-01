# HueMIDI

**HueMIDI** is a Python application designed to provide seamless control of Philips Hue lights through MIDI devices, transforming lights into a dynamic, responsive part of any audio setup. This project is ideal for use with MIDI controllers such as Ableton, Native Instruments Maschine, and other MIDI hardware or software. The current implementation provides foundational controls over Philips Hue lights, including on/off, brightness adjustments, color cycling, and temperature changes. MIDI functionality allows for real-time, interactive light shows, bringing synced lighting effects to performances or audio-driven environments.

## Vision for HueMIDI

The goal of HueMIDI is to achieve full-featured control over Philips Hue lights using MIDI controllers and software. Future development will enable comprehensive mapping between MIDI inputs and light functions, allowing users to synchronize and automate complex lighting effects using MIDI instruments, digital audio workstations (DAWs) like Ableton, and MIDI-enabled devices like Maschine. This will enable responsive, real-time control of colors, brightness, color temperature, and more, creating a bridge between audio and visual creativity.

---

## Getting Started

### Prerequisites

- **Python 3.7+**
- **Philips Hue Bridge** with compatible Hue lights
- **MIDI Device** (optional but recommended, for interactive control)
- **python-dotenv** for managing environment variables

---

## Installation

1. **Clone the Repository**  
   Clone the HueMIDI repository to your local machine:
   ```bash
   git clone https://github.com/enlyte/HueMIDI.git
   cd HueMIDI
   ```

2. **Install Dependencies**  
   Use `pip` to install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment Variables**  
   This project uses environment variables to securely store the Philips Hue Bridge IP address and username. Follow these steps to set up the `.env` file:

   - **Create the .env file**  
     Rename the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```

   - **Get Your Philips Hue Bridge IP Address**  
     Identify the local IP address of your Philips Hue Bridge. This is often available in your router settings or Hue app. Once you have the IP address, add it to the `.env` file:
     ```plaintext
     BRIDGE_IP=your_bridge_ip
     ```

   - **Generate an API Username**  
     With the bridge IP set in `.env`, run `getHueName.py` to generate an API username for your bridge. First, press the physical button on your Hue Bridge, then run the following:
     ```bash
     python getHueName.py
     ```

     This script will output an API username. Add this username to your `.env` file:
     ```plaintext
     USERNAME=your_api_username
     ```

4. **Retrieve Light IDs**  
   Run `getLightIDs.py` to list all Hue lights connected to your bridge, along with their names and IDs. This will help you identify which light IDs to use in the control scripts.
   ```bash
   python getLightIDs.py
   ```

---

## Usage

### Basic Light Control

HueMIDI provides several foundational scripts for controlling Philips Hue lights. Each script enables a different type of interaction:

- **Turn Lights On/Off**: Control individual or groups of lights.
- **Adjust Brightness**: Set brightness levels dynamically.
- **Cycle Colors**: Rotate through different colors for vibrant effects.
- **Change Color Temperature**: Adjust color temperature between warm and cool settings.

### MIDI Control

For interactive lighting control with MIDI, connect a MIDI controller to your system and run the MIDI integration script. Customize the MIDI mappings within the script to control specific lighting functions using MIDI notes, CC messages, or faders.

### Light Show

To run a preset light show across multiple lights, use `lightShow.py`. This script demonstrates various effects using threading to control multiple lights with different behaviors simultaneously. You can use this as a base to expand the light show or modify effects to suit your needs.

---

## Project Structure

```plaintext
HueMIDI/
├── .env.example          # Template for environment variables
├── getHueName.py         # Script to generate API username for Philips Hue Bridge
├── getLightIDs.py        # Retrieve and display Hue light IDs and names
├── lightControl.py       # Main light control functions (on/off, brightness, color, etc.)
├── midiControl.py        # MIDI integration functions for real-time control
├── lightShow.py          # Preset threaded light show across multiple lights
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Future Directions

- **Expanded MIDI Mapping**: Add advanced MIDI mapping features to enable more complex light patterns and effects with DAWs and MIDI controllers.
- **Effect Presets**: Pre-defined light effect presets that users can trigger via MIDI.
- **DAW Integration**: Direct integration with Ableton or other DAWs to sync lighting with musical beats and sequences.
- **GUI Interface**: A graphical interface for selecting lights, assigning effects, and customizing MIDI mappings.

---

## Contributing

Contributions are welcome! If you have ideas for new features, improvements, or bug fixes, please fork the repository and submit a pull request. Documentation updates and additional device support are also appreciated.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information. 

--- 

This README provides an overview of HueMIDI, from getting started to future development. Enjoy creating music-driven light shows with **HueMIDI**!