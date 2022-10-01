import subprocess
import re
import json
import os
import sys

files = sys.argv[1:]
for file in files:

    command_line = f"ffprobe.exe -v quiet -print_format json -show_format -show_entries stream=bit_rate,codec_type,codec_name,height {file}"
    base_name = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]

    print(f"Base: {base_name}")
    print(f"Extension: {extension}")

    process = subprocess.Popen(command_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    return_code = process.returncode
    pid = process.pid
    process.wait()

    json_all = json.loads(stdout.decode())

    print(json_all)
    new_file_values = [base_name]
    accepted = ["video", "audio"]

    for stream in json_all["streams"]:
        if stream["codec_type"] in accepted:
            new_file_values.append(stream["codec_name"])

        if stream["codec_type"] == "video":
            new_file_values.append(f"{stream['height']}p")
            new_file_values.append(f"{int((int(json_all['format']['bit_rate'])) / 1024)}kbs")

        if stream["codec_type"] == "audio":
            if "bit_rate" in stream:
                new_file_values.append(f"{int((int(stream['bit_rate'])) / 1024)}kbs")

    output_file = "_".join(new_file_values)
    output_file += extension

    os.rename(file, output_file)