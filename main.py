from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def main():
    drive = GoogleDrive(GoogleAuth())
    # needs client_secrets.json from google cloud to authorize
    user = os.getlogin()

    base_folder = f"C:/Users/{user}/REST OF DIRECTORY"

    local_folders = ( 
        f"{base_folder}/EXAMPLE", # folder in local machine
    )
    drive_folders = (
        "RANDOM NUMBERS", # respective folder in google drive
    )  

    for local_folder, drive_folder in zip(local_folders,drive_folders):
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        local_file_names = os.listdir(local_folder)

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

if __name__ == "__main__":
    main()
