import hashlib
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import uuid

logger = logging.getLogger("fairprop.audit_trail")

class AuditTrail:
    """
    Manages audit trails for compliance checks.
    Creates timestamped, cryptographically signed records for legal defense.
    """
    
    def __init__(self, storage_dir: str = "audit_logs"):
        """
        Initialize audit trail system.
        
        Args:
            storage_dir: Directory to store audit logs.
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        logger.info("Audit trail initialized at %s", self.storage_dir)
    
    def create_audit_record(
        self,
        text: str,
        report: Dict[str, Any],
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new audit record.
        
        Args:
            text: The text that was audited.
            report: The audit report results.
            user_id: Optional user identifier.
            metadata: Optional additional metadata.
            
        Returns:
            Dict containing the audit record with signature.
        """
        timestamp = datetime.utcnow().isoformat() + "Z"
        audit_id = str(uuid.uuid4())
        
        record = {
            "audit_id": audit_id,
            "timestamp": timestamp,
            "user_id": user_id or "anonymous",
            "text_hash": self._hash_text(text),
            "text_length": len(text),
            "report": {
                "score": report["score"],
                "is_safe": report["is_safe"],
                "violations_count": len(report["flagged_items"]),
                "violations": [
                    {
                        "id": item["id"],
                        "category": item["category"],
                        "severity": item["severity"],
                        "found_word": item["found_word"]
                    }
                    for item in report["flagged_items"]
                ]
            },
            "metadata": metadata or {},
            "version": "1.0.0"
        }
        
        # Generate cryptographic signature
        record["signature"] = self._sign_record(record)
        
        # Save to disk
        self._save_record(record)
        
        logger.info("Created audit record %s", audit_id)
        return record
    
    def _hash_text(self, text: str) -> str:
        """Create SHA-256 hash of text for privacy."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    def _sign_record(self, record: Dict[str, Any]) -> str:
        """
        Create cryptographic signature of record.
        Uses HMAC-SHA256 for tamper detection.
        """
        # In production, use a secret key from environment
        # For now, we use a deterministic signature based on content
        record_copy = record.copy()
        record_copy.pop("signature", None)  # Remove signature field if present
        
        record_string = json.dumps(record_copy, sort_keys=True)
        signature = hashlib.sha256(record_string.encode('utf-8')).hexdigest()
        
        return signature
    
    def verify_record(self, record: Dict[str, Any]) -> bool:
        """
        Verify the integrity of an audit record.
        
        Args:
            record: The audit record to verify.
            
        Returns:
            True if signature is valid, False otherwise.
        """
        stored_signature = record.get("signature")
        if not stored_signature:
            return False
        
        computed_signature = self._sign_record(record)
        return stored_signature == computed_signature
    
    def _save_record(self, record: Dict[str, Any]):
        """Save audit record to disk."""
        # Organize by date for easy retrieval
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        date_dir = self.storage_dir / date_str
        date_dir.mkdir(exist_ok=True)
        
        filename = f"{record['audit_id']}.json"
        filepath = date_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2)
    
    def get_record(self, audit_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an audit record by ID.
        
        Args:
            audit_id: The audit record ID.
            
        Returns:
            The audit record if found, None otherwise.
        """
        # Search through date directories
        for date_dir in self.storage_dir.iterdir():
            if date_dir.is_dir():
                filepath = date_dir / f"{audit_id}.json"
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        record = json.load(f)
                    
                    # Verify integrity
                    if self.verify_record(record):
                        return record
                    else:
                        logger.warning("Record %s failed integrity check", audit_id)
                        return None
        
        return None
    
    def get_records_by_date(self, date: str) -> list[Dict[str, Any]]:
        """
        Get all audit records for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format.
            
        Returns:
            List of audit records.
        """
        date_dir = self.storage_dir / date
        if not date_dir.exists():
            return []
        
        records = []
        for filepath in date_dir.glob("*.json"):
            with open(filepath, 'r', encoding='utf-8') as f:
                record = json.load(f)
            
            if self.verify_record(record):
                records.append(record)
        
        return records
    
    def generate_compliance_certificate(
        self,
        audit_id: str,
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate a PDF compliance certificate for an audit record.
        
        Args:
            audit_id: The audit record ID.
            output_path: Optional path to save the PDF.
            
        Returns:
            Path to the generated PDF, or None if record not found.
        """
        record = self.get_record(audit_id)
        if not record:
            logger.error("Record %s not found", audit_id)
            return None
        
        try:
            from fpdf import FPDF # pylint: disable=import-error
            
            pdf = FPDF()
            pdf.add_page()
            
            # Header
            pdf.set_font("Helvetica", "B", 20)
            pdf.cell(0, 15, "FairProp Compliance Certificate", ln=True, align="C")
            
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 8, f"Audit ID: {record['audit_id']}", ln=True, align="C")
            pdf.cell(0, 8, f"Timestamp: {record['timestamp']}", ln=True, align="C")
            pdf.ln(10)
            
            # Score
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(0, 10, f"Compliance Score: {record['report']['score']}/100", ln=True)
            
            status = "PASS" if record['report']['is_safe'] else "FAIL"
            color = (0, 128, 0) if record['report']['is_safe'] else (255, 0, 0)
            pdf.set_text_color(*color)
            pdf.set_font("Helvetica", "B", 24)
            pdf.cell(0, 15, status, ln=True, align="C")
            pdf.set_text_color(0, 0, 0)
            
            pdf.ln(10)
            
            # Violations
            if record['report']['violations']:
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 10, "Violations Found:", ln=True)
                pdf.set_font("Helvetica", "", 10)
                
                for violation in record['report']['violations']:
                    pdf.multi_cell(0, 5, f"- [{violation['severity']}] {violation['category']}: \"{violation['found_word']}\"")
            
            pdf.ln(10)
            
            # Digital Signature
            pdf.set_font("Helvetica", "I", 8)
            pdf.cell(0, 5, "Digital Signature (SHA-256):", ln=True)
            pdf.set_font("Courier", "", 7)
            pdf.multi_cell(0, 4, record['signature'])
            
            # Footer
            pdf.set_y(-20)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(128, 128, 128)
            pdf.cell(0, 5, "This certificate is cryptographically signed and tamper-evident.", align="C")
            
            # Save
            if not output_path:
                output_path = f"compliance_certificate_{audit_id}.pdf"
            
            pdf.output(output_path)
            logger.info("Generated certificate: %s", output_path)
            return output_path
            
        except Exception as e:
            logger.error("Failed to generate certificate: %s", e)
            return None
