import math


def clean_num(num):
  conv = float(num)

  if math.isnan(conv):
    return None

  return conv
