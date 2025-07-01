AGI Suite

The Open, Modular, Boundless Memory Agent Platform
Vision

AGI Suite is a blueprint and working prototype for open, modular AI agents with real, layered memory, self-reflection, continuous learning, tool/plugin ecosystem, human-in-the-loop safety, policy enforcement, and environmental embodiment. This platform is designed for research, innovation, and rapid development of next-generation AI agents.
Architecture Overview

    Boundless Memory Fabric: Hierarchical, infinite memory with vector search, on-disk archival, active forgetting, and context refresh.

    Plugin & Toolbelt System: Native runtime tools, API bridges, and modular pipeline composition.

    Metacognitive Core: Self-reflective planning, rationale tracing, and quantified uncertainty/confidence.

    Mood & Persona Manager: Adaptive, goal-aligned persona and mood switching.

    Continual Self-Learning: User feedback loops into real-time model adapters or RL agents.

    Observability & Telemetry: Live dashboards, metrics, and fully traceable agent logs.

    Human-in-the-Loop Harmony: Clarification, escalation, and safe handoff to humans when needed.

    Policy Engine: Privacy, bias, compliance, and ethical constraints enforced at runtime.

    Multi-Modal Embodiment: Adapters for text, code, images, audio, sensors, and device/action execution.

    Self-Healing Scheduler: Adaptive hook-based workflow and error/fallback recovery.

Modules

    memory_fabric: Infinite, hierarchical, semantic memory

    plugin_toolbelt: Tool/plugin management and dynamic skill onboarding

    metacog_core: Metacognitive planner, rationale, uncertainty

    mood_persona: Persona/mood runtime switching

    feedback_trainer: Continual learning and adapter pipeline

    metrics_observability: Metrics, dashboards, trace logs

    human_in_loop: Clarification and escalation to humans

    policy_manager: Pluggable policy/constraint engine

    multi_modal: Sensors, adapters, executors, and workflows

    scheduler: Central orchestrator, hooks, self-healing logic

    main.py: Entry point that ties modules together for agent run

Quick Start

    Clone the repository:
    git clone https://github.com/mycellphone/AGI-Suite.git

    Install dependencies:
    cd AGI-Suite
    pip install -r requirements.txt

    Run the main agent:
    python main.py

    Demo workflows can be found in multi_modal/workflows/

    Policies can be customized in policy_manager/policy_config.yaml

    Metrics and observability setup are in metrics_observability/

Why AGI Suite?

    More than just a chatbot: AGI Suite is a platform for real agent autonomy, memory, and action—modular and future-proof.

    Plug, play, and extend: Add new skills, sensors, or policies at runtime with no core changes.

    Transparent and safe: Every agent decision is logged, explainable, and auditable.

    Ready for research or rapid prototyping: Start building next-gen agent systems immediately.

Credits

Created by Justin Carrow
Powered by contributions from the open-source AI community.
Contributing

Open to issues, pull requests, and ideas. Want to build an adapter, tool, or dashboard? Check the docs and open a discussion.
Roadmap

    Web UI and real-time agent dashboard

    Voice, video, and multi-modal adapters

    Distributed and cloud agent orchestration

    Native mobile agent integrations

License

GMU 3.0

Fork it, improve it, and make it yours—AGI Suite is an open launchpad for the future of agent-based AI.
