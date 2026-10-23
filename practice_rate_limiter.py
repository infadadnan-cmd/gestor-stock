def get_recent_attempts(attempts, current_time, window) -> list:
    recent_attempts = []
    for attempt in attempts:
        if 0 <= current_time - attempt <= window:
            recent_attempts.append(attempt)
    return recent_attempts


def is_rate_limited(attempts, current_time, window, max_attempts) -> bool:
    recent_attempts = get_recent_attempts(attempts, current_time, window)
    return len(recent_attempts) >= max_attempts


def should_block_request(
    login_attempts: dict,
    client_id: str,
    current_time: float,
    window: float,
    max_attempts: int,
) -> bool:
    client_attempts = login_attempts.get(client_id, [])
    cleanup_old_attempts(client_attempts, current_time, window)
    return is_rate_limited(client_attempts, current_time, window, max_attempts)


def record_failed_attempt(
    login_attempts: dict, client_id: str, current_time: float
) -> None:
    if client_id not in login_attempts:
        login_attempts[client_id] = []
    login_attempts[client_id].append(current_time)


def cleanup_old_attempts(attempts: list, current_time: float, window: float) -> None:
    attempts[:] = [
        attempt for attempt in attempts if 0 <= current_time - attempt <= window
    ]
