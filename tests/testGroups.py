import json
import nose
import os
import sys
import uuid

sys.path.append('..')
from skytap.Groups import Groups  # nopep8
from skytap.Users import Users  # nopep8
groups = Groups()


def test_group_list():
    """Ensure we have some users."""
    assert len(groups) > 0, 'User list is empty.'


def test_group_id():
    """Ensure user has id."""
    for l in list(groups.data):
        g = groups[l]
        assert g.id > 0


def test_user_details():
    """Ensure user has details()."""
    for l in list(groups.data):
        g = groups[l]
        assert len(g.details()) > 0


def test_user_count_matches():
    """Make sure the user list counts match.

    Groups come in with a user_count and a list of users. Make sure these
    match.
    """
    for l in list(groups.data):
        g = groups[l]
        msg = ('Checking group ' + str(g.id) + ': ' + g.name + ' ['
               'Reported: ' + str(g.user_count) + ', '
               'Actual: ' + str(len(g.users)) + ']')
        assert g.user_count == len(g.users), msg


def test_group_str_conversion():
    """Ensure user string conversion works."""
    for l in list(groups.data):
        g = groups[l]
        assert len(str(g)) > 0


def test_group_module_main():
    ret = json.loads(groups.main([]))
    assert len(ret) == len(groups.data)


def test_group_main_good_group():
    group = list(groups.data)[0]
    ret = json.loads(groups.main([groups[group].id]))
    assert groups[group].id == ret[0]['id']


def test_group_main_bad_group():
    group = 'not a group'
    ret = json.loads(groups.main([group]))
    assert len(ret) == 0


def test_group_creation():
    """Create, modify, and delete a group."""
    name = str(uuid.uuid4())
    description = 'Group creation test.'
    group = groups.add(name, description)
    assert groups[group].name == name
    user = Users().first()
    assert groups[group].add_user(user.id)
    assert groups.delete(groups[group])
    access_deleted_group(group)


@nose.tools.raises(KeyError)
def access_deleted_group(group):
    det = groups[group].name