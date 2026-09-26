<p align="center">
  <img src="images/user-agent-dict-logo.png" alt="User Agent Dictionary Logo">
</p>

<div align="center">

![GitHub release (latest by date)](https://img.shields.io/github/v/release/Add3r/UserAgent-Parser)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://github.com/Add3r/UserAgent-Parser/blob/main/LICENSE)
[![Awesome](https://img.shields.io/badge/Awesome-%F0%9F%98%8E-blueviolet.svg)](https://shields.io/)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)
[![Support](https://img.shields.io/static/v1?label=Support&message=Ko-fi&color=ff5e5b&logo=ko-fi)](https://ko-fi.com/add3r)
![Repository Views](https://komarev.com/ghpvc/?username=Add3r&label=Repository+Views)
![Python](https://img.shields.io/badge/Python-3.11.5-blue.svg)
![Total User-Agents Archived](https://img.shields.io/badge/Total%20User--Agents%20Archived-11170-blue.svg)
![Mobile User-Agents](https://img.shields.io/badge/Mobile%20User--Agents-626-orange.svg)
![General User-Agents](https://img.shields.io/badge/General%20User--Agents-10474-green.svg)
![AI User-Agents](https://img.shields.io/badge/AI%20User--Agents-70-purple.svg)

</div>

# UserAgent Fuzzing Library

This repository contains a combined user-agent collection in [`user_agents.json`](user_agents.json). The records can be consumed by any tool that reads JSON and retain the project's existing five fields: `title`, `group`, `id`, `user-agent`, and `platform`.

The library supports proxy and application testing, including the [Proxy_Bypass](https://github.com/Add3r/Proxy_Bypass) vulnerability research tool. Browser records use `General` or `Mobile` as their `platform`; AI records use `AI` and the shared `AI-Agents` group.

## Sources and refreshes

The unified [`ua-fuzz-lib.py`](ua-fuzz-lib.py) updater reads browser user-agent strings from [useragentstring.com](https://www.useragentstring.com/pages/All/) and AI bot HTTP User-Agent values from the [Cloudflare Radar Bots API](https://developers.cloudflare.com/api/resources/radar/subresources/bots/methods/get/). The AI refresh requests the `AI_CRAWLER`, `AI_ASSISTANT`, and `AI_SEARCH` categories. Values are copied from Radar's `userAgents` field; entries with no HTTP User-Agent and obvious templates/placeholders are skipped. Radar may publish a concise identifier for some bots, so values are preserved as Radar reports them.

You can use the committed JSON file without a Cloudflare token. To refresh the complete library, create a Cloudflare API token with **Account → Radar → Read** permission. In Cloudflare, open **My Profile → API Tokens**, create a custom token, and grant that permission. See Cloudflare's [token creation guide](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/) and [Radar API guide](https://developers.cloudflare.com/radar/get-started/first-request/).

Set the token in your terminal session so it is not saved in a project file. In zsh, this prompts without echoing the token:

```zsh
read -s "CLOUDFLARE_API_TOKEN?Cloudflare API token: "
export CLOUDFLARE_API_TOKEN
echo
```

Install the dependencies and run the combined updater:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 ua-fuzz-lib.py
```

The updater fetches both sources before asking whether to print or replace the combined JSON file. If either source fails, it stops without changing the saved library. It assigns AI IDs after the browser IDs and reports counts for General, Mobile, AI, and total records. No schedule runs automatically; run the script when you want to refresh the snapshot.

## Snapshot

The checked-in snapshot contains 11,100 browser records and 70 AI User-Agent values (11,170 records total). The browser records include 10,474 General and 626 Mobile entries. The AI values cover 60 bot names; Cloudflare does not provide a concrete HTTP User-Agent for every bot in its directory.

## Statistics and charts

[`ua-stats.py`](ua-stats.py) reads the same combined `user_agents.json` file and offers the existing General/Mobile group charts plus AI bot charts and a platform breakdown. Run it after installing the requirements:

```bash
python3 ua-stats.py
```

AI records share the `AI-Agents` group by design, so AI charts count by `title` (bot name). The menu offers an AI bot-name chart, an AI bot-name word cloud, a summary of header variants per bot, and a General/Mobile/AI platform chart.

<p align="center">
  <strong>Highest Mobile User Agents</strong><br>
  <img src="Charts/Highest%20Mobile%20User-agents.png" alt="Highest Mobile User Agents">
</p>

<p align="center">
  <strong>Highest General User Agents</strong><br>
  <img src="Charts/Highest%20General%20User-agents.png" alt="Highest General User Agents">
</p>

<p align="center">
  <strong>AI bot names by Radar header variants</strong><br>
  <img src="Charts/AI%20User-agent%20variants.png" alt="AI bot names grouped by number of Radar HTTP User-Agent values">
</p>

<p align="center">
  <strong>All AI User-Agent titles by record count</strong><br>
  <img src="Charts/AI%20User-agent%20titles.png" alt="All AI User-Agent titles ranked by record count">
</p>

## License

This project is licensed under the GPL 3.0 License; see [LICENSE](LICENSE).
