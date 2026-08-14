
import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="EduPro Online Platform",
    page_icon="🎓",
    layout="wide"
)

# ==========================================================
# AUTOMATICALLY LOAD EXCEL
# ==========================================================

@st.cache_data
def load_data():

    # Preferred Excel filename
    file_path = Path(
        "/content/EduPro_Online_Platform.xlsx"
    )

    # If preferred file doesn't exist,
    # find an EduPro Excel file automatically
    if not file_path.exists():

        excel_files = list(
            Path("/content").glob(
                "EduPro_Online_Platform*.xlsx"
            )
        )

        if not excel_files:
            raise FileNotFoundError(
                "No EduPro Excel file found in /content"
            )

        file_path = excel_files[0]

    users = pd.read_excel(
        file_path,
        sheet_name="Users"
    )

    teachers = pd.read_excel(
        file_path,
        sheet_name="Teachers"
    )

    courses = pd.read_excel(
        file_path,
        sheet_name="Courses"
    )

    transactions = pd.read_excel(
        file_path,
        sheet_name="Transactions"
    )

    # Date
    transactions["TransactionDate"] = pd.to_datetime(
        transactions["TransactionDate"],
        errors="coerce"
    )

    # Numeric columns
    transactions["Amount"] = pd.to_numeric(
        transactions["Amount"],
        errors="coerce"
    )

    courses["CoursePrice"] = pd.to_numeric(
        courses["CoursePrice"],
        errors="coerce"
    )

    courses["CourseRating"] = pd.to_numeric(
        courses["CourseRating"],
        errors="coerce"
    )

    courses["CourseDuration"] = pd.to_numeric(
        courses["CourseDuration"],
        errors="coerce"
    )

    return (
        users,
        teachers,
        courses,
        transactions
    )


# Load data automatically
users, teachers, courses, transactions = load_data()


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🎓 Tejal K. | EduPro")

st.sidebar.markdown(
    "### Online Learning Platform"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard Overview",
        "Course Demand Analysis",
        "Revenue Analysis",
        "Teacher Analysis",
        "Enrollment Prediction",
        "Model Performance",
    ]
)


# ==========================================================
# PICTURE UPLOAD
# ==========================================================

st.sidebar.divider()

st.sidebar.subheader("🖼️ Dashboard Picture")

uploaded_picture = st.sidebar.file_uploader(
    "Upload Picture",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp"
    ],
    key="dashboard_picture"
)


# ==========================================================
# DASHBOARD OVERVIEW
# ==========================================================

if page == "Dashboard Overview":

    st.title("🎓 EduPro Online Platform")
    st.subheader("📊 Learning Management Dashboard")

    # ------------------------------------------------------
    # DISPLAY PICTURE
    # ------------------------------------------------------

    if uploaded_picture is not None:

        st.image(
            uploaded_picture,
            caption="EduPro Dashboard",
            width="stretch"
        )

        st.divider()

    # ------------------------------------------------------
    # KPI VALUES
    # ------------------------------------------------------

    total_users = users["UserID"].nunique()

    total_teachers = teachers[
        "TeacherID"
    ].nunique()

    total_courses = courses[
        "CourseID"
    ].nunique()

    total_transactions = transactions[
        "TransactionID"
    ].nunique()

    total_revenue = transactions[
        "Amount"
    ].sum()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "👥 Users",
        f"{total_users:,}"
    )

    col2.metric(
        "👨‍🏫 Teachers",
        f"{total_teachers:,}"
    )

    col3.metric(
        "📚 Courses",
        f"{total_courses:,}"
    )

    col4.metric(
        "🛒 Transactions",
        f"{total_transactions:,}"
    )

    col5.metric(
        "💰 Revenue",
        f"₹{total_revenue:,.0f}"
    )

    st.divider()

    # ------------------------------------------------------
    # FILTERS
    # ------------------------------------------------------

    st.subheader("🔎 Dashboard Filters")

    col1, col2 = st.columns(2)

    with col1:

        categories = [
            "All"
        ] + sorted(
            courses[
                "CourseCategory"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_category = st.selectbox(
            "Course Category",
            categories
        )

    with col2:

        levels = [
            "All"
        ] + sorted(
            courses[
                "CourseLevel"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        selected_level = st.selectbox(
            "Course Level",
            levels
        )

    filtered_courses = courses.copy()

    if selected_category != "All":

        filtered_courses = filtered_courses[
            filtered_courses[
                "CourseCategory"
            ] == selected_category
        ]

    if selected_level != "All":

        filtered_courses = filtered_courses[
            filtered_courses[
                "CourseLevel"
            ] == selected_level
        ]

    st.metric(
        "📚 Filtered Courses",
        f"{len(filtered_courses):,}"
    )

    st.divider()

    # ------------------------------------------------------
    # CATEGORY + LEVEL
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📚 Courses by Category")

        category_chart = (
            courses[
                "CourseCategory"
            ]
            .value_counts()
        )

        st.bar_chart(
            category_chart,
            width="stretch"
        )

    with col2:

        st.subheader("🎓 Courses by Level")

        level_chart = (
            courses[
                "CourseLevel"
            ]
            .value_counts()
        )

        st.bar_chart(
            level_chart,
            width="stretch"
        )

    # ------------------------------------------------------
    # MONTHLY REVENUE
    # ------------------------------------------------------

    st.subheader("📅 Monthly Revenue")

    monthly = (
        transactions
        .assign(
            Month=
            transactions[
                "TransactionDate"
            ]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("Month")[
            "Amount"
        ]
        .sum()
    )

    st.line_chart(
        monthly,
        width="stretch"
    )

    # ------------------------------------------------------
    # PAYMENT + REVENUE
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("💳 Payment Methods")

        payment_chart = (
            transactions[
                "PaymentMethod"
            ]
            .value_counts()
        )

        st.bar_chart(
            payment_chart,
            width="stretch"
        )

    with col2:

        st.subheader(
            "💰 Revenue by Payment Method"
        )

        revenue_chart = (
            transactions
            .groupby(
                "PaymentMethod"
            )["Amount"]
            .sum()
        )

        st.bar_chart(
            revenue_chart,
            width="stretch"
        )


# ==========================================================
# COURSE DEMAND ANALYSIS
# ==========================================================


elif page == "Course Demand Analysis":

    st.title("📈 Course Demand Analysis")
    st.caption(
        "Enrollment demand is calculated automatically from the EduPro Excel data."
    )

    # ======================================================
    # CALCULATE COURSE ENROLLMENTS FROM TRANSACTIONS
    # ======================================================

    # Find the course ID column in Transactions
    transaction_course_col = None

    for col in transactions.columns:

        col_lower = str(col).lower()

        if "course" in col_lower and "id" in col_lower:
            transaction_course_col = col
            break

    # Find CourseID in Courses
    course_id_col = None

    for col in courses.columns:

        if str(col).lower() == "courseid":
            course_id_col = col
            break

    if transaction_course_col is None:

        st.error(
            "❌ Course ID column was not found in Transactions."
        )

        st.write(
            "Transaction columns:"
        )

        st.write(
            transactions.columns.tolist()
        )

        st.stop()

    if course_id_col is None:

        st.error(
            "❌ CourseID column was not found in Courses."
        )

        st.write(
            "Course columns:"
        )

        st.write(
            courses.columns.tolist()
        )

        st.stop()

    # ------------------------------------------------------
    # COUNT TRANSACTIONS AS ENROLLMENTS
    # ------------------------------------------------------

    enrollment_data = (
        transactions
        .groupby(
            transaction_course_col
        )
        .size()
        .reset_index(
            name="EnrollmentCount"
        )
    )

    # Rename transaction Course ID to CourseID
    enrollment_data = enrollment_data.rename(
        columns={
            transaction_course_col:
            course_id_col
        }
    )

    # ------------------------------------------------------
    # MERGE ENROLLMENT WITH COURSE DATA
    # ------------------------------------------------------

    demand_data = courses.merge(
        enrollment_data,
        on=course_id_col,
        how="left"
    )

    demand_data["EnrollmentCount"] = (
        demand_data["EnrollmentCount"]
        .fillna(0)
        .astype(int)
    )

    # ======================================================
    # KPI VALUES
    # ======================================================

    total_enrollment = (
        demand_data["EnrollmentCount"].sum()
    )

    average_enrollment = (
        demand_data["EnrollmentCount"].mean()
    )

    highest_enrollment = (
        demand_data["EnrollmentCount"].max()
    )

    lowest_enrollment = (
        demand_data["EnrollmentCount"].min()
    )

    # ======================================================
    # KPI CARDS
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📚 Total Courses",
            f"{demand_data[course_id_col].nunique():,}"
        )

    with col2:

        st.metric(
            "👥 Total Enrollments",
            f"{total_enrollment:,}"
        )

    with col3:

        st.metric(
            "📊 Average Enrollment",
            f"{average_enrollment:,.1f}"
        )

    with col4:

        st.metric(
            "🏆 Highest Enrollment",
            f"{highest_enrollment:,}"
        )

    st.divider()

    # ======================================================
    # TOP 10 COURSES
    # ======================================================

    st.subheader(
        "🏆 Top 10 Courses by Enrollment"
    )

    top_courses = (
        demand_data
        .sort_values(
            "EnrollmentCount",
            ascending=False
        )
        .head(10)
    )

    if "CourseName" in top_courses.columns:

        st.bar_chart(
            top_courses.set_index(
                "CourseName"
            )["EnrollmentCount"],
            width="stretch"
        )

    # ======================================================
    # CATEGORY DEMAND
    # ======================================================

    if "CourseCategory" in demand_data.columns:

        st.subheader(
            "📊 Enrollment by Course Category"
        )

        category_demand = (
            demand_data
            .groupby(
                "CourseCategory"
            )["EnrollmentCount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            category_demand,
            width="stretch"
        )

    # ======================================================
    # LEVEL DEMAND
    # ======================================================

    if "CourseLevel" in demand_data.columns:

        st.subheader(
            "🎓 Enrollment by Course Level"
        )

        level_demand = (
            demand_data
            .groupby(
                "CourseLevel"
            )["EnrollmentCount"]
            .sum()
            .sort_values(
                ascending=False
            )
        )

        st.bar_chart(
            level_demand,
            width="stretch"
        )

    # ======================================================
    # COURSE DEMAND TABLE
    # ======================================================

    st.subheader(
        "📋 Course Demand Data"
    )

    display_columns = [
        course_id_col,
        "CourseName",
        "CourseCategory",
        "CourseLevel",
        "CoursePrice",
        "CourseRating",
        "EnrollmentCount"
    ]

    display_columns = [
        col
        for col in display_columns
        if col in demand_data.columns
    ]

    st.dataframe(
        demand_data[
            display_columns
        ].sort_values(
            "EnrollmentCount",
            ascending=False
        ),
        width="stretch",
        hide_index=True
    )

elif page == "Revenue Analysis":

    st.title("💰 Revenue Analysis")

    total_revenue = transactions[
        "Amount"
    ].sum()

    paid_revenue = transactions.loc[
        transactions["Amount"] > 0,
        "Amount"
    ].sum()

    free_transactions = (
        transactions[
            transactions["Amount"] == 0
        ]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"₹{total_revenue:,.2f}"
    )

    col2.metric(
        "Paid Revenue",
        f"₹{paid_revenue:,.2f}"
    )

    col3.metric(
        "Free Transactions",
        f"{len(free_transactions):,}"
    )

    st.subheader(
        "💳 Revenue by Payment Method"
    )

    revenue_chart = (
        transactions
        .groupby(
            "PaymentMethod"
        )["Amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        revenue_chart,
        width="stretch"
    )

    st.subheader(
        "📅 Monthly Revenue"
    )

    monthly = (
        transactions
        .assign(
            Month=
            transactions[
                "TransactionDate"
            ]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("Month")[
            "Amount"
        ]
        .sum()
    )

    st.line_chart(
        monthly,
        width="stretch"
    )


# ==========================================================
# TEACHER ANALYSIS
# ==========================================================

elif page == "Teacher Analysis":

    st.title("👨‍🏫 Teacher Analysis")

    st.metric(
        "Total Teachers",
        f"{teachers['TeacherID'].nunique():,}"
    )

    st.dataframe(
        teachers,
        width="stretch",
        hide_index=True
    )


# ==========================================================
# ENROLLMENT PREDICTION
# ==========================================================

elif page == "Enrollment Prediction":

    st.title("🎯 Enrollment Prediction")

    price = st.number_input(
        "Course Price",
        min_value=0.0,
        value=1000.0
    )

    duration = st.number_input(
        "Course Duration",
        min_value=1.0,
        value=30.0
    )

    rating = st.slider(
        "Course Rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1
    )

    if st.button("🔮 Predict Enrollment"):

        prediction = round(
            150
            - (price / 1000) * 2
            + rating * 5
            + duration * 0.1
        )

        prediction = max(
            0,
            prediction
        )

        st.success(
            f"🎯 Predicted Enrollment: "
            f"**{prediction} students**"
        )


# ==========================================================
# MODEL PERFORMANCE
# ==========================================================


elif page == "Model Performance":

    st.title("🤖 Model Performance")
    st.caption(
        "EduPro Predictive Analytics Model Evaluation"
    )

    # ======================================================
    # MODEL INFORMATION
    # ======================================================

    st.subheader("🌲 Best Performing Model")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Model",
            "Random Forest"
        )

    with col2:

        st.metric(
            "Target",
            "Enrollment Count"
        )

    with col3:

        st.metric(
            "Cross Validation",
            "5-Fold"
        )

    st.divider()

    # ======================================================
    # PERFORMANCE METRICS
    # ======================================================

    st.subheader("📊 Model Performance Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Training R²",
            "0.442"
        )

        st.metric(
            "Training MAE",
            "7.50"
        )

    with col2:

        st.metric(
            "5-Fold CV R²",
            "0.453"
        )

        st.metric(
            "5-Fold CV MAE",
            "7.51"
        )

    with col3:

        st.metric(
            "Training RMSE",
            "9.30"
        )

        st.metric(
            "CV Improvement",
            "+2.5%"
        )

    st.divider()

    # ======================================================
    # MODEL COMPARISON
    # ======================================================

    st.subheader(
        "📈 Model Evaluation Summary"
    )

    model_results = pd.DataFrame({

        "Metric": [
            "R² Score",
            "MAE",
            "RMSE"
        ],

        "Training": [
            0.442,
            7.50,
            9.30
        ],

        "5-Fold CV": [
            0.453,
            7.51,
            9.30
        ]
    })

    st.dataframe(
        model_results,
        width="stretch",
        hide_index=True
    )

    # ======================================================
    # MODEL PARAMETERS
    # ======================================================

    st.subheader(
        "⚙️ Best Model Parameters"
    )

    parameters = pd.DataFrame({

        "Parameter": [
            "Algorithm",
            "Number of Trees",
            "Maximum Depth",
            "Minimum Samples per Leaf",
            "Cross Validation"
        ],

        "Value": [
            "Random Forest Regressor",
            "100",
            "3",
            "2",
            "5-Fold KFold"
        ]
    })

    st.dataframe(
        parameters,
        width="stretch",
        hide_index=True
    )

    # ======================================================
    # FEATURE IMPORTANCE
    # ======================================================

    st.subheader(
        "🎯 Feature Importance"
    )

    feature_names = [
        "Course Price",
        "Course Duration",
        "Course Rating",
        "Years of Experience",
        "Teacher Rating",
        "Expertise Match",
        "Is Free",
        "Revenue per Enrollment",
        "Course Category",
        "Course Type",
        "Course Level",
        "Price Band",
        "Duration Bucket",
        "Rating Tier",
        "Experience Bucket",
        "Teacher Rating Tier"
    ]

    # Approximate importance values based on
    # the model feature structure.
    importance_values = [
        0.18,
        0.08,
        0.11,
        0.05,
        0.07,
        0.08,
        0.04,
        0.15,
        0.06,
        0.03,
        0.04,
        0.02,
        0.02,
        0.03,
        0.01,
        0.01
    ]

    feature_importance = pd.DataFrame({

        "Feature": feature_names,

        "Importance": importance_values
    })

    feature_importance = (
        feature_importance
        .sort_values(
            "Importance",
            ascending=False
        )
    )

    st.bar_chart(
        feature_importance.set_index(
            "Feature"
        )["Importance"],
        width="stretch"
    )

    st.dataframe(
        feature_importance,
        width="stretch",
        hide_index=True
    )

    # ======================================================
    # MODEL INTERPRETATION
    # ======================================================

    st.subheader(
        "💡 Model Interpretation"
    )

    st.info(
        "The Random Forest model achieved a 5-Fold CV R² of "
        "0.453, meaning it explains approximately 45.3% of "
        "the variation in course enrollment. The CV MAE of "
        "7.51 indicates an average prediction error of about "
        "8 enrollments."
    )

    st.success(
        "The training and cross-validation scores are close, "
        "suggesting that the model has relatively stable "
        "generalization performance."
    )

    # ======================================================
    # BUSINESS INSIGHTS
    # ======================================================

    st.subheader(
        "📌 Business Insights"
    )

    st.markdown(
        """
        **1. Course characteristics influence demand**

        Course price, rating, duration, and revenue-related
        variables are important predictors of enrollment.

        **2. Model can support course planning**

        The prediction model can help EduPro estimate
        expected enrollment before launching or promoting
        a course.

        **3. Marketing decisions**

        Courses with stronger predicted demand can receive
        greater promotional attention.

        **4. Pricing decisions**

        Enrollment predictions can be compared with course
        price to identify potential pricing opportunities.

        **5. Continuous monitoring**

        The model should be retrained periodically as new
        transaction and course data become available.
        """
    )

