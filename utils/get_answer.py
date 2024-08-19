def get_answer_from_question(question):
    match question.answer:
        case "option1":
            answer = question.option1
        case "option2":
            answer = question.option2
        case "option3":
            answer = question.option3
        case "option4":
            answer = question.option4
        case _:
            answer = ""

    return answer


def get_user_answer(question, user_answer):
    match user_answer:
        case "option1":
            answer = question.option1
        case "option2":
            answer = question.option2
        case "option3":
            answer = question.option3
        case "option4":
            answer = question.option4
        case _:
            answer = ""
    return answer
