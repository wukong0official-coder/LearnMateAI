
import json
import sqlite3
from pathlib import Path

import streamlit as st

# =========================================================
# LEARNMATE AI - PERSONALIZED LEARNING PLATFORM
# =========================================================

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "learnmate.db"

st.set_page_config(
    page_title="LearnMate AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# COURSE CONTENT - INTRODUCTION TO INTERMEDIATE LEVEL
# =========================================================

COURSES = {
    "Engineering Mathematics M1": {
        "Introduction to Functions and Limits": {
            "definition": "A function maps each permitted input to exactly one output. A limit describes the value a function approaches as its input approaches a particular point.",
            "example": "For f(x) = 2x + 1, f(3) = 7. Also, lim(x→2) (x + 1) = 3.",
            "question": "If f(x) = 2x + 1, what is f(4)?",
            "options": ["7", "8", "9", "10"],
            "answer": "9",
            "explanation": "Substitute x = 4: f(4) = 2(4) + 1 = 9.",
        },
        "Differential Equations": {
            "definition": "Differential equations describe relationships between a function and its derivatives. They are used to model changing quantities in engineering.",
            "example": "Solve dy/dx = 2x. Integrating both sides gives y = x² + C.",
            "question": "What is the general solution of dy/dx = 3x²?",
            "options": ["y = 3x + C", "y = x³ + C", "y = 6x + C", "y = x² + C"],
            "answer": "y = x³ + C",
            "explanation": "Integrating 3x² with respect to x gives x³ + C.",
        },
        "Laplace Transforms": {
            "definition": "The Laplace transform converts a function of time into a function of a complex variable s. It simplifies many differential equation problems.",
            "example": "The Laplace transform of 1 is 1/s, for s > 0.",
            "question": "What is the Laplace transform of t?",
            "options": ["1/s", "1/s²", "s", "1/(s+1)"],
            "answer": "1/s²",
            "explanation": "Using L{tⁿ} = n!/sⁿ⁺¹, L{t} = 1/s².",
        },
        "Multiple Integrals": {
            "definition": "Multiple integrals extend integration to functions of two or more variables and can calculate areas, volumes and mass distributions.",
            "example": "The double integral of 1 over 0 ≤ x ≤ 1 and 0 ≤ y ≤ 2 equals the rectangle's area, 2.",
            "question": "A double integral of 1 over a rectangular region represents its:",
            "options": ["Perimeter", "Area", "Slope", "Derivative"],
            "answer": "Area",
            "explanation": "Integrating 1 over a two-dimensional region gives the region's area.",
        },
    },
    "Engineering Mathematics M2": {
        "Introduction to Matrices": {
            "definition": "A matrix is a rectangular arrangement of numbers in rows and columns. Matrices are used to represent systems of equations and engineering data.",
            "example": "The matrix [[1, 2], [3, 4]] has 2 rows and 2 columns, so its order is 2 × 2.",
            "question": "What is the order of a matrix with 3 rows and 2 columns?",
            "options": ["2 × 3", "3 × 2", "3 × 3", "2 × 2"],
            "answer": "3 × 2",
            "explanation": "Matrix order is written as rows × columns.",
        },
        "Eigenvalues and Eigenvectors": {
            "definition": "An eigenvector of a square matrix A is a nonzero vector v satisfying Av = λv, where λ is its eigenvalue.",
            "example": "For A = [[2, 0], [0, 3]], the eigenvalues are 2 and 3.",
            "question": "What equation is used to find eigenvalues of A?",
            "options": ["det(A) = 1", "det(A - λI) = 0", "A + λI = 0", "A² = I"],
            "answer": "det(A - λI) = 0",
            "explanation": "Eigenvalues are roots of the characteristic equation det(A - λI) = 0.",
        },
        "Fourier Series": {
            "definition": "Fourier series represent suitable periodic functions as combinations of sine and cosine functions.",
            "example": "A periodic signal can be approximated using a fundamental frequency and its harmonics.",
            "question": "Which functions form the standard real Fourier series?",
            "options": ["Only polynomials", "Sine and cosine", "Only exponentials", "Logarithms only"],
            "answer": "Sine and cosine",
            "explanation": "A real Fourier series uses sine and cosine terms, together with a constant term.",
        },
        "Vector Calculus": {
            "definition": "Vector calculus studies scalar and vector fields using operations such as gradient, divergence and curl.",
            "example": "For f(x,y) = x² + y², the gradient is (2x, 2y).",
            "question": "The gradient of a scalar field produces a:",
            "options": ["Scalar only", "Vector field", "Matrix determinant", "Constant always"],
            "answer": "Vector field",
            "explanation": "The gradient collects the partial derivatives into a vector.",
        },
    },
    "Engineering Mathematics M3": {
        "Introduction to Probability": {
            "definition": "Probability measures how likely an event is to occur. Its value ranges from 0 (impossible) to 1 (certain).",
            "example": "For a fair six-sided die, the probability of rolling a 4 is 1/6.",
            "question": "What is the probability of getting heads when tossing a fair coin?",
            "options": ["0", "1/4", "1/2", "1"],
            "answer": "1/2",
            "explanation": "There are two equally likely outcomes, heads and tails, so P(heads) = 1/2.",
        },
        "Probability Distributions": {
            "definition": "Probability distributions describe the possible values of a random variable and their probabilities.",
            "example": "A fair coin has probability 1/2 for heads on each independent toss.",
            "question": "For a binomial distribution, which condition is important?",
            "options": ["Trials have fixed success probability", "Every outcome is continuous", "There are no trials", "The mean must be zero"],
            "answer": "Trials have fixed success probability",
            "explanation": "A binomial model uses a fixed number of independent trials with the same success probability.",
        },
        "Correlation and Regression": {
            "definition": "Correlation measures the strength and direction of association between variables. Regression models a relationship to estimate one variable from another.",
            "example": "A positive correlation may occur between hours studied and exam marks, although correlation alone does not prove causation.",
            "question": "What does a correlation coefficient near -1 indicate?",
            "options": ["Strong positive linear association", "Strong negative linear association", "No linear association", "Perfect independence always"],
            "answer": "Strong negative linear association",
            "explanation": "A coefficient near -1 indicates a strong negative linear relationship.",
        },
        "Numerical Methods": {
            "definition": "Numerical methods approximate mathematical solutions when exact analytical solutions are difficult to obtain.",
            "example": "Newton-Raphson updates an estimate using x(n+1) = x(n) - f(x(n))/f'(x(n)).",
            "question": "Newton-Raphson is primarily used to approximate:",
            "options": ["Roots of equations", "Matrix dimensions", "Units of measurement", "Random samples only"],
            "answer": "Roots of equations",
            "explanation": "The method iteratively improves an estimate of a root of f(x) = 0.",
        },
    },
    "Engineering Mathematics M4": {
        "Introduction to Complex Numbers": {
            "definition": "A complex number has the form a + bi, where a is the real part, b is the imaginary coefficient, and i² = -1.",
            "example": "In z = 3 + 2i, the real part is 3 and the imaginary coefficient is 2.",
            "question": "What is the real part of 5 - 7i?",
            "options": ["-7", "5", "7i", "5i"],
            "answer": "5",
            "explanation": "In a + bi, the real part is a. Here a = 5.",
        },
        "Complex Analysis": {
            "definition": "Complex analysis studies functions of complex variables and concepts such as analyticity, contour integration and residues.",
            "example": "For z = x + iy, its complex conjugate is x - iy.",
            "question": "What is the conjugate of z = 3 + 4i?",
            "options": ["3 - 4i", "-3 + 4i", "4 + 3i", "-3 - 4i"],
            "answer": "3 - 4i",
            "explanation": "The conjugate changes the sign of the imaginary part.",
        },
        "Z-Transforms": {
            "definition": "The Z-transform represents discrete-time sequences in the complex z-domain and is widely used in digital signal processing.",
            "example": "For a causal sequence x[n] = aⁿ, its Z-transform is z/(z-a) in its region of convergence.",
            "question": "The Z-transform is especially useful for analysing:",
            "options": ["Discrete-time systems", "Only geometric shapes", "Continuous areas only", "Chemical symbols"],
            "answer": "Discrete-time systems",
            "explanation": "It converts discrete-time difference equations into algebraic expressions in the z-domain.",
        },
        "Partial Differential Equations": {
            "definition": "Partial differential equations involve unknown functions of multiple variables and their partial derivatives.",
            "example": "The heat equation in one spatial dimension is ∂u/∂t = α ∂²u/∂x².",
            "question": "The standard heat equation models:",
            "options": ["Heat diffusion", "Matrix inversion", "Only projectile motion", "Prime numbers"],
            "answer": "Heat diffusion",
            "explanation": "The heat equation describes how temperature evolves through diffusion.",
        },
    },
    "C Programming": {
        "Introduction to C and Variables": {
            "definition": "C is a procedural programming language. Variables are named storage locations whose values can be used and changed while a program runs.",
            "example": "int age = 20; declares an integer variable named age and initializes it to 20.",
            "question": "Which C type is commonly used to store a whole number?",
            "options": ["int", "float only", "char only", "void"],
            "answer": "int",
            "explanation": "The int type is used for integer values.",
        },
        "Pointers and Arrays": {
            "definition": "A pointer stores a memory address. Arrays store elements of the same type in contiguous memory locations.",
            "example": "int x = 10; int *p = &x; makes p point to x.",
            "question": "What does the & operator do in int *p = &x?",
            "options": ["Gets the address of x", "Multiplies x", "Deletes x", "Gets the size of x"],
            "answer": "Gets the address of x",
            "explanation": "In this context, & is the address-of operator.",
        },
        "Structures and Functions": {
            "definition": "Structures group related variables of different types. Functions divide a program into reusable units of logic.",
            "example": "struct Student { int id; float mark; }; groups a student's ID and mark.",
            "question": "Why is a structure useful in C?",
            "options": ["It groups related data", "It replaces all loops", "It guarantees no errors", "It only stores characters"],
            "answer": "It groups related data",
            "explanation": "A structure lets related fields of different types be stored together.",
        },
        "Dynamic Memory Allocation": {
            "definition": "Dynamic memory allocation reserves memory during program execution using functions such as malloc, calloc, realloc and free.",
            "example": "int *p = malloc(5 * sizeof(int)); reserves memory for five integers when allocation succeeds.",
            "question": "Which function releases memory allocated dynamically in C?",
            "options": ["remove()", "free()", "close()", "clear()"],
            "answer": "free()",
            "explanation": "free() releases a dynamically allocated memory block.",
        },
    },
    "C++ Programming": {
        "Introduction to C++ and Functions": {
            "definition": "C++ is a general-purpose programming language that supports procedural and object-oriented programming. A function is a reusable block of code.",
            "example": "int add(int a, int b) { return a + b; } defines a function that returns the sum.",
            "question": "What is the main purpose of a function?",
            "options": ["Reuse a block of code", "Automatically install libraries", "Store only images", "Stop a program permanently"],
            "answer": "Reuse a block of code",
            "explanation": "Functions make programs modular and allow logic to be reused.",
        },
        "Classes and Inheritance": {
            "definition": "Classes combine data and member functions. Inheritance allows a derived class to reuse and extend a base class.",
            "example": "class Dog : public Animal {} declares Dog as publicly derived from Animal.",
            "question": "What is a major purpose of inheritance?",
            "options": ["Reuse and extend class behaviour", "Automatically remove all bugs", "Replace every function", "Prevent object creation"],
            "answer": "Reuse and extend class behaviour",
            "explanation": "Inheritance supports reuse and specialisation of existing classes.",
        },
        "Polymorphism": {
            "definition": "Polymorphism allows a common interface to represent different behaviours, using mechanisms such as function overloading and virtual functions.",
            "example": "A virtual draw() function can behave differently for Circle and Rectangle objects.",
            "question": "Which feature enables runtime polymorphism in C++?",
            "options": ["Virtual functions", "Preprocessor comments", "Integer literals", "Header guards alone"],
            "answer": "Virtual functions",
            "explanation": "Virtual functions support dynamic dispatch through base-class interfaces.",
        },
        "STL and Templates": {
            "definition": "Templates support generic programming, while the Standard Template Library provides reusable containers, algorithms and iterators.",
            "example": "std::vector<int> values = {1, 2, 3}; creates a resizable collection of integers.",
            "question": "Which STL container grows dynamically?",
            "options": ["std::vector", "int", "char", "bool"],
            "answer": "std::vector",
            "explanation": "std::vector is a dynamically resizable sequence container.",
        },
    },
    "Python Programming": {
        "Introduction to Python and Data Types": {
            "definition": "Python is a high-level programming language with readable syntax. Common data types include int, float, str, and bool.",
            "example": "name = 'Maya' stores text; score = 95 stores an integer.",
            "question": "Which Python type represents text?",
            "options": ["int", "str", "bool", "float"],
            "answer": "str",
            "explanation": "The str type represents strings, which are sequences of text characters.",
        },
        "Functions and Lambda Expressions": {
            "definition": "Functions package reusable operations. Lambda expressions create small anonymous functions.",
            "example": "square = lambda x: x * x; square(4) returns 16.",
            "question": "What does lambda x: x + 3 return when called with 5?",
            "options": ["2", "8", "15", "53"],
            "answer": "8",
            "explanation": "Substitute x = 5: 5 + 3 = 8.",
        },
        "Object-Oriented Programming": {
            "definition": "Object-oriented programming organises code around objects that combine state and behaviour.",
            "example": "A class Car can define attributes such as colour and methods such as drive().",
            "question": "In a Python instance method, what does self usually refer to?",
            "options": ["The current instance", "The parent folder", "A global constant", "The Python interpreter"],
            "answer": "The current instance",
            "explanation": "self conventionally refers to the object on which the instance method is called.",
        },
        "File Handling and Exceptions": {
            "definition": "File handling reads and writes stored data. Exception handling lets programs respond to runtime errors.",
            "example": "with open('data.txt') as file: content = file.read() reads a text file and manages its closure.",
            "question": "Why is a with statement useful when opening files?",
            "options": ["It manages resource cleanup", "It encrypts every file", "It prevents all errors", "It creates a database automatically"],
            "answer": "It manages resource cleanup",
            "explanation": "A with statement uses a context manager to close the file appropriately.",
        },
    },
    "Java Programming": {
        "Introduction to Java and Variables": {
            "definition": "Java is a class-based programming language. Variables store values, and each variable has a declared or inferred type depending on the context.",
            "example": "int score = 90; declares an integer variable named score with value 90.",
            "question": "Which Java type is commonly used to store a whole number?",
            "options": ["int", "boolean", "String only", "void"],
            "answer": "int",
            "explanation": "The int type stores integer values.",
        },
        "Inheritance and Interfaces": {
            "definition": "Inheritance allows a class to extend another class. Interfaces define contracts that implementing classes must fulfil.",
            "example": "class Dog implements Runnable must implement the required run() method unless it is abstract.",
            "question": "What does a Java interface primarily define?",
            "options": ["A contract of behaviour", "A database file", "A memory address", "An operating system"],
            "answer": "A contract of behaviour",
            "explanation": "An interface specifies behaviour that implementing classes agree to provide.",
        },
        "Collections Framework": {
            "definition": "Java collections provide data structures such as lists, sets, queues and maps for organising objects.",
            "example": "List<String> names = new ArrayList<>(); creates a resizable list of strings.",
            "question": "Which Java collection stores key-value pairs?",
            "options": ["Map", "List", "Queue only", "String"],
            "answer": "Map",
            "explanation": "A Map associates keys with values.",
        },
        "Exception Handling and Streams": {
            "definition": "Exception handling manages errors through try, catch and finally. Streams provide a way to process sequences of data.",
            "example": "numbers.stream().filter(n -> n > 5) selects elements greater than five.",
            "question": "Which Java stream operation filters elements using a condition?",
            "options": ["filter()", "collectOnly()", "catch()", "finally()"],
            "answer": "filter()",
            "explanation": "filter() retains elements that satisfy its predicate.",
        },
    },
}

# =========================================================
# DATABASE
# =========================================================

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student TEXT NOT NULL,
                course TEXT NOT NULL,
                topic TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                mistakes TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS custom_topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student TEXT NOT NULL,
                course TEXT NOT NULL,
                topic TEXT NOT NULL,
                definition TEXT NOT NULL,
                example TEXT NOT NULL
            )
        """)


def save_result(student, course, topic, score, total, mistakes):
    with sqlite3.connect(DB_PATH) as con:
        con.execute(
            """
            INSERT INTO results
            (student, course, topic, score, total, difficulty, mistakes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student, course, topic, score, total,
                "Intermediate", json.dumps(mistakes),
            ),
        )


def load_results(student):
    with sqlite3.connect(DB_PATH) as con:
        return con.execute(
            """
            SELECT course, topic, score, total, created_at, mistakes
            FROM results
            WHERE student = ?
            ORDER BY id DESC
            """,
            (student,),
        ).fetchall()


def load_custom_topics(student):
    with sqlite3.connect(DB_PATH) as con:
        return con.execute(
            """
            SELECT course, topic, definition, example
            FROM custom_topics WHERE student = ?
            """,
            (student,),
        ).fetchall()


init_db()

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "student": "",
    "logged_in": False,
    "page": "Dashboard",
    "course": "",
    "topic": "",
    "quiz_started": False,
    "quiz_finished": False,
    "quiz_saved": False,
    "ai_key": "",
    "chat": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def configured_api_key():
    """Read the local Streamlit secret first, then the session-only key."""
    try:
        built_in_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        built_in_key = ""
    return (built_in_key or st.session_state.get("ai_key", "") or "").strip()


def tutor_response(prompt, context=""):
    """Try online OpenAI first; keep core tutoring useful without API credits."""
    api_key = configured_api_key()
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": (
                        "You are LearnMate AI, a patient tutor. Teach from introductory to intermediate level. "
                        "Use the learner's quiz answers and mistakes to infer misconceptions; never ask the learner "
                        "to label their difficulty. Give a clear explanation, a worked example, and one next step."
                    )},
                    {"role": "user", "content": f"Context: {context}\nLearner request: {prompt}"},
                ],
            )
            return completion.choices[0].message.content or "I could not generate a response."
        except Exception as exc:
            error = str(exc).lower()
            if "429" in error or "no credits" in error or "insufficient_quota" in error:
                reason = "Online AI is temporarily unavailable because the API account has no remaining credits."
            else:
                reason = "Online AI is unavailable right now (check the key, internet, billing, and model access)."
    else:
        reason = "Online AI is not configured, so LearnMate is using its built-in tutor fallback."

    # Rule-based fallback, using actual lesson content and the learner's result context.
    return (
        f"**Built-in tutor mode**\n\n{reason}\n\n"
        f"**What to focus on**\n{context or 'Review the lesson definition and example, then try a related practice question.'}\n\n"
        f"**Your request:** {prompt}\n\n"
        "**Study strategy:** identify the key rule, work through one small example step by step, and then solve a similar question without looking at the explanation. "
        "This fallback works without API credits; online generative answers resume when API access is restored."
    )

# =========================================================
# =========================================================
# DARK THEME
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root { color-scheme: dark; }
html, body, [class*="css"], [data-testid="stAppViewContainer"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #080b12 !important;
    color: #f4f7fb !important;
}
[data-testid="stAppViewContainer"] { background: #080b12 !important; }
[data-testid="stHeader"] { background: rgba(8,11,18,.94) !important; }
[data-testid="stSidebar"] { background: #0d1320 !important; border-right: 1px solid #202a3b; }
[data-testid="stSidebar"] * { color: #f4f7fb !important; }
.block-container { padding-top: 1.8rem; max-width: 1500px; }
.stMarkdown, .stMarkdown p, .stMarkdown li, label, h1, h2, h3, h4, p, span,
[data-testid="stWidgetLabel"], [data-testid="stMarkdownContainer"] { color: #f4f7fb; }
.hero { padding: 30px; border-radius: 20px; color: #fff; background: linear-gradient(120deg,#172554,#312e81 65%,#164e63); border: 1px solid #334155; margin-bottom: 24px; }
.hero h1, .hero p { color: #fff !important; }
.course-card, .metric-card, .login-panel, .quiz-assistant-card {
    background: #111827 !important; color: #f4f7fb !important;
    border: 1px solid #273449 !important; border-radius: 16px; padding: 20px;
    box-shadow: 0 8px 26px rgba(0,0,0,.22);
}
.metric-number { font-size: 30px; font-weight: 800; color: #93c5fd !important; }
.login-title { text-align:center; font-size:clamp(2.5rem,6vw,4.5rem); line-height:1.1; font-weight:800; letter-spacing:-.045em; color:#a5b4fc !important; margin:0 0 1.6rem 0; }
.login-panel { max-width:560px; margin:8vh auto 0 auto; padding:2rem 2.25rem; }
.stButton > button, [data-testid="stFormSubmitButton"] button { border-radius:10px; min-height:42px; font-weight:650; background:#1d4ed8; color:#fff; border:1px solid #3b82f6; }
.stButton > button:hover { background:#2563eb; border-color:#60a5fa; color:#fff; }
input, textarea, [data-baseweb="select"] > div, [data-baseweb="input"] > div { background:#0b1220 !important; color:#f8fafc !important; border-color:#334155 !important; }
[data-testid="stChatMessage"] { background:#111827; border:1px solid #273449; border-radius:12px; }
[data-testid="stAlert"] { background:#111827; color:#f8fafc; }
hr { border-color:#273449 !important; }
small, .stCaption, [data-testid="stCaptionContainer"] { color:#a8b4c7 !important; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# COURSE AND TOPIC HELPERS
# =========================================================

def all_courses():
    result = dict(COURSES)

    for course, topic, definition, example in load_custom_topics(
        st.session_state.student
    ):
        result.setdefault(course, {})
        result[course][topic] = {
            "definition": definition,
            "example": example,
            "question": None,
            "options": [],
            "answer": None,
            "explanation": "This is a custom topic. Ask the AI tutor for practice questions.",
        }

    return result


def go(page):
    st.session_state.page = page
    st.rerun()


def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.quiz_finished = False
    st.session_state.quiz_saved = False
    st.session_state.quiz_index = 0
    st.session_state.quiz_answers = []
    st.session_state.pop("quiz_tutor_answer", None)
    st.session_state.pop("quiz_result", None)


def build_topic_question_bank(course, topic, lesson, course_map):
    """Create a larger offline quiz for every topic using its lesson content.

    Each topic gets its original knowledge question plus additional concept,
    example, explanation, and recall questions. This works without an API key.
    """
    bank = []

    # Gather other lesson content for realistic, course-wide distractors.
    other_lessons = []
    for other_course, topic_map in course_map.items():
        for other_topic, other_lesson in topic_map.items():
            if (other_course, other_topic) != (course, topic):
                if other_lesson.get("definition") and other_lesson.get("example"):
                    other_lessons.append({
                        "course": other_course,
                        "topic": other_topic,
                        "definition": other_lesson["definition"],
                        "example": other_lesson["example"],
                        "explanation": other_lesson.get("explanation", ""),
                    })

    def add_question(kind, question, correct, distractors, explanation):
        """Add one multiple-choice item with four unique options."""
        if not correct:
            return
        candidates = [str(correct)] + [str(x) for x in distractors if x and str(x) != str(correct)]
        options = list(dict.fromkeys(candidates))
        if len(options) < 4:
            for fallback in [
                f"This is not the main idea of {topic}.",
                f"This does not match the lesson example for {topic}.",
                f"This is unrelated to the key concept in {topic}.",
                f"This describes a different topic from {topic}.",
            ]:
                if fallback not in options:
                    options.append(fallback)
                if len(options) >= 4:
                    break
        options = options[:4]
        import random
        rng = random.Random(f"{course}|{topic}|{len(bank)}|{kind}")
        rng.shuffle(options)
        bank.append({
            "kind": kind,
            "question": question,
            "options": options,
            "answer": str(correct),
            "explanation": explanation or f"Review the lesson on {topic}: {lesson.get('definition', '')}",
        })

    # 1. Original topic-specific question supplied with the lesson.
    if lesson.get("question") and lesson.get("options") and lesson.get("answer"):
        add_question(
            "practice", lesson["question"], lesson["answer"], lesson["options"],
            lesson.get("explanation", "Review the lesson example and key definition."),
        )

    other_definitions = [x["definition"] for x in other_lessons]
    other_examples = [x["example"] for x in other_lessons]
    other_explanations = [x["explanation"] for x in other_lessons if x["explanation"]]

    definition = lesson.get("definition", "")
    example = lesson.get("example", "")
    explanation = lesson.get("explanation", "")

    # 2. Concept understanding.
    if definition:
        add_question(
            "concept", f"Which statement best describes {topic}?", definition,
            other_definitions,
            f"{definition}",
        )

    # 3. Recognise the lesson's worked example.
    if example:
        add_question(
            "example", f"Which example is presented in the lesson for {topic}?", example,
            other_examples,
            f"The lesson uses this example to illustrate {topic}: {example}",
        )

    # 4. Identify the main takeaway from the explanation.
    if explanation:
        add_question(
            "reasoning", f"Which explanation matches the key idea taught in {topic}?",
            explanation, other_explanations + other_definitions,
            explanation,
        )

    # 6. Apply the example to recognise the topic it belongs to.
    if example:
        topic_distractors = [f"{x['topic']}: {x['example']}" for x in other_lessons]
        add_question(
            "application", f"A learner is practising {topic}. Which lesson example should they use?",
            f"{topic}: {example}", topic_distractors,
            f"Use the example associated with {topic}: {example}",
        )

    # 7. Match the topic with its course area, reinforcing course navigation.
    if course and topic:
        course_distractors = [x for x in course_map.keys() if x != course]
        add_question(
            "course_match", f"Which course contains the topic '{topic}'?", course,
            course_distractors,
            f"'{topic}' is included in {course} in LearnMate AI.",
        )


    return bank


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:
    st.markdown(
        '<div class="login-panel">'
        '<div class="login-title">LearnMate AI</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    _, middle, _ = st.columns([1, 1.15, 1])
    with middle:
        name = st.text_input(
            "Enter your name",
            key="login_name",
            placeholder="Your name",
            label_visibility="visible",
        )
        if st.button("Start Learning →", use_container_width=True, type="primary"):
            if name.strip():
                st.session_state.student = name.strip()
                st.session_state.logged_in = True
                go("Dashboard")
            else:
                st.warning("Please enter your name.")

    st.stop()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("## 🎓 LearnMate AI")
    st.caption(f"Learning profile: {st.session_state.student}")
    st.divider()

    pages = [
        ("🏠", "Dashboard"),
        ("📚", "Learn"),
        ("📝", "Take Quiz"),
        ("🤖", "AI Assistant"),
        ("📈", "My Progress"),
        ("➕", "Add Course"),
        ("🔑", "AI Settings"),
    ]

    for emoji, page in pages:
        if st.button(
            f"{emoji}  {page}",
            use_container_width=True,
            key=f"nav_{page}",
        ):
            go(page)

    st.divider()
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.student = ""
        st.session_state.chat = []
        st.session_state.ai_key = ""
        reset_quiz()
        go("Dashboard")

courses = all_courses()
results = load_results(st.session_state.student)

# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "Dashboard":
    st.markdown(f"""
    <div class="hero">
        <h1>Welcome back, {st.session_state.student}! 👋</h1>
        <p>Your personal space to learn, practise and track progress.</p>
    </div>
    """, unsafe_allow_html=True)

    completed = len(results)
    accuracy = (
        round(100 * sum(r[2] for r in results) / sum(r[3] for r in results))
        if results and sum(r[3] for r in results) else 0
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f'<div class="metric-card">Quiz attempts'
            f'<div class="metric-number">{completed}</div></div>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f'<div class="metric-card">Overall accuracy'
            f'<div class="metric-number">{accuracy}%</div></div>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f'<div class="metric-card">Available courses'
            f'<div class="metric-number">{len(courses)}</div></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Explore your courses")

    cols = st.columns(3)
    for i, (course, topics) in enumerate(courses.items()):
        with cols[i % 3]:
            st.markdown(
                f'<div class="course-card"><h3>{course}</h3>'
                f'<p>{len(topics)} learning topics</p>'
                f'<p>Introduction to intermediate</p></div>',
                unsafe_allow_html=True,
            )
            if st.button("Study this course", key=f"course_{course}"):
                st.session_state.course = course
                st.session_state.topic = ""
                reset_quiz()
                go("Learn")

    st.subheader("Recent learning activity")
    if results:
        for course, topic, score, total, date, mistakes in results[:5]:
            st.write(f"**{course} — {topic}** · Score: {score}/{total} · {date}")
    else:
        st.info("Your quiz history will appear here after your first quiz.")

# =========================================================
# LEARN
# =========================================================

elif st.session_state.page == "Learn":
    st.title("📚 Learn a topic")
    st.write("Start with introductory concepts and progress toward intermediate topics. Read the lesson before starting the quiz.")

    course_names = list(courses.keys())
    current_course = (
        st.session_state.course
        if st.session_state.course in course_names
        else course_names[0]
    )

    course = st.selectbox(
        "Choose a subject",
        course_names,
        index=course_names.index(current_course),
    )

    topic_names = list(courses[course].keys())
    previous_topic = st.session_state.topic
    topic = st.selectbox(
        "Choose a topic",
        topic_names,
        index=topic_names.index(previous_topic)
        if previous_topic in topic_names else 0,
    )

    st.session_state.course = course
    st.session_state.topic = topic
    lesson = courses[course][topic]

    st.divider()
    st.subheader(f"📖 {topic}")
    st.markdown("**Definition and concept**")
    st.write(lesson["definition"])

    st.markdown("**Example**")
    st.info(lesson["example"])

    st.caption("Learning path: Introduction → Intermediate")

    if st.button("I understand — Start Topic Quiz →", type="primary"):
        reset_quiz()
        go("Take Quiz")

# =========================================================
# QUIZ
# =========================================================

elif st.session_state.page == "Take Quiz":
    st.title("📝 Topic Quiz")
    quiz_col, assistant_col = st.columns([1.8, 1], gap="large")

    if not st.session_state.course or not st.session_state.topic:
        with quiz_col:
            st.info("Choose a course and topic in Learn before starting a quiz.")
            if st.button("Go to Learn"):
                go("Learn")
        st.stop()

    course = st.session_state.course
    topic = st.session_state.topic
    lesson = courses.get(course, {}).get(topic)
    if not lesson:
        with quiz_col:
            st.error("This topic could not be found. Please select it again.")
        st.stop()

    question_bank = build_topic_question_bank(course, topic, lesson, courses)
    if not question_bank:
        with quiz_col:
            st.info("This custom topic has no built-in question bank yet. Use the AI Assistant for practice ideas.")
            if st.button("Ask AI for practice questions"):
                go("AI Assistant")
        st.stop()

    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = []

    with quiz_col:
        st.write(f"**Course:** {course}")
        st.write(f"**Topic:** {topic}")
        st.caption(f"{len(question_bank)} practice questions for this topic, covering core knowledge, concepts, examples, and application.")

        if not st.session_state.quiz_finished:
            q_index = min(st.session_state.quiz_index, len(question_bank) - 1)
            q = question_bank[q_index]
            st.progress((q_index) / len(question_bank), text=f"Question {q_index + 1} of {len(question_bank)}")
            st.markdown(f"### {q['question']}")

            with st.form(f"topic_quiz_form_{q_index}"):
                answer = st.radio("Select your answer", q["options"], index=None, key=f"topic_answer_{q_index}")
                submitted = st.form_submit_button("Submit answer", type="primary", use_container_width=True)

            if submitted:
                if answer is None:
                    st.warning("Please select an answer.")
                else:
                    correct = answer == q["answer"]
                    answer_record = {
                        "question": q["question"], "answer": answer,
                        "correct_answer": q["answer"], "correct": correct,
                        "explanation": q["explanation"],
                    }
                    st.session_state.quiz_answers.append(answer_record)
                    st.session_state.quiz_result = answer_record
                    if q_index + 1 >= len(question_bank):
                        # Save exactly one database row when the whole topic quiz is finished.
                        # Individual questions are practice items, not separate quizzes.
                        completed_answers = st.session_state.quiz_answers
                        quiz_score = sum(1 for item in completed_answers if item["correct"])
                        quiz_total = len(completed_answers)
                        mistakes = [topic] if quiz_score < quiz_total else []
                        if not st.session_state.get("quiz_saved", False):
                            save_result(
                                st.session_state.student, course, topic,
                                quiz_score, quiz_total, mistakes
                            )
                            st.session_state.quiz_saved = True
                        st.session_state.quiz_finished = True
                    else:
                        st.session_state.quiz_index = q_index + 1
                    st.rerun()

        if st.session_state.quiz_finished:
            answers = st.session_state.quiz_answers
            correct_count = sum(1 for item in answers if item["correct"])
            total_count = len(answers)
            score_pct = round(100 * correct_count / total_count) if total_count else 0
            st.progress(1.0, text="Topic quiz completed")
            st.subheader("Your topic results")
            m1, m2, m3 = st.columns(3)
            m1.metric("Score", f"{correct_count}/{total_count}")
            m2.metric("Accuracy", f"{score_pct}%")
            m3.metric("Questions", total_count)

            for idx, item in enumerate(answers, start=1):
                with st.expander(f"Question {idx}: {'Correct' if item['correct'] else 'Review this answer'}", expanded=not item["correct"]):
                    st.write(item["question"])
                    st.write("**Your answer:**", item["answer"])
                    st.write("**Correct answer:**", item["correct_answer"])
                    st.info(item["explanation"])

            st.subheader("🧠 Automatic learning analysis")
            if score_pct >= 80:
                st.success("Strong understanding of this topic. Next, practise an application-based or more complex problem.")
            elif score_pct >= 50:
                st.warning("Developing understanding. Review the explanations for missed questions, then retake the topic quiz.")
            else:
                st.error("Foundational review recommended. Re-read the definition and example, then practise this topic again.")

            if st.button("Retake this topic quiz", type="primary"):
                reset_quiz()
                st.rerun()
            if st.button("Choose another topic"):
                reset_quiz()
                go("Learn")

    with assistant_col:
        st.markdown("<div class='quiz-assistant-card'><h3>🤖 LearnMate AI Assistant</h3><p>Ask about the current topic while you practise. Learner guidance is based on the lesson and answers recorded so far.</p></div>", unsafe_allow_html=True)
        learner_prompt = st.text_area("Ask your tutor", key="quiz_tutor_prompt", placeholder="Explain this concept with an example...", height=110)
        if st.button("Ask LearnMate", key="ask_quiz_tutor", use_container_width=True):
            recent_answers = st.session_state.get("quiz_answers", [])
            learner_context = "; ".join(
                f"Q: {a['question']} | learner answer: {a['answer']} | correct: {a['correct_answer']} | result: {a['correct']}"
                for a in recent_answers[-5:]
            )
            lesson_context = (
                f"Course: {course}. Topic: {topic}. Definition: {lesson.get('definition', '')}. "
                f"Example: {lesson.get('example', '')}. Learner quiz history: {learner_context}"
            )
            st.session_state.quiz_tutor_answer = tutor_response(
                learner_prompt or f"Explain {topic} in simple terms", lesson_context
            )
        if st.session_state.get("quiz_tutor_answer"):
            st.markdown(st.session_state.quiz_tutor_answer)

        st.divider()
        st.caption("Automatic learner analysis")
        learner_results = load_results(st.session_state.student)
        course_results = [r for r in learner_results if r[0] == course]
        if course_results:
            course_accuracy = round(100 * sum(r[2] for r in course_results) / max(1, sum(r[3] for r in course_results)))
            st.metric("Course accuracy", f"{course_accuracy}%")
            if course_accuracy >= 80:
                st.write("Pattern: strong performance. Extend the concept with more complex practice.")
            elif course_accuracy >= 50:
                st.write("Pattern: developing understanding. Review missed answers and retry similar examples.")
            else:
                st.write("Pattern: foundational review recommended. Revisit lesson definitions and worked examples.")
        else:
            st.write("Your answers will establish a baseline. LearnMate infers learning needs from correctness and recurring mistakes.")

# =========================================================
# PROGRESS
# =========================================================

elif st.session_state.page == "My Progress":
    st.title("📈 My Learning Progress")
    st.caption("Each completed topic counts as one quiz, no matter how many questions it contains.")

    import pandas as pd
    import plotly.express as px

    st.subheader("Individual course progress")
    progress_rows = []
    for course_name, topic_map in courses.items():
        course_attempts = [r for r in results if r[0] == course_name]
        attempted_topics = len({r[1] for r in course_attempts})
        total_topics = len(topic_map)
        score_sum = sum(r[2] for r in course_attempts)
        total_sum = sum(r[3] for r in course_attempts)
        accuracy_value = round(100 * score_sum / total_sum) if total_sum else 0
        completion_value = round(100 * attempted_topics / total_topics) if total_topics else 0
        progress_rows.append({
            "Course": course_name,
            "Topics completed": attempted_topics,
            "Total topics": total_topics,
            "Course progress": f"{completion_value}%",
            "Accuracy": f"{accuracy_value}%",
            "Completed topic quizzes": len(course_attempts),
        })
        with st.expander(f"{course_name} · {completion_value}% complete", expanded=False):
            m1, m2, m3 = st.columns(3)
            m1.metric("Topics attempted", f"{attempted_topics}/{total_topics}")
            m2.metric("Quiz accuracy", f"{accuracy_value}%")
            m3.metric("Topic quizzes completed", len(course_attempts))
            st.progress(completion_value / 100, text=f"Course progress: {completion_value}%")
            st.markdown("**Topic-by-topic status**")
            for topic_name in topic_map:
                topic_attempts = [r for r in course_attempts if r[1] == topic_name]
                if topic_attempts:
                    latest = topic_attempts[0]
                    topic_accuracy = round(100 * sum(r[2] for r in topic_attempts) / max(1, sum(r[3] for r in topic_attempts)))
                    st.write(f"✅ **{topic_name}** — attempted {len(topic_attempts)} time(s), accuracy {topic_accuracy}%")
                else:
                    st.write(f"⬜ **{topic_name}** — not attempted yet")

    st.dataframe(pd.DataFrame(progress_rows), use_container_width=True, hide_index=True)

    if not results:
        st.info("Complete a topic quiz to start building your progress history. A topic quiz is recorded once, after you answer all questions in that topic.")
    else:
        df = pd.DataFrame(
            results,
            columns=["Course", "Topic", "Score", "Total", "Date", "Mistakes"],
        )
        df["Accuracy"] = 100 * df["Score"] / df["Total"].clip(lower=1)

        st.subheader("Completed topic quiz history")
        st.dataframe(
            df[["Course", "Topic", "Score", "Total", "Accuracy", "Date"]],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Accuracy by topic")
        topic_df = df.groupby(["Course", "Topic"], as_index=False)["Accuracy"].mean()
        fig = px.bar(
            topic_df,
            x="Topic",
            y="Accuracy",
            color="Course",
            range_y=[0, 100],
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Topics needing more practice")
        weak_topics = df[df["Score"] < df["Total"]]
        if weak_topics.empty:
            st.success("No incorrect answers in the recorded quizzes yet.")
        else:
            st.dataframe(
                weak_topics[["Course", "Topic", "Score", "Total", "Accuracy", "Date"]],
                use_container_width=True,
                hide_index=True,
            )

# =========================================================
# ADD CUSTOM COURSES
# =========================================================

elif st.session_state.page == "Add Course":
    st.title("➕ Add your own course or topic")
    st.write("Create a course and add a lesson that you want to learn.")

    with st.form("add_course_form"):
        course = st.text_input(
            "Course name",
            placeholder="e.g. Data Structures",
        )
        topic = st.text_input(
            "Topic name",
            placeholder="e.g. Binary Search Trees",
        )
        definition = st.text_area(
            "Topic definition",
            placeholder="Explain the main concept...",
        )
        example = st.text_area(
            "Example",
            placeholder="Add an example, formula or code snippet...",
        )
        submitted = st.form_submit_button("Save course and topic")

    if submitted:
        if not all(x.strip() for x in [course, topic, definition, example]):
            st.warning("Please fill in all four fields.")
        else:
            with sqlite3.connect(DB_PATH) as con:
                con.execute(
                    """
                    INSERT INTO custom_topics
                    (student, course, topic, definition, example)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        st.session_state.student,
                        course.strip(),
                        topic.strip(),
                        definition.strip(),
                        example.strip(),
                    ),
                )
            st.success("Your course topic has been saved.")
            st.session_state.course = course.strip()
            st.session_state.topic = topic.strip()
            st.rerun()

# =========================================================
# AI SETTINGS
# =========================================================

elif st.session_state.page == "AI Settings":
    st.title("🔑 AI Settings")
    st.write("LearnMate AI checks your local secrets file first. You can also enter a session-only key here.")

    built_in_key = ""
    try:
        built_in_key = st.secrets.get("OPENAI_API_KEY", "")
    except Exception:
        built_in_key = ""

    if built_in_key:
        st.success("A built-in API key was found in .streamlit/secrets.toml.")
    else:
        st.info("No built-in key found yet. Add OPENAI_API_KEY to .streamlit/secrets.toml, or enter a key below.")

    api_key = st.text_input(
        "Optional session API key (overrides built-in key)",
        type="password",
        value=st.session_state.ai_key,
        placeholder="Paste a key here only if you want to override the built-in key",
    )

    st.caption(
        "The built-in key is read from your local secrets file. An optional key entered here "
        "is held only in this Streamlit session and is not saved to the learning database."
    )

    if st.button("Save session key"):
        st.session_state.ai_key = api_key.strip()
        st.success("Session key saved." if api_key.strip() else "Session override cleared; the built-in key will be used if available.")

    st.markdown(
        "[Get an API key from the OpenAI developer platform](https://platform.openai.com/api-keys)"
    )
    st.info("API usage may require separate billing. A ChatGPT subscription does not automatically include API credits. When credits run out, LearnMate switches to built-in tutor guidance for quiz support.")

# =========================================================
# AI ASSISTANT
# =========================================================

elif st.session_state.page == "AI Assistant":
    st.title("🤖 LearnMate AI Tutor")
    st.write("Ask for explanations, worked examples, revision notes, or practice questions.")
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("Ask a question about what you're learning...")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        current_lesson = courses.get(st.session_state.course, {}).get(st.session_state.topic, {})
        context = (
            f"Current course: {st.session_state.course}; topic: {st.session_state.topic}. "
            f"Definition: {current_lesson.get('definition','')}. Example: {current_lesson.get('example','')}. "
            f"Recent learner quiz records: {[(r[0], r[1], r[2], r[3], r[5]) for r in results[:8]]}"
        )
        response = tutor_response(prompt, context)
        st.session_state.chat.append({"role": "assistant", "content": response})
        st.rerun()

# =========================================================
# FOOTER
# =========================================================

st.divider()
st.caption(
    "LearnMate AI · Personalized learning · "
    "Built with Python, Streamlit, SQLite and OpenAI"
)
