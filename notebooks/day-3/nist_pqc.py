import matplotlib.pyplot as plt


def draw_timeline(
    events=None,
    event_colors=None,
    figsize=(16, 5),
    title="NIST Post-Quantum Cryptography Standardization Timeline",
    show=True
):
    """
    Draw a NIST Post-Quantum Cryptography standardization timeline.

    Parameters
    ----------
    events : list, optional
        List of tuples in the form:

        (
            x_position,
            year,
            stage,
            detail
        )

    event_colors : list, optional
        Color associated with each event.

    figsize : tuple, optional
        Matplotlib figure size.

    title : str, optional
        Timeline title.

    show : bool, optional
        If True, call plt.show().

    Returns
    -------
    fig, ax
        Matplotlib Figure and Axes objects.
    """

    # ========================================================
    # DEFAULT EVENTS
    # ========================================================

    if events is None:

        events = [
            (
                0.0,
                2016,
                "Call for proposals",
                ""
            ),
            (
                0.7,
                2017,
                "Round 1",
                "82 submissions"
            ),
            (
                1.5,
                2019,
                "Round 2",
                "26 candidates"
            ),
            (
                2.3,
                2020,
                "Round 3",
                "7 finalists + 8 alternates"
            ),
            (
                3.1,
                2022,
                "Selection",
                "Algorithms selected"
            ),
            (
                4.0,
                2024,
                "Standardization",
                "ML-KEM · ML-DSA · SLH-DSA"
            ),
            (
                4.9,
                2025,
                "HQC",
                "Selected for standardization"
            ),
            (
                5.5,
                2026,
                "Falcon",
                "Selected for future FIPS"
            ),
        ]

    # ========================================================
    # DEFAULT COLORS
    # ========================================================

    if event_colors is None:

        event_colors = [
            "#6B7280",  # 2016 - Call for proposals
            "#2563EB",  # 2017 - Round 1
            "#059669",  # 2019 - Round 2
            "#D97706",  # 2020 - Round 3
            "#7C3AED",  # 2022 - Selection
            "#DC2626",  # 2024 - Standardization
            "#0891B2",  # 2025 - HQC
            "#DB2777",  # 2026 - Falcon
        ]

    # ========================================================
    # VALIDATION
    # ========================================================

    if len(event_colors) != len(events):
        raise ValueError(
            "event_colors must contain exactly one color "
            "for each event."
        )

    # ========================================================
    # COLORS
    # ========================================================

    timeline_color = "#A0A0A0"

    # ========================================================
    # FIGURE
    # ========================================================

    fig, ax = plt.subplots(figsize=figsize)

    # ========================================================
    # X POSITIONS
    # ========================================================

    x_positions = [
        event[0]
        for event in events
    ]

    # ========================================================
    # MAIN TIMELINE
    # ========================================================

    ax.hlines(
        y=0,
        xmin=min(x_positions) - 0.3,
        xmax=max(x_positions) + 0.3,
        linewidth=1.8,
        linestyle="--",
        color=timeline_color,
        zorder=1
    )

    # ========================================================
    # EVENTS
    # ========================================================

    for i, (x, year, stage, detail) in enumerate(events):

        event_color = event_colors[i]

        # --------------------------------------------
        # Alternate events above/below timeline
        # --------------------------------------------

        if i % 2 == 0:

            connector_end = 0.20
            text_y = 0.24
            text_va = "bottom"

            detail_y = 0.36
            detail_va = "top"

        else:

            connector_end = -0.20
            text_y = -0.24
            text_va = "top"

            detail_y = -0.36
            detail_va = "bottom"

        # --------------------------------------------
        # Event dot
        # --------------------------------------------

        ax.scatter(
            x,
            0,
            s=220,
            color=event_color,
            zorder=4
        )

        # --------------------------------------------
        # Connector line
        # --------------------------------------------

        ax.plot(
            [x, x],
            [0, connector_end],
            linewidth=1.5,
            color=event_color,
            zorder=3
        )

        # --------------------------------------------
        # Year + stage
        # --------------------------------------------

        ax.text(
            x,
            text_y,
            f"{year}  |  {stage}",
            ha="center",
            va=text_va,
            fontsize=10,
            fontweight="bold"
        )

        # --------------------------------------------
        # Detail
        # --------------------------------------------

        if detail:

            ax.text(
                x,
                detail_y,
                detail,
                ha="center",
                va=detail_va,
                fontsize=9
            )

    # ========================================================
    # HIGHLIGHT 2024
    # ========================================================

    x_2024 = 4.0

    ax.axvspan(
        x_2024 - 0.45,
        x_2024 + 0.45,
        alpha=0.08,
        zorder=0
    )

    ax.text(
        x_2024,
        0.47,
        "NIST PQC Standards",
        ha="center",
        va="center",
        fontsize=11,
        fontweight="bold"
    )

    # ========================================================
    # AXIS
    # ========================================================

    ax.set_xlim(
        min(x_positions) - 0.4,
        max(x_positions) + 0.4
    )

    ax.set_ylim(
        -0.48,
        0.52
    )

    # Years on X axis
    ax.set_xticks(x_positions)

    ax.set_xticklabels(
        [
            str(event[1])
            for event in events
        ],
        fontsize=9
    )

    ax.set_yticks([])

    # ========================================================
    # TITLE
    # ========================================================

    ax.set_title(
        title,
        fontsize=18,
        pad=20
    )

    # ========================================================
    # REMOVE SPINES
    # ========================================================

    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    # ========================================================
    # LAYOUT
    # ========================================================

    plt.tight_layout()

    # ========================================================
    # SHOW
    # ========================================================

    if show:
        plt.show()

    return fig, ax