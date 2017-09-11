import vlc
from os import listdir
from os.path import isfile, join
import random
import LeitnerSpacing as LS


def play_sound(filepath):
    player = vlc.MediaPlayer(filepath)
    player.play()

def generate_tone_dict(folder_path):
    sound_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    particle_dict = {}
    all_sounds = []
    print(sound_files)
    # assume that sound files are named particle,tone.mp3
    for sf in sound_files:
        sound = sf[:-4]
        all_sounds.append(sound)
        print(sound)
        try:
            tone = int(sound[-1])
        except ValueError:
            tone = 0
        particle = sound[:-1]
        try:
            particle_dict[particle].append(tone)
        except KeyError:
            particle_dict[particle] = [tone]
    return particle_dict, all_sounds

def get_spacing_tool(particle_dict):
    word_def_pairs = []
    for particle in particle_dict.keys():
        tones = particle_dict[particle]
        for tone in tones:
            sound = particle + str(tone)
            sound_file = "./mp3/" + sound + ".mp3"
            word_def_pairs.append((sound, sound_file))
    return LS.LeitnerSpacing(word_def_pairs)

if __name__ == "__main__":
    particle_dict, all_sounds = generate_tone_dict("./mp3")
    spacing_tool = get_spacing_tool(particle_dict)
    print("Welcome to the pinyin test!\nPinyin tones will be played and you will guess them. Good Luck!")
    while True:
        flash_card = spacing_tool.get_card()
        play_sound(flash_card.definition)
        answer = raw_input("What was that sound?:")
        if answer == flash_card.word:
            print("Correct!\nThe sound was {}.".format(flash_card.word))
            spacing_tool.report_result(flash_card, True)
        else:
            print("Incorrect.\nThe sound was {}.".format(flash_card.word))
            spacing_tool.report_result(flash_card, False)
        print(repr(spacing_tool))
