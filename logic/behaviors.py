def default_behavior(left_brightness, right_brightness, num_leds, color_scheme):
    leds = [(0, 0, 0)] * num_leds
    center = num_leds // 2
    segment_count = len(color_scheme)
    segment_width = center // (segment_count // 2)

    left_leds_to_light = int(left_brightness * center)
    right_leds_to_light = int(right_brightness * center)

    # Fill from edge to center for left side
    for i in range(left_leds_to_light):
        color_idx = min(i // segment_width, (segment_count // 2) - 1)
        leds[i] = color_scheme[color_idx]

    # Fill from edge to center for right side
    for i in range(right_leds_to_light):
        color_idx = min(i // segment_width, (segment_count // 2) - 1)
        leds[-(i + 1)] = color_scheme[-(color_idx + 1)]

    return leds


def directional_sweep(left_brightness, right_brightness, num_leds, color_scheme):
    leds = [(0, 0, 0)] * num_leds
    total_volume = left_brightness + right_brightness

    if total_volume < 0.01:
        return leds  # Silence, keep all off

    direction_ratio = right_brightness / total_volume  # flipped left/right
    index = int(direction_ratio * (num_leds - 1))

    # Choose a color — middle of the scheme
    color = color_scheme[len(color_scheme) // 2]
    leds[index] = color

    return leds