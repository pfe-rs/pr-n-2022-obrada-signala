from utils.frequency import get_frequency, change_pitch_and_write_to_file

input_file = "assets/C5.wav"
current_step = 0
current_frequency = get_frequency(input_file)

# Na levo
while current_frequency >= 27.5:  #najmanja frekvencija note
     current_step -= 1
     change_pitch_and_write_to_file(input_file, f"out/freq {current_frequency} step {current_step}.wav", current_step)
     current_frequency = get_frequency(f"out/freq {current_frequency} step {current_step}.wav")


current_step = 0 #nazad na centar

# Na desno
while current_frequency <= 3951.0:  #najveca frekvencija note
    current_step += 1
    change_pitch_and_write_to_file(input_file, f"out/freq {current_frequency} step {current_step}.wav", current_step)
    current_frequency = get_frequency(f"out/freq {current_frequency} step {current_step}.wav")

# Outputujemo samu notu u out, bez promene, cisto da bude tu
change_pitch_and_write_to_file(input_file, f"out/freq {current_frequency} step {current_step}.wav", 0)