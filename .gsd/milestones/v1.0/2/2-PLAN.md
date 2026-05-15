---
phase: 2
plan: 1
wave: 1
---

# Plan 2.1: Core Workshop UI Layout

## Objective
Build the main application layout for the Aegis Strategy Workshop, including a sidebar and the main content area with placeholder action buttons. Ensure the design is minimal, professional, and built with Tailwind CSS + shadcn UI.

## Context
- .gsd/SPEC.md
- .gsd/ROADMAP.md

## Tasks

<task type="auto" effort="medium">
  <name>Build Application Layout & Sidebar</name>
  <action>
    - Update `frontend/src/App.tsx` (or equivalent) to use a flexbox/grid layout containing a sidebar on the left and a main panel on the right.
    - Inside the sidebar, add a section for a "Strategy List".
    - Use shadcn UI components (like Button, Card, Separator, etc.) if they were installed. Otherwise, rely on clean Tailwind classes.
    - Keep the theme dark/professional.
  </action>
  <verify>test -f frontend/src/App.tsx && grep -q "sidebar" frontend/src/App.tsx</verify>
  <done>The main layout structure with a sidebar and a main panel is implemented.</done>
</task>

<task type="auto" effort="low">
  <name>Add UI Controls (Buttons)</name>
  <action>
    - Add "Create Strategy", "Save Strategy", and "Validate Strategy" buttons to the UI.
    - Place "Create Strategy" in the sidebar or top header.
    - Place "Save" and "Validate" in the main panel header.
    - Add empty onClick handlers for now.
  </action>
  <verify>grep -q "Create Strategy" frontend/src/App.tsx</verify>
  <done>All three required functional buttons are visible in the UI.</done>
</task>

## Success Criteria
- [ ] Sidebar and main panel are successfully rendered.
- [ ] Create, Save, and Validate buttons are present in the layout.
