from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

styles = getSampleStyleSheet()
styles['Normal'].fontSize = 10
styles['Heading1'].fontSize = 16
styles['Heading2'].fontSize = 13

filename = "Blue_Nile_Comprehensive_SRS.pdf"
doc = SimpleDocTemplate(filename, pagesize=A4)
story = []

def add(text, style="Normal", space=0.18):
    story.append(Paragraph(text, styles[style]))
    story.append(Spacer(1, space * inch))

# Title
add("<b>COMPREHENSIVE SRS DOCUMENT – BLUE NILE COFFEE PLATFORM</b>", "Heading1", 0.4)
add("AI-Enhanced E-Commerce System Specification", "Heading2", 0.4)
story.append(PageBreak())

# Introduction
add("<b>1. INTRODUCTION</b>", "Heading1")
add(
    "This Software Requirements Specification (SRS) outlines the full technical framework for the Blue Nile Coffee "
    "AI-driven e-commerce platform. It consolidates all system modules including personalization, recommendations, "
    "predictive analytics, automation, workflow tools, influencer content, and analytics integrations."
)

# System Overview
add("<b>2. SYSTEM OVERVIEW</b>", "Heading1")
add(
    "The platform uses a decoupled architecture:\n"
    "• Frontend: React / Vue / Next.js\n"
    "• Backend: Laravel API-driven framework\n"
    "• AI Layer: External APIs (Clerk.io, Pinecone, OpenAI, Mixpanel)\n"
    "• Analytics Layer: Mixpanel, TikTok Pixel, Meta Pixel, Google Analytics"
)

# Clerk.io
add("<b>3. AI PERSONALIZATION & RECOMMENDATION ENGINE</b>", "Heading1")
add("<b>3.1 Clerk.io Integration</b>", "Heading2")
add("Website: https://www.clerk.io")
add(
    "Clerk.io provides real-time product recommendations, personalized search, upsell and cross-sell automation, "
    "email recommendations, and dynamic product ranking."
)
add(
    "<b>Pricing Tiers:</b><br/>"
    "• Starter: $99–$149/month (small stores)<br/>"
    "• Professional: $149–$249/month (mid-sized stores)<br/>"
    "• Enterprise: $349+/month"
)

# Pinecone + OpenAI
add("<b>3.2 Pinecone + OpenAI Embeddings</b>", "Heading2")
add("Pinecone: https://www.pinecone.io<br/>OpenAI: https://platform.openai.com")
add(
    "This setup stores vector embeddings representing product metadata and customer behaviour. "
    "It enables similarity search and intelligent recommendation flows."
)
add(
    "<b>Pinecone Pricing:</b><br/>"
    "• Free Tier<br/>"
    "• Standard Pods: ~$0.096–$0.29 per GB-hour"
)
add(
    "<b>OpenAI Embeddings:</b><br/>"
    "• Approx. $0.02 per 1M tokens"
)

story.append(PageBreak())

# Mixpanel
add("<b>4. PREDICTIVE ANALYTICS & GROWTH INSIGHTS</b>", "Heading1")
add("<b>Mixpanel Analytics</b>", "Heading2")
add("Website: https://mixpanel.com")
add(
    "Mixpanel provides behavioural analytics including funnels, churn prediction, retention tracking, "
    "repeat purchasing analysis, and customer cohort breakdowns."
)
add(
    "<b>Pricing:</b><br/>"
    "• Free: Up to 20M monthly events<br/>"
    "• Growth Plan: ~$20–$35/month<br/>"
    "• Enterprise: Custom pricing"
)

# AI Content Automation
add("<b>5. AI CONTENT & CHAT AUTOMATION</b>", "Heading1")
add(
    "OpenAI GPT-4/GPT-5 enables automated support chat, description writing, email automation, "
    "influencer script generation, and dynamic product content."
)

# Workflow
add("<b>6. WORKFLOW AUTOMATION</b>", "Heading1")
add("Tools: Zapier (https://zapier.com), Make (https://make.com)")
add(
    "Used for CRM automation, order updates, customer notifications, internal workflow triggers, "
    "and recurring marketing automations."
)

# Influencer tools
add("<b>7. AI VIDEO & INFLUENCER TOOLING</b>", "Heading1")
add(
    "AI-driven platforms such as D-ID, Synthesia, and Runway are used to generate influencer-style UGC videos "
    "for ads, social media, and promotional material."
)

# Architecture
add("<b>8. SYSTEM ARCHITECTURE SUMMARY</b>", "Heading1")
add(
    "1. User accesses frontend application\n"
    "2. Frontend communicates with Laravel backend via REST APIs\n"
    "3. Backend integrates with AI APIs for recommendations and analytics\n"
    "4. Behaviour analytics captured through Mixpanel and Pixels\n"
    "5. Automation layer handles workflows"
)

story.append(PageBreak())

# Costs
add("<b>9. ESTIMATED MONTHLY AI OPERATING COST</b>", "Heading1")
add(
    "• Small e-commerce: ~$120/month\n"
    "• Mid-sized: $250–$500/month\n"
    "• Large enterprise: $800+/month based on API volume"
)

# Conclusion
add("<b>10. CONCLUSION</b>", "Heading1")
add(
    "This comprehensive SRS defines the AI-driven architecture required for a scalable and automated e-commerce "
    "ecosystem for Blue Nile Coffee and can be applied to any related dropshipping or multi-brand coffee platform."
)

doc.build(story)

filename