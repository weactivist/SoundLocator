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


def directional_sweep():
    smoothed_index = [None]  # mutable container for stateful closure

    def behavior(left_brightness, right_brightness, num_leds, color_scheme):
        leds = [(0, 0, 0)] * num_leds
        total_volume = left_brightness + right_brightness

        if total_volume < 0.0001:
            smoothed_index[0] = None
            return leds

        direction_ratio = right_brightness / total_volume  # flipped left/right
        target_index = int(direction_ratio * (num_leds - 1))

        # Exponential smoothing
        alpha = 0.3  # 0 = very smooth, 1 = no smoothing
        if smoothed_index[0] is None:
            smoothed_index[0] = target_index
        else:
            smoothed_index[0] = int(
                smoothed_index[0] * (1 - alpha) + target_index * alpha
            )

        # Light up multiple LEDs based on color scheme length
        color_count = len(color_scheme)
        half_span = color_count // 2

        for offset, color in enumerate(color_scheme):
            index = smoothed_index[0] - half_span + offset
            if 0 <= index < num_leds:
                leds[index] = color

        return leds

    return behavior