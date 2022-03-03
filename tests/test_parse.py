import parse


def test_extract_hash_block():
    t = """# \n# Hey\n# This one is simple\n#  - Right?\n# \nfrom code import test\n\nprint('working')\n"""
    assert parse.extract_hash_block(t) == "Hey\nThis one is simple\n - Right?"

    t = """# \n# Another\n# One.\n# """
    assert parse.extract_hash_block(t) == "Another\nOne."

    t = """no comment\at all."""
    assert parse.extract_hash_block(t) == ""

    t = """"""
    assert parse.extract_hash_block(t) == ""


def test_extract_string_block():
    t = '''"""This\nis\na\ntest"""'''
    assert parse.extract_string_block(t) == "This\nis\na\ntest"

    t = '''from badstuff import first"""Here"""'''
    assert parse.extract_string_block(t) == ""

    t = '''"""\n This\n is\n a\n test\n """'''
    assert parse.extract_string_block(t) == "\n This\n is\n a\n test\n "

    t = """no comment\at all."""
    assert parse.extract_string_block(t) == ""

    t = """"""
    assert parse.extract_string_block(t) == ""


def test_extract_imports():
    t = """import dog\nimport log\nfrom sink import water"""
    assert parse.extract_imports(t) == {"dog": ["*"], "log": ["*"], "sink": ["water"]}

    t = """from home import food\nfrom dog import cat\nimport stuff"""
    assert parse.extract_imports(t) == {
        "home": ["food"],
        "dog": ["cat"],
        "stuff": ["*"],
    }

    t = """def rando_func():\n    from bank import money\n\timport dog"""
    assert parse.extract_imports(t) == {"bank": ["money"], "dog": ["*"]}

    t = """from pet.dog import poodle"""
    assert parse.extract_imports(t) == {"pet": ["poodle"]}
    assert parse.extract_imports(t, False) == {"pet.dog": ["poodle"]}


def test_infer_local_modules():
    output = parse.infer_local_modules(
        included=("src/parse.py", "src/dog.py", "src/pet/cat.py")
    )
    assert output == [
        "src/parse.py",
        "src/dog.py",
        "src/pet/cat.py",
    ]

    output = parse.infer_local_modules(
        included=("src/parse.py", "src/dog.py", "src/pet/cat.py"), excluded=("parse.py")
    )
    assert output == ["src/dog.py", "src/pet/cat.py"]


def test_infer_module_name():
    t = "dog.py"
    assert parse.infer_module_name(t) == "dog"

    t = "src/dog.py"
    assert parse.infer_module_name(t) == "dog"

    t = "./src/pets/dog.py"
    assert parse.infer_module_name(t) == "dog"


def test_extract_module_info(test_module):
    expected = parse.ModuleInfo(
        name="test",
        internal_mods={},
        external_mods={"pets": ["dog"], "toys": ["*"]},
        description="Test file\nDescription of test file",
        path="/mnt/c/Users/steph/Projects/mud/tests/src/test.py",
    )
    assert parse.extract_module_info(test_module) == expected

    expected = parse.ModuleInfo(
        name="test",
        internal_mods={"toys": ["*"]},
        external_mods={"pets": ["dog"]},
        description="Test file\nDescription of test file",
        path="/mnt/c/Users/steph/Projects/mud/tests/src/test.py",
    )
    assert parse.extract_module_info(test_module, ["./src/toys.py"]) == expected