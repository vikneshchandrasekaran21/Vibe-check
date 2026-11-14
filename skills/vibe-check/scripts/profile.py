#!/usr/bin/env python3
"""vibe-check profile: let the code decide what the app is, before anyone answers questions.

Founders say "no payments" or "no kids" while the code says otherwise (a forgotten Stripe file,
a `dob` field in the signup form). This script searches the code, schema, forms and config for
evidence behind each profile question and records every hit with its file and line.
Rule: an answer can ADD to the profile but never REMOVE what the code shows. coverage.py
refuses to let a profile module be N/A as a whole when this script found evidence for it.

Usage:  python3 profile.py [PROJECT_DIR] [--out .vibe-check]
        python3 profile.py [PROJECT_DIR] --where   which project is this, and does it hold app code? Writes nothing and
                                                   always exits 0 (tools show other codes as "Failed"); read the
                                                   "APP CODE: yes" or "APP CODE: no" line instead
Writes: <out>/profile.md and <out>/profile.json
Read-only and offline. Python 3.8+, standard library only.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {
    "node_modules", ".git", ".next", ".nuxt", ".svelte-kit", ".output", "dist", "build", "out", "coverage",
    ".vibe-check", "vendor", ".venv", "venv", "env", "__pycache__", ".turbo", ".vercel", ".netlify", ".expo",
    "Pods", "target", ".gradle", ".idea", ".cache", ".wrangler",
}
EXT = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro", ".py", ".rb", ".php", ".go",
       ".dart", ".kt", ".swift", ".java", ".cs", ".html", ".sql", ".prisma", ".graphql", ".json", ".yaml", ".yml",
       ".toml", ".md", ".mdx", ".txt", ".tf", ".rules", ".xml", ".plist", ".gradle", ".env", ".example")
TEST_RX = re.compile(r"(^|/)(__tests__|tests?|spec|fixtures?|examples?|stories|mocks?|e2e)(/|$)|\.(test|spec|stories)\.")
I = re.I

# signal: (question, module or None, strength, label, regex)
# strength "strong" = one non-test hit is enough to load the module; "weak" = listed as a lead only
SIGNALS = [
    # children and students
    ("Children or students", "kids-education", "strong", "date-of-birth or birthday field",
     re.compile(r"\b(?:dob|date_of_birth|dateOfBirth|birth_?date|birthDate|birthday)\b", I)),
    ("Children or students", "kids-education", "strong", "age field, minimum age or under-13/under-18 logic",
     re.compile(r"\b(?:isMinor|is_minor|minAge|min_age|under_?13|under_?16|under_?18|age_?gate|ageVerified|age_verified)\b|\bage\s*(?:<|<=|>=|>)\s*1[3-8]\b", I)),
    ("Children or students", "kids-education", "strong", "parent or guardian consent or contact",
     re.compile(r"\b(?:parental_?consent|parentConsent|guardian(?:_|)(?:email|name|phone|consent|id)|parent_?email|parentEmail)\b", I)),
    ("Children or students", "kids-education", "strong", "school, class, grade, student or teacher data",
     re.compile(r"\b(?:student_?id|studentId|students|teacher_?id|teacherId|teachers|school_?id|schoolId|school_?name|classroom|class_?section|grade_?level|homework|syllabus|guardian)\b", I)),
    ("Children or students", "kids-education", "strong", "Google Classroom or school email domains",
     re.compile(r"classroom\.googleapis|googleapis\.com/auth/classroom|\.k12\.|\.sch\.(?:uk|in)|@[\w-]+\.edu\b", I)),
    ("Children or students", "kids-education", "weak", "kids, children or teen wording",
     re.compile(r"\b(?:kids?|children|child-friendly|for teens|young learners|ages \d{1,2}\s*[-–to]+\s*\d{1,2})\b", I)),
    # payments and money
    ("Payments", "fintech", "strong", "payment provider SDK or API",
     re.compile(r"""["'](?:stripe|@stripe/[\w-]+|razorpay|@paypal/[\w-]+|paypal-rest-sdk|@paddle/[\w-]+|@lemonsqueezy/[\w-]+|cashfree-pg|@cashfreepayments/[\w-]+|phonepe[\w-]*|paytmchecksum|braintree|square|mollie|@mollie/[\w-]+|adyen|@adyen/[\w-]+|instamojo|juspay[\w-]*)["']|\bimport\s+(?:stripe|razorpay)\b|api\.razorpay\.com|api\.stripe\.com|checkout\.razorpay\.com""", I)),
    ("Payments", "fintech", "strong", "hosted payment or checkout link",
     re.compile(r"buy\.stripe\.com|checkout\.stripe\.com|rzp\.io/|razorpay\.me/|paypal\.me/|pages\.razorpay\.com|lemonsqueezy\.com/checkout|gumroad\.com/l/|paddle\.com/checkout|instamojo\.com/@", I)),
    ("Payments", "fintech", "strong", "in-app purchases or subscriptions SDK",
     re.compile(r"react-native-purchases|react-native-iap|@revenuecat|StoreKit|SKPaymentQueue|BillingClient|expo-in-app-purchases|cordova-plugin-purchase|in_app_purchase", I)),
    ("Payments", "fintech", "strong", "wallet, credits, payout or refund logic",
     re.compile(r"\b(?:wallet_?balance|walletBalance|payouts?|refunds?|store_?credit|storeCredit|credits_?balance|add_?credits|addCredits)\b", I)),
    ("Payments", "fintech", "weak", "price, amount, currency or invoice fields",
     re.compile(r"\b(?:price|unit_amount|amount_?paid|currency|invoice|subscription_?status|checkout)\b", I)),
    # sensitive data
    ("Health data", "health", "strong", "health or medical data",
     re.compile(r"\b(?:diagnos[ie]s|medications?|prescriptions?|symptoms?|blood_?(?:pressure|sugar|type|group)|heart_?rate|HealthKit|health_?connect|patient_?id|patients|medical_?record|ehr|fhir|allerg(?:y|ies))\b", I)),
    ("Financial data", "fintech", "strong", "bank, card or tax identity data",
     re.compile(r"\b(?:ifsc|bank_?account|account_?number|upi_?id|vpa|card_?number|cvv|pan_?(?:number|card|no)|gstin|kyc)\b", I)),
    ("Government ID", None, "strong", "government ID numbers (Aadhaar, passport, SSN…)",
     re.compile(r"\b(?:aadhaar|aadhar|passport_?(?:no|number)|ssn|social_?security|national_?id|voter_?id|driving_?licen[cs]e)\b", I)),
    ("Location or biometrics", None, "strong", "precise location or biometric data",
     re.compile(r"\b(?:navigator\.geolocation|getCurrentPosition|latitude|longitude|expo-location|CLLocationManager|face_?id|faceId|fingerprint|biometric|LocalAuthentication)\b", I)),
    # AI
    ("AI features", "ai-features", "strong", "calls to an AI model",
     re.compile(r"""(?:from\s+|require\(\s*|import\s+)["'](?:openai|@anthropic-ai/sdk|@google/generative-ai|@google/genai|groq-sdk|@mistralai/[\w-]+|cohere-ai|replicate|ollama|ai|@ai-sdk/[\w-]+|langchain|@langchain/[\w-]+|llamaindex)["']|\bimport\s+(?:openai|anthropic)\b|chat\.completions\.create|messages\.create\(|api\.openai\.com|api\.anthropic\.com|generativelanguage\.googleapis\.com|api\.groq\.com|api\.mistral\.ai""", I)),
    ("AI agents or MCP", "ai-agents", "strong", "AI agent tools, function calling or MCP",
     re.compile(r"@modelcontextprotocol/|\bMcpServer\b|\bmcp\.server\b|tool_choice|function_call|\btools\s*:\s*\[\s*\{|createAgent|AgentExecutor|@openai/agents", I)),
    # people interacting
    ("Users post or chat", "community", "strong", "posts, comments, chat, follows or reports",
     re.compile(r"""\b(?:create\s+table\s+(?:if\s+not\s+exists\s+)?(?:public\.)?["']?(?:comments|posts|messages|chats?|conversations|follows|followers|reactions|reports|reviews)\b|model\s+(?:Comment|Post|Message|Chat|Conversation|Follow|Reaction|Report|Review)\s*\{|["'`]/api/(?:comments|posts|messages|chat|follow|reports))""", I)),
    # platforms
    ("Mobile app", "mobile", "strong", "mobile app project",
     re.compile(r"""["'](?:expo|react-native|@capacitor/core|@ionic/[\w-]+)["']\s*:|^\s*flutter:\s*$|AndroidManifest\.xml|UIApplicationMain|@main\s+struct\s+\w+\s*:\s*App""", I | re.M)),
    ("Desktop app or extension", "desktop-extensions", "strong", "desktop app or browser extension",
     re.compile(r"""["'](?:electron|@tauri-apps/api|@tauri-apps/cli)["']\s*:|"manifest_version"\s*:\s*[23]""", I)),
    ("Cloud infrastructure", "cloud-infra", "strong", "infrastructure as code or cloud SDKs",
     re.compile(r"""^\s*(?:resource|provider)\s+"(?:aws|google|azurerm)|kind:\s*(?:Deployment|StatefulSet|Ingress)\b|["']@aws-sdk/[\w-]+["']|\bboto3\b|["']@google-cloud/[\w-]+["']|["']@azure/[\w-]+["']""", I | re.M)),
    ("Several languages", "i18n", "strong", "translations or locale files",
     re.compile(r"""["'](?:i18next|react-i18next|next-intl|react-intl|vue-i18n|@formatjs/[\w-]+|@lingui/[\w-]+|svelte-i18n)["']|\bgettext\(|LocalizedStringKey|NSLocalizedString""", I)),
    ("Business or government buyers", "enterprise", "weak", "SSO, SCIM or multi-tenant organizations",
     re.compile(r"\b(?:saml|scim|okta|azure_?ad|entra|workos|organization_?id|organizationId|tenant_?id|tenantId)\b", I)),
    ("Countries", None, "weak", "India (INR, +91, GST, UPI)", re.compile(r"\bINR\b|\+91[\s-]?\d|\bGSTIN?\b|\bUPI\b|₹")),
    ("Countries", None, "weak", "EU/UK (EUR, GBP, GDPR, VAT)", re.compile(r"\bEUR\b|\bGBP\b|\bGDPR\b|\bVAT\b|€|£")),
    ("Countries", None, "weak", "US (USD, state lists, CCPA)", re.compile(r"\bUSD\b|\bCCPA\b|\bCPRA\b|California")),
]
PATH_SIGNALS = [
    ("Several languages", "i18n", "strong", "locale folder", re.compile(r"(^|/)(locales?|i18n|lang|translations)/[\w-]+\.(json|ya?ml|po)$")),
    ("Mobile app", "mobile", "strong", "native project folder", re.compile(r"(^|/)(android/app/src/main/AndroidManifest\.xml|ios/[\w-]+\.xcodeproj/|pubspec\.yaml|capacitor\.config\.(ts|json)|app\.json)$")),
    ("Children or students", "kids-education", "weak", "file or folder named for kids or schools", re.compile(r"(^|/)[^/]*(kids?|school|student|teacher|classroom|parent)[^/]*$", I)),
]


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            p = Path(dirpath) / fn
            rel = p.relative_to(root).as_posix()
            yield rel, p


MARKERS = ["package.json", "requirements.txt", "pyproject.toml", "Pipfile", "Gemfile", "composer.json", "go.mod", "Cargo.toml",
           "pubspec.yaml", "pom.xml", "build.gradle", "build.gradle.kts", "deno.json", "bun.lockb", "app.json", "index.html",
           "manage.py", "wp-config.php", "Dockerfile", "supabase", "firebase.json", "vercel.json", "netlify.toml", "wrangler.toml",
           "src", "app", "pages", "lib", "server", "api"]
NOT_PROJECTS = {"downloads", "desktop", "documents", "pictures", "movies", "music", "library", "applications"}


def where(root: Path) -> int:
    """Say which project this is. Read-only, writes nothing, never looks outside ROOT."""
    git_root, branch = None, None
    for d in [root] + list(root.parents):
        head = d / ".git" / "HEAD"
        if head.is_file():
            git_root = d
            ref = head.read_text("utf-8", errors="replace").strip()
            branch = ref.split("refs/heads/", 1)[1] if "refs/heads/" in ref else ref[:12]
            break
    found = [m for m in MARKERS if (root / m).exists()]
    code_files = 0
    for n, (rel, p) in enumerate(walk(root)):
        if n > 3000 or code_files >= 3:
            break
        if p.suffix.lower() in (".js", ".jsx", ".ts", ".tsx", ".py", ".rb", ".php", ".go", ".java", ".kt", ".swift", ".dart",
                                ".cs", ".rs", ".vue", ".svelte", ".astro", ".html"):
            code_files += 1
    strong = [m for m in found if m not in ("src", "app", "pages", "lib", "server", "api", "index.html")]
    home_like = root == Path.home() or root.name.lower() in NOT_PROJECTS or root == Path(root.anchor)
    has_code = not home_like and (bool(strong) or code_files >= 3)
    info = {"project": root.name, "path": str(root), "git_root": str(git_root) if git_root else None, "branch": branch,
            "has_app_code": has_code, "markers": found, "looks_like_a_personal_folder": home_like}
    print(json.dumps(info, indent=1))
    print("APP CODE: " + ("yes" if has_code else "no"))
    if has_code:
        print(f"Project: {root.name} · {root}" + (f" · branch {branch}" if branch else "") + f" · app code found ({', '.join(found[:5]) or 'code files'})")
        return 0
    print(f"No app code in {root}" + (" (this looks like a personal folder, not a project)" if home_like else "") +
          ". Ask the user which project folder to check; don't search other folders.")
    return 0


def main() -> int:
    argv = sys.argv[1:]
    if "--where" in argv:
        argv.remove("--where")
        return where(Path(argv[0] if argv else ".").resolve())
    out_arg = None
    if "--out" in argv:
        i = argv.index("--out"); out_arg = argv[i + 1]; del argv[i:i + 2]
    root = Path(argv[0] if argv else ".").resolve()
    out = Path(out_arg).resolve() if out_arg else root / ".vibe-check"
    hits = []
    scanned = 0
    for rel, p in walk(root):
        test = bool(TEST_RX.search(rel))
        for q, mod, strength, label, rx in PATH_SIGNALS:
            if rx.search(rel):
                hits.append({"question": q, "module": mod, "strength": strength, "label": label, "where": rel, "text": "", "test": test})
        if not (p.name.lower().endswith(EXT) or p.name.startswith(".env")) or p.name in ("package-lock.json", "yarn.lock", "pnpm-lock.yaml"):
            continue
        try:
            if p.stat().st_size > 1_500_000:
                continue
            text = p.read_text("utf-8", "replace")
        except OSError:
            continue
        scanned += 1
        for n, line in enumerate(text.splitlines(), 1):
            if len(line) > 2000:
                continue
            for q, mod, strength, label, rx in SIGNALS:
                if rx.search(line):
                    hits.append({"question": q, "module": mod, "strength": strength, "label": label,
                                 "where": f"{rel}:{n}", "text": line.strip()[:140], "test": test})
    modules = {}
    questions = {}
    for h in hits:
        questions.setdefault(h["question"], []).append(h)
        if h["module"] and h["strength"] == "strong" and not h["test"]:
            modules.setdefault(h["module"], []).append(h["where"])
    out.mkdir(parents=True, exist_ok=True)
    meta = {"tool": "vibe-check profile", "version": "3.1.0", "root": str(root),
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "files_scanned": scanned,
            "modules_with_evidence": {m: sorted(set(w))[:25] for m, w in modules.items()},
            "evidence": hits[:3000]}
    (out / "profile.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    md = ["# vibe-check profile (from the code)", "",
          "What the code shows, before any questions. **An answer can add to this, but never remove it:** a module listed "
          "under *Must run* can't be marked N/A as a whole, even if the founder says it doesn't apply. If the code is really unused, "
          "prove it (for example: no import of the file anywhere) and record that in the ledger.", "",
          "## Must run (strong evidence outside tests)", ""]
    if modules:
        for m, w in sorted(modules.items()):
            md.append(f"- **{m}**: {len(set(w))} places, e.g. `{sorted(set(w))[0]}`")
    else:
        md.append("- (none)")
    md += ["", "## Evidence by question", ""]
    for q, hs in questions.items():
        strong = [h for h in hs if h["strength"] == "strong" and not h["test"]]
        weak = [h for h in hs if h not in strong]
        md.append(f"### {q}: {'YES' if strong else ('maybe' if weak else 'no')} ({len(strong)} strong, {len(weak)} weak or in tests)")
        for h in (strong + weak)[:12]:
            tag = " *(test/example)*" if h["test"] else ("" if h["strength"] == "strong" else " *(weak)*")
            md.append(f"- {h['label']}: `{h['where']}`{tag}" + (f" `{h['text'][:90]}`" if h["text"] else ""))
        md.append("")
    (out / "profile.md").write_text("\n".join(md) + "\n")
    print(f"profile: {scanned} files -> {out / 'profile.md'}")
    for m, w in sorted(modules.items()):
        print(f"  MUST RUN {m:<20} {len(set(w)):>3} places, e.g. {sorted(set(w))[0]}")
    for q, hs in questions.items():
        if not any(h["module"] for h in hs):
            strong = [h for h in hs if h["strength"] == "strong" and not h["test"]]
            if strong:
                print(f"  NOTE     {q:<20} {len(strong):>3} places, e.g. {strong[0]['where']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
