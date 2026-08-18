# Product brief — Stage 0

## Product promise

An authorized member of an organization submits a document to a named, versioned processing
pipeline. DurableFlow makes the job's state and progress visible and eventually produces one
verifiable artifact or one explicit, recoverable terminal failure.

## Primary user journey

1. A user selects or uploads a document.
2. The user chooses a pipeline version.
3. The system validates the submission and creates one logical job.
4. The system processes the job while preserving visible progress.
5. The user can inspect status and provenance.
6. The user downloads the result or understands how to recover from failure.

Stage 1 proves only a small vertical slice: submit text, process it synchronously, and retrieve
the in-memory result.

## Initial domain vocabulary

- **Tenant:** an organization-level security and data boundary.
- **User:** an authenticated actor belonging to a tenant.
- **Document:** metadata describing an input object and its integrity.
- **Pipeline version:** an immutable definition of processing steps and processor versions.
- **Job:** one logical request to process one document with one pipeline version.
- **Attempt:** one execution of a job or step; retries create more attempts, not more logical jobs.
- **Artifact:** an immutable output with input, processor, attempt, and checksum provenance.
- **Job event:** a durable, ordered statement about a job's progress or state change.

Only `Job` and its deterministic result exist in code during Stage 1. The other concepts are
requirements, not permission to build infrastructure early.

## Product-level success

- The correct tenant can submit and inspect its jobs.
- An accepted job is never silently lost.
- Duplicate requests do not create duplicate logical work.
- Repeated execution cannot create multiple externally visible final artifacts.
- Results identify the input and processor versions that produced them.
- A disconnected client can recover the authoritative state.

Stage 1 deliberately violates durability and tenant isolation so those problems can be observed
before their mechanisms are introduced.

## Non-goals for the first stage

- production availability;
- persistent storage;
- user accounts or tenant enforcement;
- large or binary file uploads;
- asynchronous work;
- AI-generated output;
- caching;
- distributed services;
- cloud deployment; or
- Kubernetes.

