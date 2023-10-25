Sure, here's an updated `README.md` for your GitHub repository:

```markdown
# Data Engine

This repository contains a Python script `engine.py` and a data model `uniModel`. The engine is designed to manage and manipulate data related to any data model that follows the structure of `uniModel`.

## Features

- The `uniModel` class is an example data model that represents a university with various attributes such as `name`, `type`, `city`, `rank`, and others. It's used to rank universities based on different parameters.
- The `engine.py` script is a generic engine that can work with any data model similar to `uniModel`. It includes methods for handling JSON data, user input, and performing various operations on the data.
- The script provides functionalities to check for missing data, sort, search, modify, delete data and more.

## Usage

```python
from uniModel import uniModel
from engine import engine

# Create an instance of engine
data_engine = engine()

# Run the engine
data_engine.run()
```

```bash
python3 engine.py help
```

## Extending the Engine

You can extend the functionality of the engine by implementing different data classes that follow the structure of `uniModel`. This allows you to use the engine for managing and manipulating different types of data without changing the engine code.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
```

Please replace `[MIT](https://choosealicense.com/licenses/mit/)` with the actual link to your license file if it's not MIT. You can also add more sections like `Installation`, `Tests`, etc. as per your requirements. Let me know if you need help with anything else!