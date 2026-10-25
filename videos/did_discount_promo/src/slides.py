"""교육용 가상 수치로 DID 영상 초안의 다섯 화면을 만든다."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build" / "slides"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({
    "font.family": "AppleGothic",
    "axes.unicode_minus": False,
    "axes.facecolor": "#0D0F1F",
    "text.color": "#FFFFFF",
    "xtick.color": "#9CA3AF",
    "ytick.color": "#9CA3AF",
    "axes.edgecolor": "#374151",
})

# Causal Studio의 RDD/Fuzzy RDD 팔레트와 AppleGothic 글꼴을 따른다.
BG = "#0D0F1F"
BLUE = "#4DD0C4"     # 기획전 참여군 (처치)
GREEN = "#8AA6B2"    # 대조군
ORANGE = "#C8A630"   # 기획전이 없었다면 (반사실)
RED = "#EF4444"      # 추정 순증분
INK = "#FFFFFF"
MUTED = "#9CA3AF"


def canvas(number, title):
    fig = plt.figure(figsize=(12.8, 7.2), facecolor=BG)
    fig.text(.055, .93, f"{number:02d}  {title}", fontsize=31, weight="bold", color=INK)
    fig.text(.055, .055, "예약 서비스의 할인 기획전 / 교육용 가상 수치", fontsize=14, color=MUTED)
    return fig


def save(fig, number):
    fig.savefig(OUT / f"{number:02d}.png", dpi=120, facecolor=fig.get_facecolor())
    plt.close(fig)


fig = canvas(1, "기획전 덕분에 늘어난 예약은?")
fig.text(.10, .63, "참여 매장 100곳", fontsize=27, color=MUTED)
fig.text(.10, .39, "2주 동안 12,000건", fontsize=48, weight="bold", color=BLUE)
fig.text(.72, .40, "?", fontsize=115, weight="bold", color=ORANGE)
save(fig, 1)

fig = canvas(2, "전후 차이가 곧 효과일까?")
ax = fig.add_axes([.12, .23, .56, .56])
ax.bar([0, 1], [10000, 12000], width=.38, color=["#536170", BLUE])
ax.set_xticks([0, 1], ["기획전 이전 2주", "기획전 진행 2주"], fontsize=18)
ax.set_ylim(0, 14500)
ax.set_yticks([])
ax.spines[:].set_visible(False)
for i, v in enumerate([10000, 12000]):
    ax.text(i, v + 420, f"{v:,}건", ha="center", fontsize=24, color=INK)
fig.text(.72, .50, "+2,000건?", fontsize=27, color=ORANGE, weight="bold")
fig.text(.72, .35, "원래 늘었을 수도\n있지 않을까?", fontsize=19, color=MUTED)
save(fig, 2)

fig = canvas(3, "대조군의 변화도 살펴보자")
ax = fig.add_axes([.12, .23, .76, .55])
x = np.array([0, 1])
ax.plot(x, [10000, 12000], color=BLUE, marker="o", lw=5, ms=13)
ax.plot(x, [8000, 9000], color=GREEN, marker="o", lw=5, ms=13)
ax.set_xlim(-.15, 1.15)
ax.set_ylim(6800, 13500)
ax.set_xticks(x, ["이전 2주", "진행 2주"], fontsize=18)
ax.set_yticks([])
ax.spines[:].set_visible(False)
ax.text(.42, 12200, "참여군  +2,000", fontsize=23, color=BLUE)
ax.text(.05, 7200, "대조군  +1,000", fontsize=23, color=GREEN)
save(fig, 3)

pre_t = np.array([4500, 4900, 4700, 5200, 4900, 5100])
pre_c = np.array([3400, 3900, 3650, 4150, 3900, 4100])
fig = canvas(4, "좋은 대조군을 골랐을까?")
ax = fig.add_axes([.11, .31, .77, .47])
ax.plot(range(6), pre_t, color=BLUE, marker="o", lw=4, ms=10, label="기획전 참여 매장")
ax.plot(range(6), pre_c, color=GREEN, marker="o", lw=4, ms=10, label="대조군")
ax.set_ylim(3000, 5700)
ax.set_yticks([])
ax.set_xticks(range(6), ["6주 전", "5주 전", "4주 전", "3주 전", "2주 전", "직전 주"], fontsize=16)
ax.spines[:].set_visible(False)
ax.legend(frameon=False, ncol=2, fontsize=17, loc="upper left")
fig.text(.11, .18, "평행추세 가정: 기획전이 없었다면 변화도 비슷했을까?", fontsize=20, color=ORANGE)
save(fig, 4)

t = np.r_[pre_t, 5900, 6100]
c = np.r_[pre_c, 4400, 4600]
cf = np.array([5400, 5600])
assert t[-2:].sum() == 12000 and cf.sum() == 11000
assert (t[-2:].sum() - pre_t[-2:].sum()) - (c[-2:].sum() - pre_c[-2:].sum()) == 1000
fig = canvas(5, "두 변화의 차이가 기획전의 순증분")
ax = fig.add_axes([.075, .22, .61, .57])
ax.axvspan(5.5, 7.5, color=ORANGE, alpha=.11)
ax.plot(range(8), t, color=BLUE, marker="o", lw=3.5, ms=8, label="참여 매장")
ax.plot(range(8), c, color=GREEN, marker="o", lw=3.5, ms=8, label="대조군")
ax.plot([5, 6, 7], [5100, *cf], color=ORANGE, marker="o", ls="--", lw=3, ms=8, label="기획전이 없었다면")
for i in [6, 7]:
    ax.fill_between([i-.4, i+.4], cf[i-6], t[i], color=RED, alpha=.27)
    ax.text(i, (cf[i-6]+t[i])/2, "+500", ha="center", color=RED, fontsize=16, weight="bold")
ax.axvline(5.5, color=MUTED, ls="--")
ax.set_xlim(-.3, 7.5)
ax.set_ylim(3200, 6500)
ax.set_xticks(range(8), ["6주 전", "5주 전", "4주 전", "3주 전", "2주 전", "직전", "1주차", "2주차"], fontsize=12)
ax.tick_params(axis="y", labelsize=12)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=13, ncol=2, loc="upper left")
fig.text(.72, .65, "실제 예약  12,000건", fontsize=22, color=BLUE)
fig.text(.72, .52, "없었다면  11,000건", fontsize=20, color=ORANGE)
fig.text(.72, .36, "순증분  1,000건", fontsize=27, color=RED, weight="bold")
fig.text(.72, .22, "DID = 2,000 - 1,000", fontsize=20, color=INK)
save(fig, 5)

print(OUT)
