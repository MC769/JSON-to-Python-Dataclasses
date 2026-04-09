


# 🚀 json2py - JSON to Python Dataclasses

**Stop writing Python classes by hand. Generate them from JSON in 1 second.**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://python.org)

## ⚡ Quick Demo

```bash
$ echo '{"name": "John", "age": 30, "email": "john@example.com"}' > user.json
$ python json2py.py user.json --output user.py

✅ Generated: user.py
📦 Root class: User
📝 Lines of code: 28
```

## 🎯 Why Use This?

| Without json2py | With json2py |
|----------------|--------------|
| ❌ Manual class writing | ✅ Automatic generation |
| ❌ Easy to miss fields | ✅ Complete type hints |
| ❌ No nested class handling | ✅ Auto-creates nested classes |
| ❌ 10 minutes of work | ✅ 1 second |

## 📦 Installation

```bash
# Clone and run locally
git clone https://github.com/YOUR_USERNAME/json2py
cd json2py
python json2py.py input.json
```

## 🚀 Usage

### Basic Usage
```bash
# Generate from JSON file
python json2py.py response.json

# Specify output file
python json2py.py response.json --output models.py

# Use with API response
curl https://api.github.com/users/octocat | python json2py.py --output github_user.py
```

## ✨ Features

| Feature | Status |
|---------|--------|
| 🏗️ Dataclasses | ✅ |
| 🔄 Nested Objects | ✅ |
| 📝 Type Hints | ✅ |
| 📅 DateTime Detection | ✅ |
| 📋 Lists | ✅ |
| 🔧 from_dict() method | ✅ |
| 📤 to_dict() method | ✅ |

## 📖 Example

**Input JSON** (`sample.json`):
```json
{
  "user_id": 123,
  "full_name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "profile": {
    "avatar_url": "https://example.com/avatar.jpg",
    "bio": "Python developer",
    "followers": 1234
  },
  "tags": ["python", "opensource", "developer"]
}
```

**Run command:**
```bash
python json2py.py sample.json --output models.py
```

**Generated Python** (`models.py`):
```python
from dataclasses import dataclass
from typing import List

@dataclass
class Profile:
    avatar_url: str
    bio: str
    followers: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class Sample:
    user_id: int
    full_name: str
    email: str
    is_active: bool
    profile: Profile
    tags: List[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
```

**Use in your code:**
```python
from models import Sample
import json

# Load JSON
with open('response.json') as f:
    data = json.load(f)

# Convert to Python object
user = Sample.from_dict(data)
print(user.full_name)  # John Doe
print(user.profile.bio)  # Python developer

# Convert back to dict
user_dict = user.to_dict()
```

## 🛠️ Development

### Run Locally
```bash
[git clone https://github.com/MC769/json2p](https://github.com/MC769/JSON-to-Python-Dataclasses.git)
cd json2py
python json2py.py examples/sample.json
```

## 🤝 Contributing

1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

## ⭐ Show Your Support

**If this saved you time, please star the repo!**

[![Star on GitHub](https://img.shields.io/github/stars/MC769/JSON-to-Python-Dataclasses?style=social)](https://github.com/MC769/JSON-to-Python-Dataclasses)

