import subprocess
import re
import json
import os
import sys
import time

files = sys.argv[1:]
#files = ["normal.mkv"]

for file in files:

    """iframe check"""

    i_frame_command = f'ffprobe -show_frames "{file}" -read_intervals %+25 -hide_banner'
    with subprocess.Popen(i_frame_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as i_frame_process:
        i_stdout, i_stderr = i_frame_process.communicate()
        i_return_code = i_frame_process.returncode
        i_pid = i_frame_process.pid
        i_frame_process.wait()

        i_out = str(i_stdout)
        i_prob_count = i_out.count("pict_type=I")
        print(f"I frames found: {i_prob_count}")

        if i_prob_count < 3:
            i_problem = "_problem"
        else:
            i_problem = ""
    """iframe check"""

    command_line = f'ffprobe.exe -v quiet -print_format json -show_format -show_entries stream=bit_rate,codec_type,codec_name,height,channels,tags,r_frame_rate,index:stream_tags=language "{file}"'
    base_name = os.path.splitext(file)[0]
    extension = os.path.splitext(file)[1]

    print(f"Base: {base_name}")
    print(f"Extension: {extension}")

    with subprocess.Popen(command_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        stdout, stderr = process.communicate()
        return_code = process.returncode
        pid = process.pid
        process.wait()

        print(stdout.decode())
        json_all = json.loads(stdout.decode())

    print(json_all)
    new_file_values = []
    accepted = ["video", "audio"]
    
    if i_problem:
        new_file_values.append("i_frame_issue")

    # new_file_values = [x.lower() for x in new_file_values]
    new_file_values.insert(0, base_name.replace(" ", " "))

    output_file = "_".join(new_file_values)
    output_file += extension

    os.renames(file, output_file)
