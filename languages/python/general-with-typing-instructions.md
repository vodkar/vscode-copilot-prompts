---
applyTo: "**/*.py"
---

## STRONG TYPING RULES

- ALWAYS ADD **explicit type hints** to:
  - All function arguments and return values
  - All variable declarations where type isn't obvious
- USE BUILT-IN GENERICS:
  - `list`, `dict`, `set`, `tuple` instead of `List`, `Dict`, etc.
  - `type1 | type2` instead of `Union[type1, type2]`
  - `type | None` instead of `Optional[type]`
- PREFER PRECISE TYPES over `Any`; AVOID `Any` UNLESS ABSOLUTELY REQUIRED
- USE:
  - `Final[...]` for constants
  - `ClassVar[...]` for class-level variables shared across instances
  - `Self` for methods that return an instance of the class

## NAMING CONVENTIONS

- USE `snake_case` for variables, function names, and parameters
- USE `PascalCase` for class names
- USE `UPPER_SNAKE_CASE` for constants defined at module-level

## CODE STYLE PRINCIPLES

- USE `f-strings` for all string formatting
- PREFER **list/dict/set comprehensions** over manual loops when constructing collections
- ALWAYS USE `with` context managers for file/resource handling
- NEVER USE `from module import *`; IMPORT ONLY what is needed explicitly
- USE `__` AND `_` prefixes for methods/variables to indicate private/protected scope.
- AVOID DEEP NESTING, prefer early returns and helper functions to flatten logic

## DOCSTRINGS & COMMENTS

- ADD triple-quoted docstrings to all **public functions and classes**
  - USE **Google-style** docstring formatting
  - DESCRIBE parameters, return types, and side effects if any
- OMIT OBVIOUS COMMENTS—CLEAN CODE SHOULD BE SELF-EXPLANATORY

## ERROR HANDLING

- AVOID bare `except:` blocks — ALWAYS CATCH specific exception types
- AVOID using general exceptions like `Exception` or `BaseException`
- FAIL FAST: Validate inputs and raise `ValueError` / `TypeError` when appropriate
- USE `logging.exception()` to log errors with exception stack traces

## LOGGING RULES

- USE the built-in `logging` module—NEVER use `print()` for diagnostics
- USE `logger.exception()` when catching and logging exceptions
- CONFIGURE logging at module or application entry point

## GENERAL INSTRUCTIONS

- ALIGN WITH existing project conventions and patterns
- ALWAYS DOUBLE-CHECK for existing utilities or helpers before creating new ones
- KEEP FUNCTIONS SMALL, focused, and single-purpose
- BREAK complex logic into helper functions
- BE SPECIFIC in handling:
  - Language-level edge cases
  - Algorithmic complexity
  - Domain-specific constraints
- USE `@staticmethod` when instance/class state is not needed
- USE `@classmethod` for alternative constructors or class-level utilities
- FOLLOW the **Zen of Python (PEP 20)** to guide decisions on clarity and simplicity

ENFORCE ALL OF THE ABOVE IN EVERY GENERATED SNIPPET, CLASS, FUNCTION, AND MODULE.
