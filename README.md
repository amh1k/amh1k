<p align="center">
  <img src="./assets/hero.svg" width="100%" alt="Abdul Moiz Hussain" />
</p>

<p align="center">
  <a href="https://abdulmoizhussain.me"><img src="./assets/social-portfolio.svg" width="18.5%" alt="PORTFOLIO" /></a>
  <a href="https://www.linkedin.com/in/abdulmoizhussain"><img src="./assets/social-linkedin.svg" width="18.5%" alt="LINKEDIN" /></a>
  <a href="mailto:abdulmoizx97@gmail.com"><img src="./assets/social-email.svg" width="18.5%" alt="EMAIL" /></a>
  <a href="https://leetcode.com/u/abdulmoizx97/"><img src="./assets/social-leetcode.svg" width="18.5%" alt="LEETCODE" /></a>
  <a href="https://codeforces.com/profile/amh1k"><img src="./assets/social-codeforces.svg" width="18.5%" alt="CODEFORCES" /></a>
</p>

<p align="center">
  <img src="./assets/stats.svg" width="100%" alt="GitHub statistics and contribution activity" />
</p>

## Featured Projects

| Project | Stack | Description |
| --- | --- | --- |
| **[Mithril Tiles](https://github.com/amh1k/mithril-tiles)** | Go · WebSockets · PostgreSQL · React · TypeScript | Server-authoritative real-time drawing game with concurrent room event loops, reconnect-safe canvas state, authentication, scoring, timers, and automated tests. |
| **[Keepalive Monitoring](https://github.com/amh1k/keepalive-monitoring)** | Node.js · TypeScript · PostgreSQL · Redis · BullMQ · React | Uptime and incident-monitoring platform with background workers, failure thresholds, latency tracking, SSL checks, alerts, and production deployment behind Nginx. |
| **[Durin's Code](https://github.com/amh1k/DurinsCode)** | C++17 · WebAssembly · TypeScript | DSL compiler and virtual machine for interactive text adventures: lexer, recursive-descent parser, semantic analysis, TAC optimization, bytecode generation, and browser IDE. |

## Open Source Contributions

I contribute primarily to **developer tooling, Go/backend systems, Kubernetes, and cloud-native infrastructure**.  
The table below highlights the upstream work I would want a reviewer to see first.

> **Status snapshot:** 11 August 2026. PR states can change after this date.

| Project | Pull Request | Status | Description |
| --- | --- | --- | --- |
| **Alibaba OpenCodeReview** | [feat(viewer): add review comment tag filters (#779)](https://github.com/alibaba/open-code-review/pull/779) | **Merged** | Added tag-based filtering to the review viewer so users can navigate large sets of review comments more efficiently. |
| **Alibaba OpenCodeReview** | [refactor(cli): use Cobra validation for parent commands (#694)](https://github.com/alibaba/open-code-review/pull/694) | **Merged** | Moved parent-command validation into Cobra, improving CLI argument handling and reducing custom validation logic. |
| **Alibaba OpenCodeReview** | [feat(llm): add GPT-5.6 models to OpenAI provider (#666)](https://github.com/alibaba/open-code-review/pull/666) | **Merged** | Added GPT-5.6 model support to the built-in OpenAI provider configuration. |
| **Alibaba OpenCodeReview** | [feat(viewer): add repository search filter (#642)](https://github.com/alibaba/open-code-review/pull/642) | **Merged** | Added repository filtering/search to the review viewer for easier navigation across saved review sessions. |
| **Alibaba OpenCodeReview** | [refactor(diff): strip index headers from review prompts (#609)](https://github.com/alibaba/open-code-review/pull/609) | **Merged** | Removed Git index-header noise from generated review prompts so model context stays focused on meaningful diff content. |
| **Alibaba OpenCodeReview** | [fix(config): warn when active provider shadows llm settings (#588)](https://github.com/alibaba/open-code-review/pull/588) | **Merged** | Added configuration diagnostics for cases where an active provider silently takes precedence over direct LLM settings. |
| **Alibaba OpenCodeReview** | [feat(allowlist): add Prisma schema review support (#572)](https://github.com/alibaba/open-code-review/pull/572) | **Merged** | Extended review-file support to Prisma schema files. |
| **Alibaba OpenCodeReview** | [feat(rules): add comprehensive built-in Go review guidance (#569)](https://github.com/alibaba/open-code-review/pull/569) | **Merged** | Added built-in Go-specific review guidance to improve language-aware code-review quality. |
| **Alibaba OpenCodeReview** | [ci(test): add binary smoke test (#566)](https://github.com/alibaba/open-code-review/pull/566) | **Merged** | Added a CI smoke test that verifies the built CLI binary actually starts and exposes expected commands. |
| **Alibaba OpenCodeReview** | [fix(pages): handle stale lazy-loaded chunks gracefully (#542)](https://github.com/alibaba/open-code-review/pull/542) | **Merged** | Improved the web UI's behavior when a deployment leaves users with stale lazy-loaded frontend chunks. |
| **Alibaba OpenCodeReview** | [fix(delegate): guard JSON workflow against old CLI versions (#802)](https://github.com/alibaba/open-code-review/pull/802) | **Open** | Adds compatibility protection when delegation workflows are used with older OCR CLI versions. |
| **Alibaba OpenCodeReview** | [feat(pages): serve install scripts from custom domain (#797)](https://github.com/alibaba/open-code-review/pull/797) | **Open** | Adds first-party install-script delivery through the project's custom domain. |
| **Alibaba OpenCodeReview** | [fix(review): filter near-duplicate comments in review output (#776)](https://github.com/alibaba/open-code-review/pull/776) | **Open** | Reduces repetitive review output by filtering near-duplicate comments. |
| **OpenEverest · CNCF Sandbox** | [Support spaced repository paths on release-2.0 (#2812)](https://github.com/openeverest/openeverest/pull/2812) | **Open** | Ports repository-path handling so the release branch works correctly when the local checkout path contains spaces. |
| **OpenEverest · CNCF Sandbox** | [Fix dev-up with spaced repository paths (#2790)](https://github.com/openeverest/openeverest/pull/2790) | **Open** | Fixes local development startup when the OpenEverest repository is located inside a path containing spaces. |
| **OpenEverest Docs · CNCF Sandbox** | [Fix PITR link on restore backup page (#372)](https://github.com/openeverest/everest-doc/pull/372) | **Merged** | Corrected the point-in-time-recovery link in the restore documentation. |
| **OpenEverest Docs · CNCF Sandbox** | [Fix database view backup links (#371)](https://github.com/openeverest/everest-doc/pull/371) | **Merged** | Fixed broken backup-navigation links in the database-view documentation. |
| **OpenEverest Docs · CNCF Sandbox** | [Fix Mermaid diagram rendering and dark-mode contrast (#369)](https://github.com/openeverest/everest-doc/pull/369) | **Merged** | Fixed Mermaid rendering issues and improved documentation readability in dark mode. |
| **KubeStellar Console · CNCF Sandbox** | [Refactor: split resources drill-down (#21992)](https://github.com/kubestellar/console/pull/21992) | **Merged** | Split a large resources drill-down component into smaller focused pieces, reducing component complexity and improving maintainability. |
| **KubeStellar Console · CNCF Sandbox** | [Refactor: split widget export modal content (#21893)](https://github.com/kubestellar/console/pull/21893) | **Merged** | Refactored an oversized export-modal implementation into smaller, easier-to-maintain components. |
| **Apache Magpie** | [Fix/skill evals quote helper paths (#992)](https://github.com/apache/magpie/pull/992) | **Merged** | Hardened skill-evaluation scripts by correctly quoting helper paths. |
| **Apache Magpie** | [Narrow sourcehut exception handlers (#988)](https://github.com/apache/magpie/pull/988) | **Merged** | Narrowed exception handling around SourceHut integration so unrelated failures are not accidentally swallowed. |
| **Kubeflow SDK · CNCF** | [fix(spark): add default service account fallback for Spark Connect (#672)](https://github.com/kubeflow/sdk/pull/672) | **Open** | Adds a default Kubernetes service-account fallback for Spark Connect when no explicit account is configured. |

### Contribution Index

- **[Alibaba OpenCodeReview — all authored PRs](https://github.com/alibaba/open-code-review/pulls?q=is%3Apr+author%3Aamh1k)** — primary upstream focus; Go, CLI, AI code review, configuration, CI, diff processing, and viewer work.
- **[OpenEverest — authored PRs](https://github.com/openeverest/openeverest/pulls?q=is%3Apr+author%3Aamh1k)** — Kubernetes-native database platform and development tooling.
- **[OpenEverest Docs — authored PRs](https://github.com/openeverest/everest-doc/pulls?q=is%3Apr+author%3Aamh1k)** — product documentation fixes and usability improvements.
- **[KubeStellar Console — authored PRs](https://github.com/kubestellar/console/pulls?q=is%3Apr+author%3Aamh1k)** — Kubernetes multi-cluster console maintainability/refactoring.
- **[Apache Magpie — authored PRs](https://github.com/apache/magpie/pulls?q=is%3Apr+author%3Aamh1k)** — developer tooling and integration hardening.
- **[Kubeflow SDK — authored PRs](https://github.com/kubeflow/sdk/pulls?q=is%3Apr+author%3Aamh1k)** — Kubernetes/Spark SDK behavior.

---

<p align="center">
  <sub>Backend engineering · Go · Kubernetes · Distributed systems · Open source</sub>
</p>
