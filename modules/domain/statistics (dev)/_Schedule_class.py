class MakeStata:
    def __init__(self, list_of_values: list, time_slise: str) -> None:
        self.value_of_division: int | None = None
        self.values: list = list_of_values

        self.time_slise = time_slise

        self.width: int = len(sorted(map(str, list_of_values), key=lambda v: len(v), reverse=True)[0])
        self.spread: int | None = None

        self.vertical: list | None = None

        self.result: str = ""

    def count_sizes(self):
        self.spread = max(self.values) - min(self.values)
        self.value_of_division = (self.spread // 8)
        self.vertical = [self.value_of_division * i for i in range(9, 0, -1)] + [0]

    @property
    def build_top(self):
        return f"[Сообщения]|{('-'*(self.width + 2))*len(self.values)}|\n"

    def build_middle(self, value: int):
        a = f"[{'-' * ((9 - len(str(value))) // 2)}{'0' * ((9 - len(str(value))) % 2)}{value}{'-' * ((9 - len(str(value))) // 2)}]|"
        b = "".join([
            f"[{'#' * self.width if v > value + self.value_of_division else '0' * (self.width - len(str(v))) + str(v)}]"
            if v >= value else "-" * (self.width + 2) for v in self.values
        ])
        return a + b + "|\n"

    @property
    def build_bottom(self):
        half = ""*(self.width // 2) if self.width > 3 else ""
        whole = (self.width // 2) * 2 if self.width > 3 else self.width

        a = 9 - len(self.time_slise)
        res = ["[" + " "*(a//2) + self.time_slise + " "*(a//2 + a%2) + "]", "|"]
        res += ["[" + half + f"{'0'*(whole-len(str(i)))}{i}" + half + "]" for i in range(1, self.horizontal_size + 1)]
        return "".join(res + ["|"])

    def build_graph(self):
        self.result += self.build_top
        for value in self.vertical:
            self.result += self.build_middle(value=value)
        self.result += self.build_bottom

        return self.result

    @property
    def horizontal_size(self):
        return len(self.values)
