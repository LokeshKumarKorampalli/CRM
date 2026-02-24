"""Unit tests for AI Real Estate CRM application."""
import unittest
from unittest.mock import patch, MagicMock
from bson.objectid import ObjectId
from datetime import datetime


class TestApp(unittest.TestCase):
    """Test Flask routes and helper functions."""

    def setUp(self):
        """Set up test client and mock MongoDB."""
        # Patch MongoDB collections before importing app
        self.leads_patcher = patch("app.leads_collection")
        self.emails_patcher = patch("app.emails_collection")
        self.mock_leads = self.leads_patcher.start()
        self.mock_emails = self.emails_patcher.start()

        from app import app
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret-key"
        self.app = app
        self.client = app.test_client()

    def tearDown(self):
        self.leads_patcher.stop()
        self.emails_patcher.stop()

    # ---- Route tests ----

    def test_home_page(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"AI", resp.data)

    def test_buyer_entry_page(self):
        resp = self.client.get("/buyer")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Buyer", resp.data)

    def test_buyer_register_get(self):
        resp = self.client.get("/buyer/register")
        self.assertEqual(resp.status_code, 200)

    def test_buyer_register_empty_fields(self):
        resp = self.client.post(
            "/buyer/register",
            data={"name": "", "email": "a@b.com", "phone": "1234567890"},
            follow_redirects=True,
        )
        self.assertIn(b"All fields are required", resp.data)

    def test_buyer_register_invalid_email(self):
        resp = self.client.post(
            "/buyer/register",
            data={"name": "Test", "email": "not-an-email", "phone": "1234567890"},
            follow_redirects=True,
        )
        self.assertIn(b"valid email", resp.data)

    def test_buyer_register_duplicate_email(self):
        self.mock_leads.find_one.return_value = {"_id": ObjectId(), "email": "dup@test.com"}
        resp = self.client.post(
            "/buyer/register",
            data={"name": "Test", "email": "dup@test.com", "phone": "1234567890"},
            follow_redirects=True,
        )
        self.assertIn(b"already registered", resp.data)

    def test_buyer_register_success(self):
        fake_id = ObjectId()
        self.mock_leads.find_one.return_value = None
        self.mock_leads.insert_one.return_value = MagicMock(inserted_id=fake_id)

        resp = self.client.post(
            "/buyer/register",
            data={"name": "Jane Doe", "email": "jane@example.com", "phone": "5551234567"},
        )
        # Should redirect to chat page
        self.assertEqual(resp.status_code, 302)
        self.assertIn(f"/chat/{fake_id}", resp.headers["Location"])
        self.mock_leads.insert_one.assert_called_once()

    def test_buyer_login_not_found(self):
        self.mock_leads.find_one.return_value = None
        resp = self.client.post(
            "/buyer/login",
            data={"identifier": "nobody@test.com"},
            follow_redirects=True,
        )
        self.assertIn(b"Account not found", resp.data)

    def test_buyer_login_success(self):
        fake_id = ObjectId()
        self.mock_leads.find_one.return_value = {
            "_id": fake_id,
            "name": "Jane",
            "email": "jane@test.com",
        }
        resp = self.client.post(
            "/buyer/login",
            data={"identifier": "jane@test.com"},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn(f"/chat/{fake_id}", resp.headers["Location"])

    def test_logout(self):
        with self.client.session_transaction() as sess:
            sess["buyer_id"] = "some-id"
            sess["buyer_name"] = "Test"
        resp = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"logged out", resp.data)

    def test_chat_requires_login(self):
        fake_id = ObjectId()
        resp = self.client.get(f"/chat/{fake_id}", follow_redirects=True)
        self.assertIn(b"log in", resp.data)

    def test_dashboard_page(self):
        self.mock_leads.find.return_value.sort.return_value = []
        resp = self.client.get("/dashboard")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Dashboard", resp.data)

    def test_analytics_page(self):
        self.mock_leads.find.return_value = []
        resp = self.client.get("/analytics")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Analytics", resp.data)

    def test_lead_view_not_found(self):
        self.mock_leads.find_one.return_value = None
        fake_id = ObjectId()
        resp = self.client.get(f"/lead/{fake_id}")
        self.assertEqual(resp.status_code, 404)

    def test_lead_view_success(self):
        fake_id = ObjectId()
        self.mock_leads.find_one.return_value = {
            "_id": fake_id,
            "name": "Test Lead",
            "email": "test@test.com",
            "phone": "1234567890",
            "budget": 500000,
            "timeline_months": 3,
            "property_type": "3BHK",
            "location": "Austin",
            "lead_score": 75,
            "status": "Hot",
            "recommended_action": "propose_meeting",
            "decision_reason": "High budget",
            "decision_confidence": 0.85,
            "extra_details": ["pool", "garden"],
            "meeting_time": None,
            "available_slots": [],
            "execution_trace": [],
            "conversation": [],
        }
        resp = self.client.get(f"/lead/{fake_id}")
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"Test Lead", resp.data)

    # ---- Helper function tests ----

    def test_generate_buyer_summary(self):
        from app import generate_buyer_summary

        lead = {
            "location": "Austin",
            "budget": 500000,
            "property_type": "3BHK",
            "timeline_months": 6,
        }
        summary = generate_buyer_summary(lead)
        self.assertIn("Austin", summary)
        self.assertIn("500000", summary)
        self.assertIn("3BHK", summary)
        self.assertIn("6 month(s)", summary)

    def test_generate_buyer_summary_empty(self):
        from app import generate_buyer_summary

        summary = generate_buyer_summary({})
        self.assertEqual(summary, "")


if __name__ == "__main__":
    unittest.main()
