# AI Widget Agent — Implementation Plan

Use this plan as a stepwise implementation roadmap for adding an AI-driven widget building capability to the platform without sacrificing RBAC, maintainability, or layout consistency.

---

## Phase 0 — Foundation Rules

### Objective
Establish the rules that constrain the agent.

### Deliverables
- Widget manifest schema is the source of truth.
- Approved widget primitives are registered.
- Approved permission keys are discoverable.
- Approved endpoint/data bindings are discoverable.
- Validation service blocks invalid manifests.

### Acceptance Criteria
- No widget can be published without manifest validation.
- No widget can reference unknown component types.
- No widget can reference unknown permission keys.

---

## Phase 1 — Manifest + Persistence

### Objective
Create the backend structures that persist widget definitions, instances, and layouts.

### Tasks
1. Add SQLAlchemy models for:
   - widget_definitions
   - widget_permissions
   - widget_instances
   - dashboard_layouts
   - widget_agent_runs
2. Add Alembic migration.
3. Add Pydantic schemas matching `backend/widget_manifest.py`.
4. Add repository/service layer.

### Acceptance Criteria
- Widget definitions can be created and retrieved.
- Widget instances can be attached to dashboard layouts.
- JSON manifests round-trip without schema drift.

---

## Phase 2 — Frontend Widget Registry

### Objective
Build the dynamic rendering layer.

### Tasks
1. Implement a `widgetRegistry` map.
2. Add baseline primitives:
   - KPIGrid
   - StatusCards
   - EntityTable
   - AlertList
   - ActionPanel
3. Add a generic manifest renderer.
4. Add empty/error/loading/unauthorized states.
5. Add a dashboard grid shell for placement.

### Acceptance Criteria
- A valid manifest renders the correct primitive.
- Invalid component type fails fast in development.
- Required states render consistently.

---

## Phase 3 — Validation Services

### Objective
Ensure manifests are safe and deployable.

### Tasks
1. Add schema validation.
2. Add RBAC validation.
3. Add endpoint/data-binding validation.
4. Add layout constraint validation.
5. Add audit-style validation response.

### Acceptance Criteria
- Validator returns structured errors.
- Validator blocks unknown permissions and endpoints.
- Validator enforces layout size rules.

---

## Phase 4 — Agent Draft Endpoint

### Objective
Allow the AI layer to generate widget drafts.

### Tasks
1. Create `/api/v1/widget-agent/draft` endpoint.
2. Input includes:
   - prompt
   - business/location context
   - role/permission context
   - optional dashboard context
3. Agent pipeline:
   - normalize intent
   - select domain pack
   - select primitive/template
   - produce draft manifest
   - validate draft
   - return manifest + warnings + missing dependencies

### Acceptance Criteria
- Endpoint returns a valid `WidgetDraftResponse`.
- Invalid drafts are rejected or repaired before response.
- Warnings explain missing backend dependencies clearly.

---

## Phase 5 — Preview + Refine Flow

### Objective
Create a user-facing flow to preview and revise drafts.

### Tasks
1. Add builder modal or workspace.
2. Prompt input + draft generation.
3. Live preview panel.
4. Edit controls for:
   - title
   - size
   - filters
   - actions
   - visibility
5. Re-run validation after edits.

### Acceptance Criteria
- User can revise a draft without hand-editing raw JSON.
- Preview remains in sync with the manifest.
- Validation errors are visible in the UI.

---

## Phase 6 — Publish + Install Workflow

### Objective
Let an approved draft become a reusable widget and dashboard instance.

### Tasks
1. Publish validated draft as widget definition version.
2. Install widget into dashboard layout.
3. Save widget instance config and placement.
4. Record audit/provenance metadata.

### Acceptance Criteria
- Published widgets are reusable.
- Dashboard installation creates a widget instance.
- Revision history is preserved.

---

## Phase 7 — Domain Packs

### Objective
Ground the agent in operational domains.

### Suggested Order
1. Housekeeping
2. Front Desk
3. Maintenance
4. Scheduling
5. Inventory
6. Labor / Payroll

### Deliverables Per Pack
- common entities
- default filters
- common actions
- permission mappings
- starter templates
- sample prompts

### Acceptance Criteria
- Agent quality improves measurably within each domain.
- Template selection becomes more deterministic.

---

## Phase 8 — Reviewed Backend Stub Generation

### Objective
Allow the agent to propose missing backend bindings safely.

### Rules
- Never auto-publish generated backend code to production.
- Generated endpoint stubs require review.
- Generated schemas must align with existing repository patterns.

### Acceptance Criteria
- Missing dependencies are surfaced as explicit stubs.
- Developers can approve and implement from generated scaffolds.

---

## Non-Goals for MVP

Do not start with:
- unrestricted arbitrary component generation
- unrestricted SQL generation in production
- auto-installing widgets with write actions and no approval
- bypassing permission validation for previews

---

## Definition of Done

The feature is done when a user can:
1. describe a widget in natural language,
2. get a valid draft manifest,
3. preview and refine it,
4. publish it into the registry,
5. install it onto a dashboard,
6. enforce permissions and lifecycle states automatically.
