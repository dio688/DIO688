import argparse
import random
import fractions
import os


def generate_number(r):
    """
    生成一个在指定范围内的自然数或真分数
    :param r: 范围
    :return: 自然数或真分数
    """
    if random.random() < 0.5:
        return random.randint(0, r - 1)
    else:
        numerator = random.randint(1, r - 1)
        denominator = random.randint(1, r)  # 确保分母不为0
        return fractions.Fraction(numerator, denominator)


def generate_expression(r, op_count=0):
    """
    生成一个算术表达式
    :param r: 范围
    :param op_count: 运算符数量
    :return: 算术表达式
    """
    if op_count >= 3 or random.random() < 0.2:
        return generate_number(r)
    op = random.choice(['+', '-', '*', '/'])
    e1 = generate_expression(r, op_count + 1)
    e2 = generate_expression(r, op_count + 1)
    if op == '-':
        while isinstance(e1, int) and isinstance(e2, int) and e1 < e2:
            e1 = generate_expression(r, op_count + 1)
            e2 = generate_expression(r, op_count + 1)
    if op == '/':
        while isinstance(e1, int) and isinstance(e2, int) and (e1 % e2 != 0):
            e1 = generate_expression(r, op_count + 1)
            e2 = generate_expression(r, op_count + 1)
    return f"({e1} {op} {e2})"


def simplify_expression(expression):
    """
    简化表达式，去除不必要的括号
    :param expression: 算术表达式
    :return: 简化后的表达式
    """
    expression = str(expression)
    while '(( ' in expression:
        expression = expression.replace('(( ', '( ')
        expression = expression.replace(' ))', ' )')
    return expression


def calculate(expression):
    """
    计算表达式的值
    :param expression: 算术表达式
    :return: 计算结果
    """
    try:
        if not isinstance(expression, str):
            expression = str(expression)
        expression = expression.replace('/', '//')
        result = eval(expression)
        if isinstance(result, fractions.Fraction):
            if result.numerator > result.denominator:
                whole = result.numerator // result.denominator
                remainder = result.numerator % result.denominator
                if remainder == 0:
                    return whole
                return f"{whole}'{remainder}/{result.denominator}"
            return f"{result.numerator}/{result.denominator}"
        return result
    except ZeroDivisionError:
        return None


def generate_problems(n, r):
    """
    生成指定数量和范围的四则运算题目
    :param n: 题目数量
    :param r: 范围
    :return: 题目列表和答案列表
    """
    problems = set()
    answers = []
    while len(problems) < n:
        expression = generate_expression(r)
        simplified_expression = simplify_expression(expression)
        if simplified_expression in problems:
            continue
        result = calculate(expression)
        if result is not None:
            problems.add(simplified_expression)
            answers.append(result)
    return list(problems), answers


def save_to_file(filename, content):
    """
    将内容保存到文件
    :param filename: 文件名
    :param content: 内容
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for line in content:
            f.write(str(line).replace('*', '×').replace('//', '÷') + '\n')


def check_answers(exercise_file, answer_file):
    """
    检查答案的对错并统计数量
    :param exercise_file: 题目文件
    :param answer_file: 答案文件
    """
    if not os.path.exists(exercise_file) or not os.path.exists(answer_file):
        print("文件不存在，请检查路径。")
        return
    with open(exercise_file, 'r', encoding='utf-8') as f1, open(answer_file, 'r', encoding='utf-8') as f2:
        exercises = f1.readlines()
        answers = f2.readlines()
    correct = []
    wrong = []
    for i, (exercise, answer) in enumerate(zip(exercises, answers), start=1):
        exercise = exercise.strip().rstrip('=')  # 去除末尾的等号
        exercise = exercise.replace('×', '*').replace('÷', '//')
        result = calculate(exercise)
        if str(result) == answer.strip():
            correct.append(i)
        else:
            wrong.append(i)
    with open('Grade.txt', 'w', encoding='utf-8') as f:
        f.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def main():
    """
    主函数，处理命令行参数
    """
    parser = argparse.ArgumentParser(description='小学四则运算题目生成程序')
    parser.add_argument('-n', type=int, help='生成题目的个数')
    parser.add_argument('-r', type=int, help='题目中数值的范围')
    parser.add_argument('-e', help='题目文件路径')
    parser.add_argument('-a', help='答案文件路径')
    args = parser.parse_args()

    if args.n is not None and args.r is not None:
        problems, answers = generate_problems(args.n, args.r)
        save_to_file('Exercises.txt', [f"{p} =" for p in problems])
        save_to_file('Answers.txt', answers)
    elif args.e is not None and args.a is not None:
        check_answers(args.e, args.a)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
