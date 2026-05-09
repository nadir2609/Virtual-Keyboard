from dataclasses import dataclass
from typing import Mapping

from gesture import calculate_distance


@dataclass(frozen=True)
class DwellUpdate:
    should_press: bool
    progress: float
    show_progress: bool


class DwellClickDetector:
    def __init__(self, dwell_time_ms: int, move_tolerance: float):
        self._dwell_seconds = max(0.001, dwell_time_ms / 1000.0)
        self._move_tolerance = move_tolerance
        self.reset()

    def reset(self):
        self._hovered_char = None
        self._anchor = None
        self._start_time = 0.0
        self._triggered = False

    def update(self, hovered_key: Mapping[str, object] | None, index_pos, now: float):
        if hovered_key is None or index_pos is None:
            self.reset()
            return DwellUpdate(False, 0.0, False)

        hovered_char = str(hovered_key["char"])
        moved_too_much = self._anchor is not None and (
            calculate_distance(index_pos, self._anchor) > self._move_tolerance
        )

        if self._hovered_char != hovered_char or moved_too_much:
            self._hovered_char = hovered_char
            self._anchor = index_pos
            self._start_time = now
            self._triggered = False
            return DwellUpdate(False, 0.0, True)

        progress = min(1.0, (now - self._start_time) / self._dwell_seconds)
        if progress >= 1.0 and not self._triggered:
            self._triggered = True
            return DwellUpdate(True, 1.0, False)

        return DwellUpdate(False, progress, not self._triggered)
