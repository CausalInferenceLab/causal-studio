# Library Import
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import Parallel, delayed 
import statsmodels.formula.api as smf

from matplotlib.gridspec import GridSpec
import matplotlib.font_manager as fm

from xgboost import XGBRegressor

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지    

def plot_rdd_type():
    np.random.seed(42)
    c = 0
    R = np.linspace(-3, 3, 300)
    
    D_sharp = np.where(R >= c, 1.0, 0.0)
    
    D_fuzzy = np.where(R >= c,
                       0.65 + 0.1 * np.tanh(R * 2),
                       0.15 + 0.1 * np.tanh(R * 2))
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # ── Sharp RDD ──
    ax = axes[0]
    ax.plot(R[R <  c], D_sharp[R <  c], 'tomato',    linewidth=3, label=r'$P(D=1|R)$: $R < c$')
    ax.plot(R[R >= c], D_sharp[R >= c], 'steelblue', linewidth=3, label=r'$P(D=1|R)$: $R \geq c$')
    ax.axvline(c, color='gray', linestyle=':', linewidth=1.5)
    ax.scatter([c], [0], s=80, color='tomato', zorder=5, edgecolors='tomato', facecolors='none', linewidths=2)
    ax.scatter([c], [1], s=80, zorder=5)
    ax.annotate('', xy=(c, 1.0), xytext=(c, 0.0),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(c + 0.1, 0.5, '0 → 1\n(perfect jump)', fontsize=11, va='center', fontweight='bold')
    ax.text(c + 0.05, -0.07, '$c$', fontsize=12, color='gray')
    ax.set_ylim(-0.15, 1.25)
    ax.set_title('Sharp RDD', fontsize=13, fontweight='bold')
    ax.set_xlabel('Running Variable $R$', fontsize=11)
    ax.set_ylabel(r'$P(D=1 \mid R)$', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    
    # ── Fuzzy RDD ──
    ax = axes[1]
    ax.plot(R[R <  c], D_fuzzy[R <  c], 'tomato',    linewidth=3, label=r'$P(D=1|R)$: $R < c$')
    ax.plot(R[R >= c], D_fuzzy[R >= c], 'steelblue', linewidth=3, label=r'$P(D=1|R)$: $R \geq c$')
    ax.axvline(c, color='gray', linestyle=':', linewidth=1.5)
    
    d_l = np.interp(c - 0.009, R, D_fuzzy)
    d_r = np.interp(c + 0.009, R, D_fuzzy)
    ax.scatter([c], [d_l], s=80, color='tomato', zorder=5, facecolors='none', edgecolors='tomato', linewidths=2)
    ax.scatter([c], [d_r], s=80, zorder=5)
    ax.annotate('', xy=(c, d_r), xytext=(c, d_l),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(c + 0.1, (d_l + d_r) / 2,
            f'{d_l:.2f} → {d_r:.2f}\n(partial jump)', fontsize=11, va='center', fontweight='bold')
    ax.text(c + 0.05, -0.07, '$c$', fontsize=12, color='gray')
    ax.set_ylim(-0.15, 1.25)
    ax.set_title('Fuzzy RDD', fontsize=13, fontweight='bold')
    ax.set_xlabel('Running Variable $R$', fontsize=11)
    ax.set_ylabel(r'$P(D=1 \mid R)$', fontsize=11)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    
    fig.suptitle(r'Sharp vs Fuzzy RDD — $P(D=1 \mid R)$', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_rdd_treatment():
    np.random.seed(42)
    c = 0  # 임계값
    
    R = np.linspace(-3, 3, 300)
    
    # 잠재적 결과 함수
    Y0 = 1 + 0.5 * R + 0.3 * R**2
    Y1 = 3 + 0.5 * R + 0.3 * R**2
    
    # ✅ 핵심: 실제 관측값 — 스위치처럼 c 기준으로 결정
    Y_obs = np.where(R >= c, Y1, Y0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 관측 불가 (점선)
    ax.plot(R, Y0, color='tomato',    linestyle='--', linewidth=1.5, alpha=0.5, label='$Y_0(R)$ — 전체 (관측 불가)')
    ax.plot(R, Y1, color='steelblue', linestyle='--', linewidth=1.5, alpha=0.5, label='$Y_1(R)$ — 전체 (관측 불가)')
    
    # 실제 관측값 (실선) — c 기준으로 스위치
    ax.plot(R[R <  c], Y_obs[R <  c], color='tomato',    linewidth=3, label='$Y^{obs}$ = $Y_0(R)$  if  $R < c$')
    ax.plot(R[R >= c], Y_obs[R >= c], color='steelblue',  linewidth=3, label='$Y^{obs}$ = $Y_1(R)$  if  $R \\geq c$')
    
    # 임계값
    ax.axvline(x=c, color='black', linestyle=':', linewidth=1.5)
    ax.text(c + 0.05, 0.3, '$c$ (임계값)', fontsize=11, color='black')
    
    # 점프 표시
    y_left  = np.interp(c, R, Y0)
    y_right = np.interp(c, R, Y1)
    ax.annotate('', xy=(c, y_right), xytext=(c, y_left),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(c + 0.08, (y_left + y_right) / 2, 'Jump\n= Treatment Effect',
            fontsize=10, va='center')
    
    ax.scatter([c], [y_left],  s=80, color='tomato',    zorder=5, facecolors='none', edgecolors='tomato', linewidths=2)
    ax.scatter([c], [y_right], s=80, color='steelblue',  zorder=5)
    
    ax.set_xlabel('Running Variable $R$', fontsize=12)
    ax.set_ylabel('Outcome $Y$', fontsize=12)
    ax.set_title('$Y^{obs}(R) = Y_1(R)$ if $R \\geq c$,  $Y_0(R)$ if $R < c$', fontsize=13)
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.show()    

def plot_rdd_regression(beta_0=2, beta_1=0.5, beta_2=3, beta_3=0.2,
                        show_line=True, show_data=True, show_labels=True):
    c = 0
    np.random.seed(42)

    # 데이터 생성
    r = np.linspace(c-5, c+5, 200)
    D = (r > c).astype(int)
    y = beta_0 + beta_1 * r + beta_2 * D + beta_3 * D * r

    # 좌우 분리
    r_left = r[r <= c];  y_left  = y[r <= c]
    r_right = r[r > c];  y_right = y[r > c]

    # 실제 관측 데이터
    r_obs = np.random.uniform(c-5, c+5, 150)
    D_obs = (r_obs > c).astype(int)
    y_obs = beta_0 + beta_1 * r_obs + beta_2 * D_obs + beta_3 * D_obs * r_obs
    y_obs += np.random.normal(0, 0.8, size=len(r_obs))

    plt.figure(figsize=(9, 6))

    # ── 산점도 (옵션) ──
    if show_data:
        plt.scatter(r_obs[r_obs <= c], y_obs[r_obs <= c],
                    color='blue', alpha=0.25, s=20, zorder=1)
        plt.scatter(r_obs[r_obs >  c], y_obs[r_obs >  c],
                    color='red',  alpha=0.25, s=20, zorder=1)

    # ── Regression line (옵션) ──
    if show_line:
        plt.plot(r_left,  y_left,  label=r'$r \leq c$', color='blue', zorder=2)
        plt.plot(r_right, y_right, label=r'$r > c$',    color='red',  zorder=2)

        # 절편 포인트
        y_left_intercept  = beta_0
        y_right_intercept = beta_0 + beta_2
        plt.scatter([c], [y_left_intercept],  color='blue', zorder=5)
        plt.scatter([c], [y_right_intercept], color='red',  zorder=5)

        # 점프 화살표
        plt.annotate('', xy=(c, y_right_intercept), xytext=(c, y_left_intercept),
                     arrowprops=dict(arrowstyle='<->', color='black'))

        # ── 텍스트 annotation (옵션) ──
        if show_labels:
            plt.text(c - 1.8, y_left_intercept - 0.5,
                     r"$\beta_0$" + f" = {beta_0}", color='blue')
            plt.text(c + 0.2, y_right_intercept + 0.2,
                     r"$\beta_0 + \beta_2$" + f" = {beta_0 + beta_2}", color='red')
            plt.text(c + 0.2, (y_left_intercept + y_right_intercept) / 2,
                     r"Jump = $\beta_2$" + f" = {beta_2}", color='black')
            plt.text(-4.5, beta_0 + beta_1*(-4.5),
                     r"Slope = $\beta_1$" + f" = {beta_1}", color='blue')
            plt.text(2, (beta_0 + beta_2) + (beta_1 + beta_3)*2,
                     r"Slope = $\beta_1 + \beta_3$" + f" = {beta_1 + beta_3}", color='red')

    # ── cutoff ──
    plt.axvline(x=c, linestyle='--', color='black')

    plt.title("RDD Visualization with Parameters")
    plt.xlabel("Running Variable (r)")
    plt.ylabel("Outcome (y)")
    if show_line:
        plt.legend()
    plt.grid(True)
    plt.show()

def kernel(R, c, h):
    indicator = (np.abs(R-c) <= h).astype(float)
    return indicator * (1 - np.abs(R-c)/h)

def plot_kernel(c=0, h=1):
    """
    파라미터
    c: cutoff
    h: bandwidth
    """
    R = np.linspace(c-3*h, c+3*h, 500)
    
    # kernel weight 계산a
    W = kernel(R, c, h)
    
    # 그래프
    plt.figure(figsize=(8, 5))
    plt.plot(R, W)
    
    # cutoff 표시
    plt.axvline(x=c, linestyle='--')
    plt.xlabel("Running Variable (R)")
    plt.ylabel("Kernel Weight")
    plt.title("Triangular Kernel Weight around Cutoff")
    
    # plt.grid(True)
    plt.tight_layout()
    plt.show()    


def triangular_kernel(r, c, h):
    u = np.abs(r - c) / h
    return np.where(u <= 1, 1 - u, 0.0)

def uniform_kernel(r, c, h):
    u = np.abs(r - c) / h
    return np.where(u <= 1, 1.0, 0.0)

def epanechnikov_kernel(r, c, h):
    u = np.abs(r - c) / h
    return np.where(u <= 1, 0.75 * (1 - u**2), 0.0)

KERNELS = {
    'triangular':   triangular_kernel,
    'uniform':      uniform_kernel,
    'epanechnikov': epanechnikov_kernel,
}
def plot_rdd_kernel(beta_0=2, beta_1=0.5, beta_2=3, beta_3=0.2,
                    bandwidth=2.0, kernel='triangular', c=0, sample_n=300,
                    show_kernel=False, show_all_kernels=False):                          # ✅ 추가

    np.random.seed(42)

    # ── 데이터 생성 ──
    r_obs = np.random.uniform(c-5, c+5, sample_n)
    D_obs = (r_obs > c).astype(int)
    y_obs = beta_0 + beta_1 * (r_obs - c) + beta_2 * D_obs + beta_3 * D_obs * (r_obs - c)
    y_obs += np.random.normal(0, 1.0, size=len(r_obs))

    rdd_df = pd.DataFrame({
        'y':         y_obs,
        'r':         r_obs,
        'r_tilde':   r_obs - c,
        'threshold': D_obs,
    })

    # ── Kernel weights ──
    kernel_fn  = KERNELS[kernel]
    weights    = kernel_fn(rdd_df['r'], c=c, h=bandwidth)
    in_bw      = weights > 0
    rdd_bw     = rdd_df[in_bw].copy()
    weights_bw = weights[in_bw]

    model = smf.wls("y ~ r_tilde * threshold", data=rdd_bw, weights=weights_bw).fit()

    late         = model.params['threshold']
    r_fit_left   = np.linspace(c - bandwidth, c, 100)
    r_fit_right  = np.linspace(c, c + bandwidth, 100)
    df_left      = pd.DataFrame({'r_tilde': r_fit_left  - c, 'threshold': 0})
    df_right     = pd.DataFrame({'r_tilde': r_fit_right - c, 'threshold': 1})
    y_fit_left   = model.predict(df_left)
    y_fit_right  = model.predict(df_right)
    y_at_c_left  = model.predict(pd.DataFrame({'r_tilde': [0.0], 'threshold': [0]}))[0]
    y_at_c_right = model.predict(pd.DataFrame({'r_tilde': [0.0], 'threshold': [1]}))[0]

    r_line = np.linspace(c-5, c+5, 200)
    D_line = (r_line > c).astype(int)
    y_line = beta_0 + beta_1*(r_line-c) + beta_2*D_line + beta_3*D_line*(r_line-c)

    # ✅ show_kernel에 따라 subplot 구성 변경
    if show_kernel:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        ax = axes[0]
    else:
        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    # ── RDD plot ──
    ax.axvspan(c - bandwidth, c + bandwidth, alpha=0.08, color='gold',
               label=f'Bandwidth h={bandwidth}')
    ax.scatter(r_obs[~in_bw], y_obs[~in_bw],
               color='gray', alpha=0.2, s=15, label='Out of bandwidth')

    mask_left  = in_bw & (r_obs <= c)
    mask_right = in_bw & (r_obs >  c)
    w_max = weights_bw.max()
    ax.scatter(r_obs[mask_left],  y_obs[mask_left],
               s=weights[mask_left]  / w_max * 60 + 5,
               alpha=0.6, color='steelblue', label='Left (weighted)')
    ax.scatter(r_obs[mask_right], y_obs[mask_right],
               s=weights[mask_right] / w_max * 60 + 5,
               alpha=0.6, color='tomato', label='Right (weighted)')

    ax.plot(r_line[r_line <= c], y_line[r_line <= c],
            color='steelblue', linestyle='--', linewidth=1.2, alpha=0.4)
    ax.plot(r_line[r_line >  c], y_line[r_line >  c],
            color='tomato',    linestyle='--', linewidth=1.2, alpha=0.4, label='True line')
    ax.plot(r_fit_left,  y_fit_left,  color='steelblue', linewidth=2.5, label='WLS fit')
    ax.plot(r_fit_right, y_fit_right, color='tomato',    linewidth=2.5)

    ax.axvline(c, linestyle=':', color='black', linewidth=1.5)
    ax.scatter([c], [y_at_c_left],  color='steelblue', s=80, zorder=6)
    ax.scatter([c], [y_at_c_right], color='tomato',    s=80, zorder=6,
               facecolors='none', edgecolors='tomato', linewidths=2)
    ax.annotate('', xy=(c, y_at_c_right), xytext=(c, y_at_c_left),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(c + 0.15, (y_at_c_left + y_at_c_right) / 2,
            f'LATE = $\\beta_2$ = {late:.2f}\n(true $\\beta_2$ = {beta_2})',
            fontsize=10, va='center', fontweight='bold')

    ax.set_title(f'Kernel WLS RDD  ({kernel.capitalize()}, h={bandwidth}, c={c})',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Running Variable $r$')
    ax.set_ylabel('Outcome $Y$')
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(alpha=0.3)

    # ── Kernel 비교 (옵션) ──
    if show_kernel:
        ax2 = axes[1]
        r_kw   = np.linspace(-bandwidth, bandwidth, 300)
        colors = {'uniform': 'gray', 'triangular': 'steelblue', 'epanechnikov': 'tomato'}
        for name, fn in KERNELS.items():
            if show_all_kernels is True:
                w  = fn(r_kw, c=0, h=bandwidth)
                lw = 3 if name == kernel else 1.2
                ls = '-' if name == kernel else '--'
                ax2.plot(r_kw, w, color=colors[name], linewidth=lw, linestyle=ls,
                         label=name.capitalize() + (' ← selected' if name == kernel else ''))
            else:
                if name == kernel:
                    w  = fn(r_kw, c=0, h=bandwidth)
                    lw = 3 if name == kernel else 1.2
                    ls = '-' if name == kernel else '--'
                    ax2.plot(r_kw, w, color=colors[name], linewidth=lw, linestyle=ls,
                             label=name.capitalize() + (' ← selected' if name == kernel else ''))
        ax2.set_title('Kernel Weight Functions', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Distance from cutoff $c$')
        ax2.set_ylabel('Weight')
        ax2.legend(fontsize=9)
        ax2.grid(alpha=0.3)

    fig.suptitle('RDD with Kernel Weighting (statsmodels WLS)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    return model


def plot_rdd_xgb(beta_0=2, beta_1=0.5, beta_2=3, beta_3=0.2, sample_n=1000,
                 bandwidth=2.0, kernel='triangular', **xgb_kwargs):
    c = 0
    np.random.seed(42)

    # ── 데이터 생성 ──
    r_obs = np.random.uniform(c-5, c+5, sample_n)
    D_obs = (r_obs > c).astype(int)
    y_obs = beta_0 + beta_1 * r_obs + beta_2 * D_obs + beta_3 * D_obs * r_obs
    y_obs += np.random.normal(0, 1.0, size=len(r_obs))

    rdd_df = pd.DataFrame({
        'y':         y_obs,
        'r':         r_obs,
        'threshold': D_obs,
        'r_x_D':     r_obs * D_obs,   # interaction term
    })

    # ── Kernel weights ──
    kernel_fn = KERNELS[kernel]
    weights   = kernel_fn(rdd_df['r'], c=c, h=bandwidth)

    # weight > 0 인 데이터만 사용 (log(0) 방지)
    in_bw      = weights > 0
    rdd_bw     = rdd_df[in_bw].copy()
    weights_bw = weights[in_bw]

    # ── Feature matrix ──
    features = ['r', 'threshold', 'r_x_D']
    X_bw = rdd_bw[features]
    y_bw = rdd_bw['y']

    # ── XGBoost 적합 ──
    xgb_defaults = dict(n_estimators=200, max_depth=3,
                        learning_rate=0.05, subsample=0.8,
                        random_state=42)
    xgb_defaults.update(xgb_kwargs)   # 외부에서 파라미터 override 가능

    model = XGBRegressor(**xgb_defaults)
    model.fit(X_bw, y_bw, sample_weight=weights_bw)

    # ── LATE 추정 (cutoff에서의 점프) ──
    df_at_c_left  = pd.DataFrame({'r': [c], 'threshold': [0], 'r_x_D': [0.0]})
    df_at_c_right = pd.DataFrame({'r': [c], 'threshold': [1], 'r_x_D': [c * 1.0]})
    y_at_c_left   = model.predict(df_at_c_left)[0]
    y_at_c_right  = model.predict(df_at_c_right)[0]
    late          = y_at_c_right - y_at_c_left

    # ── Fitted line (bandwidth 내) ──
    r_fit_left  = np.linspace(c - bandwidth, c, 100)
    r_fit_right = np.linspace(c, c + bandwidth, 100)

    df_left  = pd.DataFrame({'r': r_fit_left,
                              'threshold': np.zeros(100),
                              'r_x_D':     np.zeros(100)})
    df_right = pd.DataFrame({'r': r_fit_right,
                              'threshold': np.ones(100),
                              'r_x_D':     r_fit_right * 1.0})

    y_fit_left  = model.predict(df_left)
    y_fit_right = model.predict(df_right)

    # ── True line ──
    r_line = np.linspace(c-5, c+5, 200)
    D_line = (r_line > c).astype(int)
    y_line = beta_0 + beta_1 * r_line + beta_2 * D_line + beta_3 * D_line * r_line

    # ════════════════════════════════════════
    # Plot
    # ════════════════════════════════════════
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # ── (Left) RDD plot ──
    ax = axes[0]

    ax.axvspan(c - bandwidth, c + bandwidth, alpha=0.08, color='gold',
               label=f'Bandwidth h={bandwidth}')
    ax.scatter(r_obs[~in_bw], y_obs[~in_bw],
               color='gray', alpha=0.2, s=15, label='Out of bandwidth')

    mask_left  = in_bw & (r_obs <= c)
    mask_right = in_bw & (r_obs >  c)
    w_max = weights_bw.max()
    ax.scatter(r_obs[mask_left],  y_obs[mask_left],
               s=weights[mask_left]  / w_max * 60 + 5,
               alpha=0.6, color='steelblue', label='Left (weighted)')
    ax.scatter(r_obs[mask_right], y_obs[mask_right],
               s=weights[mask_right] / w_max * 60 + 5,
               alpha=0.6, color='tomato', label='Right (weighted)')

    # True line (점선)
    ax.plot(r_line[r_line <= c], y_line[r_line <= c],
            color='steelblue', linestyle='--', linewidth=1.2, alpha=0.4)
    ax.plot(r_line[r_line >  c], y_line[r_line >  c],
            color='tomato',    linestyle='--', linewidth=1.2, alpha=0.4,
            label='True line')

    # XGBoost fitted line
    ax.plot(r_fit_left,  y_fit_left,  color='steelblue', linewidth=2.5, label='XGB fit')
    ax.plot(r_fit_right, y_fit_right, color='tomato',    linewidth=2.5)

    ax.axvline(c, linestyle=':', color='black', linewidth=1.5)
    ax.scatter([c], [y_at_c_left],  color='steelblue', s=80, zorder=6)
    ax.scatter([c], [y_at_c_right], color='tomato', s=80, zorder=6,
               facecolors='none', edgecolors='tomato', linewidths=2)
    ax.annotate('', xy=(c, y_at_c_right), xytext=(c, y_at_c_left),
                arrowprops=dict(arrowstyle='<->', color='black', lw=2))
    ax.text(c + 0.15, (y_at_c_left + y_at_c_right) / 2,
            f'LATE = {late:.2f}\n(true $\\beta_2$ = {beta_2})',
            fontsize=10, va='center', fontweight='bold')

    ax.set_title(f'XGBoost RDD  ({kernel.capitalize()}, h={bandwidth})',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Running Variable $R$')
    ax.set_ylabel('Outcome $Y$')
    ax.legend(fontsize=8, loc='upper left')
    ax.grid(alpha=0.3)

    # ── (Right) Feature importance ──
    ax2 = axes[1]
    importances = model.feature_importances_
    ax2.barh(features, importances, color=['steelblue', 'tomato', 'goldenrod'])
    ax2.set_title('XGBoost Feature Importance', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Importance')
    ax2.grid(alpha=0.3)

    fig.suptitle('RDD with Kernel Weighting (XGBoost)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # return model    