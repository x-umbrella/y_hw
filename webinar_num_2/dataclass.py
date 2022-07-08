from dataclasses import dataclass, asdict, astuple


@dataclass(frozen=True)
class PersonD:
    full_name: str
    age: int = 1

    def demo(self, other) -> bool:
        return self.age > other.age


class Person:
    def __init__(self, full_name: str, age: int = 1) -> None:
        self.full_name = full_name
        self.age = age

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(full_name='{self.full_name}', age={self.age}, {self.email})"

    def __lt__(self, other: PersonD) -> bool:
        return self.age < other.age


person1 = Person(full_name="Alex", age=26)
person2 = PersonD(full_name="Oleg", age=27)
print(person1)
print(person2)
