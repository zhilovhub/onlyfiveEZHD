import re


# обработка формул
def translation(content):
    content = content.replace('\\', '').replace('pi', 'π').replace('', 'f')
    sqrts = re.findall(r'sqrt{.*?}', content)
    for sqrt in sqrts:
        new_sqrt = sqrt[sqrt.find('{') + 1:-1]
        if new_sqrt:
            if new_sqrt.isdigit():
                new_sqrt = '√' + new_sqrt
            else:
                new_sqrt = '√(' + new_sqrt + ')'
            content = content.replace(sqrt, new_sqrt)
    fracs = re.findall(r'frac{.*?}{.*?}', content)
    for frac in fracs:
        new_frac = re.findall(r'{.*?}', frac)
        if len(new_frac) == 2:
            first, second = [i[i.find('{') + 1:-1] for i in new_frac]
            if not first.isdigit():
                first = '(' + first + ')'
            if not second.isdigit():
                second = '(' + second + ')'
            content = content.replace(frac, f' {first}/{second} ')
    return content


def get_answers_text(response):
    answers = []
    k = 1
    for group in response['training_tasks']:
        text_styles = group['test_task']['question_elements']
        question = text_styles[0]['text']
        try:
            if len(text_styles) > 1:
                if 'preview_url' in text_styles[1]:
                    question = question + f'\nКартинка: {text_styles[1]["preview_url"]}'
            elif text_styles[0]['content']:
                if text_styles[0]['content'][0]['type'] == 'content/math':
                    question = question + f'\nФормула из вопроса: {translation(text_styles[0]["content"][0]["content"])}'
        except Exception:
            question += '\nОшибка бота. Написать "mis" (без кавычек), чтобы мы это увидели и исправили.'
        answer = group['test_task']['answer']
        task_type = answer['type']
        right_answer_text = 'Не нашел, обратить на это внимание'
        if task_type == 'answer/single':
            right_answer = answer['right_answer']['id']
            for option in answer['options']:
                if option['id'] == right_answer:
                    # работаем над этой частью
                    right_answer_text = [option['text']]
                    if not right_answer_text[0] or len(option['content']) > 1:
                        for content in option['content']:
                            if content['type'] == 'content/math':
                                right_answer_text.append(translation(content['content']))
                            else:
                                if 'relative_url' in content:
                                    right_answer_text.append(content['relative_url'])
                                elif 'file' in content:
                                    right_answer_text.append('https://uchebnik.mos.ru/exam' + content['file']['relative_url'])
            right_answer_text = '\n'.join(right_answer_text) if right_answer_text[0] else '\n'.join(right_answer_text[1:])
            string = f'{k}. {question}\nОтвет: {right_answer_text}'
        elif task_type == 'answer/number':
            right_answer = answer['right_answer']['number']
            right_answer_text = str(right_answer)
            question = question.split('\n\n')[0]
            string = f'{k}. {question}\nОтвет: {right_answer_text}'
        elif task_type == 'answer/multiple':
            right_answer = answer['right_answer']['ids']
            right_answer_text = []
            for id in right_answer:
                for right in answer['options']:
                    if id == right['id']:
                        if right['text']:
                            right_answer_text.append('- ' + right['text'])
                        elif right['content'][0]['type'] == 'content/math':
                            right_answer_text.append('- ' + translation(right['content'][0]['content']))
                        elif right['content'][0]['type'] == 'content/atomic':
                            right_answer_text.append('- ' + right['content'][0]['relative_url'])
            right_answer_text = '\n'.join([''] + right_answer_text)
            string = f'{k}. {question}\nОтвет: {right_answer_text}'
        elif task_type == 'answer/string':
            right_answer = answer['right_answer']['string']
            string = f'{k}. {question}\nОтвет: {right_answer}'
        elif task_type == 'answer/groups':
            right_answer = answer['right_answer']
            right_answers = []
            for group in right_answer['groups']:
                first = group['group_id']
                second = group['options_ids']
                for id in answer['options']:
                    if id['id'] == first:
                        first = id['text']
                    else:
                        for ind in range(len(second)):
                            if second[ind] == id['id']:
                                if id['text']:
                                    second[ind] = id['text']
                                elif id['content'][0]['type'] == 'content/atomic':
                                    second[ind] = id['content'][0]['relative_url']
                second = ['-' + second[0]] + second[1:]
                second = '\n-'.join(second)
                right_answers.append(f'{first}:\n{second}')
            right_answers = '\n\n'.join(right_answers)
            string = f'{k}. {question}\nОтвет:\n{right_answers}'
        elif task_type == 'answer/match':
            right_answer = answer['right_answer']['match']
            right_answers = []
            for group in right_answer:
                first = group
                second = right_answer[group]
                for id in answer['options']:
                    if first == id['id']:
                        first = id['text']
                        if not first:
                            if id['content'][0]['type'] == 'content/math':
                                first = translation(id['content'][0]['content'])
                            else:
                                first = id['content'][0]['relative_url']
                    else:
                        for ind in range(len(second)):
                            if second[ind] == id['id']:
                                second[ind] = id['text']
                                if not second[ind]:
                                    if id['content'][0]['type'] == 'content/math':
                                        second[ind] = translation(id['content'][0]['content'])
                                    else:
                                        if 'file' in id['content'][0]:
                                            second[ind] = 'https://uchebnik.mos.ru/exam' + id['content'][0]['file']['relative_url']
                                        else:
                                            second[ind] = id['content'][0]['relative_url']
                second = ['- ' + second[0]] + second[1:]
                second = '\n- '.join(second)
                right_answers.append(f'{first}\n{second}')
            right_answers = '\n\n'.join(right_answers)
            string = f'{k}. {question}\nОтвет:\n{right_answers}'
        elif task_type == 'answer/order':
            right_answer = answer['right_answer']['ids_order']
            right_answers = []
            for n, id in enumerate(right_answer, start=1):
                for id_check in answer['options']:
                    if id_check['id'] == id:
                        right_answers.append(f'{n}) {id_check["text"]}')
            right_answers = '\n'.join(right_answers)
            string = f'{k}. {question}\nОтвет:\n{right_answers}'
        elif task_type == 'answer/gap/match/text':
            right_answer = answer['text_position']
            right_answers = []
            for i in right_answer:
                id = i['position_id']
                for j in answer['right_answer']['text_position_answer']:
                    if id == j['position_id']:
                        id = j['id']
                        break
                for option in answer['options']:
                    if id == option['id']:
                        right_answers.append(option['text'])
                        break
            right_answers = ' - '.join(right_answers)
            string = f'{k}. {question}\nОтвет:\n{right_answers}'
        elif task_type == 'answer/inline/choice/single':
            right_answer = answer['right_answer']['text_position_answer']
            right_answers = []
            for i in right_answer:
                position_id = i['position_id']
                id = i['id']
                for j in answer['text_position']:
                    if position_id == j['position_id']:
                        for option in j['options']:
                            if option['id'] == id:
                                right_answers.append(option['text'])
                                break
                        break
            right_answers = ' - '.join(right_answers)
            string = f'{k}. {question}\nОтвет:\n{right_answers}'

        elif task_type == "answer/table":
            right_answer = answer["right_answer"]
            right_answers = []
            options = answer["options"][0]["content"][0]["table"]["cells"]["0"]
            for column_index, answer_index in right_answer["cells"]["1"].items():
                column_name = options[column_index]
                right_answers.append(f"{column_name} - {answer_index}")
            right_answers = "\n".join(right_answers)
            string = f'{k}. {question}\nОтвет:\n{right_answers}'

        else:
            string = f'{k}. {question}\nОтвет: {task_type}'
        answers.append([string])
        k += 1
    return "\n\n".join(['\n'.join(k) for k in answers])
