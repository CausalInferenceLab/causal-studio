def plot_rdd_type():
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

def plot_rdd_regression(beta_0=2.0, beta_1=0.015, beta_2=0.5, beta_3=0.005,
                        show_line=True, show_data=True, show_labels=True):

    c = 70  # cutoff

    # -----------------------------
    # 시뮬레이션 데이터 생성
    # -----------------------------
    r_obs = np.random.uniform(40, 100, 200)
    D_obs = (r_obs > c).astype(int)

    y_obs = (
        beta_0
        + beta_1 * (r_obs - c)
        + beta_2 * D_obs
        + beta_3 * D_obs * (r_obs - c)
        + np.random.normal(0, 0.15, size=len(r_obs))
    )

    df = pd.DataFrame({
        "y": y_obs,
        "x": r_obs,
        "D": D_obs
    })

    df["x_centered"] = df["x"] - c
    df["interaction"] = df["D"] * df["x_centered"]

    # -----------------------------
    # smf 회귀
    # -----------------------------
    model = smf.ols(
        "y ~ x_centered + D + interaction",
        data=df
    ).fit()

    # 추정된 계수
    b0_hat = model.params["Intercept"].round(2)
    b1_hat = model.params["x_centered"].round(2)
    b2_hat = model.params["D"].round(2)
    b3_hat = model.params["interaction"].round(2)

    # -----------------------------
    # 회귀선 (추정치 기반)
    # -----------------------------
    r = np.linspace(40, 100, 200)
    D = (r > c).astype(int)

    y = (
        b0_hat
        + b1_hat * (r - c)
        + b2_hat * D
        + b3_hat * D * (r - c)
    )

    r_left  = r[r <= c]
    y_left  = y[r <= c]

    r_right = r[r > c]
    y_right = y[r > c]

    plt.figure(figsize=(10, 6))

    # -----------------------------
    # 산점도
    # -----------------------------
    if show_data:
        plt.scatter(
            r_obs[r_obs <= c],
            y_obs[r_obs <= c],
            color='tomato',
            alpha=0.3,
            s=20,
            zorder=1
        )

        plt.scatter(
            r_obs[r_obs > c],
            y_obs[r_obs > c],
            color='steelblue',
            alpha=0.3,
            s=20,
            zorder=1
        )

    # -----------------------------
    # 회귀선
    # -----------------------------
    if show_line:

        plt.plot(
            r_left,
            y_left,
            label=r'$X \leq c$ (No Treatment)',
            color='tomato',
            linewidth=2.5,
            zorder=2
        )

        plt.plot(
            r_right,
            y_right,
            label=r'$X > c$ (Treatment)',
            color='steelblue',
            linewidth=2.5,
            zorder=2
        )

        y_left_intercept  = b0_hat
        y_right_intercept = b0_hat + b2_hat

        plt.scatter(
            [c], [y_left_intercept],
            color='tomato',
            s=80,
            zorder=5,
            facecolors='none',
            edgecolors='tomato',
            linewidths=2
        )

        plt.scatter(
            [c], [y_right_intercept],
            color='steelblue',
            s=80,
            zorder=5
        )

        plt.annotate(
            '',
            xy=(c, y_right_intercept),
            xytext=(c, y_left_intercept),
            arrowprops=dict(arrowstyle='<->', color='black', lw=2)
        )

        # -----------------------------
        # label (추정값 사용)
        # -----------------------------
        if show_labels:

            plt.text(
                c - 14,
                y_left_intercept - 0.04,
                r"Intercept = $\hat{\beta}_0$" + f" = {b0_hat:.2f}",
                color='tomato',
                fontweight='bold',
                fontsize=10
            )

            plt.text(
                c + 0.8,
                y_right_intercept + 0.2,
                r"Intercept = $\hat{\beta}_0$ + $\hat{\beta}_2$" + f" = {(b0_hat + b2_hat):.2f}",
                color='steelblue',
                fontweight='bold',
                fontsize=10
            )

            plt.text(
                c + 0.8,
                (y_left_intercept + y_right_intercept) / 2,
                r"Jump = $\hat{\beta}_2$"
                + f" = {b2_hat:.2f}",
                color='black',
                fontweight='bold',
                fontsize=10
            )

            x_sl = 52
            y_sl = b0_hat + b1_hat * (x_sl - c)

            plt.text(
                x_sl - 10,
                y_sl,
                r"Slope = $\hat{\beta}_1$"
                + f" = {b1_hat:.2f}",
                color='tomato',
                fontsize=9
            )

            x_sr = 86
            y_sr = (
                b0_hat
                + b2_hat
                + (b1_hat + b3_hat) * (x_sr - c)
            )

            plt.text(
                x_sr - 10,
                y_sr + 0.1,
                r"Slope = $\hat{\beta}_1 + \hat{\beta}_3$"
                + f" = {(b1_hat + b3_hat):.2f}",
                color='steelblue',
                fontsize=9
            )

    plt.axvline(
        x=c,
        linestyle='--',
        color='gray',
        linewidth=1.5
    )

    plt.text(
        c + 0.3,
        plt.ylim()[0] + 0.05,
        f'$c = {c}$',
        fontsize=11,
        color='gray'
    )

    plt.title(
        "Regression Parameters Visualization (SAT Score → GPA)",
        fontsize=13,
        fontweight='bold'
    )

    plt.xlabel("SAT Score $X$", fontsize=11)
    plt.ylabel("GPA", fontsize=11)

    if show_line:
        plt.legend(fontsize=10)

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()