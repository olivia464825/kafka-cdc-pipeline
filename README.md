# BFS_DE_Kafka2026

Please follow the steps in the order below.

---

## Workflow Overview (Important)

### 1. Test Your Kafka Setup (Required)
Go to the `kafka_setup/` folder.

- Make sure Kafka, Zookeeper, and other required services can start successfully
- Verify all containers are running before moving on
- An optional demo Python app can be built using `app.py`, `requirements.txt`, and `Dockerfile`
- Resolve any setup issues before proceeding to later projects

<u>Important Docker commands:</u>
- Build from `Dockerfile`: `docker build -t <your_app_name> .`
- Build from `.yml`: `docker compose up -d`
- Stop and remove containers (including volumes): `docker compose down -v`
- View running containers: `docker compose ps`


---

### 2. Project 1: Kafka Practice (Optional)
Project 1 is ***optional*** and intended as a practice exercise.
- Instructions are provided in a PDF file under the `proj1/` folder
- Verify your result using the `expected_output.png` file
- You are encouraged to complete this project
- Project 1 is not part of the evaluation

---

### 3. Project 2: Kafka Application (Evaluation Project)
Project 2 is the ***main evaluation*** project.
- Your performance will be assessed based on Project 2
- Confirm that producers and consumers can send and receive messages
- A working Kafka setup is assumed at this stage

---

## Summary

| Step | Description | Required |
|------|------------|----------|
| Kafka setup test | Verify environment | Yes |
| Project 1 | Practice | Optional |
| Project 2 | Evaluation project | Yes |

---

Good luck!
