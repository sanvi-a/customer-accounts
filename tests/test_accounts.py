"""Unit tests for the Accounts service (run with `nosetests`)."""
import unittest

from accounts import create_app, db
from accounts.models import Account, DataValidationError

BASE_URL = "/accounts"
SAMPLE = {"name": "John Doe", "email": "john@example.com", "address": "1 Main St", "phone_number": "555-1234"}


class TestAccountService(unittest.TestCase):
    """REST API tests."""

    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def _create(self, data=None):
        resp = self.client.post(BASE_URL, json=data or SAMPLE)
        self.assertEqual(resp.status_code, 201)
        return resp.get_json()

    def test_index(self):
        """It should return service info."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Account REST API Service")

    def test_health(self):
        """It should report healthy."""
        resp = self.client.get("/health")
        self.assertEqual(resp.get_json(), {"status": "OK"})

    def test_create_account(self):
        """It should create an account."""
        resp = self.client.post(BASE_URL, json=SAMPLE)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("Location", resp.headers)
        self.assertEqual(resp.get_json()["name"], SAMPLE["name"])

    def test_create_bad_data(self):
        """It should reject incomplete data."""
        resp = self.client.post(BASE_URL, json={"name": "x"})
        self.assertEqual(resp.status_code, 400)

    def test_create_bad_media_type(self):
        """It should reject non-JSON."""
        resp = self.client.post(BASE_URL, data="x", content_type="text/plain")
        self.assertEqual(resp.status_code, 415)

    def test_list_accounts(self):
        """It should list accounts."""
        self._create()
        self._create({"name": "Jane", "email": "jane@example.com"})
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 2)

    def test_read_account(self):
        """It should read an account."""
        created = self._create()
        resp = self.client.get(f"{BASE_URL}/{created['id']}")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["email"], SAMPLE["email"])

    def test_read_not_found(self):
        """It should 404 for a missing account."""
        self.assertEqual(self.client.get(f"{BASE_URL}/0").status_code, 404)

    def test_update_account(self):
        """It should update an account."""
        created = self._create()
        changed = dict(SAMPLE, name="Johnny")
        resp = self.client.put(f"{BASE_URL}/{created['id']}", json=changed)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Johnny")

    def test_update_not_found(self):
        """It should 404 updating a missing account."""
        self.assertEqual(self.client.put(f"{BASE_URL}/0", json=SAMPLE).status_code, 404)

    def test_update_bad_data(self):
        """It should reject bad update data."""
        created = self._create()
        resp = self.client.put(f"{BASE_URL}/{created['id']}", json={"name": "x"})
        self.assertEqual(resp.status_code, 400)

    def test_update_bad_media_type(self):
        """It should reject non-JSON update."""
        created = self._create()
        resp = self.client.put(f"{BASE_URL}/{created['id']}", data="x", content_type="text/plain")
        self.assertEqual(resp.status_code, 415)

    def test_delete_account(self):
        """It should delete an account."""
        created = self._create()
        self.assertEqual(self.client.delete(f"{BASE_URL}/{created['id']}").status_code, 204)
        self.assertEqual(self.client.get(f"{BASE_URL}/{created['id']}").status_code, 404)

    def test_delete_missing_is_idempotent(self):
        """It should return 204 even if the account is already gone."""
        self.assertEqual(self.client.delete(f"{BASE_URL}/0").status_code, 204)


class TestSecurity(unittest.TestCase):
    """Talisman and CORS tests."""

    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.client = self.app.test_client()

    def test_security_headers(self):
        """It should send Talisman security headers."""
        resp = self.client.get("/", environ_overrides={"wsgi.url_scheme": "https"})
        self.assertEqual(resp.headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(resp.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(resp.headers["Content-Security-Policy"], "default-src 'self'; object-src 'none'")
        self.assertEqual(resp.headers["Referrer-Policy"], "strict-origin-when-cross-origin")

    def test_cors_headers(self):
        """It should send CORS headers."""
        resp = self.client.get("/", headers={"Origin": "https://example.com"})
        self.assertIn(resp.headers["Access-Control-Allow-Origin"], ("*", "https://example.com"))


class TestModel(unittest.TestCase):
    """Model tests."""

    def test_repr_and_deserialize_errors(self):
        """It should represent itself and validate input."""
        self.assertIn("Account", repr(Account(name="a")))
        with self.assertRaises(DataValidationError):
            Account().deserialize(None)
