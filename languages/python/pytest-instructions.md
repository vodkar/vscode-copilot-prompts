---
applyTo: "test*/**/*.py"
---


APPLY THIS PROMPT ONLY WHEN WRITING PYTHON TESTS. IGNORE `test_writing_prompt` SECTION FOR ALL OTHER PYTHON CODE.

<test_writing_prompt>

### TESTING CONVENTIONS ###

- USE PYTEST AS THE TESTING FRAMEWORK.
- PAY STRICT ATTENTION TO EXISTING FIXTURES AND CONSTANTS AND TESTS.
- DO NOT USE CLASS-BASED TESTS; USE FUNCTION-BASED TESTS.
- NAME test files and functions using `test_*.py` and `test_*`.
- CREATE `__init__.py` files in test directories to ensure they are treated as packages.

### TEST NAMING FORMAT ###

YOU MUST USE THE FOLLOWING CONVENTION FOR TEST FUNCTION NAMES:
`test_<functionality>__<specific_condition>__<expected_outcome>`

- `<functionality>` MUST START WITH `test_` AND DESCRIBE THE HIGH-LEVEL FUNCTIONALITY
- `<specific_condition>` MUST USE PREFIXES LIKE `with_`, `without_`, `on_`, etc.
- `<expected_outcome>` MUST USE VERBS LIKE `returns_`, `raises_`, `creates_`, etc.

EXAMPLES:

- `test_subscribe__on_multiple_handlers__subsribe_all`
- `test_authenticate__on_user_valid_credentials__creates_user`

### PARAMETERIZATION STRATEGY ###

- WHEN TESTING MULTIPLE INPUT VARIANTS, USE `pytest.mark.parametrize` AND `pytest.param`
- EACH PARAM CASE SHOULD BE IDENTIFIED VIA `id=...` FOR READABILITY
- KEEP PARAMETER LOGIC FLAT — AVOID COMPLEX NESTING OR MULTIPLE `if` STATEMENTS
- USE PARAMETERIZED VARIABLES IN THE SETUP AND ASSERTION STEPS CONSISTENTLY

### MOCKING & ASSERTIONS ###

- MOCK DEPENDENCIES USING `MagicMock` OR `AsyncMock`
- USE `assert_called_once_with()` OR `assert_awaited_once_with()` FOR FUNCTION INTERACTIONS
- ASSERT COMPLETE OBJECTS USING `assert object1 == object2` (AVOID FIELD-LEVEL ASSERTIONS)

### DATA REUSE AND FIXTURES ###

- USE CONSTANTS WHEN A VARIABLE IS LIMITED TO THE CURRENT TEST FILE
- USE `pytest.fixture` IF:
  - THE VALUE IS SHARED ACROSS MULTIPLE TEST FUNCTIONS OR FILES
  - IT REQUIRES NESTED FIXTURES OR DEPENDENCY CONFIGURATION
- BEFORE CREATING NEW FIXTURES, ALWAYS **LOOK UP EXISTING ONES**

### CHAIN OF THOUGHTS TO FOLLOW ###

<chain_of_thoughs_rules>
// 1. UNDERSTAND: ANALYZE THE FUNCTION TO BE TESTED AND ITS SIDE EFFECTS
// 2. BASICS: IDENTIFY INPUTS, DEPENDENCIES, AND OUTPUT EXPECTATIONS
// 3. BREAK DOWN: SEPARATE TEST INTO SETUP, CALL, AND ASSERTION PHASES
// 4. ANALYZE: FOR EACH PHASE, DETERMINE MOCK BEHAVIOR AND TEST STRATEGY
// 5. BUILD: USE PARAMETERIZED INPUTS TO COVER VARIANTS; REUSE SETUP LOGIC
// 6. EDGE CASES: CONSIDER BOUNDARIES (e.g., EMPTY LISTS, NONE, ERRORS)
// 7. FINAL ANSWER: OUTPUT A SINGLE VALID PYTEST TEST FUNCTION USING THE TEMPLATE
</chain_of_thoughs_rules>

### WHAT NOT TO DO ###

- DO NOT USE RANDOM OR NON-DETERMINISTIC VALUES WITHOUT SEEDING OR MOCKING
- NEVER NAME TEST FUNCTIONS OUTSIDE THE FORMAT `test_<func>__<condition>__<result>`
- NEVER OMIT SETUP, CALL, OR ASSERTION SECTIONS — ALL THREE MUST EXIST
- DO NOT USE MORE THAN 1 `if` STATEMENT IN PARAMETERIZED TESTS
- AVOID FIELD-BY-FIELD ASSERTIONS WHEN OBJECT-LEVEL COMPARISON IS POSSIBLE
- DO NOT RECREATE FIXTURES IF A SIMILAR ONE ALREADY EXISTS IN THE FILE

### FEW-SHOT EXAMPLES ###

#### ASYNC FUNCTION TEST (PARAMETRIZED)

```python
@pytest.mark.parametrize(
    "email",
    [
        pytest.param("test@test.com", id="test@test.com"),
        pytest.param("tEsT@test.com", id="tEsT@test.com"),
    ],
)
async def test_authenticate__on_user_valid_credentials__creates_user(user_repository: UserRepository, email: str):
    user = User(
        id=uuid4(),
        hashed_password="$some_hash",
        email="test@test.com",
    )
    user_repository.get_by_email = AsyncMock(return_value=user)
    auth_service = AuthenticationService(user_repository=user_repository)

    authenticated_user = await auth_service.authenticate_user(email, "hashed_password")

    assert authenticated_user == user
    user_repository.get_by_email.assert_awaited_once_with("test@test.com")
```

#### SIMPLE FUNCTION TEST (NO PARAMETRIZATION)

```python
class TestEvent(BaseEvent):
    data: str

async def test_subscribe__on_multiple_handlers__subsribe_all():
    async def handler1(event: TestEvent):
        pass

    async def handler2(event: TestEvent):
        pass

    subscribe(TestEvent, handler1)
    subscribe(TestEvent, handler2)

    assert handler1 in _subscribers[TestEvent]
    assert handler2 in _subscribers[TestEvent]
```

</test_writing_prompt>
