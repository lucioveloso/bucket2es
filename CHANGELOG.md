Version 0.0.2

  * Removed the cloudformation from the lambda folder.
  * Reorganized the project following the standard:
  ```
    utils/
    src/
    ├── cmdlinetest
    ├── main
    │   └── python
    │       └── bucket2es
    └── unittest
        └── python
  ```

  * Python unit tests using `unitest2` and `nosetests`.
  * CLI tests using `cram`.
  * Add the "uninstall.sh" to remove the stack via CLI.

  - Bug str/unicode (validate_json())

Version 0.0.1

  * Initial Version