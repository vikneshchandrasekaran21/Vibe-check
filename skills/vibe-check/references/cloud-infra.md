# Cloud infrastructure (AWS, Google Cloud, Azure, Kubernetes)

Load this file when the app runs on AWS, Google Cloud, Azure, DigitalOcean, Hetzner or similar, or uses Kubernetes, Terraform, Pulumi, CloudFormation or Docker Compose in production. Platform apps (Vercel, Netlify, Supabase, Firebase, Cloudflare) are covered in `platforms.md`. Read the IaC files and deployment configs. If the user has the cloud CLI logged in, run **read-only** commands only (`aws s3api get-bucket-policy-status`, `gcloud … describe`, `az … show`), never anything that changes resources.

## Storage
- [ ] 🔴 **No public buckets with private data:** S3 Block Public Access on (account and bucket), GCS uniform access without `allUsers`/`allAuthenticatedUsers`, Azure containers not set to public access. Public assets live in a separate, clearly public bucket.
- [ ] 🔴 **Cloud storage and disks encrypted** (buckets, databases, disks and snapshots) (default encryption on, customer-managed keys for sensitive data if required).
- [ ] 🟡 **Versioning and lifecycle rules** on important buckets, so deleted or overwritten files can be recovered and old data expires on schedule.
- [ ] 🟡 **Signed URLs** with short expiry for private files, never long-lived public links.

## Identity and access (IAM)
- [ ] 🔴 **No wildcard permissions** for app roles (`"Action": "*"`, `"Resource": "*"`, Owner/Editor roles for service accounts).
- [ ] 🔴 **No long-lived access keys in code or CI:** use instance roles, workload identity or OIDC for CI. Old keys are rotated or deleted.
- [ ] 🔴 **Root/owner account locked down:** MFA on, no access keys, used only for break-glass. Billing alerts set.
- [ ] 🟡 **Separate accounts or projects** for production and non-production.
- [ ] 🟡 **Cloud audit logs on** (CloudTrail, Cloud Audit Logs, Azure Activity Log) and kept for at least 90 days.

## Network
- [ ] 🔴 **Databases, caches and admin ports aren't open to the internet:** no `0.0.0.0/0` on 5432, 3306, 27017, 6379, 9200, 22 or RDP. Databases are in private subnets.
- [ ] 🔴 **TLS on every public endpoint** (load balancers, API gateways, CDNs), with HTTP redirected and old TLS versions disabled.
- [ ] 🟡 **SSH access** by key only (or through a bastion or session manager), no password login, no root login.
- [ ] 🟡 **WAF or rate limiting** at the edge for public APIs and login.

## Kubernetes and containers
- [ ] 🔴 **Secrets aren't in images or plain manifests:** use Kubernetes Secrets with encryption at rest, or an external secret manager. `docker history` shows no secrets.
- [ ] 🔴 **Containers don't run as root or privileged** unless required (`runAsNonRoot`, no `privileged: true`, read-only root filesystem where possible).
- [ ] 🟡 **Resource requests and limits** set, so one service can't starve others.
- [ ] 🟡 **Images from trusted registries,** pinned by digest or version (not `latest`), and scanned for vulnerabilities.
- [ ] 🟡 **The Kubernetes API and dashboards aren't public,** and RBAC follows least privilege.

## Infrastructure as Code
- [ ] 🟡 **IaC scanned** for misconfigurations (e.g. `tfsec`, `checkov`, `trivy config`), and state files (Terraform state) stored privately and encrypted, since they contain secrets.
- [ ] 🟡 **Changes go through review and CI,** not manual console edits (drift is detected).
- [ ] 🟡 **Backups and snapshots are automatic** for databases and volumes, and a restore has been tested (see `devops.md`).
- [ ] 🟢 **Cost controls:** budgets and alerts, auto-scaling limits, and no forgotten resources (unused instances, load balancers, IPs, snapshots).
