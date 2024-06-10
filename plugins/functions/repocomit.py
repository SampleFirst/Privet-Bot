from pyrogram import Client, filters, types, enums
import requests
import zipfile
import os
import io
from info import ADMINS 

@Client.on_message(filters.command("repos") & filters.user(ADMINS))
async def repos(client, message):
    # Split the message text and check if there are enough elements
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

                message_text = (
                    f"Repo: <b><i>{repo_name}</i></b>\n\n"
                    f"URL: <i>{repo_url}</i>\n\n"
                    f"Description: <b><i>{repo_description}</i></b>\n\n"
                    f"Language: <b><i>{language}</i></b>\n"
                    f"Size: {repo_size:.2f} KB\n"
                    f"Fork Count: {fork_count}"
                )

                await client.send_message(
                    message.chat.id,
                    text=message_text,
                    disable_web_page_preview=True,
                    parse_mode=enums.ParseMode.HTML  # Enable HTML formatting
                )
            else:
                await client.send_message(message.chat.id, "No matching repositories found.")
        else:
            await client.send_message(message.chat.id, "An error occurred while fetching data.")
    else:
        await client.send_message(message.chat.id, "Invalid usage. Provide a query after /repo command.")
        
@Client.on_message(filters.command("repocommits") & filters.user(ADMINS))
async def repo_commits(client, message):
    # Split the message text and check if there are enough elements
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

                # Fetch all commits
                commits_url = f"https://api.github.com/repos/{repo_name}/commits"
                commits_response = requests.get(commits_url, headers=headers)
                if commits_response.status_code == 200:
                    commits_data = commits_response.json()
                    
                    # Create a ZIP file in memory
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w") as zf:
                        for commit in commits_data:
                            commit_message = commit["commit"]["message"]
                            commit_hash = commit["sha"]
                            filename = f"{commit_hash}.txt"
                            zf.writestr(filename, commit_message)

                    zip_buffer.seek(0)

                    message_text = (
                        f"Repo: <b><i>{repo_name}</i></b>\n\n"
                        f"URL: <i>{repo_url}</i>\n\n"
                        f"Description: <b><i>{repo_description}</i></b>\n\n"
                        f"Language: <b><i>{language}</i></b>\n"
                        f"Size: {repo_size:.2f} KB\n"
                        f"Fork Count: {fork_count}"
                    )

                    await client.send_message(
                        message.chat.id,
                        text=message_text,
                        disable_web_page_preview=True,
                        parse_mode=enums.ParseMode.HTML  # Enable HTML formatting
                    )

                    await client.send_document(
                        message.chat.id,
                        document=types.InputFile(zip_buffer, f"{repo_name.replace('/', '_')}_commits.zip"),
                        caption="Here are all the commits in a ZIP file."
                    )
                else:
                    await client.send_message(message.chat.id, "An error occurred while fetching commits.")
            else:
                await client.send_message(message.chat.id, "No matching repositories found.")
        else:
            await client.send_message(message.chat.id, "An error occurred while fetching data.")
    else:
        await client.send_message(message.chat.id, "Invalid usage. Provide a query after /repo command.")
