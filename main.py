from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

drive = GoogleDrive(GoogleAuth())
# needs client_secrets.json from google cloud to authorize
user = os.getlogin()

folders = (
    (
        f"C:/Users/{user}/Documents/memes/image/",
        "",  # drive url for the respective folder
    ),
    (
        f"C:/Users/{user}/Documents/memes/video/",
        "",  # drive url for the respective folder
    ),
    (
        f"C:/Users/{user}/Documents/memes/reaction/",
        "",  # drive url for the respective folder
    ),
)

for folder in folders:
    if not os.path.exists(folder):
        os.mkdir(folder)

    local_folder = folder[0]
    local_file_names = os.listdir(local_folder)

    drive_folder = folder[1]
    drive_files = drive.ListFile(
        {"q": f"'{drive_folder}' in parents and trashed=false"}
    ).GetList()  # lists all the files in the drive folder
    drive_file_names = [
        f"{file['title']}.{file['mimeType'].split('/')[-1]}" for file in drive_files
    ]

    for file, file_name in zip(drive_files, drive_file_names):
        if file_name not in local_file_names:
            drive_file = drive.CreateFile(
                {
                    "id": file["id"],
                }
            )
            drive_file.GetContentFile(local_folder + file_name)

    for file in local_file_names:
        if file not in drive_file_names:
            drive_file = drive.CreateFile(
                {"title": file.split(".")[0], "parents": [{"id": drive_folder}]}
            )
            drive_file.SetContentFile(local_folder + file)
            drive_file.Upload()
