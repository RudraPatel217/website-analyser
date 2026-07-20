import pandas as pd

def generate_ai_seo_recommendations(df_pages, df_issues, df_audit):
    """
    Analyzes SEO crawl results locally using a heuristic reasoning engine
    and generates dynamic, prioritized optimization recommendations.
    No API Key required.
    """
    recs = []
    
    # 1. Performance Recommendations
    if df_audit is not None and not df_audit.empty:
        avg_speed = df_audit["Load_Time_sec"].mean()
        if avg_speed > 2.0:
            recs.append({
                "category": "Performance",
                "title": f"Optimize Server Response & Caching (Avg Response: {avg_speed:.2f}s)",
                "description": f"The average load time across {len(df_audit)} pages is {avg_speed:.2f}s, which is slower than the recommended threshold of 1.5 seconds.",
                "severity": "High",
                "impact": "Improves overall First Contentful Paint (FCP) and reduces bounce rates, signaling better page experience to search algorithms.",
                "action_item": "Leverage server-side caching (e.g. Redis), enable gzip/brotli compression, and compress static assets."
            })
        elif avg_speed > 1.2:
            recs.append({
                "category": "Performance",
                "title": "Minor Site Latency Optimizations",
                "description": f"Minor delays found on some landing assets (average load time {avg_speed:.2f}s).",
                "severity": "Medium",
                "impact": "Polishes user perception of page transitions and speed indexing metrics.",
                "action_item": "Review database queries and defer non-critical JS/CSS assets."
            })
            
        # 2. Image Alt Text Accessibility
        total_missing_alt = df_audit["Missing_Alt_Images"].sum()
        if total_missing_alt > 0:
            recs.append({
                "category": "Accessibility & SEO",
                "title": f"Resolve Missing Image Alt Attributes ({total_missing_alt} instances)",
                "description": f"Found {total_missing_alt} image elements across your site that lack descriptive 'alt' tags.",
                "severity": "Medium",
                "impact": "Enables image-based indexing in Google Image Search and ensures ADA accessibility compliance.",
                "action_item": "Audit page image assets and inject short, descriptive keyword-rich text into all alt attributes."
            })
            
        # 3. Canonical Tagging
        missing_canonical_pages = df_audit[df_audit["Canonical_Tag"] == "Missing"]
        if not missing_canonical_pages.empty:
            recs.append({
                "category": "Technical SEO",
                "title": f"Implement Canonical Tags ({len(missing_canonical_pages)} pages affected)",
                "description": f"The canonical validation check shows that {len(missing_canonical_pages)} URLs are missing self-referential canonical tags.",
                "severity": "High",
                "impact": "Prevents search engines from indexing duplicate URL parameters (e.g., tracking links) and consolidates page authority.",
                "action_item": "Inject a <link rel='canonical' href='...' /> tag referencing the definitive URL into the HTML header of all indexable pages."
            })

        # 4. Social Meta (Open Graph)
        missing_og_pages = df_audit[df_audit["Social_Meta_OG"] == "Missing"]
        if not missing_og_pages.empty:
            recs.append({
                "category": "On-Page SEO",
                "title": f"Configure Social Graph Metadata ({len(missing_og_pages)} pages missing OG tags)",
                "description": f"{len(missing_og_pages)} pages are missing Facebook Open Graph or Twitter Card tags.",
                "severity": "Low",
                "impact": "Improves click-through rates (CTR) and visual presentations when pages are shared on social platforms.",
                "action_item": "Add 'og:title', 'og:description', and 'og:image' meta tags to the document head."
            })

        # 5. Schema Structured Data
        missing_schema_pages = df_audit[df_audit["Structured_Data"] == "No"]
        if not missing_schema_pages.empty:
            recs.append({
                "category": "Technical SEO",
                "title": f"Inject Structured Schema Markup ({len(missing_schema_pages)} pages missing)",
                "description": f"No JSON-LD structure or organizational schema metadata was found on {len(missing_schema_pages)} audited URLs.",
                "severity": "Medium",
                "impact": "Allows search engines to display 'Rich Snippets' (star ratings, prices, search boxes) directly inside search results.",
                "action_item": "Generate and append organizational or article JSON-LD schema tags to your main landing pages."
            })
            
    # 6. Crawl issues (from df_issues)
    if df_issues is not None and not df_issues.empty:
        # Title length issues
        title_issues = df_issues[df_issues["Issue Name"] == "Title Length Issue"]
        if not title_issues.empty:
            recs.append({
                "category": "On-Page SEO",
                "title": f"Optimize Title Tags ({len(title_issues)} pages affected)",
                "description": f"Found {len(title_issues)} pages with sub-optimal title lengths (outside the 10-65 character sweet spot).",
                "severity": "Medium",
                "impact": "Prevents truncation of search snippets in Google results, maximizing CTR.",
                "action_item": "Rewrite affected titles to be concise, contain primary keywords, and fit within 60 characters."
            })
            
        # Meta description issues
        meta_issues = df_issues[df_issues["Issue Name"] == "Meta Description Issue"]
        if not meta_issues.empty:
            recs.append({
                "category": "On-Page SEO",
                "title": f"Revise Meta Descriptions ({len(meta_issues)} pages affected)",
                "description": f"Found {len(meta_issues)} pages with missing, too long, or too short meta descriptions.",
                "severity": "Medium",
                "impact": "Improves user search snippet layout, encouraging higher click density.",
                "action_item": "Ensure all indexable pages have unique meta descriptions between 120 and 155 characters."
            })
            
        # Missing H1 tag issues
        h1_issues = df_issues[df_issues["Issue Name"] == "Missing H1 Tag"]
        if not h1_issues.empty:
            recs.append({
                "category": "On-Page SEO",
                "title": f"Resolve Missing or Blank H1 Headers ({len(h1_issues)} pages)",
                "description": f"Auditing detected missing heading structures (no single h1 tag found) on {len(h1_issues)} pages.",
                "severity": "High",
                "impact": "Improves keyword prominence in content hierarchy, which directly influences primary rankings.",
                "action_item": "Add a single, unique H1 tag containing the primary keyword to the header section of each page."
            })
            
        # Connection failures
        conn_issues = df_issues[df_issues["Issue Name"] == "Connection Failure"]
        if not conn_issues.empty:
            recs.append({
                "category": "Technical Infrastructure",
                "title": f"Critical Server Connection Failures ({len(conn_issues)} pages)",
                "description": f"The crawler failed to establish connection or received errors on {len(conn_issues)} target pages.",
                "severity": "Critical",
                "impact": "Prevents search engine crawler indexation entirely and leads to drop out of search indexes.",
                "action_item": "Inspect DNS records, verify SSL certificate configuration, check server loads and firewall access logs."
            })
            
    # Default recommendations if no issues were found
    if not recs:
        recs.append({
            "category": "SEO Maintenance",
            "title": "Enforce Periodic Crawling & Link Monitoring",
            "description": "Excellent baseline health! No immediate structural, header, speed, or SEO metadata compliance warnings were found.",
            "severity": "Low",
            "impact": "Maintains domain authority and helps quickly identify indexing regressions.",
            "action_item": "Establish a recurring monthly crawl cycle and set up uptime alerts for critical service paths."
        })
        
    return recs
