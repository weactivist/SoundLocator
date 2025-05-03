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
