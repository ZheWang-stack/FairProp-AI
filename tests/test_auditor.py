import pytest
from fairprop import FairHousingAuditor


class TestBasicAuditing:
    """Test basic auditing functionality."""
    
    def test_auditor_initialization(self):
        """Test that auditor initializes correctly."""
        auditor = FairHousingAuditor()
        assert auditor is not None
        assert len(auditor.rules) > 0
    
    def test_clean_text_passes(self):
        """Test that clean text passes compliance check."""
        auditor = FairHousingAuditor()
        text = "Beautiful 3-bedroom apartment with modern kitchen and spacious living room."
        report = auditor.scan_text(text)
        
        assert report['score'] == 100
        assert report['is_safe'] is True
        assert len(report['flagged_items']) == 0
    
    def test_explicit_violation_detected(self):
        """Test that explicit violations are detected."""
        auditor = FairHousingAuditor()
        text = "No children allowed in this building."
        report = auditor.scan_text(text)
        
        assert report['score'] < 100
        assert report['is_safe'] is False
        assert len(report['flagged_items']) > 0
    
    def test_multiple_violations(self):
        """Test detection of multiple violations."""
        auditor = FairHousingAuditor()
        text = "Perfect for young professionals. No children. Christians preferred."
        report = auditor.scan_text(text)
        
        assert report['score'] < 70
        assert report['is_safe'] is False
        assert len(report['flagged_items']) >= 2


class TestJurisdictions:
    """Test multi-jurisdiction support."""
    
    def test_california_jurisdiction(self):
        """Test California-specific rules."""
        auditor = FairHousingAuditor(jurisdictions=['california'])
        text = "No Section 8 vouchers accepted."
        report = auditor.scan_text(text)
        
        # California prohibits source of income discrimination
        assert len(report['flagged_items']) > 0
        assert any('source of income' in item['category'].lower() 
                  for item in report['flagged_items'])
    
    def test_multiple_jurisdictions(self):
        """Test loading multiple jurisdictions."""
        auditor = FairHousingAuditor(jurisdictions=['california', 'nyc'])
        assert len(auditor.rules) > 0
        assert len(auditor.jurisdictions) == 2
    
    def test_international_jurisdiction(self):
        """Test international jurisdiction support."""
        auditor = FairHousingAuditor(jurisdictions=['uk'])
        assert len(auditor.rules) > 0


class TestCaching:
    """Test caching functionality."""
    
    def test_cache_hit(self):
        """Test that caching works for repeated scans."""
        auditor = FairHousingAuditor()
        text = "Beautiful apartment with great views."
        
        # First scan (cache miss)
        report1 = auditor.scan_text(text, use_cache=True)
        
        # Second scan (cache hit)
        report2 = auditor.scan_text(text, use_cache=True)
        
        # Results should be identical
        assert report1['score'] == report2['score']
        assert len(report1['flagged_items']) == len(report2['flagged_items'])
    
    def test_cache_bypass(self):
        """Test that cache can be bypassed."""
        auditor = FairHousingAuditor()
        text = "Spacious home with modern amenities."
        
        # Scan without cache
        report = auditor.scan_text(text, use_cache=False)
        assert report is not None


class TestRuleReload:
    """Test hot-reload functionality."""
    
    def test_reload_rules(self):
        """Test that rules can be reloaded."""
        auditor = FairHousingAuditor()
        initial_count = len(auditor.rules)
        
        result = auditor.reload_rules()
        
        assert 'old_count' in result
        assert 'new_count' in result
        assert result['old_count'] == initial_count


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_text(self):
        """Test scanning empty text."""
        auditor = FairHousingAuditor()
        report = auditor.scan_text("")
        
        assert report['score'] == 100
        assert report['is_safe'] is True
    
    def test_very_long_text(self):
        """Test scanning very long text."""
        auditor = FairHousingAuditor()
        text = "Beautiful apartment. " * 1000
        report = auditor.scan_text(text)
        
        assert report is not None
        assert 'score' in report
    
    def test_special_characters(self):
        """Test text with special characters."""
        auditor = FairHousingAuditor()
        text = "Apartment with café, résumé required! 🏠"
        report = auditor.scan_text(text)
        
        assert report is not None


class TestSeverityLevels:
    """Test different severity levels."""
    
    def test_critical_violation(self):
        """Test critical severity violations."""
        auditor = FairHousingAuditor()
        text = "No blacks allowed."
        report = auditor.scan_text(text)
        
        assert len(report['flagged_items']) > 0
        assert any(item['severity'] == 'Critical' 
                  for item in report['flagged_items'])
    
    def test_warning_level(self):
        """Test warning level violations."""
        auditor = FairHousingAuditor()
        text = "Perfect for young professionals."
        report = auditor.scan_text(text)
        
        # May trigger age-related warning
        if len(report['flagged_items']) > 0:
            assert any(item['severity'] in ['Warning', 'Critical'] 
                      for item in report['flagged_items'])


class TestLanguageSupport:
    """Test multi-language support."""
    
    def test_english_language(self):
        """Test English language initialization."""
        auditor = FairHousingAuditor(language='en')
        assert auditor.language == 'en'
    
    def test_chinese_language(self):
        """Test Chinese language initialization."""
        auditor = FairHousingAuditor(language='zh')
        assert auditor.language == 'zh'
    
    def test_spanish_language(self):
        """Test Spanish language initialization."""
        auditor = FairHousingAuditor(language='es')
        assert auditor.language == 'es'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
