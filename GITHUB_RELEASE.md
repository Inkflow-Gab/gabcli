# Mobile GitHub release guide for GabCli v0.3.0

This project is packaged for upload from a phone. You do not need a terminal to publish the first release.

## 1. Download the release package from this chat

Download:

- `GabCli-v0.3.0-source.zip` — source archive for GitHub
- `gabcli-0.3.0-py3-none-any.whl` — optional Python wheel for users who already have Python

## 2. Create the GitHub repository on mobile

1. Open `github.com` in your phone browser and sign in.
2. Tap the plus button and choose **New repository**.
3. Repository name: `gabcli`.
4. Choose Public if you want anyone to download it.
5. Create the repository.

## 3. Upload the source

From the new repository page:

1. Tap **Add file** and choose **Upload files**.
2. Upload the extracted project files if your phone file picker supports extracting ZIP files.
3. If your phone cannot extract the ZIP, upload `GabCli-v0.3.0-source.zip` as a release asset in the next step and upload this guide or a README as the repository content.
4. Commit the upload to the `main` branch.

## 4. Create the release

1. Open the repository's **Releases** page.
2. Tap **Draft a new release**.
3. New tag: `v0.3.0`.
4. Target: `main`.
5. Release title: `GabCli v0.3.0`.
6. Upload `GabCli-v0.3.0-source.zip` and optionally `gabcli-0.3.0-py3-none-any.whl`.
7. Paste the release notes below.
8. Publish the release.

## Release notes

GabCli v0.3.0 adds:

- Animated thinking and executing status indicators.
- Live shell-command output.
- Colored `+` and `-` file diffs before approval.
- `find_files`, `git_status`, and `git_diff` tools.
- Optional deletion behind `--allow-delete`.
- Secure API-key prompt when no environment variable is set.
- Optional readline history.
- Python packaging and installer support.

Users should download the source ZIP, extract it, run `./install.sh` on a computer, and then set `GABCLI_API_KEY`. A GitHub download alone does not make a command-line program run directly on iOS or ordinary Android; Android users can use a terminal environment such as Termux, while desktop users can use Python 3.9+.

## Important credential note

Never upload `.env` files or API keys to GitHub. Users should provide their own authorized API key through `GABCLI_API_KEY` or GabCli's secure prompt.
