# Standards mapping

Every item of six widely used security standards, mapped to the vibe-check checks that cover it. `coverage.py` reads these tables and adds a **Standards** section to the report: for each item, ✅ (every mapped check passed), ❌ (a mapped check failed), ◐ (some mapped checks couldn't be confirmed or weren't done) or ➖ (doesn't apply). It's a coverage view of this audit, **not a certification or a compliance attestation.**

Item IDs and names are the standards' own; the mapping and the checks are vibe-check's. Standard text isn't copied here: read each standard for its full requirements (OWASP ASVS is CC BY-SA 4.0). ASVS is mapped by chapter. Items marked **Human** need a specialist (for example memory-safety testing of native code or a mobile binary review), and the report lists them under *Only a human can confirm*.

Sources (checked 2026-11-14): OWASP Top 10:2025 (top10.owasp.org), OWASP API Security Top 10 2023, OWASP Top 10 for LLM Applications 2025, OWASP Mobile Top 10 2024, OWASP ASVS 5.0.0 (May 2025), 2025 CWE Top 25 (cwe.mitre.org). Re-check these lists when a new edition is published, then update this file.

## OWASP Top 10:2025
| ID | Name | vibe-check checks |
|---|---|---|
| A01:2025 | Broken Access Control | BS-01, BS-02, SEC-014, SEC-015, SEC-016, SEC-017, SEC-019, SEC-020, SEC-034, SEC-059, SEC-075, SEC-076, PLT-004, PLT-011, HUNT-004, LIVE-002, LIVE-003, LIVE-004, SEC-084, SEC-087 |
| A02:2025 | Security Misconfiguration | BS-11, SEC-037, SEC-046, SEC-061, SEC-079, SEC-080, PLT-043, PLT-044, OPS-041, VUL-012 |
| A03:2025 | Software Supply Chain Failures | BS-09, BS-19, SEC-048, SEC-049, SUP-001, SUP-002, SUP-003, SUP-006, SUP-007, SUP-008, SUP-014, VUL-005, VUL-006, VUL-007, VUL-008, VUL-013 |
| A04:2025 | Cryptographic Failures | SEC-040, SEC-041, SEC-042, SEC-043, SEC-044, SEC-045, SEC-047, SEC-072, SEC-089, SEC-090 |
| A05:2025 | Injection | BS-04, SEC-027, SEC-028, SEC-029, SEC-030, SEC-031, SEC-065, SEC-066, SEC-068, AIF-009 |
| A06:2025 | Insecure Design | BS-06, BS-08, HUNT-001, HUNT-002, HUNT-003, HUNT-005, SEC-053, SEC-071, REL-044 |
| A07:2025 | Authentication Failures | SEC-001, SEC-002, SEC-004, SEC-005, SEC-006, SEC-007, SEC-009, SEC-010, SEC-011, SEC-056, SEC-071, SEC-073, SEC-086, SEC-088, SEC-089 |
| A08:2025 | Software or Data Integrity Failures | BS-05, SEC-018, SEC-038, PLT-038, REL-006, SUP-007, SUP-013, SUP-015 |
| A09:2025 | Security Logging & Alerting Failures | SEC-021, OPS-014, OPS-019, OPS-020, OPS-023, AGT-011, SEC-091 |
| A10:2025 | Mishandling of Exceptional Conditions | BS-07, REL-002, REL-003, REL-049, QA-022, LIVE-007, SEC-085 |

## OWASP API Security Top 10 (2023)
| ID | Name | vibe-check checks |
|---|---|---|
| API1:2023 | Broken Object Level Authorization | SEC-015, SEC-075, LIVE-002 |
| API2:2023 | Broken Authentication | SEC-001, SEC-004, SEC-007, SEC-009, SEC-024 |
| API3:2023 | Broken Object Property Level Authorization | BS-05, SEC-018, SEC-055 |
| API4:2023 | Unrestricted Resource Consumption | SEC-053, SEC-074, SEC-077, REL-044, AIF-002, LIVE-006 |
| API5:2023 | Broken Function Level Authorization | SEC-014, SEC-016, SEC-075, LIVE-003 |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | HUNT-003, SEC-054, UX-025 |
| API7:2023 | Server Side Request Forgery | SEC-034, SEC-078 |
| API8:2023 | Security Misconfiguration | SEC-037, SEC-046, SEC-074, PLT-043 |
| API9:2023 | Improper Inventory Management | SEC-075, HUNT-004, REL-007, REL-008 |
| API10:2023 | Unsafe Consumption of APIs | REL-003, PLT-038, AIF-008, AGT-004 |

## OWASP Top 10 for LLM Applications (2025)
| ID | Name | vibe-check checks |
|---|---|---|
| LLM01:2025 | Prompt Injection | AIF-009, AGT-004 |
| LLM02:2025 | Sensitive Information Disclosure | AIF-011, AIF-012, AIF-016 |
| LLM03:2025 | Supply Chain | SUP-002, VUL-005, AGT-020 |
| LLM04:2025 | Data and Model Poisoning | AIF-022, Human: training and fine-tuning data provenance can't be checked from app code |
| LLM05:2025 | Improper Output Handling | AIF-008, AIF-013, AIF-014 |
| LLM06:2025 | Excessive Agency | AIF-010, AGT-001, AGT-002, AGT-003 |
| LLM07:2025 | System Prompt Leakage | AIF-012 |
| LLM08:2025 | Vector and Embedding Weaknesses | AIF-011, SEC-020 |
| LLM09:2025 | Misinformation | AIF-019, AIF-020 |
| LLM10:2025 | Unbounded Consumption | AIF-002, AIF-003, AIF-004, AGT-008 |

## OWASP Mobile Top 10 (2024)
| ID | Name | vibe-check checks |
|---|---|---|
| M1 | Improper Credential Usage | SEC-022, MOB-011 |
| M2 | Inadequate Supply Chain Security | SEC-048, SUP-002, VUL-010 |
| M3 | Insecure Authentication/Authorization | SEC-001, SEC-014, MOB-014 |
| M4 | Insufficient Input/Output Validation | SEC-027, MOB-015 |
| M5 | Insecure Communication | SEC-045, MOB-013 |
| M6 | Inadequate Privacy Controls | LEG-001, MOB-003, MOB-004, MOB-006 |
| M7 | Insufficient Binary Protections | MOB-016, Human: obfuscation and tamper resistance need a mobile binary review |
| M8 | Security Misconfiguration | MOB-014, MOB-015, MOB-016 |
| M9 | Insecure Data Storage | MOB-012, MOB-017 |
| M10 | Insufficient Cryptography | SEC-041, SEC-042, SEC-047 |

## OWASP ASVS 5.0.0 (by chapter)
| ID | Name | vibe-check checks |
|---|---|---|
| V1 | Encoding and Sanitization | SEC-028, SEC-029, SEC-030, SEC-031, SEC-038, SEC-065, SEC-066, SEC-068 |
| V2 | Validation and Business Logic | BS-04, BS-08, SEC-027, SEC-053, HUNT-002, HUNT-003, REL-048 |
| V3 | Web Frontend Security | SEC-003, SEC-035, SEC-036, SEC-046, SUP-015, SUP-017 |
| V4 | API and Web Service | SEC-037, SEC-074, SEC-075, SEC-076, REL-001 |
| V5 | File Handling | SEC-032, SEC-033, SEC-077, SEC-078, LIVE-008 |
| V6 | Authentication | SEC-001, SEC-005, SEC-006, SEC-007, SEC-008, SEC-010, SEC-071, SEC-073 |
| V7 | Session Management | SEC-002, SEC-003, SEC-009, QA-037 |
| V8 | Authorization | BS-01, SEC-014, SEC-015, SEC-016, SEC-017, SEC-020, SEC-075 |
| V9 | Self-contained Tokens | SEC-004, SEC-009 |
| V10 | OAuth and OIDC | SEC-011, SEC-013 |
| V11 | Cryptography | SEC-041, SEC-042, SEC-043, SEC-044, SEC-047, SEC-072 |
| V12 | Secure Communication | SEC-040, SEC-045, MOB-013 |
| V13 | Configuration | SEC-022, SEC-023, SEC-079, SEC-080, PLT-043, PLT-044, VUL-012, OPS-042 |
| V14 | Data Protection | SEC-055, SEC-057, SEC-058, SEC-063, SEC-064, LEG-012 |
| V15 | Secure Coding and Architecture | SEC-048, SEC-067, SEC-082, SUP-002, VUL-005, REL-032 |
| V16 | Security Logging and Error Handling | SEC-021, OPS-014, OPS-019, OPS-023, REL-002, QA-022 |
| V17 | WebRTC | SEC-076, Human: TURN, media and signaling security for WebRTC apps needs a specialist review |

## 2025 CWE Top 25
| ID | Name | vibe-check checks |
|---|---|---|
| CWE-79 | Cross-site Scripting | SEC-030 |
| CWE-89 | SQL Injection | SEC-028 |
| CWE-352 | Cross-Site Request Forgery (CSRF) | SEC-036 |
| CWE-862 | Missing Authorization | BS-01, SEC-014 |
| CWE-787 | Out-of-bounds Write | VUL-003, VUL-005, Human: memory-safety testing (fuzzing, sanitizers) of the app's own native code |
| CWE-22 | Path Traversal | SEC-033, SEC-077 |
| CWE-416 | Use After Free | VUL-003, VUL-005, Human: memory-safety testing (fuzzing, sanitizers) of the app's own native code |
| CWE-125 | Out-of-bounds Read | VUL-003, VUL-005, Human: memory-safety testing (fuzzing, sanitizers) of the app's own native code |
| CWE-78 | OS Command Injection | SEC-031 |
| CWE-94 | Code Injection | SEC-031, SEC-065 |
| CWE-120 | Classic Buffer Overflow | VUL-003, VUL-005, Human: memory-safety testing (fuzzing, sanitizers) of the app's own native code |
| CWE-434 | Unrestricted Upload of Dangerous File Type | SEC-032, LIVE-008 |
| CWE-476 | NULL Pointer Dereference | REL-002, VUL-005 |
| CWE-121 | Stack-based Buffer Overflow | VUL-003, VUL-005, Human: memory-safety testing (fuzzing, sanitizers) of the app's own native code |
| CWE-502 | Deserialization of Untrusted Data | SEC-038 |
| CWE-122 | Heap-based Buffer Overflow | VUL-003, VUL-005, Human: memory-safety testing (fuzzing, sanitizers) of the app's own native code |
| CWE-863 | Incorrect Authorization | SEC-016, SEC-075, SEC-084 |
| CWE-20 | Improper Input Validation | BS-04, SEC-027 |
| CWE-284 | Improper Access Control | SEC-014, SEC-019 |
| CWE-200 | Exposure of Sensitive Information | SEC-055, SEC-061, SEC-079 |
| CWE-306 | Missing Authentication for Critical Function | SEC-014, LIVE-004 |
| CWE-918 | Server-Side Request Forgery (SSRF) | SEC-034, SEC-078 |
| CWE-77 | Command Injection | SEC-031 |
| CWE-639 | Authorization Bypass Through User-Controlled Key | SEC-015 |
| CWE-770 | Allocation of Resources Without Limits or Throttling | SEC-053, REL-044, AIF-002 |
