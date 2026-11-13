# Cloud infrastructure (AWS, Google Cloud, Azure, Kubernetes)

Load this file when the app runs on AWS, Google Cloud, Azure, DigitalOcean, Hetzner or similar, or uses Kubernetes, Terraform, Pulumi, CloudFormation or Docker Compose in production. Platform apps (Vercel, Netlify, Supabase, Firebase, Cloudflare) are covered in `platforms.md`. Read the IaC files and deployment configs. If the user has the cloud CLI logged in, run **read-only** commands only (`aws s3api get-bucket-policy-status`, `gcloud … describe`, `az … show`), never anything that changes resources.

## Storage
- [ ] 🔴 CLD-001 **No public buckets with private data:** S3 Block Public Access on (account and bucket), GCS uniform access without `allUsers`/`allAuthenticatedUsers`, Azure containers not set to public access. Public assets live in a separate, clearly public bucket.
- [ ] 🔴 CLD-002 **Cloud storage and disks encrypted** (buckets, databases, disks and snapshots) (default encryption on, customer-managed keys for sensitive data if required).
- [ ] 🟡 CLD-003 **Versioning and lifecycle rules** on important buckets, so deleted or overwritten files can be recovered and old data expires on schedule.
- [ ] 🟡 CLD-004 **Signed URLs** with short expiry for private files, never long-lived public links.

## Identity and access (IAM)
- [ ] 🔴 CLD-005 **No wildcard permissions** for app roles (`"Action": "*"`, `"Resource": "*"`, Owner/Editor roles for service accounts).
- [ ] 🔴 CLD-006 **No long-lived access keys in code or CI:** use instance roles, workload identity or OIDC for CI. Old keys are rotated or deleted.
- [ ] 🔴 CLD-007 **Root/owner account locked down:** MFA on, no access keys, used only for break-glass. Billing alerts set.
- [ ] 🟡 CLD-008 **Separate accounts or projects** for production and non-production.
- [ ] 🟡 CLD-009 **Cloud audit logs on** (CloudTrail, Cloud Audit Logs, Azure Activity Log) and kept for at least 90 days.

## Network
- [ ] 🔴 CLD-010 **Databases, caches and admin ports aren't open to the internet:** no `0.0.0.0/0` on 5432, 3306, 27017, 6379, 9200, 22 or RDP. Databases are in private subnets.
- [ ] 🔴 CLD-011 **TLS on every public endpoint** (load balancers, API gateways, CDNs), with HTTP redirected and old TLS versions disabled.
- [ ] 🟡 CLD-012 **SSH access** by key only (or through a bastion or session manager), no password login, no root login.
- [ ] 🟡 CLD-013 **WAF or rate limiting** at the edge for public APIs and login.

## Kubernetes and containers
- [ ] 🔴 CLD-014 **Secrets aren't in images or plain manifests:** use Kubernetes Secrets with encryption at rest, or an external secret manager. `docker history` shows no secrets.
- [ ] 🔴 CLD-015 **Containers don't run as root or privileged** unless required (`runAsNonRoot`, no `privileged: true`, read-only root filesystem where possible).
- [ ] 🟡 CLD-016 **Resource requests and limits** set, so one service can't starve others.
- [ ] 🟡 CLD-017 **Images from trusted registries,** pinned by digest or version (not `latest`), and scanned for vulnerabilities.
- [ ] 🟡 CLD-018 **The Kubernetes API and dashboards aren't public,** and RBAC follows least privilege.

## Infrastructure as Code
- [ ] 🟡 CLD-019 **IaC scanned** for misconfigurations (e.g. `tfsec`, `checkov`, `trivy config`), and state files (Terraform state) stored privately and encrypted, since they contain secrets.
- [ ] 🟡 CLD-020 **Changes go through review and CI,** not manual console edits (drift is detected).
- [ ] 🟡 CLD-021 **Backups and snapshots are automatic** for databases and volumes, and a restore has been tested (see `devops.md`).
- [ ] 🟢 CLD-022 **Cost controls:** budgets and alerts, auto-scaling limits, and no forgotten resources (unused instances, load balancers, IPs, snapshots).
