import os
import zipfile
import io
from io import BytesIO
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, enums
import subprocess
import requests
from info import ADMINS, LOG_CHANNEL

@Client.on_message(filters.command("repo") & filters.user(ADMINS))
async def repo(client, message):
    if message.from_user.id in ADMINS:
        command_parts = message.text.split("/repo ", 1)
        if len(command_parts) > 1:
            query = command_parts[1]
            headers = {"Authorization": "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"}
            url = f"https://api.github.com/search/repositories?q={query}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if "items" in data and len(data["items"]) > 0:
                    repo = data["items"][0]
                    repo_name = repo["full_name"]
                    repo_url = repo["html_url"]
                    fork_count = repo["forks_count"]
                    repo_size = repo["size"] / 1024  # Convert size to KB
                    language = repo["language"]
                    repo_description = repo.get("description", "No description available")

                    branches_url = f"https://api.github.com/repos/{repo_name}/branches"
                    branches_response = requests.get(branches_url, headers=headers)
                    branches_data = branches_response.json()

                    branches_text = ""
                    if len(branches_data) > 1:
                        branch_list = []
                        for index, branch in enumerate(branches_data, start=1):
                            branch_name = branch["name"]
                            if branch_name == repo['default_branch']:
                                branch_list.append(f"{index}. *{branch_name}* (default)")
                            else:
                                branch_list.append(f"{index}. {branch_name}")

                        branches_text = "\nBranches:\n" + "\n".join(branch_list)

                    formatted_link = f"{repo_url}/archive/refs/heads/{repo['default_branch']}.zip"

                    # Additional information
                    owner = repo["owner"]["login"]
                    last_update = repo["updated_at"]
                    last_commit_url = f"{repo_url}/commits/{repo['default_branch']}"
                    developer = repo["owner"]["login"]
                    license = repo.get("license", {}).get("spdx_id", "Not specified")

                    contributors_url = f"https://api.github.com/repos/{repo_name}/contributors"
                    contributors_response = requests.get(contributors_url, headers=headers)
                    contributors_data = contributors_response.json()
                    contributors_list = [contributor["login"] for contributor in contributors_data]

                    issues_url = f"https://api.github.com/repos/{repo_name}/issues"
                    issues_params = {"state": "all"}
                    issues_response = requests.get(issues_url, headers=headers, params=issues_params)
                    issues_data = issues_response.json()
                    open_issues = sum(1 for issue in issues_data if issue["state"] == "open")
                    closed_issues = sum(1 for issue in issues_data if issue["state"] == "closed")

                    message_text = (
                        f"Repo: <b><i>{repo_name}</i></b>\n\n"
                        f"URL: <i>{repo_url}</i>\n"
                        f"Owner: {owner}\n"
                        f"Developer: {developer}\n"
                       f"Description: <b><i>{repo_description}</i></b>\n\n"
                        f"Language: <b><i>{language}</i></b>\n"
                        f"Size: {repo_size:.2f} KB\n"
                        f"Fork Count: {fork_count}\n"
                        f"Last Update: {last_update}\n"
                        f"Last Commit: [Details]({last_commit_url})"
                        f"{branches_text}\n\n"
                        f"Additional Information:\n"
                        f"- **License**: {license}\n"
                        f"- **Contributors**: {', '.join(contributors_list)}\n"
                        f"- **Issues**: [Open: {open_issues}, Closed: {closed_issues}]"
                    )

                    await client.send_message(
                        message.chat.id,
                        text=message_text,
                        disable_web_page_preview=True,
                        parse_mode=enums.ParseMode.HTML  # Enable HTML formatting
                    )

                    if branches_data:
                        for branch in branches_data:
                            branch_name = branch["name"]
                            formatted_link = f"{repo_url}/archive/refs/heads/{branch_name}.zip"
                            await client.send_message(
                                message.chat.id,
                                text=f"Branch *{branch_name}*:\n\n{formatted_link}"
                            )
                    else:
                        await client.send_message(
                            message.chat.id,
                            text=f"Default Branch *{repo['default_branch']}*:\n\n{formatted_link}"
                        )
                else:
                    await client.send_message(message.chat.id, "No matching repositories found.")
            else:
                await client.send_message(message.chat.id, "An error occurred while fetching data.")
        else:
            await client.send_message(message.chat.id, "Invalid usage. Provide a query after /repo command.")
    else:
        await client.send_message(message.chat.id, "This feature is only available for admins.")

@Client.on_message(filters.command("private_repo") & filters.user(ADMINS))
async def private_repo(client, message):
    if message.from_user.id in ADMINS:
        command_parts = message.text.split("/private_repo ", 1)
        if len(command_parts) > 1:
            repo_url = command_parts[1]
            try:
                response = requests.get(repo_url, headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer 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"})
            except Exception as e:
                await client.send_message(message.chat.id, f"Error: {str(e)}")
                return

            if response.status_code == 200:
                repo_data = response.json()
                repo_name = repo_data["full_name"]
                repo_size = repo_data["size"] / 1024  # Convert size to KB
                language = repo_data["language"]
                repo_description = repo_data.get("description", "No description available")

                # Clone the repository
                try:
                    subprocess.check_call(["git", "clone", repo_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError as e:
                    await client.send_message(message.chat.id, f"Error: {str(e)}")
                    return

                # Create a zip file
                zip_filename = f"{repo_name}.zip"
                with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk("."):
                        for filename in files:
                            if filename.endswith(".git"):
                                continue
                            filepath = os.path.join(root, filename)
                            zippath = os.path.relpath(filepath, ".").replace("\\", "/")
                            zipf.write(filepath, zippath)

                # Send the zip file
                try:
                    await client.send_document(message.chat.id, io.BytesIO(open(zip_filename, "rb").read()), caption=f"Private Repository: {repo_name}")
                except FloodWait as e:
                    await client.send_message(message.chat.id, f"FloodWait exception: {str(e)}")
                except Exception as e:
                    await client.send_message(message.chat.id, f"Error: {str(e)}")
                finally:
                    os.remove(zip_filename)
            else:
                await client.send_message(message.chat.id, "An error occurred while fetching data.")
        else:
            await client.send_message(message.chat.id, "Invalid usage. Provide a repository URL after /private_repo command.")
    else:
        await client.send_message(message.chat.id, "This feature is only available for admins.")
        
        
@Client.on_message(filters.command("download"))
async def download_repo(client, message):
    if len(message.command) != 2:
        await message.reply("Please provide a GitHub repository URL.")
        return

    repo_url = message.command[1]
    zip_filename = "repo.zip"

    # Get repository info from GitHub API
    repo_info = requests.get(f"{repo_url}/archive/refs/heads/master.zip", stream=True).headers
    if "content-length" not in repo_info:
        await message.reply("Failed to download repository.")
        return

    # Download repository as zip file
    zip_size = int(repo_info["content-length"])
    progress = 0
    with requests.get(f"{repo_url}/archive/refs/heads/master.zip", stream=True) as repo_zip:
        repo_zip.raise_for_status()
        async for chunk in client.stream(repo_zip.iter_content(1024)):
            progress += len(chunk)
            await message.reply_text(f"Downloading... {progress}/{zip_size} bytes")

    # Save zip file to memory
    zip_buffer = BytesIO(repo_zip.content)

    # Extract zip file to memory
    with zipfile.ZipFile(zip_buffer, "r") as zip_file:
        zip_file.extractall(path=zip_filename)

    # Send zip file to user
    await message.reply_document(document=zip_filename)

    # Clean up
    os.remove(zip_filename)

