import streamlit as st
import json
import os
from datetime import datetime
from fpdf import FPDF
from fairprop import FairHousingAuditor

# --- Page Configuration ---
st.set_page_config(
    page_title="FairProp Compliance Auditor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar ---
with st.sidebar:
    st.title("🛡️ FairProp")
    st.markdown("### Compliance Auditor")
    st.info("**Compliance Standard:** HUD 2024")
    
    st.markdown("---")
    st.markdown("#### About")
    st.write(
        "FairProp is an enterprise-grade auditing tool designed to ensure "
        "real estate listings comply with the Fair Housing Act (FHA)."
    )
    
    st.markdown("---")
    st.warning(
        "**Legal Disclaimer:** This tool provides automated compliance "
        "checks based on rule-based logic. It is **not legal advice**. "
        "Always consult with a compliance officer or legal professional."
    )
    st.caption("Powered by Open Source | Fair Housing Act (42 U.S.C. § 3601 et seq.)")

# --- Audit Engine Helpers ---
@st.cache_resource
def get_auditor():
    """Singleton access to the auditor to avoid reloading heavy AI models."""
    rules_path = os.path.join(os.getcwd(), "fha_rules.json")
    return FairHousingAuditor(rules_path=rules_path)

def run_text_audit(text):
    try:
        auditor = get_auditor()
        return auditor.scan_text(text)
    except Exception as e:
        st.error(f"Audit Engine Error: {e}")
        return None

def run_image_audit(image_file):
    try:
        auditor = get_auditor()
        return auditor.scan_image(image_file)
    except Exception as e:
        st.error(f"OCR Audit Engine Error: {e}")
        return None

def get_ai_fix(text):
    try:
        auditor = get_auditor()
        return auditor.suggest_fix(text)
    except Exception as e:
        return f"AI Fix failed: {e}"

# --- PDF Generation Helpers ---
def create_pdf_certificate(text, report):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 20, "FairProp Compliance Certificate", ln=True, align="C")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    
    # Score Section
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Audit Safety Score:", ln=True)
    pdf.set_font("Helvetica", "B", 48)
    
    score = report['score']
    if report['is_safe']:
        pdf.set_text_color(0, 128, 0) # Green
    else:
        pdf.set_text_color(255, 0, 0) # Red
        
    pdf.cell(0, 30, f"{score}/100", ln=True, align="C")
    pdf.set_text_color(0, 0, 0) # Reset to black
    
    # Pass/Fail Stamp
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 24)
    if report['is_safe']:
        pdf.set_fill_color(200, 255, 200)
        pdf.cell(0, 20, "PASS", ln=True, align="C", fill=True)
    else:
        pdf.set_fill_color(255, 200, 200)
        pdf.cell(0, 20, "FAIL", ln=True, align="C", fill=True)
    
    pdf.ln(10)
    
    # Original Text
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Listing Description:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 5, text)
    
    pdf.ln(10)
    
    # Findings Summary
    if report['flagged_items']:
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Key Findings:", ln=True)
        pdf.set_font("Helvetica", "", 10)
        for item in report['flagged_items']:
            pdf.set_font("Helvetica", "B", 10)
            pdf.multi_cell(0, 5, f"- [{item['severity']}] {item['category']}: Found '{item['found_word']}'")
            pdf.set_font("Helvetica", "I", 9)
            pdf.multi_cell(0, 5, f"  Suggestion: {item['suggestion']}")
            pdf.ln(2)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, "Audited by FairProp Open Source Engine", align="C")
    
    return pdf.output()

# --- UI Component Helpers ---
def display_report(text, report):
    if report:
        st.markdown("---")
        
        # --- Metrics ---
        col1, col2 = st.columns([1, 4])
        with col1:
            st.metric(
                label="Safety Score",
                value=f"{report['score']}/100",
                delta=None,
                delta_color="normal"
            )
        
        with col2:
            if report['is_safe']:
                st.success("✅ **Listing passed major compliance checks.**")
            elif report['score'] > 40:
                st.warning("⚠️ **Compliance risks detected. Revision recommended.**")
            else:
                st.error("🚨 **High-risk violations found. Immediate correction required.**")

        # --- AI Auto-Fix Section ---
        if not report['is_safe']:
            st.markdown("### ✨ AI Suggested Revision (Auto-Fix)")
            with st.spinner("Generating compliant version..."):
                fixed_text = get_ai_fix(text)
                if fixed_text:
                    st.success("**Revised Listing:**")
                    st.write(fixed_text)
                    st.info("💡 Note: Review the AI suggestion to ensure it still accurately describes the property.")

        # --- Download Button ---
        try:
            pdf_data = create_pdf_certificate(text, report)
            st.download_button(
                label="📄 Download Compliance Certificate",
                data=pdf_data,
                file_name=f"FairProp_Audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                type="secondary"
            )
        except Exception as e:
            st.error(f"Failed to generate certificate: {e}")

        # --- Detailed Reports ---
        if report['flagged_items']:
            st.subheader("Audit Findings")
            
            for item in report['flagged_items']:
                severity = item['severity']
                with st.expander(f"{'🔴' if severity == 'Critical' else '🟡'} [{severity}] {item['category']} - Flagged word: \"{item['found_word']}\""):
                    
                    st.markdown(f"**Trigger detected:** `{item['found_word']}`")
                    st.markdown(f"**Legal Basis:** {item['legal_basis']}")
                    
                    if severity == "Critical":
                        st.error(f"**Compliance Issue:** This violates FHA standards regarding `{item['category']}`.")
                    else:
                        st.warning(f"**Compliance Warning:** This may be perceived as implicit bias regarding `{item['category']}`.")
                    
                    st.markdown(f"💡 **Suggestion:** *{item['suggestion']}*")
        else:
            st.balloons()
            st.success("No FHA violations detected based on current rule set.")

# --- UI Header ---
st.title("Real Estate Listing Compliance Audit")
st.markdown(
    "Paste your property description or **upload a flyer image** to scan for potential FHA violations."
)

# --- Main App Layout ---
tab1, tab2 = st.tabs(["📝 Text Description", "🖼️ Upload Flyer Image"])

with tab1:
    listing_description = st.text_area(
        "Listing Description",
        placeholder="Enter the property description here...",
        height=200,
        key="text_input_main"
    )
    if st.button("Run Text Audit", type="primary", key="btn_text_audit"):
        if not listing_description.strip():
            st.warning("Please enter a description to scan.")
        else:
            with st.spinner("Analyzing text content..."):
                report = run_text_audit(listing_description)
                display_report(listing_description, report)

with tab2:
    uploaded_file = st.file_uploader("Choose a flyer image...", type=["jpg", "jpeg", "png"], key="flyer_uploader")
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Flyer", use_container_width=True)
        if st.button("Run Image OCR Audit", type="primary", key="btn_image_audit"):
            with st.spinner("Extracting text and analyzing image..."):
                result = run_image_audit(uploaded_file)
                if result:
                    st.info("**Extracted Text from Image:**")
                    st.code(result['extracted_text'], wrap_lines=True)
                    display_report(result['extracted_text'], result['report'])

# --- Footer ---
st.markdown("---")
st.caption(f"© {datetime.now().year} FairProp Compliance Solutions. All rights reserved.")
