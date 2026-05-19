from __future__ import annotations

import time
from collections import deque


class GroqRateLimiter:
    """Track tokens/min and daily budget for Groq free tier."""

    def __init__(
        self,
        *,
        daily_token_budget: int,
        tpm_soft_limit: int,
        inter_request_delay_sec: float,
    ) -> None:
        self.daily_token_budget = daily_token_budget
        self.tpm_soft_limit = tpm_soft_limit
        self.inter_request_delay_sec = inter_request_delay_sec
        self.daily_tokens_used = 0
        self._window: deque[tuple[float, int]] = deque()

    def record(self, tokens: int) -> None:
        now = time.time()
        self.daily_tokens_used += tokens
        self._window.append((now, tokens))
        self._prune(now)

    def _prune(self, now: float) -> None:
        while self._window and now - self._window[0][0] > 60.0:
            self._window.popleft()

    def tokens_last_minute(self) -> int:
        now = time.time()
        self._prune(now)
        return sum(t for _, t in self._window)

    def assert_daily_budget(self, estimated_next: int = 0) -> None:
        if self.daily_tokens_used + estimated_next > self.daily_token_budget:
            raise RuntimeError(
                f"Groq daily token budget exceeded: {self.daily_tokens_used + estimated_next}"
                f" > {self.daily_token_budget}"
            )

    def wait_for_tpm(self) -> None:
        while self.tokens_last_minute() >= self.tpm_soft_limit:
            time.sleep(2.0)

    def pause_between_requests(self) -> None:
        time.sleep(self.inter_request_delay_sec)
