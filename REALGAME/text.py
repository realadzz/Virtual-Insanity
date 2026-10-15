# text
# the typewriter effect, where letters pop up one at a time like in undertale
# anything story-ish uses type_print instead of print. maps and menus still use normal print so they show up instantly

import time

# how many letters appear per second. 0 turns the animation off completely
LETTERS_PER_SECOND = 30

# set this to True for a short extra pause after . ! ? like in undertale
PAUSE_ON_PUNCTUATION = False
PUNCTUATION_PAUSE = 0.15  # seconds


def wait_until(target_time):
    # time.sleep() isn't very accurate (on lots of windows pcs it can be up to ~16ms late), which makes the text stutter
    # so this only sleeps while there's plenty of time left, then keeps checking the clock until it's exactly time
    while True:
        remaining = target_time - time.perf_counter()
        if remaining <= 0:
            return
        if remaining > 0.02:
            time.sleep(remaining - 0.018)  # even if this wakes up late, it's still before the target
        else:
            time.sleep(0)  # just lets the computer do other stuff for a moment while waiting


def type_print(text, end="\n"):
    if LETTERS_PER_SECOND <= 0:
        print(text, end=end)
        return

    delay = 1 / LETTERS_PER_SECOND

    # every letter gets its own exact time to appear, worked out from when the line started.
    # that way small delays can't build up, and the text flows at a perfectly steady speed
    next_letter_time = time.perf_counter()
    for character in text:
        print(character, end="", flush=True)  # flush=True shows the letter straight away
        next_letter_time += delay
        if PAUSE_ON_PUNCTUATION and character in ".!?":
            next_letter_time += PUNCTUATION_PAUSE
        wait_until(next_letter_time)
    print(end, end="", flush=True)


def type_input(text):
    # same as input(), but the question gets typed out first
    type_print(text, end="")
    return input()
