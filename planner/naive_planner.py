import numpy as np
from tqdm import tqdm

from data.reader import DataReader
from planner.planner import Planner
from scorer.scorer import Scorer
from utils.graph import Graph


class NaivePlanner(Planner):
    is_parallel = True

    def __init__(self, scorer: Scorer):
        self.scorer = scorer

    def learn(self, train_reader: DataReader, dev_reader: DataReader):
        for i in range(5):
            self.scorer.learn(train_reader, dev_reader)
            if not self.scorer.is_trainable:
                break
        return self

    def score(self, g: Graph, plan: str):
        return self.scorer.score(plan)

    def plan_best(self, g: Graph, ranker_plans=None):
        if ranker_plans:
            all_plans = list(set(ranker_plans))
        else:
            all_plans = list(self.plan_all(g))

        best_plan = ""
        best_plan_score = 0

        for plan in tqdm(all_plans):
            score = self.scorer.score(plan)
            if score > best_plan_score:
                best_plan_score = score
                best_plan = plan

        return best_plan
