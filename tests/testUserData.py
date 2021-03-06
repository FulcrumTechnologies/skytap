"""Test Skytap Userdata API access."""
import json
import os
import sys

sys.path.append('..')
from skytap.Environments import Environments  # noqa

environments = Environments()
things_to_check = 25


def test_str_vs_contents():
    """Ensure str() returns the contents."""
    count = 0
    for e in environments:
        assert str(e.user_data) == str(e.user_data.contents)
        for v in e.vms:
            if count > things_to_check:
                return
            count += 1
            assert str(v.user_data) == str(v.user_data.contents)


def test_modify_user_data():
    """Use add and delete functions to modify userdata."""

    e = environments.first()
    print('Testing environment: ' + str(e.id) + ': ' + e.name)
    print(e.user_data.add("rick", "sanchez"))
    e.refresh()

    print(e.user_data.add_line("Wubba lubba dub dub!", 0))
    e.refresh()

    assert(e.user_data.data["rick"] == "sanchez")

    print(e.user_data.delete("rick"))
    e.refresh()

    print(e.user_data.delete_line("Wubba lubba dub dub!"))
    e.refresh()
