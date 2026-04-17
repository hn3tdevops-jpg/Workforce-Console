# WORKFORCE WEB UI — COPILOT IMPLEMENTATION FILE

Use this file as the implementation brief for GitHub Copilot / coding agent.

## Goal

Convert the existing Next.js app at:

```text
apps/web/hospitable-web
```

into the main **Workforce Web UI** with:

- a **Superadmin console**
- a **Tenant Admin console**
- **permission-driven navigation**
- a **shared app shell**
- **module workspaces** for:
  - Dashboard
  - Workforce Core
  - Hospitable Ops
  - Scheduling
  - Timeclock
  - Users / Roles / Permissions
  - System configuration

Do **not** create a brand-new frontend from scratch. Extend and refactor the existing app.

---

# 1. EXISTING REPO CONTEXT

Backend already exists under:

```text
apps/api/app
```

Existing FastAPI app entry:

```text
apps/api/app/main.py
```

Existing API router:

```text
apps/api/app/api/router.py
```

Existing Hospitable module:

```text
apps/api/app/modules/hospitable
```

Existing Next.js frontend foundation:

```text
apps/web/hospitable-web
```

Important existing files:

```text
apps/web/hospitable-web/app/layout.tsx
apps/web/hospitable-web/app/page.tsx
apps/web/hospitable-web/components/Sidebar.tsx
apps/web/hospitable-web/components/Topbar.tsx
apps/web/hospitable-web/components/BusinessSelector.tsx
apps/web/hospitable-web/lib/api.ts
```

The current web app is a **Hospitable Ops UI**. We now need to evolve it into the broader **Workforce Admin Console** while keeping Hospitable as one workspace/module.

---

# 2. ARCHITECTURE PRINCIPLES

## 2.1 App strategy

Use a single web application with route groups for role-specific workspaces.

Target high-level IA:

```text
/
  dashboard
/superadmin
  overview
  businesses
  locations
  users
  roles
  permissions
  feature-flags
  audit-log
  integrations
  api-keys
  jobs
/admin
  overview
  business-settings
  locations
  teams
  members
  roles
  dashboards
/workforce
  overview
  scheduling
  shifts
  assignments
  timeclock
/hospitable
  dashboard
  rooms
  housekeeping
  maintenance
  inventory
  property-setup
/system
  profile
  preferences
  notifications
  access
```

## 2.2 Navigation strategy

Navigation must be **permission-driven**, not hardcoded only by route.

A user should only see modules and pages they are allowed to access.

## 2.3 Keep current web stack

Continue using:

- Next.js App Router
- TypeScript
- the existing component structure
- the existing API proxy pattern

Do not introduce a different frontend framework.

## 2.4 Progressive hardening

Implement in layers:

1. App shell and route structure
2. API client and typed DTOs
3. Superadmin pages
4. Tenant admin pages
5. Permission-driven menu
6. Shared tables/forms/filters
7. Auth/session wiring
8. Polish and testing

---

# 3. TARGET DIRECTORY STRUCTURE

Refactor `apps/web/hospitable-web` toward this structure:

```text
apps/web/hospitable-web/
  app/
    (console)/
      layout.tsx
      page.tsx
    superadmin/
      page.tsx
      businesses/page.tsx
      locations/page.tsx
      users/page.tsx
      roles/page.tsx
      permissions/page.tsx
      feature-flags/page.tsx
      audit-log/page.tsx
      integrations/page.tsx
      api-keys/page.tsx
    admin/
      page.tsx
      business-settings/page.tsx
      locations/page.tsx
      members/page.tsx
      roles/page.tsx
      dashboards/page.tsx
    workforce/
      page.tsx
      scheduling/page.tsx
      shifts/page.tsx
      assignments/page.tsx
      timeclock/page.tsx
    hospitable/
      page.tsx
      rooms/page.tsx
      housekeeping/page.tsx
      maintenance/page.tsx
      inventory/page.tsx
      property-setup/page.tsx
    system/
      profile/page.tsx
      preferences/page.tsx
      access/page.tsx
    api/
      v1/
        control/
        tenant/
        workforce/
        hospitable/
  components/
    shell/
      AppShell.tsx
      Sidebar.tsx
      Topbar.tsx
      WorkspaceHeader.tsx
      Breadcrumbs.tsx
    nav/
      nav-config.ts
      PermissionNav.tsx
      WorkspaceSwitcher.tsx
    data-display/
      StatCard.tsx
      DataTable.tsx
      EmptyState.tsx
      StatusBadge.tsx
      FilterBar.tsx
    superadmin/
      BusinessTable.tsx
      UserTable.tsx
      RoleTable.tsx
      FeatureFlagTable.tsx
      AuditLogTable.tsx
    admin/
      LocationTable.tsx
      MemberTable.tsx
    forms/
      BusinessForm.tsx
      LocationForm.tsx
      RoleForm.tsx
      UserForm.tsx
  lib/
    api.ts
    auth.ts
    permissions.ts
    nav.ts
    utils.ts
    constants.ts
    types/
      common.ts
      auth.ts
      superadmin.ts
      admin.ts
      workforce.ts
      hospitable.ts
  hooks/
    useCurrentUser.ts
    useCurrentBusiness.ts
    useCurrentLocation.ts
    usePermissions.ts
    useWorkspace.ts
  styles/
    tokens.css
    theme.css
```

Use this structure as the direction even if some files are introduced incrementally.

---

# 4. WORKSPACES

## 4.1 Superadmin workspace

Purpose: platform-wide control plane.

Pages to build first:

```text
/superadmin
/superadmin/businesses
/superadmin/locations
/superadmin/users
/superadmin/roles
/superadmin/permissions
/superadmin/feature-flags
/superadmin/audit-log
```

Core widgets:

- platform totals
- total businesses
- total locations
- total users
- active modules by tenant
- recent platform events
- pending setup/integration items

Table actions:

- create business
- edit business
- activate/deactivate business
- create location
- create user
- assign roles
- inspect feature flags
- inspect audit log

## 4.2 Tenant admin workspace

Purpose: business-scoped administration.

Pages:

```text
/admin
/admin/business-settings
/admin/locations
/admin/members
/admin/roles
/admin/dashboards
```

Core widgets:

- business profile summary
- active locations
- member count
- permission template count
- enabled modules
- current operational alerts

## 4.3 Workforce workspace

Purpose: labor and scheduling operations.

Pages:

```text
/workforce
/workforce/scheduling
/workforce/shifts
/workforce/assignments
/workforce/timeclock
```

Initial implementation can be placeholder pages if backend coverage is incomplete, but route and navigation must exist.

## 4.4 Hospitable workspace

Move current root-level pages into `/hospitable/*` and treat them as one workspace.

Pages:

```text
/hospitable
/hospitable/rooms
/hospitable/housekeeping
/hospitable/maintenance
/hospitable/inventory
/hospitable/property-setup
```

Current existing functionality should be preserved, not removed.

---

# 5. ROUTING REFACTOR

## 5.1 Current issue

Current app uses the root pages as Hospitable pages:

- `/`
- `/rooms`
- `/housekeeping`
- `/maintenance`
- `/inventory`
- `/property-setup`
- `/settings`

This makes the app feel like a single-purpose property app.

## 5.2 Refactor target

Make `/` a general Workforce landing/dashboard and move Hospitable pages under `/hospitable`.

### Required route behavior

- `/` = overall Workforce dashboard
- `/superadmin` = platform console
- `/admin` = tenant admin
- `/workforce` = core workforce operations
- `/hospitable` = property operations dashboard

### Migration rule

Retain backward compatibility temporarily by redirecting old routes:

- `/rooms` -> `/hospitable/rooms`
- `/housekeeping` -> `/hospitable/housekeeping`
- `/maintenance` -> `/hospitable/maintenance`
- `/inventory` -> `/hospitable/inventory`
- `/property-setup` -> `/hospitable/property-setup`
- `/settings` -> `/system/preferences` or `/admin/business-settings` depending on context

Implement redirects in a clean, explicit way.

---

# 6. APP SHELL

Replace the current Hospitable-only shell with a generic Workforce shell.

## 6.1 Create `AppShell`

Create:

```text
components/shell/AppShell.tsx
```

Responsibilities:

- shared page framing
- sidebar
- topbar
- content area
- mobile overlay handling
- business/location context display
- workspace switcher

## 6.2 Sidebar requirements

Refactor existing `components/Sidebar.tsx` into a generic shell sidebar.

Must support:

- grouped navigation sections
- workspace-aware links
- permission filtering
- collapsible behavior
- mobile open/close state
- active-route highlighting
- business selector
- location selector

## 6.3 Topbar requirements

Topbar should include:

- menu toggle
- workspace title
- business selector
- location selector
- quick actions
- alerts/notifications stub
- user menu

## 6.4 Workspace switcher

Provide quick switching between:

- Superadmin
- Admin
- Workforce
- Hospitable

This can be a dropdown in the topbar.

---

# 7. NAVIGATION MODEL

Create a typed navigation registry.

## 7.1 File

```text
components/nav/nav-config.ts
```

## 7.2 Type shape

Create a type like:

```ts
export type NavItem = {
  key: string
  label: string
  href: string
  icon?: string
  workspace: 'global' | 'superadmin' | 'admin' | 'workforce' | 'hospitable' | 'system'
  requiredPermissions?: string[]
  children?: NavItem[]
}
```

## 7.3 Requirements

- define all menu items in one place
- filter them by current user permissions
- support section grouping
- support hidden items if no access

---

# 8. PERMISSIONS SYSTEM IN UI

Create frontend permission helpers even if backend auth is still evolving.

## 8.1 Add files

```text
lib/permissions.ts
hooks/usePermissions.ts
lib/types/auth.ts
```

## 8.2 Frontend permission model

Use string permission keys, for example:

```text
platform.business.read
platform.business.write
platform.user.read
platform.user.write
platform.role.read
platform.role.write
platform.audit.read
tenant.location.read
tenant.location.write
tenant.member.read
tenant.member.write
tenant.role.read
tenant.role.write
workforce.schedule.read
workforce.schedule.write
workforce.shift.read
workforce.shift.write
hospitable.room.read
hospitable.room.write
hospitable.task.read
hospitable.task.write
hospitable.maintenance.read
hospitable.maintenance.write
```

## 8.3 Implement helpers

Functions to provide:

```ts
hasPermission(user, perm)
hasAnyPermission(user, perms)
hasAllPermissions(user, perms)
filterNavItemsByPermission(items, user)
```

## 8.4 UI gating

Use permission gating for:

- menu entries
- buttons
- create/edit actions
- page access
- empty access-denied states

---

# 9. CURRENT USER / SESSION CONTEXT

Create a lightweight current-user model in the frontend.

## 9.1 Add types

```ts
export interface CurrentUser {
  id: string
  email: string
  full_name: string
  is_superadmin: boolean
  business_id?: string | null
  location_ids?: string[]
  permissions: string[]
  active_business_id?: string | null
  active_location_id?: string | null
}
```

## 9.2 Add hook

```text
hooks/useCurrentUser.ts
```

Initially this can use a mock API or bootstrap endpoint if a formal auth session endpoint does not exist yet.

## 9.3 Add bootstrap endpoint if missing

If necessary, add a backend endpoint such as:

```text
GET /api/v1/bootstrap/session
```

Return:

- current user
- active business
- active location
- permission list
- enabled workspaces/modules

---

# 10. API CLIENT EXPANSION

Refactor `apps/web/hospitable-web/lib/api.ts` into a broader Workforce client.

## 10.1 Preserve hospitable API calls

Keep existing hospitable methods intact.

## 10.2 Expand by namespace

Refactor to an object shape like:

```ts
export const api = {
  bootstrap: {...},
  superadmin: {...},
  admin: {...},
  workforce: {...},
  hospitable: {...},
}
```

## 10.3 Add DTO types

Create shared types under:

```text
lib/types/superadmin.ts
lib/types/admin.ts
lib/types/workforce.ts
lib/types/hospitable.ts
```

## 10.4 Superadmin API methods

Add methods for:

```ts
listBusinesses()
getBusiness(id)
createBusiness(payload)
updateBusiness(id, payload)
listLocations(params)
createLocation(payload)
listUsers(params)
createUser(payload)
listRoles(params)
createRole(payload)
listPermissions()
listFeatureFlags()
listAuditLog(params)
```

## 10.5 Backend alignment

If these backend endpoints do not exist yet, generate them in FastAPI under a control-plane namespace.

Target backend namespace:

```text
/api/v1/control/*
```

Suggested endpoints:

```text
GET    /api/v1/control/dashboard/summary
GET    /api/v1/control/businesses
POST   /api/v1/control/businesses
GET    /api/v1/control/businesses/{business_id}
PATCH  /api/v1/control/businesses/{business_id}
GET    /api/v1/control/locations
POST   /api/v1/control/locations
GET    /api/v1/control/users
POST   /api/v1/control/users
GET    /api/v1/control/roles
POST   /api/v1/control/roles
GET    /api/v1/control/permissions
GET    /api/v1/control/feature-flags
GET    /api/v1/control/audit-log
```

Tenant namespace suggestion:

```text
/api/v1/tenant/{business_id}/*
```

Suggested endpoints:

```text
GET    /api/v1/tenant/{business_id}/dashboard/summary
GET    /api/v1/tenant/{business_id}/locations
POST   /api/v1/tenant/{business_id}/locations
GET    /api/v1/tenant/{business_id}/members
POST   /api/v1/tenant/{business_id}/members
GET    /api/v1/tenant/{business_id}/roles
POST   /api/v1/tenant/{business_id}/roles
```

If the repo already has overlapping endpoints, adapt to the existing conventions instead of duplicating.

---

# 11. SUPERADMIN PAGES — DETAILED BUILD ORDER

Build these first.

## 11.1 `/superadmin/page.tsx`

Create a platform overview dashboard with:

- total businesses
- total locations
- total users
- active modules
- total open operational issues
- recent audit events
- quick links to setup pages

Use shared stat cards and shared tables.

## 11.2 `/superadmin/businesses/page.tsx`

Table columns:

- business name
- slug/code
- status
- owner/admin count
- location count
- enabled modules
- created date
- actions

Actions:

- create
- edit
- activate/deactivate
- open tenant admin view

## 11.3 `/superadmin/locations/page.tsx`

Table columns:

- location name
- business
- timezone
- status
- enabled modules
- created date
- actions

## 11.4 `/superadmin/users/page.tsx`

Table columns:

- full name
- email
- business membership count
- location membership count
- superadmin flag
- status
- last activity if available
- actions

## 11.5 `/superadmin/roles/page.tsx`

Table columns:

- role name
- scope type
- business/location scope
- permission count
- assignment count
- actions

## 11.6 `/superadmin/permissions/page.tsx`

Display a searchable permission registry grouped by domain.

Example groups:

- platform
- tenant
- workforce
- hospitable
- scheduling
- timeclock

## 11.7 `/superadmin/feature-flags/page.tsx`

Display feature toggles by:

- key
- description
- default
- current value
- scope
- affected module

## 11.8 `/superadmin/audit-log/page.tsx`

Filters:

- date range
- actor
- entity type
- action type
- business
- location

Columns:

- time
- actor
- action
- entity
- scope
- details snippet

---

# 12. TENANT ADMIN PAGES — DETAILED BUILD ORDER

## 12.1 `/admin/page.tsx`

Business overview dashboard with:

- active locations
- members
- role templates
- module status
- operational alerts
- recent admin events

## 12.2 `/admin/business-settings/page.tsx`

Sections:

- business profile
- timezone/currency defaults
- module enablement
- branding
- integrations

## 12.3 `/admin/locations/page.tsx`

Manage business locations.

Columns:

- name
- code
- timezone
- status
- enabled modules
- manager count
- actions

## 12.4 `/admin/members/page.tsx`

Manage business members and their assignments.

Columns:

- name
- email
- role summary
- assigned locations
- last activity
- actions

## 12.5 `/admin/roles/page.tsx`

Business-scoped role templates and permission bundles.

## 12.6 `/admin/dashboards/page.tsx`

Placeholder page if dynamic dashboards are not ready yet, but it must exist.

---

# 13. HOSPITABLE WORKSPACE REFACTOR

The current root pages already provide a foundation. Re-home them under `/hospitable`.

## 13.1 Pages to move/duplicate cleanly

Current:

```text
app/page.tsx
app/rooms/page.tsx
app/housekeeping/page.tsx
app/maintenance/page.tsx
app/inventory/page.tsx
app/property-setup/page.tsx
app/settings/page.tsx
```

Target:

```text
app/hospitable/page.tsx
app/hospitable/rooms/page.tsx
app/hospitable/housekeeping/page.tsx
app/hospitable/maintenance/page.tsx
app/hospitable/inventory/page.tsx
app/hospitable/property-setup/page.tsx
```

## 13.2 Preserve existing API usage

The current `lib/api.ts` already has useful typed methods for the hospitable backend. Reuse them.

## 13.3 Upgrade current labels

Change branding from pure “Hospitable Ops” to “Workforce” at the shell level, but keep a visible workspace label for the Hospitable area.

---

# 14. SHARED COMPONENT LIBRARY

Create reusable components.

## 14.1 `StatusBadge`

Handle statuses across all modules.

Support variants such as:

- success
- warning
- danger
- neutral
- info

Map domain statuses to visual variants.

## 14.2 `StatCard`

Generic KPI card with:

- label
- value
- optional delta
- optional description
- optional action

## 14.3 `DataTable`

Reusable table wrapper with:

- loading state
- empty state
- row actions
- search slot
- filter slot
- pagination placeholder

## 14.4 `FilterBar`

Generic filter row.

## 14.5 `WorkspaceHeader`

Shared title/subtitle/action bar.

## 14.6 `EmptyState`

Reusable empty state with icon/title/body/action.

---

# 15. DESIGN SYSTEM / THEME

Keep and extend the current styling. The app should feel like one system.

## 15.1 Create tokens

Add or centralize CSS tokens for:

- background
- surface
- border
- text
- muted text
- primary
- success
- warning
- danger
- info
- sidebar width
- topbar height
- spacing scale
- radius scale

## 15.2 Theme support

Support:

- light
- dark
- system

Use the same theme across all workspaces.

## 15.3 Visual hierarchy

Differentiate workspace contexts mostly through labels and minor accents, not through totally different design systems.

---

# 16. BUSINESS AND LOCATION CONTEXT

The UI must treat business and location as first-class context selectors.

## 16.1 Current state

The current sidebar has a hardcoded property selector.

## 16.2 Required refactor

Replace hardcoded values with dynamic selectors.

Need:

- business selector
- location selector
- sync active selection to URL/search params or app state
- use selectors to scope API calls

## 16.3 Hook files

Create:

```text
hooks/useCurrentBusiness.ts
hooks/useCurrentLocation.ts
```

## 16.4 Minimum behavior

- superadmins can switch businesses and locations
- tenant admins can switch locations inside their business
- workspace pages read from active context automatically

---

# 17. BACKEND WORK NEEDED TO SUPPORT UI

If backend support is incomplete, add the minimum endpoints required by the web app.

## 17.1 Bootstrap/session endpoint

Add:

```text
GET /api/v1/bootstrap/session
```

Response should include:

- current user
- permissions
- active business
- active location
- available businesses
- available locations
- enabled modules/workspaces

## 17.2 Control-plane endpoints

Add FastAPI router files under something like:

```text
apps/api/app/api/v1/endpoints/control.py
apps/api/app/api/v1/endpoints/tenant_admin.py
```

Register them from `apps/api/app/api/router.py`.

## 17.3 Seed/demo endpoints or mock services

If necessary for initial UI rendering, create demo-safe query services returning lists of:

- businesses
- locations
- users
- roles
- feature flags
- audit log entries

Use real DB models if already present; otherwise add temporary service functions with clear TODO markers.

---

# 18. TYPES TO ADD

Add type files with interfaces for all major admin entities.

## 18.1 `lib/types/superadmin.ts`

Include:

```ts
export interface BusinessSummary {
  id: string
  name: string
  code?: string | null
  status: 'active' | 'inactive' | 'pending'
  location_count: number
  user_count: number
  enabled_modules: string[]
  created_at?: string | null
}

export interface PlatformUserSummary {
  id: string
  full_name: string
  email: string
  is_superadmin: boolean
  status: 'active' | 'inactive' | 'invited'
  business_count: number
  location_count: number
  last_activity_at?: string | null
}

export interface RoleSummary {
  id: string
  name: string
  scope_type: 'platform' | 'business' | 'location'
  permission_count: number
  assignment_count: number
}

export interface PermissionSummary {
  key: string
  domain: string
  action: string
  description?: string | null
}

export interface FeatureFlagSummary {
  key: string
  description?: string | null
  scope: 'global' | 'business' | 'location'
  enabled: boolean
}

export interface AuditLogEntry {
  id: string
  occurred_at: string
  actor_name?: string | null
  actor_id?: string | null
  action: string
  entity_type: string
  entity_id?: string | null
  scope_type?: string | null
  scope_id?: string | null
  summary?: string | null
}
```

## 18.2 `lib/types/admin.ts`

Add business/location/member focused types.

## 18.3 `lib/types/common.ts`

Add generic pagination and option types.

---

# 19. IMPLEMENTATION DETAILS FOR COPILOT

## 19.1 Refactor existing `Sidebar.tsx`

Current sidebar is tightly coupled to Hospitable. Convert it into a generic component that reads from the nav registry and current workspace.

Do not hardcode:

- Silver Sands Motel
- only Operations/Configuration sections
- only Hospitable labels

## 19.2 Refactor root dashboard

Current `app/page.tsx` is a Hospitable dashboard. Replace it with a Workforce overview page.

The current Hospitable dashboard logic should move to `app/hospitable/page.tsx`.

## 19.3 Preserve API helpers

Current `lib/api.ts` has useful hospitable DTOs and methods. Keep those, but namespace them under `api.hospitable`.

## 19.4 Avoid giant monolith files

Break UI code into reusable components, hooks, and typed models.

## 19.5 Keep placeholders explicit

Where backend support is incomplete, implement placeholder UIs with clear TODOs and mock-safe fallbacks rather than leaving broken pages.

---

# 20. INITIAL PAGE CONTENT EXPECTATIONS

## 20.1 Root `/`

Display a Workforce overview dashboard with cards such as:

- Businesses
- Locations
- Members
- Open operational tasks
- Open maintenance issues
- Active shifts

Also include quick links to:

- Superadmin
- Admin
- Workforce
- Hospitable

## 20.2 `/superadmin`

Platform overview.

## 20.3 `/admin`

Tenant summary.

## 20.4 `/workforce`

Operational summary, even if some sections are initially placeholder.

## 20.5 `/hospitable`

Current operational overview for property ops.

---

# 21. ACCEPTANCE CRITERIA

Implement until all of the following are true:

## App shell

- There is one shared app shell.
- Sidebar is collapsible.
- Mobile sidebar works.
- Topbar includes workspace/business/location context.

## Routing

- Root is a Workforce overview.
- Hospitable routes live under `/hospitable/*`.
- Superadmin routes exist under `/superadmin/*`.
- Admin routes exist under `/admin/*`.
- Workforce routes exist under `/workforce/*`.

## Navigation

- Navigation is defined from a registry.
- Navigation can be filtered by permissions.
- Workspace switching works.

## Superadmin pages

- Overview page exists.
- Businesses page exists.
- Users page exists.
- Roles page exists.
- Permissions page exists.
- Feature flags page exists.
- Audit log page exists.

## Tenant admin pages

- Overview page exists.
- Business settings page exists.
- Locations page exists.
- Members page exists.
- Roles page exists.

## Hospitable

- Existing functionality is preserved.
- Existing pages are rehomed under `/hospitable/*`.
- Existing API integrations still work.

## API client

- Client is namespaced by domain.
- Typed interfaces exist for major admin entities.
- Loading and error states exist on pages.

## UX

- Empty states exist.
- Tables are readable.
- Buttons/actions are clearly labeled.
- Theme remains coherent across workspaces.

---

# 22. RECOMMENDED IMPLEMENTATION ORDER

Execute in this order:

1. Create shared shell and route structure.
2. Create nav registry and permission filtering helpers.
3. Move current Hospitable pages under `/hospitable`.
4. Replace root dashboard with Workforce overview.
5. Expand `lib/api.ts` into namespaced client.
6. Build superadmin overview and tables.
7. Build tenant admin overview and tables.
8. Add business/location context selectors.
9. Add bootstrap/session endpoint if missing.
10. Add control-plane backend endpoints as needed.
11. Add placeholder workforce pages.
12. Add tests for navigation and key pages.

---

# 23. TESTING REQUIREMENTS

Add or update tests for:

- sidebar renders workspace sections correctly
- permission-filtered nav hides restricted items
- root dashboard renders
- `/superadmin/businesses` renders table
- `/admin/locations` renders table
- old hospitable routes redirect correctly

Use the existing frontend test setup where possible.

---

# 24. DO NOTS

- Do not build a separate new frontend app.
- Do not throw away the existing Hospitable pages.
- Do not hardcode Silver Sands everywhere in shared UI.
- Do not hardcode business IDs in navigation.
- Do not make navigation depend on visual labels only.
- Do not duplicate backend functionality if a matching endpoint already exists.

---

# 25. FIRST PR TARGET

The first implementation PR should include:

- shared `AppShell`
- nav registry
- permission helper utilities
- route restructure
- root Workforce overview page
- `/superadmin` overview page
- `/superadmin/businesses` page
- `/admin` overview page
- `/hospitable/*` migrated routes
- updated sidebar/topbar/business selector

This PR should make the app look and behave like a real Workforce console, even if some pages still use placeholder data.

---

# 26. OPTIONAL PHASE 2

After the admin console foundation is stable, add:

- drag/drop dashboard widgets
- advanced audit explorer
- feature-flag editor
- location setup wizard
- module enable/disable UI
- role-template cloning
- API key management UI
- integration health cards
- job/worker queue dashboard

---

# 27. DIRECT CODE TASKS FOR COPILOT

Perform these concrete tasks:

1. Refactor the existing `Sidebar.tsx` into a generic Workforce sidebar.
2. Create `components/nav/nav-config.ts` and move menu definitions there.
3. Create `lib/permissions.ts` and `hooks/usePermissions.ts`.
4. Move the current dashboard page to `app/hospitable/page.tsx`.
5. Create a new `app/page.tsx` Workforce overview dashboard.
6. Create `/superadmin` and `/admin` route trees.
7. Expand `lib/api.ts` into a namespaced typed client.
8. Add shared table/stat/empty-state components.
9. Add business and location selectors backed by state/hooks.
10. Add backend endpoints required to populate the new admin pages if missing.

Deliver code in small, coherent commits if possible, but prioritize a working integrated result.
