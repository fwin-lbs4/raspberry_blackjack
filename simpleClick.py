import time
import keyboard

class dice:
  def get_switch():
    return keyboard.is_pressed("space")

def get_clicks():
  # waiting for first click
  while not dice.get_switch():
    # Q1: what is the reason for the next command?
    time.sleep(0.05)
  state = True
  prev_state = True
  # Q2: why is clicks initialized with 1?
  clicks = 1
  first_click = time.time()
  # 0.3 seconds to do another click
  while time.time() < first_click + 0.3:
    # INSERT CODE HERE
    # Set prev_state to state, to keep track of what state was last loop
    prev_state = state

    # if the switch is pressed set state to True
    state = dice.get_switch()

    # when state was set to true and prev_state was false, we just pressed the button
    if state and not prev_state:
      clicks += 1
    # Q3: clock is approx. 67Hz.
    # How can you calculate that value from time.sleep(0.015)
    time.sleep(0.015)
  return clicks

print(get_clicks())