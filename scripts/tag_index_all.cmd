ffprobe -print_format json -show_format -show_entries stream=bit_rate,codec_type,codec_name,height,channels,tags,r_frame_rate,index:stream_tags %1
pause