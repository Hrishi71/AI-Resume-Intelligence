
import re

# Skills organized by category

SKILL_DATABASE = {

    # 1. Programming Languages
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript",
        "C", "C++", "C#", "Go", "Golang", "Rust",
        "Kotlin", "Swift", "PHP", "Ruby", "Scala",
        "R", "Dart", "Perl", "Bash", "Shell",
        "PowerShell", "SQL", "Cypher"
    ],

    # 2. Python Ecosystem
    "Python Ecosystem": [
        "NumPy", "Pandas", "Polars", "Matplotlib",
        "Seaborn", "SciPy", "Pydantic", "Requests",
        "BeautifulSoup", "Scrapy", "Pillow",
        "OpenCV", "Pytest", "Unittest",
        "Virtualenv", "Poetry", "Pipenv",
        "Jupyter Notebook", "IPython"
    ],

    # 3. AI and Machine Learning
    "AI and Machine Learning": [
        "Machine Learning", "Deep Learning",
        "Supervised Learning", "Unsupervised Learning",
        "Reinforcement Learning", "Transfer Learning",
        "Feature Engineering", "Model Training",
        "Model Evaluation", "Model Deployment",
        "Scikit-learn", "TensorFlow", "PyTorch",
        "Keras", "XGBoost", "LightGBM", "CatBoost",
        "Natural Language Processing",
        "Computer Vision", "Neural Networks",
        "Convolutional Neural Networks",
        "Recurrent Neural Networks",
        "Transformers", "Hugging Face",
        "Hugging Face Transformers", "ONNX"
    ],

    # 4. Generative AI and LLM Engineering
    "Generative AI and LLMs": [
        "Generative AI", "Large Language Models",
        "LLM Engineering", "Prompt Engineering",
        "Structured Prompting", "Context Engineering",
        "Retrieval-Augmented Generation",
        "Semantic Search", "Vector Search",
        "Hybrid Search", "Reranking",
        "Embedding Models", "Text Embeddings",
        "Vector Databases", "Chunking",
        "Document Processing", "Hallucination Reduction",
        "LLM Evaluation", "LLM Fine-tuning",
        "Fine-tuning", "PEFT", "LoRA", "QLoRA",
        "Quantization", "Inference Optimization",
        "Function Calling", "Tool Calling",
        "Structured Outputs", "JSON Schema",
        "Multimodal AI", "Vision Language Models",
        "AI Agents", "Agentic AI",
        "Agentic Workflows", "Multi-Agent Systems",
        "Guardrails", "AI Safety",
        "Model Context Protocol"
    ],

    # 5. LLM Frameworks and Platforms
    "LLM Frameworks and Platforms": [
        "LangChain", "LangGraph", "LlamaIndex",
        "Haystack", "Semantic Kernel",
        "AutoGen", "CrewAI", "DSPy",
        "OpenAI", "OpenAI API", "Azure OpenAI",
        "Anthropic", "Claude API",
        "Google Gemini", "Gemini API",
        "Hugging Face", "Ollama",
        "vLLM", "LM Studio", "LiteLLM",
        "Instructor", "Guidance"
    ],

    # 6. Backend Development
    "Backend Development": [
        "Django", "Django REST Framework",
        "FastAPI", "Flask", "Falcon",
        "Starlette", "Sanic",
        "Node.js", "Express.js", "NestJS",
        "Next.js", "Spring Boot", "Spring Framework",
        "ASP.NET Core", "Laravel", "Ruby on Rails",
        "REST", "RESTful APIs", "GraphQL",
        "gRPC", "WebSockets", "Webhooks",
        "API Development", "API Design",
        "API Integration", "Microservices",
        "Monolithic Architecture",
        "Asynchronous Programming",
        "Asynchronous Tasks", "Concurrency",
        "Multithreading", "Multiprocessing",
        "Background Jobs", "Task Queues",
        "Authentication", "Authorization",
        "JWT", "OAuth 2.0", "OpenID Connect",
        "RBAC", "Rate Limiting", "Caching"
    ],

    # 7. Frontend Development
    "Frontend Development": [
        "HTML", "HTML5", "CSS", "CSS3",
        "JavaScript", "TypeScript",
        "React", "Next.js", "Angular", "Vue.js",
        "Svelte", "Vite", "Webpack",
        "Tailwind CSS", "Bootstrap",
        "Material UI", "Shadcn UI",
        "Redux", "Redux Toolkit", "Zustand",
        "React Query", "TanStack Query",
        "Framer Motion", "Responsive Design",
        "Progressive Web Apps",
        "Single Page Applications"
    ],

    # 8. Databases and Storage
    "Databases and Storage": [
        "PostgreSQL", "MySQL", "SQLite",
        "Microsoft SQL Server", "Oracle Database",
        "MongoDB", "Redis", "Cassandra",
        "DynamoDB", "Elasticsearch", "OpenSearch",
        "Neo4j", "ChromaDB", "Pinecone",
        "Weaviate", "Milvus", "Qdrant",
        "FAISS", "Supabase", "Firebase",
        "Database Design", "Database Indexing",
        "Database Optimization", "Query Optimization",
        "Database Migrations", "ORM",
        "SQLAlchemy", "Django ORM",
        "Prisma", "Drizzle ORM",
        "Graph Database", "Graph Query Language",
        "Cypher", "Data Modeling",
        "ACID Transactions", "Database Replication",
        "Database Sharding"
    ],

    # 9. Data Engineering and Streaming
    "Data Engineering": [
        "Apache Kafka", "Apache Spark",
        "Apache Airflow", "Apache Flink",
        "RabbitMQ", "Celery", "Pandas",
        "ETL", "ELT", "Data Pipelines",
        "Data Warehousing", "Data Lakes",
        "Data Processing", "Stream Processing",
        "Batch Processing", "Data Transformation",
        "Snowflake", "Databricks", "dbt",
        "Apache Hadoop", "Delta Lake"
    ],

    # 10. Cloud Platforms
    "Cloud and Infrastructure": [
        "AWS", "Microsoft Azure", "Google Cloud",
        "Amazon EC2", "Amazon S3",
        "AWS Lambda", "Amazon RDS",
        "Amazon ECS", "Amazon EKS",
        "Azure Functions", "Azure Blob Storage",
        "Azure Kubernetes Service",
        "Google Cloud Run", "Google Cloud Storage",
        "Serverless Computing", "Cloud Computing",
        "Cloud Architecture", "Infrastructure as Code"
    ],

    # 11. DevOps and Deployment
    "DevOps and Deployment": [
        "Git", "GitHub", "GitLab", "Bitbucket",
        "Docker", "Docker Compose",
        "Kubernetes", "Helm", "Minikube",
        "Jenkins", "GitHub Actions",
        "GitLab CI", "CI/CD",
        "Continuous Integration",
        "Continuous Delivery",
        "Continuous Deployment",
        "Terraform", "Ansible",
        "Prometheus", "Grafana",
        "Nginx", "Apache",
        "Linux", "Ubuntu", "Bash Scripting",
        "Deployment Automation",
        "Containerization", "Orchestration"
    ],

    # 12. Software Engineering and Architecture
    "Software Engineering": [
        "Data Structures", "Algorithms",
        "Object-Oriented Programming",
        "Functional Programming",
        "Design Patterns", "SOLID Principles",
        "Clean Code", "Refactoring",
        "System Design", "Low-Level Design",
        "High-Level Design",
        "Distributed Systems",
        "Event-Driven Architecture",
        "Event Sourcing", "CQRS",
        "Domain-Driven Design",
        "Scalability", "High Availability",
        "Fault Tolerance", "Load Balancing",
        "Horizontal Scaling", "Vertical Scaling",
        "Caching Strategies", "Message Queues",
        "Concurrency Control",
        "Idempotency", "Circuit Breaker",
        "Exponential Backoff"
    ],

    # 13. Testing and Quality Assurance
    "Testing and Quality Assurance": [
        "Unit Testing", "Integration Testing",
        "End-to-End Testing", "Functional Testing",
        "Regression Testing", "Load Testing",
        "Performance Testing", "Stress Testing",
        "Security Testing", "Test Automation",
        "Pytest", "Jest", "Mocha",
        "Playwright", "Cypress", "Selenium",
        "Postman", "Newman",
        "Test-Driven Development",
        "Behavior-Driven Development",
        "Mocking", "Code Coverage"
    ],

    # 14. Security
    "Security": [
        "Cybersecurity", "Application Security",
        "Web Security", "API Security",
        "OWASP", "OWASP Top 10",
        "JWT Authentication", "OAuth",
        "Role-Based Access Control",
        "Encryption", "Hashing",
        "TLS", "SSL", "HTTPS",
        "Secure Coding", "Input Validation",
        "SQL Injection Prevention",
        "Cross-Site Scripting",
        "Cross-Site Request Forgery",
        "Secrets Management",
        "Post-Quantum Cryptography",
        "Cryptographic Agility",
        "Vulnerability Assessment"
    ],

    # 15. Monitoring and Observability
    "Monitoring and Observability": [
        "Logging", "Monitoring", "Observability",
        "Distributed Tracing", "OpenTelemetry",
        "Prometheus", "Grafana",
        "ELK Stack", "Datadog",
        "New Relic", "Application Performance Monitoring",
        "Error Tracking", "Metrics Collection"
    ]
}



# Alternative names for technical skills

SKILL_ALIASES = {

    # Programming languages
    "JavaScript": ["JS", "ECMAScript", "ES6"],
    "TypeScript": ["TS"],
    "C++": ["CPP"],
    "C#": ["C Sharp"],
    "Golang": ["Go"],

    # Python ecosystem
    "Scikit-learn": ["Sklearn", "Scikit Learn"],
    "NumPy": ["Numpy"],
    "Pytest": ["PyTest"],

    # AI and Machine Learning
    "Natural Language Processing": ["NLP"],
    "Computer Vision": ["CV"],
    "Large Language Models": ["LLM", "LLMs"],
    "Generative AI": ["GenAI", "Gen AI"],
    "Retrieval-Augmented Generation": [
        "RAG",
        "Retrieval Augmented Generation"
    ],
    "Prompt Engineering": ["Prompt Design"],
    "Embedding Models": ["Embedding Model"],
    "Vector Databases": ["Vector DB", "Vector DBs"],
    "AI Agents": ["Intelligent Agents"],
    "Multimodal AI": ["Multimodal"],
    "Model Context Protocol": ["MCP"],

    # LLM frameworks
    "LangChain": ["Lang Chain"],
    "LangGraph": ["Lang Graph"],
    "LlamaIndex": ["Llama Index"],
    "Azure OpenAI": ["Azure OpenAI Service"],
    "OpenAI API": ["OpenAI APIs"],
    "Google Gemini": ["Gemini"],
    "Hugging Face": ["HuggingFace"],

    # Backend
    "Django REST Framework": ["DRF", "Django REST"],
    "FastAPI": ["Fast API"],
    "Node.js": ["NodeJS", "Node"],
    "Express.js": ["Express", "ExpressJS"],
    "RESTful APIs": ["REST API", "REST APIs"],
    "GraphQL": ["Graph QL"],
    "gRPC": ["Google Remote Procedure Call"],
    "JSON Web Token": ["JWT"],
    "Role-Based Access Control": ["RBAC"],
    "OAuth 2.0": ["OAuth2", "OAuth"],
    "Asynchronous Programming": ["Async Programming"],
    "Microservices": ["Microservice Architecture"],

    # Frontend
    "React": ["React.js", "ReactJS"],
    "Vue.js": ["Vue", "VueJS"],
    "Next.js": ["NextJS"],
    "Angular": ["AngularJS"],
    "Tailwind CSS": ["Tailwind"],
    "Redux Toolkit": ["RTK"],
    "Responsive Design": ["Mobile Responsive Design"],

    # Databases
    "PostgreSQL": ["Postgres", "Postgre"],
    "MongoDB": ["Mongo DB"],
    "Microsoft SQL Server": ["MS SQL", "MSSQL"],
    "Neo4j": ["Neo 4j"],
    "ChromaDB": ["Chroma"],
    "Elasticsearch": ["Elastic Search"],
    "Graph Database": ["Graph DB", "Graph Databases"],
    "Database Indexing": ["Indexing"],
    "Database Optimization": ["DB Optimization"],

    # Data engineering
    "Apache Kafka": ["Kafka"],
    "Apache Spark": ["Spark"],
    "Apache Airflow": ["Airflow"],
    "Apache Flink": ["Flink"],
    "RabbitMQ": ["Rabbit MQ"],
    "ETL": ["Extract Transform Load"],
    "ELT": ["Extract Load Transform"],

    # Cloud
    "Microsoft Azure": ["Azure"],
    "Google Cloud": ["GCP", "Google Cloud Platform"],
    "Amazon Web Services": ["AWS"],

    # DevOps
    "GitHub Actions": ["GitHub Action"],
    "GitLab CI": ["GitLab CI/CD"],
    "Continuous Integration": ["CI"],
    "Continuous Delivery": ["CD"],
    "Continuous Deployment": ["CD"],
    "Infrastructure as Code": ["IaC"],
    "Docker Compose": ["Docker-Compose"],

    # Software engineering
    "Object-Oriented Programming": ["OOP"],
    "Data Structures and Algorithms": ["DSA"],
    "Low-Level Design": ["LLD"],
    "High-Level Design": ["HLD"],
    "Domain-Driven Design": ["DDD"],
    "Event-Driven Architecture": ["EDA"],
    "Exponential Backoff": ["Exponential Retry"],

    # Testing
    "End-to-End Testing": ["E2E Testing", "E2E"],
    "Test-Driven Development": ["TDD"],
    "Behavior-Driven Development": ["BDD"],
    "Integration Testing": ["Integration Tests"],
    "Unit Testing": ["Unit Tests"],

    # Security
    "Cross-Site Scripting": ["XSS"],
    "Cross-Site Request Forgery": ["CSRF"],
    "Transport Layer Security": ["TLS"],
    "Post-Quantum Cryptography": ["PQC"],
    "Role-Based Access Control": ["RBAC"],

    # Monitoring
    "Application Performance Monitoring": ["APM"],
    "Distributed Tracing": ["Tracing"],
    "OpenTelemetry": ["OTel"]
}






def matches_skill(text, skill):
    escaped_skill = re.escape(skill)

    pattern = (
        r"(?<!\w)"
        + escaped_skill
        + r"(?!\w)"
    )

    for match in re.finditer(pattern, text, re.IGNORECASE):

        # Prevent Java from matching inside JavaScript
        if skill.lower() == "java":
            remaining = text[match.end():]
            if remaining.lower().startswith("script"):
                continue

        # Prevent C from matching inside C++ or C#
        if skill.lower() == "c":
            remaining = text[match.end():]
            if remaining.startswith(("+", "#")):
                continue

        # Prevent JavaScript from matching inside React.js
        if skill.lower() == "javascript":
            preceding = text[:match.start()]
            if preceding.lower().endswith("react."):
                continue
                # Prevent JS alias from matching .js file/framework suffixes
        if skill.lower() == "js":
            preceding = text[:match.start()]
            if preceding.endswith("."):
                continue
            
        return True

    return False




def find_skill_match(text, skill):

    terms = [skill] + SKILL_ALIASES.get(skill, [])

    for term in terms:

        if matches_skill(text, term):
            return term

    return None


def extract_skills(resume_text):
    """
    Extract unique canonical skill names
    while preserving database order.
    """

    detected_skills = []

    for category, skills in SKILL_DATABASE.items():

        for skill in skills:

            match = find_skill_match(resume_text, skill)

            if match and skill not in detected_skills:
                detected_skills.append(skill)

    return detected_skills



def extract_skills_by_category(resume_text):
    """
    Extract unique canonical skills and organize them
    by their primary category.
    """

    results = {}

    for category, skills in SKILL_DATABASE.items():

        detected = []

        for skill in skills:

            match = find_skill_match(resume_text, skill)

            if match and skill not in detected:
                detected.append(skill)

        if detected:
            results[category] = detected

    return results
