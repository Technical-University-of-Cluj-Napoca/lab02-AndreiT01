from urllib.request import urlopen
class Node :
    def __init__(self,word: str):
        self.word = word
        self.left = None
        self.right = None

class BST :
    def __init__(self, source:str, **kargs):
        is_url = bool(kargs.get("url", False))
        is_file = bool(kargs.get("file", False))

        if is_url == is_file:
            raise ValueError("Cannot be both url and file")
        
        if is_url:
            with urlopen(source) as r:
                words = r.read().decode("utf-8", errors="ignore").splitlines()  
        else: 
            with open(source, "r", encoding="utf-8", errors="ignore") as f:
                words = f.read().splitlines()

        words = sorted({w.strip().lower() for w in words if w.strip()})

        def build(lo: int, hi: int) -> Node | None:
            if lo>hi:
                return None
            mid = (lo + hi) // 2
            node = Node(words[mid])
            node.left = build(lo,mid-1)
            node.right = build(mid + 1 , hi)
            return node
        
        self.root = build(0, len(words) - 1)
        self.result = []
    
    def autocomplete(self, prefix:str)->list[str]:
        self.result = []
        if not prefix :
            return self.result
        p = prefix.lower()
        upper = p + "\uffff"
        _collect(self.root, p)
        return self.result

    def _collect(self, node: Node, prefix:str) ->None:
        if node is None:
            return
        if node.word >=prefix:
            _collect(node.left, prefix)
        if prefix <= node.word:
            _collect(node.right,prefix)
        if node.word.startswith(prefix):
            self.result.append(node.word)