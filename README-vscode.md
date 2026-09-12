# AI Security for Developers and Practitioners

## Building safe, trustworthy, and resilient AI systems ##

These instructions will guide you through configuring a GitHub Codespaces environment that you can use to do the labs. 

**1. Change your codespace's default timeout from 30 minutes to longer (60 for half-day sessions, 90 for deep dive sessions).**
To do this, when logged in to GitHub, go to https://github.com/settings/codespaces and scroll down on that page until you see the *Default idle timeout* section. Adjust the value as desired.

![Changing codespace idle timeout value](./images/vscode1.png?raw=true "Changing codespace idle timeout value")

**2. Click on the button below to start a new codespace from this repository.**

Click here ➡️  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/ai-security-full?quickstart=1)

**3. Then click on the option to create a new codespace.**

![Creating new codespace from button](./images/vscode2.png?raw=true "Creating new codespace from button")

This will run for a long time while it gets everything ready.

After the initial startup, it will run a script to setup the python environment and install needed python pieces. This will take several more minutes to run. It will look like this while this is running.

![Final prep](./images/vscode3.png?raw=true "Final prep")

The codespace is ready to use when you see a prompt like the one shown below in its terminal.

![Ready to use](./images/vscode4.png?raw=true "Ready to use")


**4. Open up the *labs.md* file so you can follow along with the labs.**
You can either open it in a separate browser instance or open it in the codespace. 

![Opening labs](./images/vscode5.png?raw=true "Opening labs")

**5. (Recommended) Set your Groq API key.**
Several labs can use a hosted model on Groq instead of the local Ollama model — it is noticeably faster. In the codespace terminal run:

```
bash scripts/setup-key.sh
```

Without a key the labs still run against the local Ollama model; only the hosted safety classifier in Lab 3 is skipped.

**Now, you are ready for the labs!**


