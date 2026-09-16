from __future__ import annotations

import unittest
from pathlib import Path

from north_co2_model.model import load_model_inputs, run_custom_scenario, run_scenario


class ModelRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.inputs = load_model_inputs(cls.root)
        cls.announced = run_scenario(cls.inputs, "announced_2030")
        cls.user_case = run_scenario(cls.inputs, "user_inventory_4mt")

    def test_sink_coordinate_and_boundary(self) -> None:
        sink = self.inputs.config["sink"]
        self.assertEqual(sink["x_l93_m"], 636000.0)
        self.assertEqual(sink["y_l93_m"], 7105000.0)
        self.assertEqual(sink["node_type"], "receiving_site")
        self.assertFalse(self.announced.summary["downstream_terminal_shipping_storage_included"])
        self.assertEqual(
            self.announced.summary["model_stages"],
            ["capture", "purification", "transport_to_dunkerque_site"],
        )

    def test_irep_inventory_reconciles(self) -> None:
        total = sum(source.irep_2024_total_co2_tpy for source in self.inputs.sources)
        self.assertAlmostEqual(total, 7_539_800.0, places=3)

    def test_announced_case_uses_anchor_projects(self) -> None:
        active = {
            row["source_id"]
            for row in self.announced.source_results
            if row["allocated_product_co2_tpy"] > 0
        }
        self.assertEqual(active, {"S1", "S3"})
        self.assertAlmostEqual(self.announced.summary["total_purified_co2_tpy"], 1_410_000.0, places=3)
        self.assertLessEqual(
            self.announced.summary["total_purified_co2_tpy"],
            self.announced.summary["sink_capacity_tpy"],
        )

    def test_stage_mass_balances(self) -> None:
        for result in (self.announced, self.user_case):
            for row in result.source_results:
                self.assertAlmostEqual(
                    row["captured_before_purification_tpy"],
                    row["allocated_product_co2_tpy"] + row["purification_loss_tpy"],
                    places=6,
                )
            self.assertAlmostEqual(
                result.summary["total_purified_co2_tpy"] - result.summary["pipeline_leakage_tpy"],
                result.summary["sink_received_after_pipeline_leakage_tpy"],
                places=6,
            )

    def test_sink_capacity_is_enforced(self) -> None:
        self.assertLessEqual(
            self.user_case.summary["total_purified_co2_tpy"],
            self.user_case.summary["sink_capacity_tpy"] + 1e-6,
        )
        self.assertGreaterEqual(self.user_case.summary["total_curtailed_product_co2_tpy"], 0.0)

    def test_active_inventory_is_compact_five_source_set(self) -> None:
        self.assertEqual([source.source_id for source in self.inputs.sources], ["S1", "S2", "S3", "S4", "S5"])
        self.assertEqual(len(self.inputs.sources), 5)

    def test_peng_robinson_is_used_in_transport(self) -> None:
        self.assertEqual(self.announced.summary["transport_equation_of_state"], "Peng-Robinson")
        self.assertGreater(self.announced.summary["transport_eos_density_min_kg_per_m3"], 0.0)
        for segment in self.announced.pipeline_segments:
            self.assertEqual(segment["equation_of_state"], "Peng-Robinson")
            self.assertGreater(segment["eos_density_kg_per_m3"], 0.0)
            self.assertGreater(segment["eos_compressibility_factor"], 0.0)

    def test_environmental_study_reconciles(self) -> None:
        summary = self.announced.summary
        self.assertTrue(summary["environmental_study_included"])
        self.assertGreater(summary["environmental_total_climate_burden_tco2e_per_year"], 0.0)
        self.assertLessEqual(
            summary["environmental_lifecycle_net_avoided_co2_tpy"],
            summary["chain_net_avoided_co2_tpy"],
        )
        self.assertGreater(len(summary["environmental_transport_benchmarks"]), 0)

    def test_hydraulic_constraints(self) -> None:
        transport = self.inputs.config["transport"]
        for result in (self.announced, self.user_case):
            self.assertGreaterEqual(
                result.summary["minimum_arrival_pressure_bar"] + 1e-8,
                transport["minimum_arrival_pressure_bar"],
            )
            for segment in result.pipeline_segments:
                self.assertLessEqual(
                    segment["velocity_m_per_s"],
                    transport["maximum_velocity_m_per_s"] + 1e-8,
                )

    def test_three_stage_costs_are_separate_and_reconcile(self) -> None:
        summary = self.announced.summary
        self.assertGreater(summary["capture_capex_eur"], 0.0)
        self.assertGreater(summary["purification_capex_eur"], 0.0)
        self.assertGreater(summary["pipeline_capex_eur"], 0.0)
        self.assertNotIn("terminal_capex_eur", summary)
        self.assertAlmostEqual(
            summary["total_chain_capex_eur"],
            summary["capture_capex_eur"]
            + summary["purification_capex_eur"]
            + summary["pipeline_capex_eur"],
            places=6,
        )
        self.assertAlmostEqual(
            summary["total_chain_annual_cost_eur"],
            summary["capture_annual_cost_eur"]
            + summary["purification_annual_cost_eur"]
            + summary["pipeline_annual_cost_eur"],
            places=6,
        )

    def test_active_products_pass_six_component_screen(self) -> None:
        self.assertEqual(self.user_case.summary["product_spec_components_screened"], 6)
        self.assertEqual(self.user_case.summary["product_spec_components_in_reference"], 27)
        self.assertAlmostEqual(
            self.user_case.summary["product_spec_screening_coverage_fraction"],
            6 / 27,
            places=12,
        )
        screened = {limit.component for limit in self.inputs.product_limits}
        referenced = {limit.component for limit in self.inputs.reference_product_limits}
        self.assertTrue(screened.issubset(referenced))
        self.assertEqual(
            set(self.user_case.summary["product_spec_components_not_screened"]),
            referenced - screened,
        )
        for row in self.user_case.source_results:
            if row["allocated_product_co2_tpy"] > 0:
                self.assertTrue(row["product_spec_screening_pass"], row["product_spec_failures"])

    def test_uncertainty_range_contains_base_case(self) -> None:
        summary = self.user_case.summary
        self.assertLess(summary["full_chain_cost_low_eur_per_t_received"], summary["full_chain_cost_eur_per_t_received"])
        self.assertGreater(summary["full_chain_cost_high_eur_per_t_received"], summary["full_chain_cost_eur_per_t_received"])

    def test_custom_case_does_not_modify_base_inputs(self) -> None:
        original_scenarios = set(self.inputs.config["scenarios"])
        custom = run_custom_scenario(
            self.inputs,
            active_source_ids=["S1"],
            flow_basis="irep_2024_total",
            sink_capacity_tpy=1_500_000.0,
            finance_overrides={"electricity_price_eur_per_mwh": 100.0},
        )
        self.assertEqual(custom.summary["active_sources"], 1)
        self.assertEqual(set(self.inputs.config["scenarios"]), original_scenarios)


if __name__ == "__main__":
    unittest.main()
