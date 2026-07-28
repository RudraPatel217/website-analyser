import pandas as pd

def generate_excel_report(df_all_domain, df_all_pages, df_all_issues, df_all_audit, filename):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_all_domain.to_excel(
            writer, sheet_name='Domain_Info', index=False)
        df_all_pages.to_excel(
            writer, sheet_name='Crawled_Pages', index=False)
        if not df_all_issues.empty:
            df_all_issues.to_excel(
                writer, sheet_name='SEO_Issues', index=False)
        if not df_all_audit.empty:
            df_all_audit.to_excel(
                writer, sheet_name='Technical_Audit', index=False)

def generate_security_report(cyber_results, filename):
    summary_data = []
    ssl_data = []
    headers_data = []
    threats_data = []
    recs_data = []
    
    for res in cyber_results:
        domain = res["domain"]
        summary_data.append({
            "Domain": domain,
            "Security Score": res["global_score"],
            "Security Grade": res["grade"],
            "Risk Rating": res["rating"],
            "HTTP Status": res["status_code"],
            "Response Time (sec)": res["load_time"]
        })
        
        ssl = res["ssl_info"]
        ssl_data.append({
            "Domain": domain,
            "SSL Valid": ssl["valid"],
            "Issuer Common Name": ssl["issuer_cn"],
            "Issuer Organization": ssl["issuer_org"],
            "Expiration Date": ssl["expiry_date"],
            "Days Remaining": ssl["days_left"],
            "Error Details": ssl["error"]
        })
        
        for h in res["header_findings"]:
            headers_data.append({
                "Domain": domain,
                "Security Header": h["header"],
                "Status": h["status"],
                "Value": h["value"],
                "Severity": h["severity"],
                "Description": h["desc"]
            })
            
        for reason in res["phishing_reasons"]:
            threats_data.append({
                "Domain": domain,
                "Threat Type": "Phishing Indicator",
                "Finding": reason
            })
            
        for reason in res["malware_reasons"]:
            threats_data.append({
                "Domain": domain,
                "Threat Type": "Malware Risk",
                "Finding": reason
            })
            
        for rec in res["recommendations"]:
            recs_data.append({
                "Domain": domain,
                "Remediation Action Item": rec
            })
            
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Security_Summary', index=False)
        pd.DataFrame(ssl_data).to_excel(writer, sheet_name='SSL_Validation', index=False)
        pd.DataFrame(headers_data).to_excel(writer, sheet_name='Security_Headers', index=False)
        if threats_data:
            pd.DataFrame(threats_data).to_excel(writer, sheet_name='Threat_Alerts', index=False)
        else:
            pd.DataFrame([{"Domain": "N/A", "Threat Type": "None", "Finding": "No threat alerts identified."}]).to_excel(writer, sheet_name='Threat_Alerts', index=False)
        pd.DataFrame(recs_data).to_excel(writer, sheet_name='Remediation_Plan', index=False)


def generate_unified_report(df_all_domain, df_all_pages, df_all_issues, df_all_audit, cyber_results, filename):
    summary_data = []
    ssl_data = []
    headers_data = []
    threats_data = []
    recs_data = []
    
    for res in cyber_results:
        domain = res["domain"]
        summary_data.append({
            "Domain": domain,
            "Security Score": res["global_score"],
            "Security Grade": res["grade"],
            "Risk Rating": res["rating"],
            "HTTP Status": res["status_code"],
            "Response Time (sec)": res["load_time"]
        })
        
        ssl = res["ssl_info"]
        ssl_data.append({
            "Domain": domain,
            "SSL Valid": ssl["valid"],
            "Issuer Common Name": ssl["issuer_cn"],
            "Issuer Organization": ssl["issuer_org"],
            "Expiration Date": ssl["expiry_date"],
            "Days Remaining": ssl["days_left"],
            "Error Details": ssl["error"]
        })
        
        for h in res["header_findings"]:
            headers_data.append({
                "Domain": domain,
                "Security Header": h["header"],
                "Status": h["status"],
                "Value": h["value"],
                "Severity": h["severity"],
                "Description": h["desc"]
            })
            
        for reason in res["phishing_reasons"]:
            threats_data.append({
                "Domain": domain,
                "Threat Type": "Phishing Indicator",
                "Finding": reason
            })
            
        for reason in res["malware_reasons"]:
            threats_data.append({
                "Domain": domain,
                "Threat Type": "Malware Risk",
                "Finding": reason
            })
            
        for rec in res["recommendations"]:
            recs_data.append({
                "Domain": domain,
                "Remediation Action Item": rec
            })
            
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df_all_domain.to_excel(writer, sheet_name='Domain_Info', index=False)
        df_all_pages.to_excel(writer, sheet_name='Crawled_Pages', index=False)
        if not df_all_issues.empty:
            df_all_issues.to_excel(writer, sheet_name='SEO_Issues', index=False)
        if not df_all_audit.empty:
            df_all_audit.to_excel(writer, sheet_name='Technical_Audit', index=False)
            
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Security_Summary', index=False)
        pd.DataFrame(ssl_data).to_excel(writer, sheet_name='SSL_Validation', index=False)
        pd.DataFrame(headers_data).to_excel(writer, sheet_name='Security_Headers', index=False)
        if threats_data:
            pd.DataFrame(threats_data).to_excel(writer, sheet_name='Threat_Alerts', index=False)
        else:
            pd.DataFrame([{"Domain": "N/A", "Threat Type": "None", "Finding": "No threat alerts identified."}]).to_excel(writer, sheet_name='Threat_Alerts', index=False)
        pd.DataFrame(recs_data).to_excel(writer, sheet_name='Remediation_Plan', index=False)

