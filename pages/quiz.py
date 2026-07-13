import streamlit as st

def show_quiz():
    """
    Display the Green Energy Challenge quiz.
    """

    st.title("🎮 Green Energy Challenge")

    st.markdown("""
Test your knowledge of renewable energy and discover how green you are!
""")

    questions = [
        {
            "question": "Which renewable energy source uses sunlight to generate electricity?",
            "options": ["Wind", "Solar", "Hydro", "Biomass"],
            "answer": "Solar"
        },
        {
            "question": "Which energy source uses flowing water to produce electricity?",
            "options": ["Solar", "Hydro", "Wind", "Geothermal"],
            "answer": "Hydro"
        },
        {
            "question": "Which renewable energy source comes from heat inside the Earth?",
            "options": ["Wind", "Biomass", "Geothermal", "Solar"],
            "answer": "Geothermal"
        },
        {
            "question": "Which greenhouse gas is mainly reduced by using renewable energy?",
            "options": ["Nitrogen", "Oxygen", "Carbon Dioxide", "Hydrogen"],
            "answer": "Carbon Dioxide"
        },
        {
            "question": "Which country currently has one of the world's largest solar energy capacities?",
            "options": ["India", "China", "Brazil", "Australia"],
            "answer": "China"
        }
    ]

    score = 0

    st.subheader("📝 Quiz Questions")

    for i, question in enumerate(questions):

        answer = st.radio(
            f"Q{i+1}. {question['question']}",
            question["options"],
            key=f"quiz_{i}"
        )

        if answer == question["answer"]:
            score += 1

    st.markdown("---")

    if st.button("✅ Submit Quiz", use_container_width=True):

        percentage = score / len(questions)

        st.subheader("📊 Quiz Results")

        st.metric(
            "🏆 Score",
            f"{score} / {len(questions)}"
        )

        st.progress(percentage)

        if percentage == 1.0:
            st.balloons()
            st.success(
                "🏆 Excellent! You're a Renewable Energy Champion!"
            )

        elif percentage >= 0.80:
            st.success(
                "🌱 Great Job! You have excellent knowledge of renewable energy."
            )

        elif percentage >= 0.60:
            st.info(
                "👍 Good effort! You're on the right path toward becoming a sustainability expert."
            )

        else:
            st.warning(
                "📚 Keep learning about renewable energy and try again!"
            )

        st.markdown("---")

        st.markdown("### 🌍 Correct Answers")

        for i, question in enumerate(questions):
            st.write(
                f"**Q{i+1}.** {question['answer']}"
            )

        st.success(
            "🌿 Every step toward learning renewable energy helps build a greener future!"
        )
