from os.path import join

import ffmpeg


# def split_video_into_images(v):
#     # res = subprocess.check_output(["ffmpeg", "-skip_frame", "nokey", "-i", v, "-vsync", "0", "-frame_pts", "true", "-r", "1000", "out%d.png"])
#     # for line in res.splitlines():
#     bashCommand = "ffmpeg -skip_frame nokey -i " + v + " -vsync 0 -frame_pts true -r 1000 hw%d.png"
#     output = subprocess.check_output(['bash', '-c', bashCommand])

def split_video_into_images(folder):
    v = join(folder, folder + ".mp4")
    try:
        (ffmpeg.input(v)
         .filter('fps', fps=2)
         .output(join(folder, '%d.png'),
                 video_bitrate='5000k',
                 sws_flags='bilinear',
                 start_number=0)
         .run(capture_stdout=True, capture_stderr=True))
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))


if __name__ == '__main__':
    split_video_into_images("2020-08-16-08-31-14-497963")
