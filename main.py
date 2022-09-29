from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

drive = GoogleDrive(GoogleAuth())
# needs client_secrets.json from google cloud to authorize
user = os.getlogin()

base_folder = f"C:/Users/{user}/Documents/memes/"

if not os.path.exists(base_folder):
    os.mkdir(base_folder)

folders = (
    (
        f"{base_folder}image/",
        "1Yh9VM4WmgANL1Jr4ffMKJ0nLjsDhot1q",  # drive url for the respective folder
    ),
    (
        f"{base_folder}video/",
        "18PO69jkS_EOcRe01E1Z3-PxhoYlyLFp2",  # drive url for the respective folder
    ),
    (
        f"{base_folder}reaction/",
        "1oSXrlXuoOR8M3vs4zznk--AlEQEarfrq",  # drive url for the respective folder
    ),
)

for folder in folders:
    local_folder = folder[0]

    if not os.path.exists(local_folder):
        os.mkdir(local_folder)

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
            print(f"downloaded '{file_name}'")

    for file in local_file_names:
        if file not in drive_file_names:
            drive_file = drive.CreateFile(
                {"title": file.split(".")[0], "parents": [{"id": drive_folder}]}
            )
            drive_file.SetContentFile(local_folder + file)
            drive_file.Upload()
            print(f"uploaded '{file}'")

os.system("pause")
