def test_save_user_and_check_database(user_repository, connection, user):
    user_repository.save(user)

    row = connection.execute(
        "SELECT id, username, email, password_hash FROM users WHERE email = ?",
        (user.email,),
    ).fetchone()
    assert user.id is not None
    assert row is not None
    assert row["username"] == user.username
    assert row["email"] == user.email
    assert row["password_hash"] == user.password_hash


def test_get_by_email(user_repository, user):
    user_repository.save(user)
    retrieved_user = user_repository.get_by_email(user.email)
    assert retrieved_user is not None
    assert retrieved_user.id == user.id
    assert retrieved_user.username == user.username
    assert retrieved_user.email == user.email
    assert retrieved_user.password_hash == user.password_hash


def test_get_by_email_returns_none_when_user_does_not_exist(user_repository):
    retrieved_user = user_repository.get_by_email("notfound@email.com")

    assert retrieved_user is None
