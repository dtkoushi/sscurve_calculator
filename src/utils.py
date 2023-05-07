import numpy as np

def divide_value(value, current, goal, tangent):
    diff = (goal - abs(current)) / tangent * np.sign(value)
    return diff, value - diff

def create_loop(amps, is_returned=True, div=100):
  arrays = []
  for amp in amps:
    range1 = np.linspace(0.0, amp, div + 1)
    range2 = np.linspace(amp - amp / div, 0.0, div)
    arrays.append(range1)
    arrays.append(range2)
  if is_returned:
    return np.concatenate(arrays)
  return np.concatenate(arrays[:-1])