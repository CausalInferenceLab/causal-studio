"""Load scenes for the ko edition for existing Manim commands."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from videos.why_causal_inference.ko.scenes import (
    scene_01_why_causal_questions_matter,
    scene_02_association_is_not_causation,
    scene_03_counterfactual_worlds,
    scene_04_multiverse_ite_ate_att,
    scene_05_multiverse_table_ate_att,
    scene_06_observed_mean_difference_trap,
    scene_07_bias_decomposition,
    scene_08_when_association_becomes_causation,
    scene_09_randomized_experiment,
    scene_10_online_classroom_rct,
    scene_11_rct_limits_and_beyond,
)


class Scene01_WhyCausalQuestionsMatter(scene_01_why_causal_questions_matter.Scene01_WhyCausalQuestionsMatter):
    pass


class Scene02_AssociationIsNotCausation(scene_02_association_is_not_causation.Scene02_AssociationIsNotCausation):
    pass


class Scene03_CounterfactualWorlds(scene_03_counterfactual_worlds.Scene03_CounterfactualWorlds):
    pass


class Scene04_MultiverseIteAteAtt(scene_04_multiverse_ite_ate_att.Scene04_MultiverseIteAteAtt):
    pass


class Scene05_MultiverseTableAteAtt(scene_05_multiverse_table_ate_att.Scene05_MultiverseTableAteAtt):
    pass


class Scene06_ObservedMeanDifferenceTrap(scene_06_observed_mean_difference_trap.Scene06_ObservedMeanDifferenceTrap):
    pass


class Scene07_BiasDecomposition(scene_07_bias_decomposition.Scene07_BiasDecomposition):
    pass


class Scene08_WhenAssociationBecomesCausation(scene_08_when_association_becomes_causation.Scene08_WhenAssociationBecomesCausation):
    pass


class Scene09_RandomizedExperiment(scene_09_randomized_experiment.Scene09_RandomizedExperiment):
    pass


class Scene10_OnlineClassroomRCT(scene_10_online_classroom_rct.Scene10_OnlineClassroomRCT):
    pass


class Scene11_RctLimitsAndBeyond(scene_11_rct_limits_and_beyond.Scene11_RctLimitsAndBeyond):
    pass
