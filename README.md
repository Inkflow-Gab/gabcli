# GabCli

GabCli is an animated, approval-first terminal AI coding assistant for any OpenAI-compatible Chat Completions API. It can inspect a project, propose edits, show a colored `+`/`-` diff, stream approved commands in real time, inspect Git state, and keep you informed about the active model, working directory, activity state, and token usage.

## Quick start

Python 3.9+ and the standard library are enough. No runtime packages are required.

```bash
export GABCLI_API_KEY='your-authorized-api-key'
./gabcli
```

If `GABCLI_API_KEY` is not set and GabCli is running in a terminal, it securely prompts for the key with hidden input. The key is not saved by GabCli.

The default configuration matches the documented endpoint at `https://omni.bidzzofc.my.id/docs`:

```text
Base URL: https://omni.bidzzofc.my.id/v1
Model:    web-cookies
```

Override configuration when needed:

```bash
export GABCLI_BASE_URL='https://omni.bidzzofc.my.id/v1'
export GABCLI_MODEL='web-cookies'
./gabcli --dir ~/my-project
```

One-shot mode:

```bash
./gabcli --dir ~/my-project "Inspect this project and explain its structure"
```

## Reviewable changes

When the assistant wants to write or delete a file, GabCli shows a colored unified diff before asking for approval:

- Green `+` lines are additions.
- Red `-` lines are removals.
- Cyan `@@` lines identify changed hunks.
- The approval line includes a summary such as `+12 -4`.

Example:

```text
[approval needed] write_file
update src/app.py (+3 -1, 420 characters)
--- a/src/app.py
+++ b/src/app.py
@@ -10,3 +10,5 @@
 old line
-new line
+replacement line
+new line
Allow? [y/N]
```

Approved changes are available during the session with `/changes`. File deletion is disabled by default; enable the extra safety gate with:

```bash
./gabcli --allow-delete
```

Deletion still requires approval unless `--yes` is also supplied.

## Activity and safety

- Animated spinner statuses show `thinking`, model details, and estimated token usage while waiting.
- Streaming assistant output is printed as it arrives.
- Approved shell commands stream output live with a `│` prefix.
- The final usage line uses exact gateway usage when supplied, with a conservative estimate otherwise.
- Tools include file reading, writing, search, glob-based file discovery, Git status, Git diff, directory listing, command execution, and optional file deletion.
- File writes, directory creation, deletion, and shell commands require approval by default.
- `--yes` auto-approves changes and commands; use it only in a trusted project.
- Paths are restricted to the selected working directory.
- Hidden chain-of-thought is not printed; GabCli shows short activity labels instead.
- API keys are never included in the source files. Do not commit `.env` or paste secrets into prompts.

## Interactive commands

```text
/help                 Show commands
/status               Show model, directory, and session token counts
/model [NAME]         Show or change the active model
/cd PATH              Change directory and clear context
/clear                Clear conversation
/tools                Show available tools
/changes              Show approved file changes in this session
/version              Show the GabCli version
/quit                 Exit
```

Arrow-key prompt history is available through Python's readline support. It is kept in memory by default. To persist it intentionally, set:

```bash
export GABCLI_HISTORY_FILE="$HOME/.gabcli_history"
```

## Install from a GitHub release

The repository is release-ready with `pyproject.toml`, an installer, tests, and a GitHub Actions release workflow.

### Source archive or clone

```bash
git clone https://github.com/YOUR-USER/gabcli.git
cd gabcli
./install.sh
export PATH="$HOME/.local/bin:$PATH"
export GABCLI_API_KEY='your-authorized-api-key'
gabcli
```

The release workflow publishes a wheel and source archive whenever a `v*` tag is pushed. If you download a source archive from GitHub, extract it and run `./install.sh`.

### One-line public release installer

After publishing the repository and the `v0.3.0` release, users can install the public wheel without a GitHub token:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR-USER/gabcli/main/install-from-github.sh | sh -s -- YOUR-USER/gabcli v0.3.0
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/YOUR-USER/gabcli/main/install-from-github.ps1 -OutFile install-gabcli.ps1
.\\install-gabcli.ps1 -Repository YOUR-USER/gabcli -Version v0.3.0
```

Then each user supplies their own model API key:

```bash
export GABCLI_API_KEY='their-authorized-api-key'
gabcli
```

### Python package installation

```bash
python3 -m pip install .
export GABCLI_API_KEY='your-authorized-api-key'
gabcli
```

No GitHub repository is created automatically by this workspace; replace `YOUR-USER` with the account where you publish the project.
Do not embed a GitHub personal access token in an installer. Public releases download anonymously; private repositories require each downloader to authenticate with their own GitHub account.

## Development checks

```bash
python3 -m py_compile gabcli.py gabcli_ui.py gabcli_diff.py
python3 -m unittest discover -s tests -v
python3 -m pip wheel . --no-deps -w dist
```

## Configuration template

See `.env.example`. It is a template only and contains no real credential.
