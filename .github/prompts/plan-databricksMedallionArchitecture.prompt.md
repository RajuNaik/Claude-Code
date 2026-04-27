# Plan: Create Databricks Medallion Architecture Skill

**Add a reusable medallion architecture skill to Claude-Code (`03-skills/databricks-medallion-architecture/`) teaching data engineers design patterns for Databricks medallion architecture. Focuses on architecture theory and governance (not heavy PySpark). Integrates with existing skill system and passes all 4 pre-commit quality gates.**

---

## Steps

### Phase 1: Skill Structure Setup *(foundation)*
1. Create folder `03-skills/databricks-medallion-architecture/`
2. Create SKILL.md with YAML frontmatter (name, description, version)
3. Create subdirectories: `templates/`, `references/`
4. Verify no naming conflicts with existing skills

### Phase 2: SKILL.md Content *(depends on Phase 1)*
1. Add **Overview** section (what medallion is, why Databricks)
2. Add **When to Use This Skill** section (trigger conditions)
3. Add **Core Concepts** section with 3-4 Mermaid diagrams:
   - Bronze/silver/gold layer architecture
   - Data flow and transformation patterns
   - Decision trees (when to transform in bronze vs. silver)
4. Add **Design Patterns** workflow (5-7 use cases):
   - Real-time + batch ingestion
   - Data quality & validation
   - Multi-tenant isolation
   - Cost optimization (retention, Z-order, compaction)
   - Incremental processing
5. Add **Governance & Security** section (RBAC, lineage, compliance)
6. Add **Version History** section (v1.0.0, current date)

### Phase 3: Template Files *(parallel with Phase 2; depends on Phase 1)*
1. Create `templates/medallion-structure.yaml` — folder hierarchy, naming, partitioning strategy
2. Create `templates/bronze-layer-pattern.md` — ingestion pattern with metadata
3. Create `templates/silver-layer-pattern.md` — transformation rules and schema evolution
4. Create `templates/data-governance.json` — access control schema, lineage tags

### Phase 4: Reference Documentation *(parallel with Phases 2-3)*
1. Create `references/performance-tuning.md` — Z-order, partitioning, compaction, caching
2. Create `references/cost-optimization.md` — retention policies, storage tiers, compute optimization
3. Create `references/common-patterns.md` — real-world medallion examples (IoT, financial, etc.)

### Phase 5: Quality Validation & Pre-Commit *(depends on Phases 2-4)*
1. Run `markdownlint` on SKILL.md — fix formatting issues
2. Validate all Mermaid diagrams parse (run `mmdc` or preview in VS Code)
3. Verify cross-references (relative paths, code fence language tags)
4. Test external Databricks docs URLs are reachable
5. Run `pre-commit run --all-files` locally — all 4 checks must pass
6. Test EPUB build: `uv run scripts/build_epub.py` — diagrams must render

### Phase 6: Integration & Documentation *(depends on Phase 5)*
1. Update `03-skills/README.md` to list new skill
2. Add brief cross-reference from main README if appropriate
3. Verify skill appears in Copilot skill selector

---

## Relevant Files & Patterns

- **03-skills/blog-draft/SKILL.md** — YAML frontmatter and workflow structure reference
- **03-skills/code-review/SKILL.md** — Multi-section workflow design pattern
- **CLAUDE.md** — Pre-commit quality gate requirements (markdown-lint, cross-references, mermaid-syntax, link-check)
- **.pre-commit-config.yaml** — Defines validation rules

---

## Verification

1. ✅ SKILL.md frontmatter valid (name, description, version present)
2. ✅ Pre-commit passes locally: `pre-commit run --all-files` (all 4 checks)
3. ✅ Mermaid diagrams render in VS Code Markdown preview
4. ✅ Cross-references work (internal links valid, code fences have language tags)
5. ✅ EPUB builds: `uv run scripts/build_epub.py` completes without errors
6. ✅ Directory structure matches existing skill folders (`templates/`, `references/`)
7. ✅ 03-skills/README.md updated with new skill listing

---

## Decisions & Scope

- **In scope**: Medallion architecture patterns, bronze/silver/gold layers, data governance, design decision tables, Mermaid diagrams, YAML/JSON config templates
- **Out of scope**: Heavy PySpark code examples, cluster management, DevOps/CI-CD, BI/dashboard layer design
- **Audience**: Data engineers (not DBAs or BI analysts)
- **Design approach**: Patterns + governance focus (link to Databricks docs for implementation details)
- **Versioning**: v1.0.0 = core medallion + 3-4 design patterns; defer advanced patterns (feature stores, streaming optimization) to v2.0

---

## Further Considerations

1. **External URL Validation** — Databricks doc links must use permalinks and be reachable for link-check to pass. *Recommendation: Use official `docs.databricks.com` URLs and test before finalizing.*

2. **Mermaid Diagram Scope** — Medallion requires complex flowcharts. *Recommendation: Create 3-4 focused diagrams (one per aspect) rather than one mega-diagram for readability.*

3. **PySpark Code Depth** — Keeping out heavy implementation is intentional per scope. *Recommendation: Reference docs in templates, focus skill on "when/why" not "how to code".*
