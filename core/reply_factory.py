
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(
        message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    return True, ""


def get_next_question(user_data, questions):
    answered_questions = user_data.get('answers', {}).keys()
    for question in questions:
        if question['id'] not in answered_questions:
            user_data['current_question'] = question['id']
            return question['text']

    return None


def generate_final_response(user_data, questions):
    answers = user_data.get('answers', {})
    score = 0

    for question in questions:
        correct_answer = question['correct_answer']
        user_answer = answers.get(question['id'])
        if user_answer == correct_answer:
            score += 1

    total_questions = len(questions)
    return f"Quiz completed! You scored {score} out of {total_questions}."


def record_current_answer(user_data, user_response):
    current_question = user_data.get('current_question')
    answers = user_data.get('answers', {})

    if current_question is None:
        return "No current question to answer."

    # Validate the response (assuming it's a multiple choice with options 'A', 'B', 'C', 'D')
    if user_response not in ['A', 'B', 'C', 'D']:
        return "Invalid response. Please answer with 'A', 'B', 'C', or 'D'."

    # Store the answer
    answers[current_question] = user_response
    user_data['answers'] = answers

    return "Answer recorded."
