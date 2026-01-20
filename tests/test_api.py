import pytest
from fastapi.testclient import TestClient
from api_server import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test REST API endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data['service'] == 'FairProp Compliance API'
        assert data['version'] == '2.0.0'
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
        assert 'rules_loaded' in data
    
    def test_single_scan(self):
        """Test single text scan endpoint."""
        response = client.post("/api/scan", json={
            "text": "Beautiful 3-bedroom apartment with modern kitchen.",
            "jurisdictions": [],
            "use_cache": True
        })
        assert response.status_code == 200
        data = response.json()
        assert 'score' in data
        assert 'is_safe' in data
        assert 'flagged_items' in data
    
    def test_scan_with_violation(self):
        """Test scan detects violations."""
        response = client.post("/api/scan", json={
            "text": "No children allowed in this building.",
            "jurisdictions": []
        })
        assert response.status_code == 200
        data = response.json()
        assert data['score'] < 100
        assert data['is_safe'] is False
        assert len(data['flagged_items']) > 0
    
    def test_batch_scan(self):
        """Test batch scanning endpoint."""
        response = client.post("/api/scan/batch", json={
            "items": [
                {"text": "First listing", "jurisdictions": []},
                {"text": "Second listing", "jurisdictions": []}
            ]
        })
        assert response.status_code == 200
        data = response.json()
        assert 'results' in data
        assert 'total_scanned' in data
        assert data['total_scanned'] == 2
    
    def test_reload_rules(self):
        """Test rule reload endpoint."""
        response = client.post("/api/reload-rules")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert 'old_count' in data
        assert 'new_count' in data
    
    def test_stats_endpoint(self):
        """Test statistics endpoint."""
        response = client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert 'total_scans' in data


class TestAPIValidation:
    """Test API input validation."""
    
    def test_missing_text_field(self):
        """Test that missing text field returns error."""
        response = client.post("/api/scan", json={
            "jurisdictions": []
        })
        assert response.status_code == 422  # Validation error
    
    def test_invalid_jurisdiction(self):
        """Test handling of invalid jurisdiction."""
        response = client.post("/api/scan", json={
            "text": "Test listing",
            "jurisdictions": ["invalid_jurisdiction"]
        })
        # Should still work, just won't load invalid jurisdiction
        assert response.status_code == 200


class TestCaching:
    """Test API caching behavior."""
    
    def test_cache_enabled(self):
        """Test scan with caching enabled."""
        response = client.post("/api/scan", json={
            "text": "Luxury apartment with great amenities.",
            "use_cache": True
        })
        assert response.status_code == 200
    
    def test_cache_disabled(self):
        """Test scan with caching disabled."""
        response = client.post("/api/scan", json={
            "text": "Luxury apartment with great amenities.",
            "use_cache": False
        })
        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
