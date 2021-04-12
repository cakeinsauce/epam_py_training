import pytest
from counter import instances_counter


@instances_counter
class User:
    pass


@pytest.fixture(autouse=True)
def reset_instances_counter():
    User.reset_instances_counter()


def test_no_instances():
    # Testing get_created_instances with no class instances.
    assert User.get_created_instances() == 0


def test_few_instances():
    # Testing get_created_instances with few class instances.
    user, _, _ = User(), User(), User()
    assert user.get_created_instances() == 3


def test_reset_instances_counter_zero():
    # Testing reset_instances_counter with no class instances.
    assert User.get_created_instances() == 0 and User.reset_instances_counter() == 0


def test_reset_instances_counter_few():
    # Testing reset_instances_counter with few class instances.
    user, _, _ = User(), User(), User()
    assert user.reset_instances_counter() == 3 and user.get_created_instances() == 0
