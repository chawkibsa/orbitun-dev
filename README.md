# orbitun-dev

## Guided Interactive Demontrations
To provide a hands-on experience, we’ve created an interactive guided demos to walks you through key functionalities of orbitundev.

You can access the demo via the following link:

https://www.iorad.com/library/263615?roleId=13114

<img width="500" alt="Image" src="https://github.com/user-attachments/assets/ce0757d3-1677-4794-9727-c0d8dc492a57" />
<img width="500" alt="Image" src="https://github.com/user-attachments/assets/fa0bcef2-e28d-4df0-8a60-6616032b72f4" />
<img width="500" alt="Image" src="https://github.com/user-attachments/assets/e1029b4c-3163-4bb9-80ac-771c9cd40645" />
<img width="500" alt="Image" src="https://github.com/user-attachments/assets/cc3d4670-c9bf-4d7b-a505-0ff64186e7a7" />

We encourage you to follow the steps in the demos to get a deeper understanding of the project.

## Overview
orbitun-dev is the development release of the orbitun project. It has been released to enable the community to contribute, develop, test, deploy, and improve.

orbitun-dev provides programmatic control over security configurations through exposed APIs that interacts with installed agents (sensors) on endpoints.

It allows administrators and security professionals with real-time monitoring and enforcement of CIS (Center for Internet Security) compliance benchmarks.

## Key Features
- **Automated Security Auditing**: Conducts continuous security assessments based on CIS benchmarks.
- **Remediation & Hardening**: Implements corrective actions to align systems with compliance standards.
- **Agent-Based Architecture**: Deployed sensors interact with a centralized API for security policy enforcement.
- **Real-Time Monitoring**: Provides security teams with insights into system compliance status.
- **API-Driven**: Allows seamless integration with existing security workflows.
- **Cross-Platform Support(furture)**: Planned support for multiple operating systems.
- **ML (future)**: AI-driven analytics for advanced prioritization, anomaly detection and compliance automation.

## Problem It Solves
- Out of the box automated compliance enforcement, with no manual effort.
- Standard security policies across distributed environments.
- Real-time insights into security posture and deviations.

## Installation & Usage
To test orbitun locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/chawkibsa/orbitun-dev.git
   cd orbitun-dev
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. and set up the database (you should have Postgres installed):
   ```bash
   create user orbitundev with encrypted password 'orbitundev';
   CREATE DATABASE orbitundb OWNER orbitundev;
   ```
4. Start the server:
   ```bash
   python3 -m app.main
   ```
5. Access orbitundev API documentation.
6. Deploy agents on target machines (optional).

## Contribution Guidelines
orbitun-dev is open for contributions from the security and development community. We welcome:
- Bug reports and feature requests.
- Code contributions via pull requests.
- Security and performance enhancements.

To contribute:
1. Fork the repository and create a new branch.
2. Implement changes and ensure they adhere to project guidelines.
3. Submit a pull request for review.

---

We appreciate your interest in orbitun-dev ! Join us in making security automation more efficient and accessible.

