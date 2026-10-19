# Handover prompt for Claude in Arduino App Lab

Copy everything between the two lines below and paste it into Claude in App Lab as your first message.

---

You are taking over an existing robot build: Abadi Rover (Arduino UNO Q on an ELEGOO Conqueror tracked chassis, App Lab only).

The project's single source of truth is this GitHub repository:
https://github.com/ms95ir-ctrl/Abadi_Rover

Before doing anything:
1. Read `plan.md` in full, starting with the **Current Status** line at the top. Then read `docs/wiring.md`.
2. Follow the rules in `plan.md` and `.cursor/rules/plan-first.mdc`:
   - The locked pin table and locked power design must never be changed, renamed or "cleaned up". If anything conflicts, STOP and ask me.
   - One stage at a time. No code for a later stage until I confirm the current stage passed on real hardware.
   - Keep replies short. Write every command out in full and explain what it does. I am not comfortable with terminal or git shorthand.
3. The gamepad is already paired and connected (you did that). Remaining Stage 2 checks: stick and button values print in an App Lab app with NO motors, and the controller reconnects after being switched off and on.
4. Keep app code in this repository, and update the **Current Status** line in `plan.md` (with my confirmation) when a stage passes.

If you can't open the repository, tell me and I'll give you access.

Start by telling me in one or two sentences what you'll do for the remaining Stage 2 checks, then wait for my confirmation.

---
