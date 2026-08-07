                                            
                                            -------------------------PLEASE RUN train.py BEFORE RUNNING THE CODE---------------
                                             

# DECORA 🛏️

**DECORA** is an AI-assisted bedroom interior design system that recommends suitable furniture and generates a 2D bedroom layout based on room dimensions, architectural elements, design style, budget, and furniture requirements.

The project combines **machine learning, database-driven furniture information, rule-based spatial constraints, a custom layout algorithm, FastAPI, and Matplotlib visualization** into an end-to-end bedroom design system.
> **Project:** DECORA  
> **Domain:** Artificial Intelligence / Machine Learning / Interior Design  
> **Current scope:** Bedroom decoration  
> **Project type:** Academic B.Tech Artificial Intelligence project

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Objectives](#-objectives)
- [Features](#-features)
- [How DECORA Works](#-how-decora-works)
- [System Architecture](#-system-architecture)
- [Machine Learning](#-machine-learning)
- [Layout Generation Algorithm](#-layout-generation-algorithm)
- [Layout Algorithm Components](#-layout-algorithm-components)
- [Constraint System](#-constraint-system)
- [Furniture Placement](#-furniture-placement)
- [Database](#-database)
- [Backend](#-backend)
- [Frontend](#-frontend)
- [Visualization](#-visualization)
- [Dataset](#-dataset)
- [Model Evaluation](#-model-evaluation)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running DECORA](#-running-decora)
- [Training the Model](#-training-the-model)
- [Example Workflow](#-example-workflow)
- [Security Before Publishing](#-security-before-publishing)
- [Current Limitations](#-current-limitations)
- [Future Improvements](#-future-improvements)
- [Team](#-team)
- [License](#-license)

---

# 📌 Overview

DECORA is designed to automate part of the bedroom interior-design process.

Instead of manually deciding:

- What furniture should be used?
- Will the furniture fit?
- Where should each item be placed?
- How should furniture interact with doors and windows?
- Does the selected style and budget match the furniture?

the user provides basic room information and DECORA processes it through a combination of machine learning and rule-based layout generation.

The system has two major intelligent components:

### 1. Furniture Recommendation

The machine-learning model predicts suitable furniture configurations from the available room and preference information.

### 2. Layout Generation

The layout engine takes the recommended furniture and determines suitable positions while applying room, furniture, door, window, and collision constraints.

In simple terms:

```text
Machine Learning
       ↓
"What furniture should be used?"
       ↓
Layout Algorithm
       ↓
"Where should the furniture be placed?"
       ↓
Final Bedroom Layout
```

---

# ❓ Problem Statement

Bedroom interior design requires consideration of several factors simultaneously:

- Room dimensions
- Furniture dimensions
- Door position
- Window position
- Available walking space
- Furniture compatibility
- Design style
- Budget

Manual planning can be time-consuming and difficult for users without interior-design experience.

DECORA attempts to provide a computational solution that combines machine-learning recommendations with deterministic spatial constraints to generate a usable bedroom layout.

---

# 🎯 Objectives

The main objectives of DECORA are:

- Build an AI-assisted bedroom furniture recommendation system.
- Recommend furniture based on room and user preferences.
- Consider room dimensions during recommendation and placement.
- Support different design styles.
- Support different budget categories.
- Consider door and window locations.
- Prevent furniture from leaving the room boundaries.
- Reduce furniture overlap.
- Apply furniture-specific placement rules.
- Store and retrieve furniture information through a database.
- Generate a visual 2D bedroom layout.
- Connect the complete system through a web-based backend.

---

# ✨ Features

- 🛏️ Bedroom-specific design
- 📐 Dimension-aware room layout
- 🪑 Furniture recommendation
- 🤖 Machine-learning-based prediction
- 🚪 Door-aware placement
- 🪟 Window-aware placement
- 📏 Furniture dimension handling
- 🚫 Furniture collision/overlap checking
- 📦 Constraint-based furniture placement
- 💰 Budget-based recommendation
- 🎨 Style-based recommendation
- 🗄️ SQLite database
- ⚡ FastAPI backend
- 🖥️ Web frontend
- 📊 Matplotlib visualization
- 📁 Generated-output management

---

# 🔄 How DECORA Works

The overall pipeline is:

```text
                   USER
                    │
                    ↓
          ┌───────────────────┐
          │   Room Information│
          │ Dimensions        │
          │ Door / Windows    │
          │ Style / Budget    │
          │ Required Furniture│
          └─────────┬─────────┘
                    ↓
          ┌───────────────────┐
          │   FastAPI Backend │
          └─────────┬─────────┘
                    ↓
          ┌───────────────────┐
          │ Room/Input Model  │
          └─────────┬─────────┘
                    ↓
       ┌────────────┴────────────┐
       ↓                         ↓
┌───────────────┐       ┌────────────────┐
│ ML Furniture  │       │ Furniture /    │
│ Recommendation│       │ Layout Data    │
└───────┬───────┘       └───────┬────────┘
        └────────────┬───────────┘
                     ↓
            ┌──────────────────┐
            │ Constraint Check │
            └────────┬─────────┘
                     ↓
            ┌──────────────────┐
            │  Layout Engine   │
            └────────┬─────────┘
                     ↓
            ┌──────────────────┐
            │  Visualization   │
            │    Matplotlib    │
            └────────┬─────────┘
                     ↓
              Final 2D Layout
```

---

# 🏗️ System Architecture

```text
┌──────────────────────────────────────────────────┐
│                    FRONTEND                      │
│                 HTML / CSS / JS                  │
└───────────────────────┬──────────────────────────┘
                        │
                        ↓
┌──────────────────────────────────────────────────┐
│                    FASTAPI                       │
│                 Backend / API                    │
└───────────────────────┬──────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
   ┌────────────┐ ┌────────────┐ ┌─────────────┐
   │ ML Model   │ │ Database   │ │ Input Model │
   │ Prediction │ │  SQLite    │ │ Validation  │
   └──────┬─────┘ └──────┬─────┘ └─────────────┘
          └───────────────┼───────────────┘
                          ↓
                ┌───────────────────┐
                │ Constraint System │
                └─────────┬─────────┘
                          ↓
                ┌───────────────────┐
                │   Layout Engine   │
                └─────────┬─────────┘
                          ↓
                ┌───────────────────┐
                │    Matplotlib     │
                │   Visualization   │
                └───────────────────┘
```

---

# 🤖 Machine Learning

DECORA uses a classification-based machine-learning pipeline for furniture recommendation.

## ML Pipeline

```text
Dataset
   ↓
Data Preprocessing
   ↓
Categorical Encoding
   ↓
Train / Test Split
   ↓
Random Forest Classifier
   ↓
Multi-Output Prediction
   ↓
Evaluation
   ↓
Model Serialization
```

## Main ML Components

### Random Forest Classifier

DECORA uses `RandomForestClassifier` for classification.

Random Forest combines predictions from multiple decision trees and can provide better generalization than relying on a single decision tree.

### MultiOutputClassifier

DECORA has multiple furniture-related outputs.

`MultiOutputClassifier` allows the classification system to handle several target variables.

Conceptually:

```text
                Room Input
                    │
                    ↓
            ┌──────────────┐
            │ Random Forest│
            └──────┬───────┘
                   ↓
       ┌───────────┼───────────┐
       ↓           ↓           ↓
      Bed        Table      Wardrobe
       ↓           ↓           ↓
             Furniture Set
```

### LabelEncoder

Categorical input/output values are converted into numerical representations using `LabelEncoder`.

### Joblib

The trained model can be serialized with Joblib so it can be loaded by the backend without retraining every time.

---

# 📐 Layout Generation Algorithm

The layout-generation system is a core part of DECORA.

The ML model determines:

> **What furniture should be recommended?**

The layout engine determines:

> **Where should the furniture be placed?**

This separation is important because a machine-learning prediction does not automatically guarantee that a furniture arrangement is physically valid.

---

## Layout Pipeline

```text
Room Dimensions
      ↓
Identify Door and Windows
      ↓
Determine Room Boundaries
      ↓
Obtain Recommended Furniture
      ↓
Retrieve Furniture Dimensions
      ↓
Select Placement Strategy
      ↓
Generate Candidate Position
      ↓
Check Room Boundary
      ↓
Check Furniture Collision
      ↓
Check Architectural Rules
      ↓
Check Furniture-Specific Rules
      ↓
Accept / Reject Position
      ↓
Generate Final Coordinates
      ↓
Matplotlib Visualization
```

---

# 🧩 Layout Algorithm Components

The current repository contains a dedicated:

```text
backend/
└── layout_algo/
```

package.

The package is separated into furniture-specific modules and the main layout engine.

```text
layout_algo/
├── __init__.py
├── bed.py
├── bookshelf.py
├── chair.py
├── dresser.py
├── engine.py
├── table.py
└── wardrobe.py
```

This organization allows different furniture types to have their own placement logic instead of putting every furniture rule into one large file.

### Furniture modules

The current layout package contains modules for:

- `bed.py`
- `bookshelf.py`
- `chair.py`
- `dresser.py`
- `table.py`
- `wardrobe.py`

### `engine.py`

The layout engine coordinates the furniture-placement process and applies the relevant placement logic.

This modular structure makes it easier to add new furniture types later.

---

# 📏 Room Representation

The room is treated as a 2D rectangular space.

Conceptually:

```text
                 Room Width
        <────────────────────────>

        ┌─────────────────────────┐
        │                         │
        │                         │
        │        ROOM             │
        │                         │
        │                         │
        └─────────────────────────┘
```

Furniture is represented using its position and dimensions.

A furniture rectangle can be described as:

```text
(x, y, width, height)
```

The layout system uses these values to determine whether the furniture can be placed at a particular location.

---

# 🪑 Furniture Placement

Furniture placement is performed according to the furniture type and available room space.

Each furniture item can have its own placement logic.

For example:

```text
Bed
 ↓
Find suitable room region
 ↓
Check boundaries
 ↓
Check collisions
 ↓
Accept position
```

Another furniture item may have different rules:

```text
Table
 ↓
Check available window
 ↓
Prefer placement in front of window
 ↓
Check boundaries
 ↓
Check collisions
 ↓
Accept position
```

This modular approach is why the layout algorithm is separated into individual furniture modules.

---

# 🚫 Boundary Checking

A furniture item must remain inside the room.

For a rectangular furniture item:

```text
left edge   >= room left boundary
right edge  <= room right boundary

bottom edge >= room bottom boundary
top edge    <= room top boundary
```

A candidate position that violates these conditions is rejected.

---

# 🚫 Furniture Collision Checking

The layout engine also checks whether furniture overlaps existing furniture.

Valid:

```text
┌────────────┐
│    BED     │
└────────────┘

                 ┌──────────┐
                 │  TABLE   │
                 └──────────┘
```

Invalid:

```text
┌────────────┐
│    BED     │
│       ┌────┼──────┐
│       │ TABLE     │
└───────┴───────────┘
```

The objective is to avoid placing furniture in an occupied region.

---

# 🚪 Door Constraints

The door is treated as an architectural element rather than ordinary furniture.

The current design uses:

- One door
- Fixed/corner-based door placement
- The door is not dynamically placed in the middle of a wall

The usable room area is therefore affected by the door location.

---

# 🪟 Window Constraints

Windows are also considered during layout generation.

The current project supports one or two windows depending on the input.

Window-wall information can be represented using wall directions such as:

```text
north
south
east
west
```

The layout algorithm can use this information for furniture-specific rules.

---

# 🪑 Study Table / Window Rule

One of the project's furniture-specific rules is the placement of the study table relative to a window.

When a suitable window is available, the table can be positioned in front of the corresponding window wall.

Conceptually:

```text
┌──────────────────────────────┐
│            WINDOW            │
│       ┌──────────────┐       │
│       │    TABLE     │       │
│       └──────────────┘       │
│                              │
│                              │
└──────────────────────────────┘
```

This demonstrates the use of semantic placement rules in addition to simple geometric collision checking.

---

# 🧮 Candidate Placement Strategy

The layout system can be understood as a constraint-based search process.

```text
Select Furniture
       ↓
Generate Candidate Position
       ↓
Inside Room?
   ┌───┴───┐
  YES      NO
   │        │
   ↓        └────→ Try another position
Overlap?
   ┌───┴───┐
  NO       YES
   │        │
   ↓        └────→ Try another position
Special Rule Satisfied?
       │
       ↓
   Accept Position
```

The accepted furniture coordinates are then passed to the visualization system.

---

# 🧠 Why DECORA Uses ML + Rules

A purely machine-learning-based approach is not sufficient for the entire problem.

Machine learning can learn patterns such as:

```text
Room + Style + Budget
          ↓
Recommended Furniture
```

But ML alone does not necessarily guarantee:

- Furniture stays inside the room.
- Furniture does not overlap.
- Door space remains usable.
- Window-related rules are respected.
- Furniture dimensions are physically compatible.

Therefore DECORA uses a hybrid approach:

```text
            USER INPUT
                │
                ↓
        ┌───────────────┐
        │ Machine       │
        │ Learning      │
        └───────┬───────┘
                │
        Furniture Choice
                ↓
        ┌───────────────┐
        │ Layout /      │
        │ Constraints   │
        └───────┬───────┘
                │
        Physical Placement
                ↓
          Final Layout
```

This is one of the key architectural ideas behind DECORA.

---

# 🗄️ Database

DECORA uses **SQLite** for storing project data.

The repository contains:

```text
backend/
├── database.py
└── decora.db
```

The database provides persistent storage that can be used by the application for furniture/layout-related information.

The layout and recommendation components can use database information such as furniture availability and dimensions when generating a room.

---

# 🔌 Backend

The backend is implemented with **FastAPI**.

The main backend files include:

```text
backend/
├── main.py
├── b_models.py
├── database.py
├── furniture_codes.py
├── furniture_recommender.py
├── layout_engine.py
├── visualization.py
└── test.png
```

### `main.py`

Acts as the main FastAPI application entry point.

### `b_models.py`

Contains backend data models used for structured input and validation.

### `database.py`

Handles database-related functionality.

### `furniture_codes.py`

Contains furniture-related codes/representations used by the application.

### `furniture_recommender.py`

Handles the furniture recommendation component.

### `layout_engine.py`

Connects the application to the layout-generation process.

### `visualization.py`

Handles visualization of generated room layouts.

---

# 🖥️ Frontend

The repository contains a dedicated:

```text
decora/
└── frontend/
```

directory for the web interface.

The frontend communicates with the backend to collect user input and display the generated result.

The frontend is implemented using web technologies such as:

- HTML
- CSS
- JavaScript

The exact frontend files are kept inside the `frontend` directory.

---

# 📊 Visualization

DECORA uses **Matplotlib** to visualize the generated bedroom layout.

The visualization represents:

- Room boundaries
- Doors
- Windows
- Furniture
- Furniture positions
- Furniture dimensions

The result is a 2D representation of the room.

Generated visual outputs can be stored in:

```text
backend/
└── generated_outputs/
```

The repository also contains visualization-related development files such as:

```text
backend/
└── visualization.py
```

---

# 📁 Project Structure

The current project organization is:

```text
MAIN_DECORA_CODE/
│
├── .vscode/
│
├── 3.11.9_decora_environment/
│
├── decora/
│   │
│   ├── backend/
│   │   │
│   │   ├── __pycache__/
│   │   ├── data/
│   │   ├── generated_outputs/
│   │   │
│   │   ├── layout_algo/
│   │   │   ├── __init__.py
│   │   │   ├── bed.py
│   │   │   ├── bookshelf.py
│   │   │   ├── chair.py
│   │   │   ├── dresser.py
│   │   │   ├── engine.py
│   │   │   ├── table.py
│   │   │   └── wardrobe.py
│   │   │
│   │   ├── ml_model/
│   │   ├── __init__.py
│   │   ├── .env
│   │   ├── b_models.py
│   │   ├── database.py
│   │   ├── decora.db
│   │   ├── furniture_codes.py
│   │   ├── furniture_recommender.py
│   │   ├── layout_engine.py
│   │   ├── main.py
│   │   ├── test.png
│   │   └── visualization.py
│   │
│   ├── frontend/
│   │
│   └── training/
│
├── decora_env/
├── lyt_plot/
├── Required_things/
└── .gitignore
```

> The structure above reflects the current development organization. Files such as `__pycache__`, virtual environments, `.env`, and other local development artifacts should normally **not** be committed to a public GitHub repository.

---

# 📚 Dataset

The current DECORA development dataset contains approximately:

**2,000 bedroom-layout records**

The dataset contains information related to:

- Room dimensions
- Bedroom style
- Budget
- Furniture configurations
- Furniture-related attributes

The furniture fields represent furniture type information rather than simple binary flags.

Missing furniture values indicate that the corresponding furniture is not placed.

> **Important:** The current dataset is synthetic/generated data and is primarily intended for project development and experimentation.

---

# 🧪 Training and Testing

The current machine-learning pipeline uses:

```text
80% → Training
20% → Testing
```

The testing portion is kept separate from the training data to evaluate model performance on unseen examples.

---

# 📈 Model Evaluation

The current development version achieved approximately:

## **61.4% Test Accuracy**

This is a development-stage result rather than a claim of production-level accuracy.

Performance is influenced by:

- Dataset size
- Synthetic data quality
- Feature selection
- Class distribution
- Label quality
- Furniture categories
- Model hyperparameters
- Complexity of the recommendation problem

A larger and more realistic dataset would be expected to provide better opportunities for improving the model.

---

# 🛠️ Technologies Used

### Programming

- Python

### Machine Learning

- Scikit-learn
- Pandas
- Joblib

### Backend

- FastAPI
- Pydantic

### Database

- SQLite

### Visualization

- Matplotlib

### Frontend

- HTML
- CSS
- JavaScript

### Development

- VS Code
- Git
- GitHub
- Python virtual environments

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/DECORA.git
cd DECORA
```

## 2. Create a Python Environment

DECORA was developed using Python 3.11.

```bash
python3.11 -m venv decora_env
```

## 3. Activate the Environment

### Linux / macOS

```bash
source decora_env/bin/activate
```

### Windows

```bash
decora_env\Scripts\activate
```

## 4. Install Dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

If the dependency file has not yet been added, install the project's required Python packages according to the final environment configuration.

---

# ▶️ Running DECORA

From the project directory, start the FastAPI application using the final backend entry point.

For a typical FastAPI setup:

```bash
uvicorn backend.main:app --reload
```

If the project is executed from inside the `decora` directory:

```bash
cd decora
uvicorn backend.main:app --reload
```

The exact command may be adjusted depending on the final Python import path.

---

# 🧠 Training the Model

The repository contains a dedicated:

```text
decora/
└── training/
```

directory.

The training scripts can be used to:

1. Load the dataset.
2. Preprocess the data.
3. Encode categorical features.
4. Split the data.
5. Train the Random Forest model.
6. Perform multi-output prediction.
7. Evaluate the model.
8. Save the trained model.

A typical training command is:

```bash
python training/train.py
```

> Update the command to the exact training script name in the final repository.

---

# 🔁 Example User Workflow

A typical DECORA request can follow this process:

### Step 1 — User Input

The user provides information such as:

```text
Room Length
Room Width
Door
Windows
Style
Budget
Required Furniture
Room Type
```

### Step 2 — Backend Validation

FastAPI receives the request and validates the structured input.

### Step 3 — Furniture Recommendation

The recommendation model predicts a suitable furniture configuration.

### Step 4 — Furniture Information

The system obtains furniture information such as dimensions and type.

### Step 5 — Layout Generation

The layout engine starts placing the recommended furniture.

### Step 6 — Constraint Checking

The system checks:

- Room boundaries
- Door position
- Window position
- Furniture overlap
- Furniture-specific rules

### Step 7 — Coordinate Generation

Each accepted furniture item receives a position in the room.

### Step 8 — Visualization

Matplotlib renders the final 2D room layout.

### Step 9 — Output

The generated output can be stored in the project's output directory and returned/displayed to the user.

---

# 🔒 Security Before Publishing to GitHub

Before making DECORA public, **do not upload secrets or local development environments**.

The current VS Code project contains:

```text
.env
```

A `.env` file may contain sensitive information such as API keys or credentials.

### Do NOT commit:

```text
.env
3.11.9_decora_environment/
decora_env/
__pycache__/
*.pyc
```

Your `.gitignore` should cover these files/directories.

For example:

```gitignore
# Python
__pycache__/
*.py[cod]

# Virtual environments
venv/
.venv/
decora_env/
3.11.9_decora_environment/

# Environment variables
.env
.env.*

# IDE
.vscode/

# Logs
*.log
```

Also review:

- Database contents
- Generated outputs
- Personal files
- Credentials
- Large model files
- Large datasets

before pushing the repository.

---

# ⚠️ Current Limitations

### 1. Synthetic Dataset

The current dataset is generated/synthetic and may not fully represent real-world bedroom layouts.

### 2. Model Accuracy

The current model achieves approximately 61.4% test accuracy.

### 3. Limited Furniture Categories

The current layout algorithm contains a defined set of furniture modules:

- Bed
- Bookshelf
- Chair
- Dresser
- Table
- Wardrobe

More furniture types can be added later.

### 4. 2D Visualization

The current system generates 2D layouts rather than full 3D interior scenes.

### 5. Rule-Based Layout

The current layout engine relies primarily on geometric and rule-based constraints rather than a global optimization algorithm.

### 6. Real-World Validation

The generated layout is a computational recommendation and does not replace professional architectural or interior-design planning.

---

# 🚀 Future Improvements

## Dataset

- Larger real-world interior datasets
- Real furniture dimensions
- More diverse room configurations
- Better class balancing
- Human-designed layouts
- Better labels

## Machine Learning

- Hyperparameter optimization
- Feature engineering
- Cross-validation
- Improved multi-output models
- More advanced recommendation methods
- Neural-network-based recommendation
- Better evaluation metrics

## Layout Algorithm

- More furniture modules
- Furniture rotation
- Better collision detection
- Walking-space optimization
- Door-opening clearance
- Window-access constraints
- Global layout optimization
- Constraint-satisfaction algorithms
- Genetic algorithms
- More sophisticated spatial reasoning

## Visualization

- Interactive 2D layout
- 3D room visualization
- Realistic furniture models
- Furniture textures
- Lighting
- Color customization

## Generative AI

A future version could combine the generated geometric layout with an image-generation model to create a realistic visual render of the designed bedroom.

---

# 🧠 Core Design Philosophy

DECORA is designed as a **hybrid AI + rule-based system**.

Machine learning handles the data-driven part:

```text
"What furniture is suitable?"
```

The layout engine handles the deterministic spatial part:

```text
"Can this furniture physically fit here?"
```

The two systems work together:

```text
                    DECORA
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
       ML Recommendation    Layout Algorithm
             │                   │
       Furniture Choice     Spatial Placement
             │                   │
             └─────────┬─────────┘
                       ↓
                 Final Layout
```

This architecture allows DECORA to combine the strengths of machine learning with explicit spatial constraints.

---

# 🎓 Academic Purpose

DECORA was developed to explore practical applications of Artificial Intelligence and software engineering.

The project demonstrates the integration of:

- Machine Learning
- Classification
- Multi-output prediction
- Data preprocessing
- Label encoding
- Model evaluation
- Constraint-based reasoning
- Spatial layout generation
- Database integration
- REST API development
- Backend/frontend integration
- 2D visualization
- Modular software architecture

The project demonstrates that a practical AI application can combine learned patterns with deterministic rules rather than relying on a single technique.

---

# 📸 Screenshots

Add screenshots of the completed application to make the repository easier to understand.

Recommended screenshots:

```text
screenshots/
├── homepage.png
├── input-form.png
├── recommendation.png
├── generated-layout.png
└── final-result.png
```

Example Markdown:

```markdown
![DECORA Interface](screenshots/homepage.png)

![Generated Bedroom Layout](screenshots/generated-layout.png)
```

---

# 👥 Team

## Team DECORA

Add the final team members and roles here:

```text
Member 1 — Machine Learning
Member 2 — Backend Development
Member 3 — Frontend Development
Member 4 — Database / Integration
```

Replace the placeholders with the actual team information before publishing.

---

# 📄 License

This project was developed primarily for academic and educational purposes.

If the repository is intended to be open source, an appropriate open-source license can be added.

For example:

```text
MIT License
```

The final license should reflect the team's intended usage and distribution terms.

---

# 🙏 Acknowledgements

DECORA was built using the open-source Python ecosystem.

The project makes use of technologies and libraries including:

- Python
- Scikit-learn
- Pandas
- Joblib
- FastAPI
- Pydantic
- Matplotlib
- SQLite

---

# ⭐ DECORA

```text
                 USER INPUT
                     │
                     ↓
             ROOM INFORMATION
                     │
                     ↓
           ┌──────────────────┐
           │ ML RECOMMENDATION│
           └────────┬─────────┘
                    ↓
             FURNITURE SET
                    │
                    ↓
           ┌──────────────────┐
           │ LAYOUT ALGORITHM │
           └────────┬─────────┘
                    ↓
          CONSTRAINT CHECKING
                    │
                    ↓
             FURNITURE POSITIONS
                    │
                    ↓
             MATPLOTLIB OUTPUT
                    │
                    ↓
              FINAL BEDROOM
                 LAYOUT
```

**DECORA — From room information to an AI-assisted, constraint-aware bedroom layout.**
