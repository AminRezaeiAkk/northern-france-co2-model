from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "report_assets"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#102A43"
BLUE = "#2E74B5"
TEAL = "#17A398"
GREEN = "#2A9D78"
ORANGE = "#E67E22"
PURPLE = "#7451D9"
GRAY = "#64748B"
LIGHT = "#F3F6F9"
GRID = "#D9E2EC"
RED = "#B84A3A"

SCENARIOS = [
    "announced_2030",
    "reported_2024_cluster",
    "user_inventory_4mt",
    "user_inventory_unconstrained",
]
LABELS = {
    "announced_2030": "Announced\nprojects",
    "reported_2024_cluster": "Reported 2024\ncluster",
    "user_inventory_4mt": "Provided inventory\n4 Mt/y limit",
    "user_inventory_unconstrained": "Provided inventory\nunconstrained",
}


def style_axes(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#9FB3C8")
    ax.tick_params(colors=NAVY, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.7)
    ax.set_axisbelow(True)


def box(ax, x, y, w, h, title, body, color, title_size=12, body_size=8.8):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.018,rounding_size=0.03",
        linewidth=1.6,
        edgecolor=color,
        facecolor="#FFFFFF",
    )
    ax.add_patch(patch)
    ax.text(x + 0.04 * w, y + 0.73 * h, title, color=color, fontsize=title_size, fontweight="bold", va="center")
    ax.text(x + 0.04 * w, y + 0.44 * h, body, color=NAVY, fontsize=body_size, va="center", linespacing=1.25)


def arrow(ax, x1, y1, x2, y2, color=GRAY):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, linewidth=1.5, color=color))


def chain_overview():
    fig, ax = plt.subplots(figsize=(14, 4.4), dpi=220)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.4)
    ax.axis("off")
    ax.text(0.2, 4.05, "Three-stage calculation boundary", fontsize=20, fontweight="bold", color=NAVY)
    ax.text(0.2, 3.70, "Industrial gas to conditioned CO2 at the Port of Dunkerque receiving point", fontsize=10.5, color=GRAY)
    box(ax, 0.35, 1.05, 3.65, 2.15, "1  CAPTURE", "Select connectable gas streams\nSeparate CO2 from source gas\nApply capture rate and availability", BLUE)
    box(ax, 5.17, 1.05, 3.65, 2.15, "2  PURIFICATION", "Remove condensate and water\nRemove source-dependent impurities\nCompress conditioned CO2 to 110 bar", TEAL)
    box(ax, 10.00, 1.05, 3.65, 2.15, "3  PIPELINE TRANSPORT", "Aggregate source flows\nSelect topology and nominal diameter\nDeliver to the Dunkerque coordinate", ORANGE)
    arrow(ax, 4.08, 2.12, 5.08, 2.12)
    arrow(ax, 8.90, 2.12, 9.90, 2.12)
    ax.text(7.0, 0.58, "Environmental study overlays all three physical stages: energy emissions + leakage + transport lifecycle screening", ha="center", fontsize=9.3, color=GREEN, fontweight="bold")
    ax.text(7.0, 0.27, "Excluded: terminal liquefaction, shipping, injection and geological storage", ha="center", fontsize=8.7, color=GRAY)
    fig.savefig(OUT / "chain_overview.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def capture_methods():
    fig, ax = plt.subplots(figsize=(14, 8.2), dpi=220)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.2)
    ax.axis("off")
    ax.text(0.2, 7.82, "Capture methods represented by source", fontsize=20, fontweight="bold", color=NAVY)
    lanes = [
        (6.10, "CRYOCAP FG - RETY LIME", BLUE, ["Kiln gas", "Cooling and cleaning", "Compression", "Cryogenic separation", "Concentrated CO2"]),
        (4.47, "OXYFUEL + CRYOCAP OXY - LUMBRES", PURPLE, ["Oxygen + kiln", "CO2-rich exhaust", "Water/acid gas removal", "Cryogenic + membrane", "Concentrated CO2"]),
        (2.84, "AMINE CAPTURE - AUNEUIL / ALUMINIUM", GREEN, ["Selected flue gas", "Cooling and pretreatment", "Amine absorber", "Steam regeneration", "Wet CO2"]),
        (1.21, "DMX - SELECTED STEELWORKS GAS", ORANGE, ["Cleaned BF gas", "DMX absorber", "Rich/lean phase split", "Rich-phase regeneration", "Wet CO2"]),
    ]
    for y, title, color, steps in lanes:
        ax.text(0.22, y + 0.82, title, fontsize=11, color=color, fontweight="bold")
        xs = np.linspace(0.35, 11.55, len(steps))
        for i, (x, label) in enumerate(zip(xs, steps)):
            patch = FancyBboxPatch((x, y), 2.0, 0.62, boxstyle="round,pad=0.015,rounding_size=0.04", linewidth=1.3, edgecolor=color, facecolor="#FFFFFF")
            ax.add_patch(patch)
            ax.text(x + 1.0, y + 0.31, label, ha="center", va="center", fontsize=8.3, color=NAVY, wrap=True)
            if i < len(steps) - 1:
                arrow(ax, x + 2.04, y + 0.31, xs[i + 1] - 0.08, y + 0.31, color=color)
    ax.text(0.22, 0.25, "BF gas = blast-furnace gas. Amine capture uses reversible chemical absorption; cryogenic capture uses compression and low-temperature separation.", fontsize=9, color=GRAY)
    fig.savefig(OUT / "capture_methods.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def purification_train():
    fig, ax = plt.subplots(figsize=(14, 4.8), dpi=220)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    ax.text(0.2, 4.42, "Purification and compression functions", fontsize=20, fontweight="bold", color=NAVY)
    ax.text(0.2, 4.06, "The equipment type is selected according to the captured stream; the calculation represents recovery, electricity and cost.", fontsize=9.7, color=GRAY)
    steps = [
        ("Captured CO2", "Wet stream from\ncapture plant", BLUE),
        ("Condensate removal", "Cooler and\nseparator vessel", TEAL),
        ("Dehydration", "Solid desiccant or\nselected dryer", GREEN),
        ("Impurity control", "Adsorption, washing,\nmembrane or cold separation", PURPLE),
        ("Compression", "Multiple stages with\ninterstage cooling", ORANGE),
        ("Pipeline product", "Conditioned CO2\nat 110 bar", RED),
    ]
    xs = np.linspace(0.25, 11.85, len(steps))
    for i, (title, body, color) in enumerate(steps):
        box(ax, xs[i], 1.20, 1.95, 1.95, title, body, color, title_size=10.2, body_size=8.2)
        if i < len(steps) - 1:
            arrow(ax, xs[i] + 1.99, 2.17, xs[i + 1] - 0.08, 2.17)
    ax.text(7.0, 0.55, "Represented mass recovery: 99.5%  |  Electricity: 0.09-0.18 MWh per tonne of product", ha="center", fontsize=10, color=NAVY, fontweight="bold")
    fig.savefig(OUT / "purification_train.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def scenario_comparison():
    df = pd.read_csv(ROOT / "outputs" / "scenario_comparison.csv")
    labels = [LABELS[s] for s in df["scenario"]]
    x = np.arange(len(df))
    fig, axs = plt.subplots(2, 2, figsize=(13.5, 9.2), dpi=220)
    fig.suptitle("Scenario comparison", fontsize=20, fontweight="bold", color=NAVY, x=0.06, ha="left")

    ax = axs[0, 0]
    received = df["sink_received_after_pipeline_leakage_tpy"] / 1e6
    avoided = df["chain_net_avoided_co2_tpy"] / 1e6
    w = 0.34
    ax.bar(x - w / 2, received, w, label="Received", color=BLUE)
    ax.bar(x + w / 2, avoided, w, label="Within-scope avoided", color=TEAL)
    ax.set_ylabel("Mt/y", color=NAVY)
    ax.set_title("CO2 flow", loc="left", color=NAVY, fontweight="bold")
    ax.set_xticks(x, labels)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    style_axes(ax)

    ax = axs[0, 1]
    cap = df["capture_capex_eur"] / 1e6
    pur = df["purification_capex_eur"] / 1e6
    pipe = df["pipeline_capex_eur"] / 1e6
    ax.bar(x, cap, color=BLUE, label="Capture")
    ax.bar(x, pur, bottom=cap, color=TEAL, label="Purification")
    ax.bar(x, pipe, bottom=cap + pur, color=ORANGE, label="Transport")
    ax.set_ylabel("million EUR", color=NAVY)
    ax.set_title("Capital by stage", loc="left", color=NAVY, fontweight="bold")
    ax.set_xticks(x, labels)
    ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper left")
    style_axes(ax)

    ax = axs[1, 0]
    ccap = df["capture_cost_eur_per_t_received"]
    cpur = df["purification_cost_eur_per_t_received"]
    cpipe = df["pipeline_cost_eur_per_t_received"]
    ax.bar(x, ccap, color=BLUE, label="Capture")
    ax.bar(x, cpur, bottom=ccap, color=TEAL, label="Purification")
    ax.bar(x, cpipe, bottom=ccap + cpur, color=ORANGE, label="Transport")
    low = df["full_chain_cost_low_eur_per_t_received"]
    high = df["full_chain_cost_high_eur_per_t_received"]
    base = df["full_chain_cost_eur_per_t_received"]
    ax.errorbar(x, base, yerr=np.vstack([base - low, high - base]), fmt="none", ecolor=NAVY, capsize=4, linewidth=1.2)
    ax.set_ylabel("EUR/t received", color=NAVY)
    ax.set_title("Annualized cost and deterministic range", loc="left", color=NAVY, fontweight="bold")
    ax.set_xticks(x, labels)
    style_axes(ax)

    ax = axs[1, 1]
    route = df["pipeline_route_length_km"]
    ax.bar(x, route, color=PURPLE)
    ax.set_ylabel("km", color=NAVY)
    ax.set_title("Total collection route", loc="left", color=NAVY, fontweight="bold")
    ax.set_xticks(x, labels)
    style_axes(ax)

    for ax in axs.flat:
        ax.tick_params(axis="x", labelrotation=0)
    fig.tight_layout(rect=(0, 0, 1, 0.95), h_pad=2.5, w_pad=2.0)
    fig.savefig(OUT / "scenario_comparison.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def pressure_profiles():
    fig, ax = plt.subplots(figsize=(12.5, 6.7), dpi=220)
    colors = [BLUE, TEAL, PURPLE, ORANGE]
    details = []
    for scenario, color in zip(SCENARIOS, colors):
        seg = pd.read_csv(ROOT / "outputs" / scenario / "pipeline_segments.csv")
        next_edge = {row.from_node: row for row in seg.itertuples(index=False)}
        candidates = []
        for start in next_edge:
            node = start
            distance = [0.0]
            pressure = [110.0]
            nodes = [start]
            visited = set()
            while node != "SINK" and node in next_edge and node not in visited:
                visited.add(node)
                row = next_edge[node]
                distance.append(distance[-1] + float(row.route_length_km))
                pressure.append(pressure[-1] - float(row.pressure_drop_bar))
                node = row.to_node
                nodes.append(node)
            if node == "SINK":
                candidates.append((110.0 - pressure[-1], distance, pressure, nodes))
        worst = max(candidates, key=lambda item: item[0])
        _, distance, pressure, nodes = worst
        ax.plot(distance, pressure, marker="o", linewidth=2.2, markersize=4.5, color=color, label=LABELS[scenario].replace("\n", " "))
        details.append((scenario, " -> ".join(nodes), distance[-1], pressure[-1]))
    ax.axhline(85.0, color=RED, linestyle="--", linewidth=1.5, label="Minimum permitted arrival: 85 bar")
    ax.set_xlabel("Cumulative routed distance from source (km)", color=NAVY)
    ax.set_ylabel("Calculated pressure (bar)", color=NAVY)
    ax.set_title("Worst source-to-sink pressure path in each scenario", loc="left", fontsize=17, fontweight="bold", color=NAVY)
    ax.set_ylim(82, 112)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(OUT / "pressure_profiles.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    (OUT / "pressure_profile_paths.json").write_text(json.dumps(details, indent=2), encoding="utf-8")


def source_flows():
    all_rows = []
    for scenario in SCENARIOS:
        df = pd.read_csv(ROOT / "outputs" / scenario / "source_results.csv")
        for row in df.itertuples(index=False):
            all_rows.append({"scenario": scenario, "source_id": row.source_id, "flow": row.allocated_product_co2_tpy / 1000.0})
    frame = pd.DataFrame(all_rows)
    piv = frame.pivot(index="scenario", columns="source_id", values="flow").reindex(SCENARIOS).fillna(0)
    fig, ax = plt.subplots(figsize=(12.5, 6.6), dpi=220)
    bottom = np.zeros(len(piv))
    source_colors = [BLUE, "#91A8C0", GREEN, PURPLE, ORANGE, RED]
    for source, color in zip(piv.columns, source_colors):
        values = piv[source].to_numpy()
        ax.bar(np.arange(len(piv)), values, bottom=bottom, color=color, label=source)
        bottom += values
    ax.set_xticks(np.arange(len(piv)), [LABELS[s] for s in piv.index])
    ax.set_ylabel("Allocated product CO2 (kt/y)", color=NAVY)
    ax.set_title("Source contribution to pipeline product", loc="left", fontsize=17, fontweight="bold", color=NAVY)
    ax.legend(ncol=6, frameon=False, loc="upper left", fontsize=8.5)
    style_axes(ax)
    fig.tight_layout()
    fig.savefig(OUT / "source_flows.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def environmental_comparison():
    df = pd.read_csv(ROOT / "outputs" / "scenario_comparison.csv")
    labels = [LABELS[s] for s in df["scenario"]]
    x = np.arange(len(df))
    fig, ax = plt.subplots(figsize=(12.5, 6.7), dpi=220)
    burden = df["environmental_climate_burden_kgco2e_per_t_received"]
    bars = ax.bar(x, burden, color=TEAL)
    ax.set_xticks(x, labels)
    ax.set_ylabel("kg CO2-eq per tonne received", color=NAVY)
    ax.set_title("Environmental screening: lifecycle climate burden intensity", loc="left", fontsize=17, fontweight="bold", color=NAVY)
    style_axes(ax)
    for bar, value in zip(bars, burden):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{value:.1f}", ha="center", va="bottom", fontsize=9, color=NAVY)
    fig.tight_layout()
    fig.savefig(OUT / "environmental_comparison.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    chain_overview()
    capture_methods()
    purification_train()
    scenario_comparison()
    pressure_profiles()
    source_flows()
    environmental_comparison()
    print(f"Wrote report figures to {OUT}")


if __name__ == "__main__":
    main()
