DEBUG = False


class Node:
        def __init__(self,
                     val,
                     parent= None,
                     is_termial=False):
            self.val = val
            self.next = dict()
            self.parent = parent
            self.is_terminal = is_termial
            self.word = ""
            self.link = None
            self.word_link = None
            self.moves = dict()

        def get_link(self):
            if self.link is not None:
                if DEBUG:
                    print(f"Ссылка для узла '{self.val}' уже вычислена: {self.link.val}")
                return self.link
            if self.val is None:
                self.link = self
                if DEBUG:
                    print(f"Узел '{self.val}' является корневым, ссылка на себя")
            elif self.parent.val is None:
                self.link = self.parent
                if DEBUG:
                    print(f"Узел '{self.val}' является дочерним корня, ссылка на корень")
            else:
                if DEBUG:
                    print(f"Вычисление ссылки для узла '{self.val}' через родителя '{self.parent.val}'")
                self.link = self.parent.get_link().get_move(self.val)
                if DEBUG:
                    print(f"Ссылка для узла '{self.val}' установлена на '{self.link.val}'")
            return self.link

        def get_move(self, c):
            if self.moves.get(c, None) is not None:
                if DEBUG:
                    print(f"Переход по символу '{c}' из узла '{self.val}' уже вычислен: {self.moves[c].val}")
                return self.moves[c]
            if self.next.get(c, None) is not None:
                self.moves[c] = self.next[c]
                if DEBUG:
                    print(f"Переход по символу '{c}' из узла '{self.val}' найден: {self.moves[c].val}")
            elif self.val is not None:
                if DEBUG:
                    print(f"Переход по символу '{c}' из узла '{self.val}' не найден, вычисление через ссылку")
                self.moves[c] = self.get_link().get_move(c)
                if DEBUG:
                    print(f"Переход по символу '{c}' из узла '{self.val}' установлен на '{self.moves[c].val}'")
            else:
                self.moves[c] = self
                if DEBUG:
                    print(f"Узел '{self.val}' является корневым, переход по символу '{c}' на себя")
            return self.moves[c]

        def get_word_link(self):
            if self.word_link is not None:
                if DEBUG:
                    print(f"Ссылка на слово для узла '{self.val}' уже вычислена: {self.word_link.val}")
                return self.word_link
            link = self.get_link()
            if DEBUG:
                print(f"Вычисление ссылки на слово для узла '{self.val}' через ссылку '{link.val}'")
            if link.val is None or link.is_terminal:
                self.word_link = link
                if DEBUG:
                    print(f"Ссылка на слово для узла '{self.val}' установлена на '{self.word_link.val}'")
            else:
                if DEBUG:
                    print(f"Рекурсивное вычисление ссылки на слово для узла '{self.val}'")
                self.word_link = link.get_word_link()
                if DEBUG:
                    print(f"Ссылка на слово для узла '{self.val}' установлена на '{self.word_link.val}'")
            return self.word_link


class Vertex:
    def __init__(self):
        self._root = Node(None)
        self._words = dict()
        self._len = 0

    def __len__(self):
        return self._len

    def append(self, word):
        if word in self._words:
            if DEBUG:
                print(f"Слово '{word}' уже добавлено, пропуск")
            return
        node = self._root
        if DEBUG:
            print(f"Добавление слова '{word}'")
        for letter in word:
            next_node = node.next.get(letter, None)
            if next_node:
                if DEBUG:
                    print(f"Переход по символу '{letter}' из узла '{node.val}'")
                node = next_node
            else:
                if DEBUG:
                    print(f"Создание нового узла для символа '{letter}' в узле '{node.val}'")
                node.next[letter] = Node(letter)
                node.next[letter].parent = node
                node = node.next[letter]
        node.is_terminal = True
        node.word = word
        self._len += 1
        self._words[word] = self._len
        if DEBUG:
            print(f"Слово '{word}' добавлено, терминальный узел: '{node.val}'")

    def extend(self, words):
        if DEBUG:
            print(f"Добавление списка слов: {words}")
        for word in words:
            self.append(word)

    def find(self, text):
        if DEBUG:
            print(f"Поиск в тексте: '{text}'")
        node = self._root
        answer = []
        for i, c in enumerate(text):
            if DEBUG:
                print(f"Обработка символа '{c}' на позиции {i}")
            node = node.get_move(c)
            if node.val is None:
                if DEBUG:
                    print(f"Узел '{node.val}' является корневым, пропуск")
                continue
            if node.is_terminal:
                if DEBUG:
                    print(f"Найден терминальный узел '{node.val}' для слова '{node.word}'")
                answer.append((i + 2 - len(node.word), self._words[node.word]))
            u = node.get_word_link()
            while u.val is not None:
                if DEBUG:
                    print(f"Переход по ссылке на слово для узла '{u.val}'")
                answer.append((i + 2 - len(u.word), self._words[u.word]))
                u = u.get_word_link()
        if DEBUG:
            print(f"Результат поиска: {answer}")
        return sorted(answer)

    def max_outgoing_edges(self):
        max_edges = 0
        queue = [self._root]
        visited = set()

        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            edges = len(node.next)
            max_edges = max(max_edges, edges)
            if DEBUG:
                print(f"Узел '{node.val}' имеет {edges} исходящих дуг")
            queue.extend(node.next.values())

        if DEBUG:
            print(f"Максимальное количество исходящих дуг: {max_edges}")
        return max_edges

    def remove_patterns(self, text):
        matches = self.find(text)
        if not matches:
            if DEBUG:
                print(f"Образцы не найдены, возвращается исходная строка: '{text}'")
            return text

        ban = set()
        for m in matches:
            y = 0
            for k, v in self._words.items():
                if m[1] == v:
                    y = k
                    break
            ban |= set(range(m[0] - 1, m[0] + len(y) - 1))
        return "".join(text[i] for i in range(len(text)) if i not in ban)


T = input()
n = int(input())
P = [input() for _ in range(n)]
vertex = Vertex()
vertex.extend(P)

for include in vertex.find(T):
    print(include[0], include[1])

print(vertex.max_outgoing_edges())
print(vertex.remove_patterns(T))
