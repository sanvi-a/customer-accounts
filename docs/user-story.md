# User Story Template

Use this template for every GitHub issue (`.github/ISSUE_TEMPLATE/user-story.md`).

```
**As a** [role]
**I need** [function]
**So that** [benefit]

### Details and Assumptions
* [document what you know]

### Acceptance Criteria
Given [some context]
When [certain action is taken]
Then [the outcome of the action is observed]
```

# Product Backlog (issue titles used in the Kanban board)

Create one issue per story, using these exact titles. Column flow: New Issues -> Ice Box -> Product Backlog -> Sprint Backlog -> In Progress -> Done.

| # | Issue title | Label | Planned sprint |
|---|---|---|---|
| 1 | Setting up the development environment | technical debt | Sprint 1 |
| 2 | Create an account in the service | enhancement | Sprint 1 |
| 3 | Read an account from the service | enhancement | Sprint 1 |
| 4 | List all accounts in the service | enhancement | Sprint 2 |
| 5 | Update an account in the service | enhancement | Sprint 2 |
| 6 | Delete an account from the service | enhancement | Sprint 2 |
| 7 | Need the ability to automate continuous integration checks | technical debt | Sprint 2 |
| 8 | Need to add security headers and CORS policies | technical debt | Sprint 3 |
| 9 | Containerize your microservice using Docker | technical debt | Sprint 3 |
| 10 | Deploy your Docker image to Kubernetes | technical debt | Sprint 3 |
| 11 | Create a CD pipeline to automate deployment to Kubernetes | technical debt | Sprint 3 |

The sprint split is only a suggestion. Follow the sprint assignments your lab instructions give you, since the form expects two new stories in Sprint 2 and three in Sprint 3.

# Example stories

### Setting up the development environment
**As a** developer
**I need** a configured dev environment (setup.cfg with nosetests, coverage, flake8, pylint)
**So that** I can write and test code consistently

### Details and Assumptions
* Python virtual environment with `requirements.txt` installed

### Acceptance Criteria
```
Given a fresh clone of the repository
When I run nosetests, flake8 and pylint
Then they execute using the settings in setup.cfg
```

### Read an account from the service
**As a** customer service rep
**I need** to retrieve one account by id
**So that** I can view that customer's details

### Acceptance Criteria
```
Given an account exists
When I GET /accounts/{id}
Then I receive that account with a 200 status
```

### Need to add security headers and CORS policies
**As a** security engineer
**I need** HTTP security headers and a CORS policy
**So that** the service resists common web attacks

### Acceptance Criteria
```
Given the service is running
When I request any endpoint
Then the response includes X-Frame-Options, X-Content-Type-Options,
     Content-Security-Policy and Referrer-Policy
And cross-origin requests receive Access-Control-Allow-Origin
```
