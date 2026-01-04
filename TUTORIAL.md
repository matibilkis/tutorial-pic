# HTCondor Tutorial: Step-by-Step Guide

This document provides a detailed walkthrough of using HTCondor at PIC for quantum machine learning research.

## Table of Contents

1. [Introduction to HTCondor](#introduction-to-htcondor)
2. [Setting Up Your Environment](#setting-up-your-environment)
3. [Understanding the Submission File](#understanding-the-submission-file)
4. [Running Your First Job](#running-your-first-job)
5. [Monitoring and Debugging](#monitoring-and-debugging)
6. [Best Practices](#best-practices)

---

## Introduction to HTCondor

### What is HTCondor?

HTCondor is a specialized workload management system for compute-intensive jobs. Unlike traditional batch systems, HTCondor uses a **matchmaking** approach where:

- **Jobs advertise** their requirements (CPUs, memory, disk, etc.)
- **Worker nodes advertise** their capabilities
- **HTCondor matches** jobs to suitable resources automatically

### Key Concepts

#### ClassAds (Classified Advertisements)
Both jobs and machines are described using ClassAds - a language for expressing attributes and requirements.

**Job ClassAd Example:**
```ini
request_cpus = 4
request_memory = 8 GB
requirements = Has_avx == true
```

**Machine ClassAd Example:**
```ini
Cpus = 8
Memory = 32 GB
Has_avx = true
```

#### Fair-Share Scheduling
PIC implements fair-share scheduling to ensure equitable resource distribution:
- Each research group has a quota (e.g., 9% for ATLAS)
- Jobs below quota get higher priority
- Jobs above quota get lower priority

#### Job Flavors
Jobs are categorized by expected runtime:
- **Short**: < 6 hours
- **Medium**: 6-24 hours
- **Long**: > 24 hours

---

## Setting Up Your Environment

### 1. Access PIC Infrastructure

Ensure you have:
- Valid PIC account credentials
- SSH access to PIC login nodes
- Appropriate group membership (QML-CVC)

### 2. Project Structure

Organize your project as follows:

```
tutorial-pic/
├── main.py                    # Your computational script
├── HPC/
│   ├── submit.sub             # HTCondor submission file
│   ├── subash.sh              # Job execution script
│   └── params.txt             # Parameter combinations
└── jobs/                      # Output directory (created automatically)
    ├── outs/                  # Standard output
    ├── errs/                  # Standard error
    └── logs/                  # HTCondor logs
```

### 3. Python Environment

Set up a virtual environment with required packages:

```bash
# Create virtual environment
python3 -m venv ~/qvenv

# Activate environment
source ~/qvenv/bin/activate

# Install dependencies
pip install pennylane numpy
```

---

## Understanding the Submission File

Let's break down `HPC/submit.sub` line by line:

### Executable and Arguments

```ini
executable = HPC/subash.sh
args = $(p1) $(p2) $(seed)
```

- `executable`: The script that runs on worker nodes
- `args`: Command-line arguments (variables substituted from queue)

### Output Files

```ini
output = ../jobs/outs/$(p1)_$(p2).out
error = ../jobs/errs/$(p1)_$(p2).err
log = ../jobs/logs/$(p1)_$(p2).log
```

- `output`: Standard output (print statements, results)
- `error`: Standard error (error messages, warnings)
- `log`: HTCondor job lifecycle events

### Resource Requirements

```ini
request_cpus = 1
request_memory = 2 GB
+flavour = "short"
requirements = Has_avx == true
```

- `request_cpus`: Number of CPU cores needed
- `request_memory`: Memory requirement
- `+flavour`: Job runtime category
- `requirements`: Hardware/software constraints

### Queue Statement

```ini
queue p1 p2 from /path/to/params.txt
```

Creates one job per line in `params.txt`. Each line should contain two space-separated values for `p1` and `p2`.

---

## Running Your First Job

### Step 1: Generate Parameters

Use the Jupyter notebook to create parameter combinations:

```python
import numpy as np

N = 8
p1 = np.linspace(0., 2*np.pi, N)
p2 = np.linspace(0., 2*np.pi, N)

with open('HPC/params.txt', 'w') as outf:
    for x in p1:
        for y in p2:
            outf.write("{} {}\n".format(x, y))
```

This creates 64 parameter combinations (8×8 grid).

### Step 2: Prepare Output Directories

```bash
mkdir -p jobs/outs jobs/errs jobs/logs
```

### Step 3: Submit Jobs

```bash
condor_submit HPC/submit.sub
```

Expected output:
```
Submitting job(s).
1 job(s) submitted to cluster 12345.
```

### Step 4: Monitor Jobs

```bash
# View all your jobs
condor_q

# View specific job details
condor_q -nobatch <JobID>

# Analyze why jobs are idle
condor_q -analyze
```

---

## Monitoring and Debugging

### Job States

HTCondor jobs can be in several states:

- **I (Idle)**: Waiting for resources
- **R (Running)**: Currently executing
- **H (Held)**: Blocked (check hold reason)
- **C (Completed)**: Finished successfully
- **X (Removed)**: Cancelled by user

### Useful Commands

#### View Job Queue
```bash
condor_q
condor_q -nobatch    # Detailed view
condor_q -hold       # Show held jobs only
```

#### Analyze Job Status
```bash
condor_q -analyze <JobID>        # Basic analysis
condor_q -better-analyze <JobID> # Detailed analysis
```

#### View Job Output
```bash
# Real-time output streaming
condor_tail -f <JobID>

# View output files directly
cat jobs/outs/0.0_0.0.out
cat jobs/errs/0.0_0.0.err
```

#### Debug Running Jobs
```bash
# SSH into running job
condor_ssh_to_job <JobID>

# View job history
condor_history
condor_history <JobID>  # Specific job
```

### Common Issues

#### Jobs Stuck in Idle

**Problem**: Jobs remain idle for extended periods.

**Diagnosis**:
```bash
condor_q -analyze <JobID>
```

**Common causes**:
- Insufficient resources (requested too many CPUs/memory)
- Requirements not met (e.g., no AVX support available)
- Fair-share quota exceeded

**Solutions**:
- Reduce resource requests
- Relax requirements
- Wait for quota to reset

#### Jobs Held

**Problem**: Jobs are held and won't run.

**Diagnosis**:
```bash
condor_q -hold
```

**Common hold reasons**:
- `Walltime exceeded`: Job ran longer than requested
- `Memory exceeded`: Job used more memory than requested
- `Too many restarts`: Check disk space and quotas

**Solutions**:
- Increase `+flavour` for longer jobs
- Increase `request_memory`
- Check disk quotas: `quota -s`

#### Jobs Failing

**Problem**: Jobs complete but exit with errors.

**Diagnosis**:
```bash
cat jobs/errs/<job>.err
cat jobs/logs/<job>.log
```

**Common causes**:
- Missing dependencies (Python packages, files)
- Incorrect file paths
- Environment not set up correctly

**Solutions**:
- Verify virtual environment activation in `subash.sh`
- Check file paths are absolute or relative to working directory
- Test script locally before submitting

---

## Best Practices

### 1. Resource Allocation

**Request only what you need:**
```ini
# Good: Appropriate for single-threaded Python script
request_cpus = 1
request_memory = 2 GB

# Bad: Over-requesting wastes resources
request_cpus = 8
request_memory = 64 GB
```

**Choose appropriate flavor:**
- Use `short` for quick tests (< 6h)
- Use `medium` for typical computations (6-24h)
- Use `long` only when necessary (> 24h)

### 2. File Management

**Use absolute paths:**
```python
# Good
save_dir = "/data/cvcqml/common/user/results/"

# Bad (relative paths can break)
save_dir = "../results/"
```

**Organize outputs:**
- Use descriptive filenames with parameters
- Create separate directories per experiment
- Clean up old results regularly

### 3. Reproducibility

**Set random seeds:**
```python
np.random.seed(seed)  # Use seed from command line
```

**Log parameters:**
```python
print(f"Parameters: p1={p1}, p2={p2}, seed={seed}")
```

**Version control:**
- Commit code before submitting jobs
- Tag releases for important experiments

### 4. Testing

**Test locally first:**
```bash
# Run script manually
python main.py --p1 0.0 --p2 0.0 --seed 42

# Test submission script
bash HPC/subash.sh 0.0 0.0 42
```

**Submit small batches:**
- Start with 1-2 jobs to verify setup
- Gradually increase to full parameter sweep

### 5. Monitoring

**Set up notifications:**
```ini
# In submit.sub
notification = Complete
notify_user = your.email@example.com
```

**Regular checks:**
- Monitor job queue periodically
- Check for held/failed jobs
- Verify outputs are being generated

### 6. Efficiency

**Batch similar jobs:**
- Use queue statements for parameter sweeps
- Group jobs with similar resource needs

**Optimize I/O:**
- Minimize file transfers
- Use efficient data formats (NumPy arrays, HDF5)
- Avoid writing many small files

---

## Advanced Topics

### DAGMan Workflows

For complex workflows with dependencies, use DAGMan:

```ini
# workflow.dag
JOB A jobA.sub
JOB B jobB.sub
JOB C jobC.sub
PARENT A B CHILD C
```

### Container Support

HTCondor supports containers for reproducible environments:

```ini
# Use Apptainer/Singularity
+WantContainer = true
container_image = "myimage.sif"
```

### Interactive Jobs

For debugging, submit interactive jobs:

```bash
condor_submit -i
```

---

## Additional Resources

- [PIC HTCondor Wiki](https://pwiki.pic.es/index.php?title=HTCondor): Official PIC documentation
- [HTCondor Manual](https://htcondor.readthedocs.io/): Complete HTCondor documentation
- [PIC Tutorial Examples](https://github.com/PortdInformacioCientifica/htcondor-tutorial): More examples

---

## Getting Help

If you encounter issues:

1. Check the [PIC HTCondor Wiki](https://pwiki.pic.es/index.php?title=HTCondor)
2. Use `condor_q -analyze` to diagnose problems
3. Contact PIC support: contact@pic.es
4. Consult with your research group

---

**Happy Computing! 🚀**

