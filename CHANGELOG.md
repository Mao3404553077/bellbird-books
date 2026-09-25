# Changelog

All notable changes to this project are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Initial project skeleton (Flask app factory, blueprints, base template).
- Book inventory CRUD with multi-field search (title / author / shelf / ISBN).
- Second-hand book per-copy records with condition grading.
- Customer record keeping.
- Order creation with four-state workflow (placed / arrived / collected / cancelled).
- Counter-facing dashboard: live stock, pending orders, low-stock alerts.
- Production deployment blueprint for Render.com (`render.yaml`, `Procfile`).
- Per-environment configuration (`config.py`, `.env.example`).
