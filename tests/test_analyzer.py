import unittest

from creator_growth.analyzer import VideoRow, analyze_rows


class CreatorGrowthTests(unittest.TestCase):
    def test_detects_outlier_and_generates_next_topic(self):
        rows = [
            VideoRow("IG", "A", "Huge", "AI video", "Why it works", "breakdown", "English", 100000, 1000, 5000, 100),
            VideoRow("IG", "B", "Normal", "AI news", "Update", "recap", "English", 1000, 1000, 20, 1),
        ]
        briefs = analyze_rows(rows)
        self.assertEqual(briefs[0].title, "Huge")
        self.assertGreater(briefs[0].outlier_score, 1)
        self.assertIn("Hindi", briefs[0].localization_plan[0])


if __name__ == "__main__":
    unittest.main()

