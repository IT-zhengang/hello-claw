---
title: "OpenSandbox: Building Safe Boundaries for AI Agents"
---

# OpenSandbox: Building Safe Boundaries for AI Agents

<AiPickArticle>

<AiPickCover
  eyebrow="AI Open Source Picks · Issue 01"
  title="OpenSandbox"
  description="A general-purpose sandbox platform for AI agents that turns code execution, browser automation, remote development, and network boundary control into one orchestrated, extensible, and auditable runtime substrate."
  :chips='["Protocol-first", "Four-layer design", "Secure runtimes", "Kubernetes-native"]'
/>

<AiPickSummaryGrid
  :items='[
    { "label": "Bottom line", "value": "This is not a Docker wrapper. It is a control plane for agent execution environments." },
    { "label": "Best section", "value": "How Lifecycle, Execd, and Egress APIs jointly define the sandbox boundary." },
    { "label": "Who should read it", "value": "Teams building code execution, remote dev boxes, browser automation, code interpreters, or agent runtimes." },
    { "label": "Engineering lesson", "value": "Separate what runs from what it can reach, then govern each layer through protocols, runtime orchestration, network policy, and isolated instances." }
  ]'
/>

> **Lead**: Once an AI agent can execute code on its own, who guarantees that your server does not become the next compromised host? OpenSandbox, recently open-sourced by Alibaba, answers that with a four-layer architecture built for isolation, orchestration, and auditability.

---

## 1. Why sandboxes matter now

In January 2026, a well-known AI coding assistant disclosed a serious security issue: with carefully crafted prompts, attackers were able to steer the model into producing malicious code that read sensitive server files. That is not a science-fiction scenario anymore. It is an operational reality for any system that lets LLMs act.

**The root problems are straightforward:**

- 🚨 **Model-generated code is not trustworthy by default**: prompt injection can coerce destructive commands such as `rm -rf /`.
- 🚨 **Default container isolation is often too weak**: a plain Docker deployment is not a sufficient security boundary for hostile workloads.
- 🚨 **Resource abuse is easy**: one infinite loop can burn through CPU and memory.
- 🚨 **Data leakage is subtle**: poor session isolation can expose sensitive data across tasks and users.

This is why modern AI execution systems need a real sandbox platform rather than an ad-hoc container launcher.

---

## 2. What OpenSandbox is

OpenSandbox is Alibaba's open-source answer to that execution problem: a general-purpose sandbox platform designed specifically for AI workloads. It is positioned not as a one-off demo, but as reusable infrastructure for real production systems.

![OpenSandbox project overview](../../../static/ai-open-source-picks/opensandbox/images/opensandbox-overview.png)

### 2.1 Positioning

OpenSandbox is a **protocol-driven, production-grade** sandbox platform rather than a thin Docker abstraction.

It targets five common AI scenarios:

- Coding assistants such as Claude Code, Gemini CLI, and Codex CLI
- Browser automation with tools like Chrome and Playwright
- Multi-language code interpreters
- Remote development environments such as VS Code Web and desktop sessions
- Reinforcement-learning training workloads

It is also designed to scale cleanly from a laptop Docker setup to a Kubernetes cluster, and it exposes SDKs across multiple languages including Python, JavaScript/TypeScript, Java/Kotlin, and C#/.NET.

### 2.2 Technical highlights

```text
🔐 Security isolation through gVisor, Kata Containers, and Firecracker-style secure runtimes
🌐 Network control with ingress proxying plus egress policy enforcement
⚡ High performance through Go-based core components and SSE streaming
🛠️ Extensibility through a four-layer architecture defined by OpenAPI 3.1
```

---

## 3. The four-layer architecture

At the heart of OpenSandbox is a clean separation of responsibilities. The platform is split into four layers, each with its own contract and replaceable implementation.

### 3.1 End-to-end view

![OpenSandbox four-layer architecture](../../../static/ai-open-source-picks/opensandbox/images/opensandbox-architecture.png)

**The request path looks like this:**

1. Your application calls an SDK.
2. The SDK talks to the Lifecycle API or Execution API over HTTP.
3. The runtime layer creates and manages containers through Docker or Kubernetes.
4. An `execd` daemon inside the sandbox instance exposes execution and file interfaces.
5. Ingress and egress sidecars control traffic entering or leaving the sandbox.

### 3.2 SDK layer

The SDK layer is what developers touch first. Each language package wraps the same protocol surface and tries to make sandbox creation, command execution, file transfer, and code-interpreter sessions feel ordinary.

```python
# Base sandbox SDK
from opensandbox import SandboxClient

client = SandboxClient(base_url="http://localhost:8080")

# Create a sandbox
sandbox = client.create(
    image="python:3.11",
    resources={"cpu": "2", "memory": "4Gi"},
    ttl=3600,  # auto-destroy after one hour
)

# Execute a command
result = sandbox.execute(
    "pip install numpy && python -c 'import numpy as np; print(np.random.rand())'"
)
print(result.stdout)

# File operations
sandbox.upload("script.py", "print('hello')")
sandbox.download("output.txt")

# Multi-language interpreter session
from opensandbox_code_interpreter import CodeInterpreter

interpreter = CodeInterpreter(sandbox)
session = interpreter.create_session(language="python")

session.execute("x = 10")
result = session.execute("x * 2")
print(result.output)  # 20
```

**Why this layer matters:**

- Every SDK is generated from the same OpenAPI contract, which keeps capabilities aligned across languages.
- Async APIs reduce blocking behavior in client applications.
- Auth, retries, and protocol details are hidden from the application surface.
- MCP integration makes it easier to plug sandbox capabilities into agent frameworks.

### 3.3 Specs layer

This is one of the smartest parts of the project. OpenSandbox defines the system through APIs first, which means lifecycle control, execution, and network governance all have explicit contracts.

#### Lifecycle API (`sandbox-lifecycle.yml`)

```text
POST   /sandboxes              # create a sandbox
GET    /sandboxes              # list sandboxes
GET    /sandboxes/{id}         # sandbox details
DELETE /sandboxes/{id}         # delete a sandbox
POST   /sandboxes/{id}/pause   # pause a sandbox
POST   /sandboxes/{id}/resume  # resume a sandbox
POST   /sandboxes/{id}/renew   # extend TTL
```

The lifecycle API effectively becomes the control-plane surface for creation, suspension, resume, expiry, and cleanup.

**State machine design:**

![Lifecycle API state machine](../../../static/ai-open-source-picks/opensandbox/images/opensandbox-lifecycle.png)

A real sandbox platform needs reliable transitions, not just “start” and “stop”. OpenSandbox's state model makes those transitions explicit and easier to automate.

#### Execution API (`execd-api.yaml`)

```text
# command execution
POST   /exec                   # run a command
GET    /exec/{pid}/logs        # stream logs through SSE
POST   /exec/{pid}/kill        # terminate a process

# file operations
GET    /files                  # list files
POST   /files/upload           # upload a file
GET    /files/download         # download a file
PUT    /files/rename           # rename a file
DELETE /files                  # delete files or directories

# code interpreter
POST   /kernels                # create a Jupyter kernel
POST   /kernels/{id}/execute   # execute code
GET    /kernels/{id}/outputs   # fetch outputs

# system metrics
GET    /metrics/cpu            # CPU usage
GET    /metrics/memory         # memory usage
```

This API is exposed by `execd` inside each sandbox instance. It is the closest thing OpenSandbox has to an “operating system interface” for agent workloads.

#### Egress API (`egress-api.yaml`)

```text
GET    /egress/policies        # get policies
POST   /egress/policies        # create policies
PUT    /egress/policies/{id}   # update policies
DELETE /egress/policies/{id}   # delete policies
```

That separate API matters because network governance is not an afterthought. It is part of the platform's explicit control surface.

```json
{
  "sandbox_id": "sb-123",
  "rules": [
    {
      "direction": "outbound",
      "protocol": "tcp",
      "port_range": "443",
      "cidr": "0.0.0.0/0",
      "action": "allow"
    },
    {
      "direction": "outbound",
      "protocol": "tcp",
      "port_range": "22",
      "cidr": "10.0.0.0/8",
      "action": "deny"
    }
  ]
}
```

### 3.4 Runtime layer

The runtime layer is the orchestrator. It translates protocol-level requests into concrete sandbox instances and keeps the whole system in sync.

#### FastAPI lifecycle server

The lifecycle server, implemented in FastAPI, is responsible for:

1. Receiving SDK requests
2. Calling Docker or Kubernetes APIs
3. Injecting `execd`
4. Configuring ingress and egress sidecars
5. Tracking sandbox metadata such as state, resources, and TTL

```python
# server/opensandbox_server/main.py
from fastapi import FastAPI
from docker import DockerClient
from kubernetes import client as k8s_client

app = FastAPI()

class SandboxManager:
    def __init__(self, runtime: str = "docker"):
        if runtime == "docker":
            self.client = DockerClient.from_env()
        else:
            self.client = k8s_client.CoreV1Api()

    async def create_sandbox(self, spec: SandboxSpec) -> Sandbox:
        sandbox_id = generate_uuid()
        container_config = {
            "image": spec.image,
            "command": ["/execd"],
            "environment": spec.env_vars,
            "labels": {
                "opensandbox.io/sandbox-id": sandbox_id,
                "opensandbox.io/state": "pending",
            },
        }

        if isinstance(self.client, DockerClient):
            container = self.client.containers.run(**container_config, detach=True)
        else:
            container = self.client.create_namespaced_pod(
                namespace="sandboxes",
                body=container_config,
            )

        await wait_for_execd_ready(sandbox_id)
        sandbox = Sandbox(id=sandbox_id, container=container, state="running")
        self.update_state(sandbox_id, "running")
        return sandbox

manager = SandboxManager()

@app.post("/sandboxes")
async def create_sandbox(spec: SandboxSpec):
    sandbox = await manager.create_sandbox(spec)
    return sandbox.to_dict()
```

#### Ingress proxy gateway

Ingress is handled by a Go reverse proxy that maps a public request path to the correct sandbox instance and port.

```text
# access a web app running inside sandbox sb-123 on port 8080
GET https://opensandbox.example.com/sandboxes/sb-123/port/8080

# access a VNC desktop on port 5900
GET https://opensandbox.example.com/sandboxes/sb-123/port/5900
```

This matters because remote browser sessions, VS Code Web instances, and exposed notebook UIs all rely on predictable sandbox routing.

#### Egress network control

Outbound traffic is governed by a separate sidecar that enforces packet-level and DNS-level rules.

```bash
# allow HTTPS only
iptables -A OUTPUT -p tcp --dport 443 -j ACCEPT

# block internal networks
iptables -A OUTPUT -d 10.0.0.0/8 -j DROP
iptables -A OUTPUT -d 192.168.0.0/16 -j DROP

# default deny
iptables -A OUTPUT -j DROP
```

The key architectural point is that egress policy is first-class. OpenSandbox does not assume that runtime isolation alone is enough.

### 3.5 Sandbox instance layer

At the bottom, each sandbox is a dedicated isolated instance that actually runs user workloads.

#### `execd` daemon

The `execd` daemon is a lightweight Go HTTP server injected into every sandbox image.

**Core responsibilities:**

1. Running child processes via `os/exec`
2. Exposing RESTful file operations
3. Integrating Jupyter kernels for multi-language execution
4. Collecting metrics from `/proc`

```text
HTTP Server
└── Gin Framework
    ├── Router
    │   ├── Exec Handler
    │   ├── File Handler
    │   ├── Kernel Handler
    │   └── Metrics Handler
    ├── os/exec
    │   └── Process Manager
    ├── io/fs
    ├── Jupyter Server
    │   ├── ZeroMQ Protocol
    │   └── Session Manager
    └── stat / meminfo
```

```go
// components/execd/main.go
package main

import (
    "github.com/gin-gonic/gin"
    "opensandbox/execd/handlers"
)

func main() {
    r := gin.Default()

    r.POST("/exec", handlers.ExecuteCommand)
    r.GET("/files/*path", handlers.ListFiles)
    r.POST("/files/upload", handlers.UploadFile)
    r.POST("/kernels", handlers.CreateKernel)
    r.GET("/metrics/cpu", handlers.GetCPUMetrics)

    go startJupyterServer()
    r.Run(":8080")
}
```

#### Jupyter server integration

OpenSandbox bakes in Jupyter-based interpreter capability for languages such as Python, Java, JavaScript, TypeScript, Go, and Bash. That gives it an immediate path toward “code interpreter” style products.

---

## 4. Security design: depth, not slogans

OpenSandbox uses a layered defensive model.

### 4.1 Container isolation

Traditional Docker setups share the host kernel. That is convenient, but risky for hostile or model-generated workloads.

OpenSandbox supports stronger execution runtimes such as:

1. **gVisor**: a user-space kernel layer that intercepts syscalls
2. **Kata Containers**: lightweight VMs with stronger isolation semantics
3. **Firecracker microVM**: highly optimized microVM-based execution

```yaml
# server/config.yaml
runtime:
  type: "kubernetes"
  secure_container:
    enabled: true
    runtime_class: "kata"  # or "gvisor", "firecracker"
```

### 4.2 Network isolation

Ingress is denied by default unless a port is explicitly exposed through the proxy layer.

Egress is policy-driven and can be restricted by IP range, port, and protocol. That matters for data exfiltration prevention as much as for pure security.

```python
# create a sandbox that can only reach a specific API segment
sandbox = client.create(
    image="python:3.11",
    egress_policy={
        "default_action": "deny",
        "rules": [
            {"protocol": "tcp", "port": 443, "cidr": "203.0.113.0/24"}
        ],
    },
)
```

### 4.3 Resource limits

CPU, memory, and lifetime controls prevent sandboxes from turning into noisy neighbors or abandoned cost sinks.

```python
sandbox = client.create(
    image="python:3.11",
    resources={
        "cpu": "2",
        "memory": "4Gi",
        "gpu": "0",
    },
)
```

```python
sandbox = client.create(image="python:3.11", ttl=3600)
sandbox.renew(ttl=1800)
```

### 4.4 Audit and monitoring

A serious agent runtime needs more than “run code and hope”. OpenSandbox records execution, file operations, and network activity, and it exposes live resource metrics.

```python
metrics = sandbox.get_metrics()
print(f"CPU: {metrics.cpu_percent}%")
print(f"Memory: {metrics.memory_used / 1024 / 1024}MB")
```

---

## 5. Kubernetes mode: from single host to fleet

OpenSandbox supports both Docker and Kubernetes runtime modes.

### 5.1 BatchSandbox for parallel workloads

In Kubernetes mode, OpenSandbox defines a `BatchSandbox` CRD for large-scale parallel workloads.

```yaml
apiVersion: opensandbox.io/v1
kind: BatchSandbox
metadata:
  name: agent-evaluation
spec:
  replicas: 100
  template:
    image: "agent-cli:latest"
    resources:
      cpu: "1"
      memory: "2Gi"
    command: ["run-evaluation"]
  completion_policy: "All"
```

This is the kind of abstraction that starts to matter when you are evaluating many agent runs or provisioning execution environments at cluster scale.

### 5.2 SIG Agent-Sandbox compatibility

OpenSandbox also aligns itself with the SIG Agent-Sandbox direction, which improves portability across agent frameworks and standard-compliant tooling.

---

## 6. Real use case: building a code interpreter service

A practical way to read OpenSandbox is to imagine building a ChatGPT-style code interpreter service on top of it.

### 6.1 High-level flow

```text
User -> FastAPI service: upload file + ask a question
FastAPI service -> object storage: persist file
FastAPI service -> OpenSandbox: create sandbox and mount file
FastAPI service -> User: return sandbox ID
User -> LLM: ask for data analysis
LLM -> OpenSandbox: generate and execute Python code
OpenSandbox -> FastAPI service: return results + chart
FastAPI service -> User: show analysis result
OpenSandbox -> OpenSandbox: delete sandbox when TTL expires
```

### 6.2 Core code sketch

```python
from fastapi import FastAPI, UploadFile
from opensandbox import SandboxClient
from openai import OpenAI

app = FastAPI()
sandbox_client = SandboxClient(base_url="http://localhost:8080")
llm_client = OpenAI(api_key="sk-xxx")

@app.post("/chat")
async def chat(file: UploadFile, question: str):
    sandbox = sandbox_client.create(
        image="python:3.11-code-interpreter",
        resources={"cpu": "2", "memory": "4Gi"},
        ttl=1800,
    )

    sandbox.upload(file.filename, file.file.read())

    prompt = f"""
You have a data-analysis task. File {file.filename} has been uploaded to the sandbox.

User question: {question}

Write Python code that:
1. reads the file
2. analyzes the data
3. saves a chart as chart.png

Return code only.
"""

    response = llm_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    code = response.choices[0].message.content

    result = sandbox.execute(code, timeout=60)
    chart_data = sandbox.download("chart.png")

    return {
        "code": code,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "chart": chart_data,
    }
```

### 6.3 Operational optimizations

- Pool warm sandboxes to reduce cold-start latency
- Cache images locally to speed up pulls
- Reuse sandboxes for short-lived multi-turn sessions
- Offload long tasks to async job queues

---

## 7. Why OpenSandbox stands out

| Capability | OpenSandbox | E2B | AWS Bedrock Code Interpreter | In-house build |
| --- | --- | --- | --- | --- |
| Open source | ✅ Apache 2.0 | ❌ Commercial | ❌ Closed | Depends |
| Multi-language SDKs | ✅ 4+ languages | ✅ 3 languages | ❌ Python only | Must build |
| Kubernetes-native | ✅ Strong support | ⚠️ Limited | ❌ No | Must build |
| Secure runtimes | ✅ gVisor / Kata | ✅ Firecracker | ✅ Proprietary | Must build |
| Network control | ✅ Ingress + Egress | ✅ Limited | ⚠️ Mostly egress | Must build |
| Cost model | ✅ Free | ❌ Usage-based | ❌ Usage-based | High engineering cost |
| Ecosystem | ✅ CNCF + Alibaba backing | ⚠️ Startup | ❌ Closed AWS surface | N/A |

**Its practical strengths are:**

1. Open-source control with no hard vendor lock-in
2. Production-oriented design rather than a narrow demo API
3. Broad scenario coverage across agent tooling, browser automation, and code execution
4. Strong Kubernetes alignment for large deployments

---

## 8. Reported performance characteristics

According to the article's summary of official and community tests:

- On a 16-core / 32GB node, OpenSandbox can reportedly sustain roughly 50–100 concurrent sandboxes depending on resource quotas.
- Sandbox startup is cited at about 1–3 seconds with Docker and 5–10 seconds with Kata Containers.
- Code execution overhead for Python is described as close to local execution.
- Jupyter kernel startup is around 1–2 seconds.

These numbers should be read as directional rather than universal benchmarks, but they indicate the project is targeting operational, not purely experimental, workloads.

---

## 9. Roadmap direction

The roadmap highlighted in the article is managed through OSEP (OpenSandbox Enhancement Proposal) and points toward:

### Near term

- Go SDK support
- WebAssembly runtime support
- Better GPU scheduling and MIG slicing

### Mid term

- Edge deployment support
- Federated-learning integrations
- AI-assisted autoscaling and resource scheduling

### Longer term

- TEE-backed trusted execution
- Tamper-resistant audit trails
- Cross-cloud sandbox orchestration

---

## 10. Fast start

### 10.1 Docker mode

```bash
git clone https://github.com/alibaba/OpenSandbox.git
cd OpenSandbox
docker-compose up -d
curl http://localhost:8080/health
```

### 10.2 Python test sandbox

```bash
pip install opensandbox

cat > test.py <<'EOF'
from opensandbox import SandboxClient

client = SandboxClient(base_url="http://localhost:8080")
sandbox = client.create(image="python:3.11")
result = sandbox.execute("python -c 'print("Hello, OpenSandbox!")'")
print(result.stdout)
sandbox.delete()
EOF

python test.py
```

### 10.3 Kubernetes deployment

```bash
helm repo add opensandbox https://alibaba.github.io/OpenSandbox/helm
helm install opensandbox opensandbox/opensandbox
kubectl apply -f ingress.yaml
kubectl port-forward svc/opensandbox-dashboard 8080:80
```

---

## 11. Common questions and practical guidance

### How do sandboxes communicate?

By default, they should not. If you need coordination, use shared storage, an external queue, or explicitly allowed network policies.

### How do you persist data?

```python
sandbox = client.create(
    image="python:3.11",
    volumes=[
        {"host_path": "/data", "mount_path": "/mnt/data"}
    ],
)
```

### What if a sandbox is attacked?

1. Pause it immediately
2. Export logs and snapshots for investigation
3. Destroy it
4. Review egress records for signs of exfiltration

### Practical checklist

- Always set a TTL
- Enable a stronger runtime in production
- Prefer default-deny egress
- Keep base images updated
- Turn on audit logging

---

## 12. Why this project is worth studying

OpenSandbox is interesting because it treats sandboxing as a **system design problem**, not just a container startup problem.

The most important ideas are:

1. **Protocol-first design**: contracts define the platform surface
2. **Layered architecture**: each concern can evolve independently
3. **Security by depth**: runtime, network, and resource controls work together
4. **Cloud-native posture**: Kubernetes is not an afterthought
5. **Open-source leverage**: teams can adapt the platform instead of renting a black box

If you are building agent infrastructure, the real value is not just “safe code execution”. It is the way OpenSandbox decomposes execution into lifecycle management, in-instance capability, and explicit network policy. That decomposition is the reusable lesson.

## References

<AiPickReferenceList
  :items='[
    { "title": "OpenSandbox repository", "description": "The primary source for code, deployment notes, and the public surface area of the project.", "href": "https://github.com/alibaba/OpenSandbox" },
    { "title": "CNCF Landscape", "description": "Useful for placing OpenSandbox within the wider cloud-native infrastructure map.", "href": "https://landscape.cncf.io/" },
    { "title": "Alibaba OpenSandbox blog coverage", "description": "Helpful context for project intent, scenario framing, and ecosystem positioning.", "href": "https://zread.ai/alibaba/OpenSandbox" },
    { "title": "Jupyter kernel protocol docs", "description": "A good background reference for the multi-language interpreter model used inside the sandbox.", "href": "https://jupyter-client.readthedocs.io/" }
  ]'
/>

</AiPickArticle>
