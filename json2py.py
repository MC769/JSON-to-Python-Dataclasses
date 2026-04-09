
"""
json2py - Convert JSON to Python Dataclasses instantly
Fixed version with proper nested class support
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

def to_snake_case(name: str) -> str:
    """Convert CamelCase or kebab-case to snake_case"""
    name = name.replace("-", "_")
    result = []
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            result.append('_')
        result.append(char.lower())
    return ''.join(result)

def to_pascal_case(name: str) -> str:
   
    return ''.join(word.capitalize() for word in name.split('_'))

def get_python_type(value: Any) -> tuple[str, set]:
   
    imports = set()
    
    if isinstance(value, bool):
        return "bool", imports
    elif isinstance(value, int):
        return "int", imports
    elif isinstance(value, float):
        return "float", imports
    elif isinstance(value, str):
        # Check if it looks like ISO datetime
        if 'T' in value and (value.count('-') >= 2 or value.count(':') >= 2):
            imports.add("from datetime import datetime")
            return "datetime", imports
        return "str", imports
    elif isinstance(value, list):
        if not value:
            imports.add("from typing import List, Any")
            return "List[Any]", imports
        
        
        element_type, element_imports = get_python_type(value[0])
        imports.update(element_imports)
        
        
        all_same = all(type(item) == type(value[0]) for item in value)
        if all_same and element_type not in ["Any", "dict"]:
            imports.add("from typing import List")
            return f"List[{element_type}]", imports
        else:
            imports.add("from typing import List, Any")
            return "List[Any]", imports
    elif value is None:
        imports.add("from typing import Optional")
        return "Optional[Any]", imports
    else:
        imports.add("from typing import Any")
        return "Any", imports

def dict_to_dataclass(class_name: str, data: Dict, all_classes: Dict[str, str]) -> str:
    
    
    imports = set()
    fields = []
    
    for key, value in data.items():
        field_name = to_snake_case(key)
        
        if isinstance(value, dict):
           
            nested_class_name = to_pascal_case(field_name)
            field_type = nested_class_name
            
           
            if nested_class_name not in all_classes:
                nested_code = dict_to_dataclass(nested_class_name, value, all_classes)
                all_classes[nested_class_name] = nested_code
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            
            nested_class_name = to_pascal_case(field_name.rstrip('s'))
            field_type = f"List[{nested_class_name}]"
            imports.add("from typing import List")
            
            
            if nested_class_name not in all_classes and value[0]:
                nested_code = dict_to_dataclass(nested_class_name, value[0], all_classes)
                all_classes[nested_class_name] = nested_code
        else:
            # Primitive type or simple list
            field_type, type_imports = get_python_type(value)
            imports.update(type_imports)
        
        # Handle None values
        if value is None:
            field_type = f"Optional[{field_type}]"
            imports.add("from typing import Optional")
        
        fields.append(f"    {field_name}: {field_type}")
    
    # Build the dataclass
    imports_str = "\n".join(sorted(imports)) if imports else ""
    if imports_str:
        imports_str += "\n\n"
    
    fields_str = "\n".join(fields)
    
    return f"""{imports_str}@dataclass
class {class_name}:
{fields_str}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
    
    def to_dict(self):
        return {{k: v for k, v in self.__dict__.items() if v is not None}}
"""

def generate_python_code(data: Dict, root_name: str) -> str:
    """Generate complete Python code from JSON data"""
    
    all_classes = {}
    root_class = dict_to_dataclass(to_pascal_case(root_name), data, all_classes)
    
    # Build the complete file
    imports = "from dataclasses import dataclass\n"
    imports += "from typing import Any, Dict, List, Optional\n\n"
    
    # Add all nested classes first, then the root class
    result = imports
    for class_code in all_classes.values():
        result += class_code + "\n\n"
    result += root_class
    
    return result

def main():
    if len(sys.argv) < 2:
        print("❌ Usage: python json2py.py <input.json> [--output output.py]")
        print("\nExample:")
        print("  python json2py.py user.json")
        print("  python json2py.py api-response.json --output models.py")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "models.py"
    
    # Parse --output flag
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    # Read JSON
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)
    
  
    root_name = Path(input_file).stem
    python_code = generate_python_code(data, root_name)
    

    with open(output_file, 'w') as f:
        f.write(python_code)
    
    print(f"✅ Generated: {output_file}")
    print(f"📦 Root class: {to_pascal_case(root_name)}")
    
    # Count classes
    class_count = python_code.count("@dataclass")
    print(f"📚 Total classes: {class_count}")
    
    # Count lines
    lines = len(python_code.split('\n'))
    print(f"📝 Lines of code: {lines}")

if __name__ == "__main__":
    main()
