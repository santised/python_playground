from PIL import Image
import sys
import os

thumbnail_size = (500, 500)
root = "/home/amo/Git-Personal/python_playground/"

"""
     ██╗██████╗ ███████╗ ██████╗ 
     ██║██╔══██╗██╔════╝██╔════╝ 
     ██║██████╔╝█████╗  ██║  ███╗
██   ██║██╔═══╝ ██╔══╝  ██║   ██║
╚█████╔╝██║     ███████╗╚██████╔╝
 ╚════╝ ╚═╝     ╚══════╝ ╚═════╝ 
"""


def convert_image(file_path, webp_file):
    name, extension = os.path.splitext(webp_file)

    if extension != ".webp":
        return

    jpeg_file = name + ".jpg"
    try:
        with Image.open(os.path.join(file_path, webp_file), "r") as wf:
            rgb_wf = wf.convert("RGB")
            rgb_wf.save(file_path + jpeg_file)
    except OSError:
        print("cannot convert", webp_file)


"""
████████╗██╗  ██╗██╗   ██╗███╗   ███╗██████╗ ███╗   ██╗ █████╗ ██╗██╗     ███████╗
╚══██╔══╝██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██║██║     ██╔════╝
   ██║   ███████║██║   ██║██╔████╔██║██████╔╝██╔██╗ ██║███████║██║██║     ███████╗
   ██║   ██╔══██║██║   ██║██║╚██╔╝██║██╔══██╗██║╚██╗██║██╔══██║██║██║     ╚════██║
   ██║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║██████╔╝██║ ╚████║██║  ██║██║███████╗███████║
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
"""


def create_thumbnails(file_path, big_pic):
    name, extension = os.path.splitext(big_pic)

    if extension != ".jpg":
        return

    thumbnail_name = "thumb_" + name + extension
    try:
        with Image.open(os.path.join(file_path, big_pic), "r") as bp:
            if bp.format == "JPEG":
                bp.thumbnail(thumbnail_size)
                bp.save(file_path + thumbnail_name)
    except OSError:
        print("Cannot create thumbnail for", big_pic)


# Main
if __name__ == "__main__":
    # Create the root to the given folder
    # os.path.abspath() does not work in this case as it gives
    # the absolute path to where the script is being run.

    # convert the given images to JPEG before turning them into thumbnails
    # file_root = os.path.join(root, sys.argv[1])
    # Uncomment the following if giving the aboslute path to the files
    file_root = sys.argv[1]
    for subdir, dirs, files in os.walk(file_root):
        for file in files:
            convert_image(file_root, file)

    # Convert the converted images to thumbnails
    for subdir, dirs, files in os.walk(file_root):
        for file in files:
            create_thumbnails(file_root, file)
