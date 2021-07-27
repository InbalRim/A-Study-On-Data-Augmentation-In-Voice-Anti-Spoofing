#################################################################################################################
# This script is made to generate augmented data using the pydub library supported with ffmpeg.
# It receives args (so it can run as a few different processes to increase speed) and creates the
# files in the relevant directory.
# it will create for each part and for each bitrate.
# the directories must exist prior.
#
# Note - pydub will not run good with Opus. if you want to generate opus data you need to build ffmpeg with
# libopus (see ffmpeg website for more details)
#################################################################################################################


from pydub import AudioSegment
import os
import argparse
import sys

# Paths (relevant for opus/vorbis only)
sys.path.append('/usr/local/bin/ffmpeg')
ffmpeg_path = "/usr/local/bin"
os.environ["PATH"] += os.pathsep + ffmpeg_path

# args
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--part", type=int, help="0 = train, 1 = dev", default=1)
parser.add_argument("--bitrate", type=int, help="0 = 16, 1 = 32, 2 = 64", default=2)
args = parser.parse_args()



# Hyper parameters - paths
train_path = os.path.join('./data/LA/ASVspoof2019_LA_train')
dev_path = os.path.join('./data/LA/ASVspoof2019_LA_dev')
paths_list_big = [train_path, dev_path]

compression_method = 'OGG' # can be for example MP3/MP4(AAC)/OGG(vorbis)/OPUS...
bitrates_big = ["16K" , "32K", "96K"]

paths_list = [paths_list_big[args.part]]
bitrates = [bitrates_big[args.bitrate]]

print("Part will be part: {}".format(paths_list))
print("Bitrate will be will be part: {}".format(bitrates))
print("Compression Method: {}".format(compression_method))


# junk path for temporary files
junk_path = os.path.join('./data/LA/data_augmentation/temp'+str(args.part) +str(args.bitrate)+ '.' + compression_method.lower())

#specify codec
if compression_method == 'MP4':
    codec = 'aac'
elif compression_method == 'OPUS':
    codec = 'opus'
elif compression_method == 'OGG':
    codec = 'ogg'

# run on train / dev
for part in paths_list:

    #list of all audio files in directory
    files = os.listdir(part + '/flac/')

    # run on each bitrate
    for bitrate in bitrates:

        # run on all the files
        for i, file in enumerate(files):
            #
            # generate new file path (pth) from original file (orig)
            orig = str(part + '/' + 'flac'+ '/' + file)
            pth = str(part + '/' + compression_method + '/' + bitrate[:-1] + '/' + file[:-5] + '_'
                      + compression_method + '_' + bitrate[:-1] + '.flac')

            if codec != "opus" and codec != 'ogg':
                # read file into object and write mp3/m4a file
                sig = AudioSegment.from_file(orig, 'flac')
                sig.export(junk_path, format=compression_method.lower() , bitrate = bitrate)#, codec = codec)

                # read mp3/m4a and then write new file
                sigNew = AudioSegment.from_file(junk_path, compression_method.lower())
                sigNew.export(pth, format="flac")
            else:
                os.system("ffmpeg -i "+orig+" -b:a "+bitrate+" "+junk_path + ' -loglevel 0 -y' )

                os.system("ffmpeg -i "+junk_path+" -ar 16000 -sample_fmt s16 "+pth + ' -loglevel 0 -y')




            if not(i%50):
               print(bitrate + ' ' + file + ' ' + str(i))

print("Done")
exit()

## to use this from the terminal you can use this:
# python compression_augmentation.py  &> output.txt &
# tail -f output.txt

