from __future__ import annotations

from dataclasses import dataclass
from math import inf
from typing import Mapping


@dataclass
class _Edge:
    to: int
    rev: int
    cap: int
    cost: int


def _max_cardinality(
    gold_count: int,
    actual_count: int,
    scores: Mapping[tuple[int, int], int],
) -> int:
    adjacency: list[list[int]] = [[] for _ in range(gold_count)]
    for gold_index, actual_index in sorted(scores):
        adjacency[gold_index].append(actual_index)

    actual_to_gold: dict[int, int] = {}

    def augment(gold_index: int, seen: set[int]) -> bool:
        for actual_index in adjacency[gold_index]:
            if actual_index in seen:
                continue
            seen.add(actual_index)
            owner = actual_to_gold.get(actual_index)
            if owner is None or augment(owner, seen):
                actual_to_gold[actual_index] = gold_index
                return True
        return False

    cardinality = 0
    for gold_index in range(gold_count):
        if augment(gold_index, set()):
            cardinality += 1
    return cardinality


def _optimal_assignment(
    gold_count: int,
    actual_count: int,
    scores: Mapping[tuple[int, int], int],
    forbidden: frozenset[tuple[int, int]] = frozenset(),
) -> tuple[dict[int, int], tuple[int, int]]:
    allowed = {
        pair: score
        for pair, score in scores.items()
        if pair not in forbidden
    }
    target_flow = _max_cardinality(gold_count, actual_count, allowed)
    if target_flow == 0:
        return {}, (0, 0)

    source = 0
    gold_offset = 1
    actual_offset = gold_offset + gold_count
    sink = actual_offset + actual_count
    node_count = sink + 1
    graph: list[list[_Edge]] = [[] for _ in range(node_count)]
    pair_edges: dict[tuple[int, int], _Edge] = {}

    def add_edge(source_node: int, target_node: int, capacity: int, cost: int) -> _Edge:
        forward = _Edge(target_node, len(graph[target_node]), capacity, cost)
        reverse = _Edge(source_node, len(graph[source_node]), 0, -cost)
        graph[source_node].append(forward)
        graph[target_node].append(reverse)
        return forward

    for gold_index in range(gold_count):
        add_edge(source, gold_offset + gold_index, 1, 0)
    for actual_index in range(actual_count):
        add_edge(actual_offset + actual_index, sink, 1, 0)
    for (gold_index, actual_index), score in sorted(allowed.items()):
        pair_edges[(gold_index, actual_index)] = add_edge(
            gold_offset + gold_index,
            actual_offset + actual_index,
            1,
            -score,
        )

    flow = 0
    while flow < target_flow:
        distance = [inf] * node_count
        previous: list[tuple[int, int] | None] = [None] * node_count
        distance[source] = 0

        for _ in range(node_count - 1):
            changed = False
            for source_node in range(node_count):
                if distance[source_node] == inf:
                    continue
                for edge_index, edge in enumerate(graph[source_node]):
                    if edge.cap <= 0:
                        continue
                    candidate = distance[source_node] + edge.cost
                    if candidate < distance[edge.to]:
                        distance[edge.to] = candidate
                        previous[edge.to] = (source_node, edge_index)
                        changed = True
            if not changed:
                break

        if previous[sink] is None:
            raise RuntimeError("maximum-cardinality assignment became unreachable")

        node = sink
        while node != source:
            source_node, edge_index = previous[node]
            edge = graph[source_node][edge_index]
            edge.cap -= 1
            graph[node][edge.rev].cap += 1
            node = source_node
        flow += 1

    assignment = {
        gold_index: actual_index
        for (gold_index, actual_index), edge in pair_edges.items()
        if edge.cap == 0
    }
    total_score = sum(scores[(gold_index, actual_index)] for gold_index, actual_index in assignment.items())
    return assignment, (len(assignment), total_score)


def forced_optimal_pairs(
    gold_count: int,
    actual_count: int,
    scores: Mapping[tuple[int, int], int],
) -> dict[int, int]:
    """Return only pairs forced by every globally optimal assignment.

    Optimization is lexicographic: maximize eligible one-to-one cardinality,
    then maximize total semantic score. A pair is accepted only if forbidding
    it worsens that global optimum. Therefore list order cannot resolve a
    global ambiguity.
    """
    representative, optimum = _optimal_assignment(gold_count, actual_count, scores)
    forced: dict[int, int] = {}
    for gold_index, actual_index in representative.items():
        _, alternative = _optimal_assignment(
            gold_count,
            actual_count,
            scores,
            forbidden=frozenset({(gold_index, actual_index)}),
        )
        if alternative < optimum:
            forced[gold_index] = actual_index
    return forced
