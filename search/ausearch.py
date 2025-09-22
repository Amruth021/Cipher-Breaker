import heapq, time
from collections import defaultdict

class AuSearchV2:
    def __init__(self, plugins, checker, threshold=0.8, max_depth=4, max_expansions=200):
        self.plugins = plugins
        self.checker = checker
        self.threshold = threshold
        self.max_depth = max_depth
        self.max_expansions = max_expansions

    def search(self, text, top_k=3):
        # pre-check hash
        for p in self.plugins:
            if p.name == "Hash" and p.accepts(text):
                return [(p.transform(text)[0], ["Hash"], 1.0)]

        pq = []
        heapq.heappush(pq, (-self.checker.score(text), text, [], 0))  # priority = -score (max-heap)
        seen = set()
        results = []
        expansions = 0

        while pq and expansions < self.max_expansions:
            neg_priority, current, pipeline, depth = heapq.heappop(pq)
            if (current, tuple(pipeline)) in seen: 
                continue
            seen.add((current, tuple(pipeline)))

            score = self.checker.score(current)
            if score >= self.threshold:
                results.append((current, pipeline, score))
                if len(results) >= top_k:
                    break

            if depth >= self.max_depth:
                continue

            # sort plugins by cheap confidence (and optionally ML guidance)
            candidates = sorted(self.plugins, key=lambda p: -p.confidence(current))
            for plugin in candidates:
                if plugin.name == "Hash": 
                    continue
                if plugin.accepts(current):
                    for out in plugin.transform(current):
                        if not out:
                            continue
                        expansions += 1
                        s = self.checker.score(out)
                        heapq.heappush(pq, (-s, out, pipeline + [plugin.name], depth + 1))
                        if expansions >= self.max_expansions:
                            break
                if expansions >= self.max_expansions:
                    break

        return results  # zero or up to top_k tuples

