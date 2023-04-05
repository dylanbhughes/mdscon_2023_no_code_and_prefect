# MDSConf 2023 - Using No-Code and Custom Pipelines Together with Prefect
<!-- 
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/dylanbhughes/mdscon_2023_no_code_and_prefect) -->

## Welcome

[Insert Welcome Message HERE]

## Setting up for development

To get started with this lab you have two options. First, you can use this repo directly from GitHub Codespaces as this repo is configured as a development container. A **development container** is a running container with a well-defined tool/runtime stack and its prerequisites.

### Local Development

* Clone the repo
* Using whichever python environment you like, `pip install -r requirements.txt`
* Check things are working with `which prefect`

### GitHub Codespaces

If your local machine isn't already configured for python development, you can follow these steps to open this repo in a Codespace and follow along:

1. Visit [this repo on GitHub](https://github.com/dylanbhughes/mdscon_2023_no_code_and_prefect)
2. Fork the repository so that you have your own copy under your GitHub account.
3. Click the **Code** drop-down menu.
4. Click on the **Codespaces** tab.
5. Click **Create codespace on main**.

For more information on creating your codespace, visit the [GitHub documentation](https://docs.github.com/en/free-pro-team@latest/github/developing-online-with-codespaces/creating-a-codespace#creating-a-codespace).

## Preparing for the lab

Now that your environment is all set, it's time to sign up for the tools we'll need for the lab.

1. Go to <https://www.fivetran.com> and sign up for a free account. No credit card required!
2. You'll visit <https://app.prefect.cloud> to sign up for a free Prefect Cloud account. No credit card required!
3. Get an API Key from Prefect Cloud
4. Run `prefect cloud login` in your development environment and paste your new API key.
5. Set up a Google Cloud account with BigQuery enabled: <https://console.cloud.google.com/>
