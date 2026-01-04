# HTCondor Tutorial for Quantum Machine Learning

<div align="center">

![HTCondor](https://img.shields.io/badge/HTCondor-9.0+-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![PennyLane](https://img.shields.io/badge/PennyLane-Quantum-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**A comprehensive guide to running quantum machine learning workloads on HTCondor at PIC**

[Overview](#-overview) • [Quick Start](#-quick-start) • [Tutorial Structure](#-tutorial-structure) • [Resources](#-resources)

</div>

---

## 📋 Overview

This repository provides a **hands-on tutorial** for submitting and managing computational jobs on the [Port d'Informació Científica (PIC)](https://www.pic.es/) HTCondor cluster. Designed specifically for the [QML-CVC research group](https://qml.cvc.uab.es/), this tutorial demonstrates how to leverage high-performance computing resources for quantum machine learning research.

### What You'll Learn

- ✅ **HTCondor fundamentals**: Understanding job submission, monitoring, and management
- ✅ **Parameter sweeps**: Efficiently running large-scale computational experiments
- ✅ **Best practices**: Resource allocation, file management, and error handling
- ✅ **Real-world example**: Quantum circuit simulation using PennyLane

### Why HTCondor?

HTCondor is a powerful distributed computing platform that enables:
- **High-throughput computing**: Run thousands of jobs efficiently
- **Resource matching**: Automatic allocation based on job requirements
- **Fair-share scheduling**: Ensures equitable resource distribution
- **Fault tolerance**: Automatic job retry and recovery mechanisms

---

## 🚀 Quick Start

### Prerequisites

- Access to PIC HTCondor cluster
- Python 3.8+ with PennyLane installed
- Basic familiarity with command-line tools

### Example: Quantum Circuit Parameter Sweep

This tutorial demonstrates a parameter sweep over a quantum circuit using PennyLane. The example:

1. **Defines a quantum circuit** with two rotation parameters
2. **Generates a parameter grid** for systematic exploration
3. **Submits jobs** to HTCondor for parallel execution
4. **Collects results** from distributed computation

```bash
# 1. Generate parameter combinations
python define_params_and_check_circuit.ipynb

# 2. Submit jobs to HTCondor
condor_submit HPC/submit.sub

# 3. Monitor job status
condor_q

# 4. Check results
ls jobs/outs/
```

---

## 📁 Tutorial Structure

```
tutorial-pic/
├── README.md                          # This file
├── main.py                            # Quantum circuit simulation script
├── define_params_and_check_circuit.ipynb  # Parameter generation notebook
├── HPC/
│   ├── submit.sub                     # HTCondor submission file
│   ├── subash.sh                      # Job execution script
│   └── params.txt                     # Parameter combinations
└── jobs/                              # Job outputs (created on execution)
    ├── outs/                          # Standard output files
    ├── errs/                          # Error output files
    └── logs/                          # HTCondor log files
```

### Key Files Explained

#### `main.py`
The core computational script that:
- Defines a quantum circuit with RX and RZ rotations
- Samples from the circuit using PennyLane
- Saves results to disk for post-processing

#### `HPC/submit.sub`
HTCondor submission file specifying:
- **Resource requirements**: CPUs, memory, disk space
- **Job flavor**: Short, medium, or long-running jobs
- **File transfers**: Input/output file handling
- **Queue configuration**: Parameter sweep setup

#### `HPC/subash.sh`
Bash script that:
- Activates the Python virtual environment
- Executes the main script with parameters
- Handles environment setup and cleanup

---

## 🎓 HTCondor Concepts

### Job Submission Workflow

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   User      │─────▶│   Schedd    │─────▶│  Negotiator │
│  Interface  │      │  (Queue)     │      │  (Matcher)  │
└─────────────┘      └──────────────┘      └─────────────┘
                                                  │
                                                  ▼
                                         ┌─────────────┐
                                         │  Worker     │
                                         │  Node       │
                                         │  (Execution)│
                                         └─────────────┘
```

### Key HTCondor Commands

| Command | Description |
|---------|-------------|
| `condor_submit` | Submit jobs to the queue |
| `condor_q` | View job status and queue |
| `condor_q -analyze` | Diagnose why jobs are idle |
| `condor_rm` | Remove jobs from queue |
| `condor_history` | View completed jobs |
| `condor_tail` | View job output in real-time |

### Resource Allocation

HTCondor uses **ClassAds** (classified advertisements) to match jobs with available resources:

- **Job requirements**: What your job needs (CPUs, memory, disk, etc.)
- **Machine attributes**: What worker nodes provide
- **Automatic matching**: HTCondor finds the best fit

Example from `submit.sub`:
```ini
request_cpus = 1
request_memory = 2 GB
+flavour = "short"
requirements = Has_avx == true
```

---

## 📚 Resources

### Official Documentation

- **[PIC HTCondor Wiki](https://pwiki.pic.es/index.php?title=HTCondor)**: Comprehensive guide to HTCondor at PIC
- **[HTCondor User Manual](https://htcondor.readthedocs.io/en/v9_0/users-manual/index.html)**: Official HTCondor documentation
- **[PIC Website](https://www.pic.es/)**: Information about PIC infrastructure and services

### Research Groups

- **[QML-CVC Group](https://qml.cvc.uab.es/)**: Quantum Machine Learning at Computer Vision Center
- **[PIC Collaborations](https://www.pic.es/collaborations)**: Research projects supported by PIC

### Additional Learning

- [HTCondor Tutorial Examples](https://github.com/PortdInformacioCientifica/htcondor-tutorial): Official PIC tutorial repository
- [HTCondor User Guide Slides](https://docs.google.com/presentation/d/1-64fEcfLyxLzSpZH-tbV-SjMAc0CvMpWhE0I4oaDKkQ/edit?usp=sharing): Presentation slides from PIC

---

## 🔧 Configuration Details

### Job Flavors

PIC HTCondor supports different job flavors based on runtime:

- **`short`**: Jobs running < 6 hours
- **`medium`**: Jobs running 6-24 hours  
- **`long`**: Jobs running > 24 hours

### Common Requirements

- **`Has_avx == true`**: Require AVX instruction set support
- **`TARGET.Arch == "X86_64"`**: Specify architecture
- **`TARGET.OpSys == "LINUX"`**: Operating system requirement

### File Transfer Options

HTCondor can automatically transfer files:
- **Input files**: Scripts, data files, executables
- **Output files**: Results, logs, error reports
- **Transfer modes**: Local, remote, or both

---

## 🐛 Troubleshooting

### Jobs Stuck in Idle State

Use `condor_q -analyze` to diagnose:
```bash
condor_q -analyze <JobID>
```

Common issues:
- **Insufficient resources**: Requested CPUs/memory not available
- **Requirements not met**: Hardware constraints not satisfied
- **Fair-share limits**: Group quota exceeded

### Jobs Held

Check hold reason:
```bash
condor_q -hold
```

Common hold reasons:
- **Walltime exceeded**: Job ran longer than requested
- **Memory exceeded**: Job used more memory than requested
- **Too many restarts**: Check disk space and quotas

### Monitoring Job Progress

```bash
# Real-time output
condor_tail -f <JobID>

# SSH into running job (for debugging)
condor_ssh_to_job <JobID>
```

---

## 📊 Example Output

After successful execution, results are organized by parameter values:

```
cost_reconstruction/
├── [0.0 0.0]/
│   └── results.npy
├── [0.0 0.8975979]/
│   └── results.npy
└── ...
```

Each directory contains the quantum circuit samples for that parameter combination.

---

## 🤝 Contributing

This tutorial was created for the QML-CVC research group. For improvements or questions:

1. Review the [PIC HTCondor Wiki](https://pwiki.pic.es/index.php?title=HTCondor) for official guidelines
2. Check existing issues and discussions
3. Submit improvements via pull requests

---

## 📄 License

This tutorial is provided as-is for educational purposes. Please refer to PIC's usage policies and terms of service.

---

## 🙏 Acknowledgments

- **Port d'Informació Científica (PIC)** for providing HTCondor infrastructure
- **QML-CVC Research Group** for the use case and feedback
- **HTCondor Development Team** for excellent documentation and tools

---

<div align="center">

**Made with ❤️ for the quantum computing and HPC community**

[Report Issue](https://github.com/yourusername/tutorial-pic/issues) • [Request Feature](https://github.com/yourusername/tutorial-pic/issues)

</div>

