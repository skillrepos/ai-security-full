# AI Security for Developers and Practitioners (Full Day)

## Building safe, trustworthy, and resilient AI systems ##


These instructions will guide you through configuring a GitHub Codespaces environment that you can use to run the course labs. 

<br><br>

**1. Change your codespace's default timeout from 30 minutes to longer.**
To do this, when logged in to GitHub, go to https://github.com/settings/codespaces and scroll down on that page until you see the *Default idle timeout* section. Adjust the value as desired.

<br><br>

![Changing codespace idle timeout value](./images/aa4.png?raw=true "Changing codespace idle timeout value")

<br><br>

**2. Click on the button below to start a new codespace from this repository.**

Click here ➡️  [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/skillrepos/ai-security-full?quickstart=1)

<br><br>

**3. Then click on the option to create a new codespace.**

![Creating new codespace from button](./images/sl19.png?raw=true "Creating new codespace from button")

This will run for several minutes while it gets everything ready. **While this is running, you can do step 4.**

<br><br>

**4. Get a free API key for groq to enable use of more powerful models for some of the labs.**

a. In a browser, go to https://console.groq.com and create an account. (If you have an email with a button to confirm, make sure the link is trying to open in the same browser where you were using groq before. If not, you can copy the link from the "click here" section and paste into the right browser.)

b. In the top right of the Groq screen, click on **API Keys**

![API keys](./images/aip55.png?raw=true "API keys")

c. Then click the **Create API Key** button.

![Create API Key](./images/aip56.png?raw=true "Create API Key")


d. Fill in the information, verify you're human if asked, and click **Submit**.

![Create API Key](./images/aip57.png?raw=true "Create API Key")

e. **Copy the key** (you can't view it again later).

![Copy the key](./images/aip58.png?raw=true "Copy the key")

<br><br>

**5. Ensure the codespace is done setting up.**

After the initial startup, it will run a script to setup the python environment, install needed python pieces, install Ollama, and then download the models we will use. This will take several more minutes to run. It will look like this while this is running.

![Final prep](./images/sl21.png?raw=true "Final prep")

The codespace is ready to use when you see a prompt like the one shown below in its terminal.

![Ready to use](./images/sl23.png?raw=true "Ready to use")

<br><br>

**6. Setup your groq key in your codespace.**

In the codespace **TERMINAL**, run the command below to set your key for all terminals. Paste your key when prompted and then hit *Enter*:

```
source scripts/setup-key.sh
```

Afterwards, you should see output that indicates two environment variables (AGENT_PROVIDER and GROQ_API_KEY) are set.

![Getting API key](./images/aip60.png?raw=true "Getting API key")

<br><br>

**7. Run the *warm-up* script for faster LLM interactions.**

```
python scripts/warmup_ollama.py 
```

<br><br>

**8. Open up the *labs.md* file so you can follow along with the labs.**
You can either open it in a separate browser instance or open it in the codespace. 

<br><br>

![Opening labs](./images/sl22.png?raw=true "Opening labs")

**Now, you are ready for the labs!**

<br><br>


**NOTE: If your codespace times out and you need to reopen it**

1. Go to https://github.com/your_github_userid/codespaces
2. Find the codespace in the list, right-click, and select *Open in browser*
3. Repeat steps 5 & 6 from the main section above to set the Groq env keys and run the warmup script again.
<br/><br/>


## Troubleshooting

- **A lab reports it cannot reach Ollama** - the server isn't running. Run `bash scripts/startOllama.sh` from the repo root, then retry. Check `/tmp/ollama.log` if it persists.
- **The first model call is slow (~30-60s)** - run `python3 scripts/warmup_ollama.py` once, then retry. Later calls in the same session are fast.
- **Groq returns 429 (rate limit)** - you've exceeded the free tier's ~30 req/min. Wait a few seconds and retry, or `export LLM_BACKEND=ollama` to switch to the local model. Make sure each person uses their own key.
- **Groq returns 401 / invalid key** - `GROQ_API_KEY` is missing or wrong. Re-copy the key from console.groq.com, or unset it to fall back to Ollama.
- **A `python` command "hangs"** - the RAG and MCP labs use interactive prompts or run servers. Follow the lab's stop instruction (`quit` or `Ctrl+C`).
- **`Address already in use` in Lab 4** - a previous server is still running. Stop it with `Ctrl+C`, or `kill $(lsof -t -i:8000)` / `:9000`.
- **`ModuleNotFoundError: yaml` in Lab 7** - run `pip install -r requirements.txt` from the repo root.
- **Skeleton file errors before merging** - the skeleton files are meant to be completed via the `code -d` diff-merge step first. Each lab tells you when to merge.

## License and attribution

For educational use only by the attendees of our workshops.

© 2026 Tech Skills Transformations and Brent C. Laster. All rights reserved.
