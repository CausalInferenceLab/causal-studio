# Sharp to fuzzy at the same cutoff

The last comparison in scene 1 shows why crossing the cutoff can change treatment probability by less than 100 percentage points. The score axis, probability scale, and 370 cutoff stay fixed. The lines for scores below and above 370 keep their colors as the gap shrinks from 0% → 100% to 15% → 65%.

- [3Blue1Brown, `TransitionToSkewDistribution.construct`](https://github.com/3b1b/videos/blob/31f8ffe/_2023/clt/main.py#L815) transforms a plot in the same region and replaces the probability labels in the same beat. This scene applies that technique to the two line segments, endpoint markers, and numeric labels.
- [`BayesDiagram.general_set_likelihood`](https://github.com/3b1b/videos/blob/31f8ffe/_2019/bayes/part1.py#L179) shows probability changing in anchored geometry. Here, probability already has a natural y-axis and the excess motion of a separate area diagram would obscure the cutoff.
- [`TalkAboutSignOfConstant3D`](https://github.com/3b1b/videos/blob/31f8ffe/_2023/gauss_int/herschel.py#L1176) connects a surface to a changing cross-section. This comparison uses one input and one probability axis, so it uses a fixed two-dimensional view.

The transform takes place inside the existing penultimate narration beat, from 47.462s to 55.310s in Korean and 40.356s to 46.997s in English. The narrated values appear beside the markers and then hold before the closing question. The [Manim CE implementation](recap.py) is shared by both editions.
