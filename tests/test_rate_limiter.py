from unittest.mock import patch

from gestor_de_stock.infrastructure.security.rate_limiter import InMemoryRateLimiter
from practice_rate_limiter import (
    cleanup_old_attempts,
    get_recent_attempts,
    is_rate_limited,
    record_failed_attempt,
    should_block_request,
)


def test_is_rate_limited_when_limit_reached():
    attempts = [1010.0, 1025.0, 1040.0, 1050.0, 1060.0]

    result = is_rate_limited(
        attempts=attempts,
        current_time=1070.0,
        window=60,
        max_attempts=5,
    )

    assert result is True


def test_allows_request_when_limit_not_reached():
    login_attempts = {"client_1": [1010.0, 1025.0, 1040.0, 1050.0]}
    result = should_block_request(
        login_attempts=login_attempts,
        client_id="client_1",
        current_time=1065.0,
        window=60,
        max_attempts=5,
    )
    assert result is False
    assert login_attempts["client_1"] == [1010.0, 1025.0, 1040.0, 1050.0]
    assert len(login_attempts["client_1"]) == 4


def test_blocks_request_when_limit_reached():
    login_attempts = {"client_1": [1020.0, 1025.0, 1040.0, 1050.0, 1060.0]}
    result = should_block_request(
        login_attempts=login_attempts,
        client_id="client_1",
        current_time=1070.0,
        window=60,
        max_attempts=5,
    )
    assert result is True
    assert login_attempts["client_1"] == [1020.0, 1025.0, 1040.0, 1050.0, 1060.0]


def test_records_existing_client_failed_attempt():
    login_attempts = {"client_1": [1010.0, 1025.0, 1040.0]}
    current_time = 1065.0
    record_failed_attempt(login_attempts, "client_1", current_time)
    assert login_attempts["client_1"] == [1010.0, 1025.0, 1040.0, 1065.0]


def test_records_new_client_failed_attempt():
    login_attempts = {"client_1": [1010.0, 1025.0, 1040.0]}
    current_time = 1065.0
    record_failed_attempt(login_attempts, "client_2", current_time)
    assert login_attempts["client_2"] == [1065.0]


def test_rate_limiter_independent_clients():
    login_attempts = {
        "client_1": [1010.0, 1025.0, 1040.0, 1050.0, 1060.0],
        "client_2": [1050.0, 1060.0],
    }
    current_time = 1070.0
    window = 60
    max_attempts = 5

    result_client_1 = should_block_request(
        login_attempts=login_attempts,
        client_id="client_1",
        current_time=current_time,
        window=window,
        max_attempts=max_attempts,
    )
    result_client_2 = should_block_request(
        login_attempts=login_attempts,
        client_id="client_2",
        current_time=current_time,
        window=window,
        max_attempts=max_attempts,
    )

    assert result_client_1 is True
    assert result_client_2 is False


def test_attempt_at_window_boundary_is_recent():
    attempts = [1010.0, 1025.0, 1040.0, 1050.0]
    current_time = 1070.0
    window = 60

    recent_attempts = get_recent_attempts(attempts, current_time, window)
    assert recent_attempts == [1010.0, 1025.0, 1040.0, 1050.0]


def test_attempt_just_outside_window_is_not_recent():
    attempts = [1009.0, 1025.0, 1040.0, 1050.0]
    current_time = 1070.0
    window = 60

    recent_attempts = get_recent_attempts(attempts, current_time, window)
    assert recent_attempts == [1025.0, 1040.0, 1050.0]


def test_future_attempt_is_not_recent():
    attempts = [1080.0, 1090.0]
    current_time = 1070.0
    window = 60

    recent_attempts = get_recent_attempts(attempts, current_time, window)
    assert recent_attempts == []


def test_cleanup_removes_old_attempts_and_preserves_recent_ones():
    attempts = [1000.0, 1010.0, 1025.0, 1040.0, 1050.0]
    current_time = 1080.0
    window = 60

    cleanup_old_attempts(attempts, current_time, window)
    assert attempts == [1025.0, 1040.0, 1050.0]


def test_cleanup_removes_old_attempts_with_block_request():
    login_attempts = {
        "client_1": [1000.0, 1010.0, 1025.0, 1040.0, 1050.0, 1060.0, 1070.0]
    }
    current_time = 1080.0
    window = 60
    max_attempts = 5

    result = should_block_request(
        login_attempts=login_attempts,
        client_id="client_1",
        current_time=current_time,
        window=window,
        max_attempts=max_attempts,
    )

    assert result is True
    assert login_attempts["client_1"] == [1025.0, 1040.0, 1050.0, 1060.0, 1070.0]


def test_allows_request_after_attempts_expire():
    rate_limiter = InMemoryRateLimiter(60, 5)
    with patch(
        "gestor_de_stock.infrastructure.security.rate_limiter.time.monotonic",
        return_value=100.0,
    ):
        for _ in range(5):
            rate_limiter.record_failed_attempt("client_1")
    with patch(
        "gestor_de_stock.infrastructure.security.rate_limiter.time.monotonic",
        return_value=161.0,
    ):
        result = rate_limiter.should_block_request("client_1")

    assert result is False
