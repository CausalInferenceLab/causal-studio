import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import statsmodels.api as sm
from scipy import stats

def plot_fuzzy_rdd(true_effect=0.6):   
    """
    Fuzzy RDD 예시: 장학금 기준 점수가 학업 성취도에 미치는 인과효과
    - Running Variable: 입학 시험 점수 (0~100)
    - Cutoff: 60점
    - Treatment: 장학금 수혜 여부 (60점 이상이면 확률 증가, but not 100%)
    - Outcome: 1년 후 GPA (0~4.0)
    """
    
    # ── 재현성 ──────────────────────────────────────────────────
    np.random.seed(42)
    n = 2000
    CUTOFF = 60
    
    # ── 데이터 생성 ──────────────────────────────────────────────
    score = np.random.uniform(20, 100, n)          # running variable
    
    # 장학금 수혜 확률: cutoff 기준으로 점프 (Fuzzy)
    prob_treat = np.where(score >= CUTOFF, 0.80, 0.15)
    prob_treat += np.random.normal(0, 0.05, n)
    prob_treat = np.clip(prob_treat, 0, 1)
    treatment = np.random.binomial(1, prob_treat)  # D_i
    
    # GPA: 점수의 선형 효과 + 처치 효과 + 노이즈
    gpa = (
        1.5
        + 0.015 * (score - CUTOFF)
        + true_effect * treatment
        + np.random.normal(0, 0.4, n)
    )
    gpa = np.clip(gpa, 0, 4.0)
    
    df = pd.DataFrame({'score': score, 'treatment': treatment, 'gpa': gpa})
    df['above'] = (df['score'] >= CUTOFF).astype(int)   # Z_i (도구변수)
    df['score_c'] = df['score'] - CUTOFF                # 중심화된 running variable
    
    # ── 2SLS (bandwidth = ±20점 근방) ───────────────────────────
    bw = 20
    sub = df[np.abs(df['score_c']) <= bw].copy()
    
    # First Stage: D_i ~ Z_i + (X_i - c) + Z_i*(X_i - c)
    fs_X = sm.add_constant(pd.DataFrame({
        'Z':        sub['above'],
        'score_c':  sub['score_c'],
        'Z_sc':     sub['above'] * sub['score_c'],
    }))
    fs_model  = sm.OLS(sub['treatment'], fs_X).fit()
    sub['D_hat'] = fs_model.fittedvalues
    
    # F-statistic for Z in first stage
    f_stat = fs_model.fvalue
    alpha1 = fs_model.params['Z']
    
    # Second Stage: Y_i ~ D_hat + (X_i - c) + D_hat*(X_i - c)
    ss_X = sm.add_constant(pd.DataFrame({
        'D_hat':   sub['D_hat'],
        'score_c': sub['score_c'],
        'Dh_sc':   sub['D_hat'] * sub['score_c'],
    }))
    ss_model = sm.OLS(sub['gpa'], ss_X).fit()
    LATE = ss_model.params['D_hat']
    LATE_se = ss_model.bse['D_hat']
    LATE_ci = ss_model.conf_int().loc['D_hat'].values
    
    # ── ITT_Y: Y ~ Z_i 회귀에서 컷오프 점프 (regression-based) ─────
    ity_X = sm.add_constant(pd.DataFrame({
        'Z':       sub['above'],
        'score_c': sub['score_c'],
        'Z_sc':    sub['above'] * sub['score_c'],
    }))
    ity_model = sm.OLS(sub['gpa'], ity_X).fit()
    ITT_Y    = ity_model.params['Z']   # Y의 컷오프 점프 (회귀 기반)
    ITT_Y_se = ity_model.bse['Z']
    
    # ── ITT_D: First Stage α₁ 그대로 사용 (동일 모델) ──────────────
    ITT_D    = alpha1                  # = fs_model.params['Z']
    ITT_D_se = fs_model.bse['Z']
    
    # ── Wald = ITT_Y / ITT_D  (2SLS LATE와 수렴해야 함) ────────────
    wald = ITT_Y / ITT_D if ITT_D != 0 else np.nan
    
    print(f"[First Stage]  α₁ (Z→D jump) = {alpha1:.4f},  F-stat = {f_stat:.2f}")
    print(f"[LATE (2SLS)]  β₁ = {LATE:.4f}  SE = {LATE_se:.4f}")
    print(f"[95% CI]       [{LATE_ci[0]:.4f}, {LATE_ci[1]:.4f}]")
    print(f"[Wald]         {wald:.4f}")
    print(f"[ITT_Y]        {ITT_Y:.4f}   [ITT_D]  {ITT_D:.4f}")
    
    # ── 시각화 ───────────────────────────────────────────────────
    DARK   = '#0f1117'
    PANEL  = '#1a1d27'
    ACCENT = '#4f9cf9'
    GREEN  = '#43d9a2'
    RED    = '#f97b4f'
    GRAY   = '#8b8fa8'
    WHITE  = '#e8eaf0'
    
    fig = plt.figure(figsize=(16, 14), facecolor=DARK)
    fig.suptitle(
        'Fuzzy RDD Analysis\nScholarship Cutoff & Academic Achievement',
        fontsize=18, fontweight='bold', color=WHITE, y=0.98
    )
    
    gs = GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35,
                  left=0.07, right=0.96, top=0.92, bottom=0.06)
    
    ax1 = fig.add_subplot(gs[0, :2])   # Treatment probability (wide)
    ax2 = fig.add_subplot(gs[0, 2])    # First stage F-stat gauge
    ax3 = fig.add_subplot(gs[1, :2])   # Outcome scatter + RDD fit
    ax4 = fig.add_subplot(gs[1, 2])    # LATE + CI
    ax5 = fig.add_subplot(gs[2, :])    # ITT decomposition
    
    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_color('#2e3147')
    
    def bin_means(data, col_x, col_y, bins=40):
        data = data.copy()
        data['bin'] = pd.cut(data[col_x], bins=bins)
        g = data.groupby('bin', observed=True).agg(
            x=(col_x, 'mean'), y=(col_y, 'mean')
        ).dropna()
        return g['x'].values, g['y'].values
    
    # ── Plot 1: Treatment Probability ────────────────────────────
    bx, by = bin_means(df, 'score', 'treatment', bins=40)
    mask_l = bx < CUTOFF
    mask_r = bx >= CUTOFF
    
    ax1.scatter(bx[mask_l], by[mask_l], color=GRAY,   s=30, alpha=0.8, zorder=3)
    ax1.scatter(bx[mask_r], by[mask_r], color=ACCENT,  s=30, alpha=0.8, zorder=3)
    
    # 로컬 선형 피팅
    for mask, col in [(mask_l, GRAY), (mask_r, ACCENT)]:
        xv = bx[mask]; yv = by[mask]
        if len(xv) > 2:
            z = np.polyfit(xv, yv, 1)
            xs = np.linspace(xv.min(), xv.max(), 100)
            ax1.plot(xs, np.polyval(z, xs), color=col, lw=2.5)
    
    ax1.axvline(CUTOFF, color=RED, lw=2, ls='--', zorder=4)
    ax1.set_title('① First Stage: Treatment Probability', color=WHITE, fontsize=12, pad=8)
    ax1.set_xlabel('Entrance Exam Score', color=GRAY, fontsize=10)
    ax1.set_ylabel('P(Scholarship = 1)', color=GRAY, fontsize=10)
    ax1.tick_params(colors=GRAY)
    ax1.set_ylim(-0.05, 1.1)
    
    jump_txt = f'Jump ≈ {alpha1:.3f}'
    ax1.annotate(jump_txt, xy=(CUTOFF, 0.5),
                 xytext=(CUTOFF + 3, 0.35),
                 color=RED, fontsize=10, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))
    
    # ── Plot 2: F-stat Gauge ─────────────────────────────────────
    theta = np.linspace(np.pi, 0, 300)
    ax2.plot(np.cos(theta), np.sin(theta), color='#2e3147', lw=8)
    
    # 색상 구간
    for t_start, t_end, col in [
        (np.pi,       np.pi*2/3, RED),
        (np.pi*2/3,   np.pi/3,   '#f9d44f'),
        (np.pi/3,     0,         GREEN),
    ]:
        ts = np.linspace(t_start, t_end, 100)
        ax2.plot(np.cos(ts), np.sin(ts), color=col, lw=8)
    
    # 바늘: F=10 기준으로 0~30 스케일
    f_clamped = min(f_stat, 30)
    needle_angle = np.pi - (f_clamped / 30) * np.pi
    ax2.annotate('', xy=(0.75*np.cos(needle_angle), 0.75*np.sin(needle_angle)),
                 xytext=(0, 0),
                 arrowprops=dict(arrowstyle='->', color=WHITE, lw=2.5))
    ax2.text(0, -0.25, f'F = {f_stat:.1f}', ha='center', color=WHITE,
             fontsize=14, fontweight='bold')
    ax2.text(0, -0.50, '(>10: Strong IV)', ha='center', color=GREEN, fontsize=9)
    ax2.text(-1, -0.1, 'Weak', color=RED,   fontsize=8, ha='center')
    ax2.text( 1, -0.1, 'Strong', color=GREEN, fontsize=8, ha='center')
    ax2.set_xlim(-1.3, 1.3); ax2.set_ylim(-0.7, 1.2)
    ax2.set_aspect('equal'); ax2.axis('off')
    ax2.set_title('First Stage F-stat', color=WHITE, fontsize=12, pad=8)
    
    # ── Plot 3: Outcome Scatter ───────────────────────────────────
    gx, gy = bin_means(df, 'score', 'gpa', bins=40)
    mask_l = gx < CUTOFF
    mask_r = gx >= CUTOFF
    
    ax3.scatter(gx[mask_l], gy[mask_l], color=GRAY,  s=30, alpha=0.8, zorder=3)
    ax3.scatter(gx[mask_r], gy[mask_r], color=ACCENT, s=30, alpha=0.8, zorder=3)
    
    for mask, col in [(mask_l, GRAY), (mask_r, ACCENT)]:
        xv = gx[mask]; yv = gy[mask]
        if len(xv) > 2:
            z = np.polyfit(xv, yv, 1)
            xs = np.linspace(xv.min(), xv.max(), 100)
            ax3.plot(xs, np.polyval(z, xs), color=col, lw=2.5)
    
    ax3.axvline(CUTOFF, color=RED, lw=2, ls='--', zorder=4)
    
    # ITT_Y 표시
    left_fit  = np.polyfit(gx[mask_l], gy[mask_l], 1)
    right_fit = np.polyfit(gx[mask_r], gy[mask_r], 1)
    y_left_at_c  = np.polyval(left_fit,  CUTOFF)
    y_right_at_c = np.polyval(right_fit, CUTOFF)
    
    ax3.annotate('', xy=(CUTOFF + 0.3, y_right_at_c),
                 xytext=(CUTOFF + 0.3, y_left_at_c),
                 arrowprops=dict(arrowstyle='<->', color=GREEN, lw=2))
    ax3.text(CUTOFF + 1.5, (y_left_at_c + y_right_at_c)/2,
             f'ITT_Y (reg.)\n= {ITT_Y:.3f}', color=GREEN, fontsize=9, va='center')
    
    ax3.set_title('② Second Stage: GPA Outcome', color=WHITE, fontsize=12, pad=8)
    ax3.set_xlabel('Entrance Exam Score', color=GRAY, fontsize=10)
    ax3.set_ylabel('GPA (1st year)', color=GRAY, fontsize=10)
    ax3.tick_params(colors=GRAY)
    
    # ── Plot 4: Forest Plot (LATE + CI) ─────────────────────────
    y_pos = 0
    
    # CI 구간 음영
    ax4.barh(y_pos, LATE_ci[1] - LATE_ci[0], left=LATE_ci[0],
             height=0.25, color=ACCENT, alpha=0.25, zorder=2)
    
    # CI 수평선
    ax4.hlines(y_pos, LATE_ci[0], LATE_ci[1],
               colors=ACCENT, lw=2.5, zorder=3)
    
    # 끝 캡
    ax4.vlines([LATE_ci[0], LATE_ci[1]], y_pos - 0.07, y_pos + 0.07,
               colors=ACCENT, lw=2.5, zorder=3)
    
    # 점 추정값 (다이아몬드)
    ax4.scatter([LATE], [y_pos], color=WHITE, s=120,
                marker='D', zorder=5, edgecolors=ACCENT, linewidths=1.5)
    
    # True effect 수직선
    ax4.axvline(true_effect, color=GREEN, lw=1.5, ls=':',
                label=f'True effect = {true_effect}', zorder=1)
    
    # 영(0) 기준선
    ax4.axvline(0, color=GRAY, lw=1, ls='--', alpha=0.6, zorder=1)
    
    # 값 레이블
    ax4.text(LATE, y_pos + 0.18, f'{LATE:.3f}',
             ha='center', color=WHITE, fontsize=13, fontweight='bold')
    ci_txt = f'95% CI: [{LATE_ci[0]:.3f}, {LATE_ci[1]:.3f}]'
    ax4.text(LATE, y_pos - 0.22, ci_txt,
             ha='center', color=GRAY, fontsize=9)
    
    # SE 텍스트
    ax4.text(LATE, y_pos - 0.35, f'SE = {LATE_se:.3f}',
             ha='center', color=GRAY, fontsize=9)
    
    ax4.set_xlim(min(LATE_ci[0] - 0.3, -0.1), max(LATE_ci[1] + 0.3, true_effect + 0.2))
    ax4.set_ylim(-0.6, 0.6)
    ax4.set_yticks([0])
    ax4.set_yticklabels(['LATE (2SLS)'], color=WHITE, fontsize=10)
    ax4.set_title('LATE Estimate  (Forest Plot)', color=WHITE, fontsize=12, pad=8)
    ax4.set_xlabel('Effect on GPA', color=GRAY, fontsize=10)
    ax4.tick_params(colors=GRAY)
    ax4.legend(facecolor=DARK, labelcolor=GREEN, fontsize=8, loc='upper left')
    
    # ── Plot 5: ITT 분해 ─────────────────────────────────────────
    categories = ['ITT_Y\n(Y jump)', 'ITT_D\n(D jump)', 'LATE\n= ITT_Y / ITT_D']
    values     = [ITT_Y, ITT_D, LATE]
    colors_bar = [GREEN, RED, ACCENT]
    
    bars = ax5.bar(categories, values, color=colors_bar, width=0.4,
                   edgecolor=DARK, linewidth=1.5, zorder=3)
    for bar, val in zip(bars, values):
        ax5.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.01,
                 f'{val:.4f}', ha='center', color=WHITE,
                 fontsize=12, fontweight='bold')
    
    # 수식 표시
    formula = (r'$\hat{\tau}_{Fuzzy} = \frac{\mathrm{ITT}_Y\,(reg.)}{\mathrm{ITT}_D\,(reg.)}'
               rf' = \frac{{{ITT_Y:.3f}}}{{{ITT_D:.3f}}} \approx {LATE:.3f}$')
    ax5.text(0.5, 0.88, formula, transform=ax5.transAxes,
             ha='center', color=WHITE, fontsize=13,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#2e3147', edgecolor=ACCENT, lw=1.5))
    
    ax5.axhline(0, color=GRAY, lw=1)
    ax5.set_title('③ Wald Estimator Decomposition: ITT_Y / ITT_D = LATE', color=WHITE, fontsize=12, pad=8)
    ax5.set_ylabel('Magnitude', color=GRAY, fontsize=10)
    ax5.tick_params(colors=GRAY)
    ax5.set_ylim(0, max(values) * 1.5)
    
    # ── 범례 ─────────────────────────────────────────────────────
    legend_patches = [
        mpatches.Patch(color=GRAY,   label='Below Cutoff (Z=0)'),
        mpatches.Patch(color=ACCENT, label='Above Cutoff (Z=1)'),
        mpatches.Patch(color=RED,    label=f'Cutoff = {CUTOFF}'),
    ]
    fig.legend(handles=legend_patches, loc='lower center', ncol=3,
               facecolor=DARK, labelcolor=WHITE, fontsize=10,
               bbox_to_anchor=(0.5, 0.01), framealpha=0.5)
    
    plt.show()