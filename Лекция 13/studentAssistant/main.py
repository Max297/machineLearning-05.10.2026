"""
MCP-сервер помощника студента вуза.
Использует только встроенные библиотеки Python + FastMCP.
Все данные хранятся в памяти процесса.
"""
from __future__ import annotations

from fastmcp import FastMCP


# ======================================================================
# Хранилище данных (in-memory)
# ======================================================================

STUDENTS: dict[str, dict] = {
    "s1001": {"name": "Иванов Иван Иванович",   "group": "ПИ-21"},
    "s1002": {"name": "Петрова Анна Сергеевна", "group": "ПИ-21"},
    "s1003": {"name": "Сидоров Алексей Павлович", "group": "ПИ-22"},
}

# Успеваемость: студент -> список оценок
GRADES: dict[str, list[dict]] = {
    "s1001": [
        {"subject": "Математический анализ", "grade": 5, "date": "2026-06-10", "form": "экзамен"},
        {"subject": "Программирование",      "grade": 4, "date": "2026-06-15", "form": "зачёт"},
        {"subject": "Физика",                "grade": 5, "date": "2026-06-20", "form": "экзамен"},
        {"subject": "Английский язык",       "grade": 4, "date": "2026-06-25", "form": "зачёт"},
    ],
    "s1002": [
        {"subject": "Математический анализ", "grade": 4, "date": "2026-06-10", "form": "экзамен"},
        {"subject": "Программирование",      "grade": 5, "date": "2026-06-15", "form": "зачёт"},
        {"subject": "Физика",                "grade": 4, "date": "2026-06-20", "form": "экзамен"},
    ],
    "s1003": [
        {"subject": "Математический анализ", "grade": 3, "date": "2026-06-10", "form": "экзамен"},
        {"subject": "Программирование",      "grade": 4, "date": "2026-06-15", "form": "зачёт"},
    ],
}

# Расписание: группа -> список занятий
SCHEDULE: dict[str, list[dict]] = {
    "ПИ-21": [
        {"day": "Понедельник", "time": "09:00-10:30", "subject": "Математический анализ",
         "teacher": "Смирнов А.В.", "room": "305"},
        {"day": "Понедельник", "time": "10:40-12:10", "subject": "Физика",
         "teacher": "Кузнецова Е.И.", "room": "210"},
        {"day": "Вторник",   "time": "09:00-10:30", "subject": "Программирование",
         "teacher": "Николаев Д.С.", "room": "412"},
        {"day": "Среда",     "time": "12:20-13:50", "subject": "Английский язык",
         "teacher": "Белова О.Н.", "room": "118"},
        {"day": "Четверг",   "time": "09:00-10:30", "subject": "Математический анализ",
         "teacher": "Смирнов А.В.", "room": "305"},
        {"day": "Пятница",   "time": "10:40-12:10", "subject": "Физика",
         "teacher": "Кузнецова Е.И.", "room": "210"},
    ],
    "ПИ-22": [
        {"day": "Понедельник", "time": "10:40-12:10", "subject": "Программирование",
         "teacher": "Николаев Д.С.", "room": "412"},
        {"day": "Вторник",   "time": "09:00-10:30", "subject": "Математический анализ",
         "teacher": "Смирнов А.В.", "room": "305"},
        {"day": "Среда",     "time": "09:00-10:30", "subject": "Физика",
         "teacher": "Кузнецова Е.И.", "room": "210"},
        {"day": "Четверг",   "time": "12:20-13:50", "subject": "Английский язык",
         "teacher": "Белова О.Н.", "room": "118"},
    ],
}

# Преподаватели (ключ — ФИО, как в расписании)
TEACHERS: dict[str, dict] = {
    "Смирнов А.В.":    {"full_name": "Смирнов Алексей Владимирович",
                        "department": "Кафедра высшей математики",
                        "office": "каб. 318, главный корпус",
                        "hours": "Вт, Чт 14:00–16:00"},
    "Кузнецова Е.И.":  {"full_name": "Кузнецова Елена Игоревна",
                        "department": "Кафедра общей физики",
                        "office": "каб. 215, главный корпус",
                        "hours": "Пн, Ср 15:00–17:00"},
    "Николаев Д.С.":   {"full_name": "Николаев Дмитрий Сергеевич",
                        "department": "Кафедра информатики и программирования",
                        "office": "каб. 420, корпус ИТ",
                        "hours": "Ср, Пт 13:00–15:00"},
    "Белова О.Н.":     {"full_name": "Белова Ольга Николаевна",
                        "department": "Кафедра иностранных языков",
                        "office": "каб. 122, гуманитарный корпус",
                        "hours": "Пн–Пт 10:00–12:00"},
}

# Задачи студента
TASKS: dict[str, list[dict]] = {
    "s1001": [
        {"title": "Решить варианты №5–8 по мат. анализу",
         "subject": "Математический анализ",
         "deadline": "2026-08-28", "status": "upcoming"},
        {"title": "Лабораторная работа: сортировки",
         "subject": "Программирование",
         "deadline": "2026-09-02", "status": "upcoming"},
        {"title": "Реферат по истории физики",
         "subject": "Физика",
         "deadline": "2026-08-20", "status": "submitted"},
        {"title": "Эссе My Future Profession",
         "subject": "Английский язык",
         "deadline": "2026-08-15", "status": "submitted"},
    ],
    "s1002": [
        {"title": "Контрольная работа по интегралам",
         "subject": "Математический анализ",
         "deadline": "2026-08-30", "status": "upcoming"},
        {"title": "Проект: веб-чат на сокетах",
         "subject": "Программирование",
         "deadline": "2026-09-10", "status": "upcoming"},
        {"title": "Лабораторная: маятник Обербека",
         "subject": "Физика",
         "deadline": "2026-08-22", "status": "submitted"},
    ],
    "s1003": [
        {"title": "Домашнее задание: ряды",
         "subject": "Математический анализ",
         "deadline": "2026-08-29", "status": "upcoming"},
        {"title": "Лабораторная: структуры данных",
         "subject": "Программирование",
         "deadline": "2026-09-05", "status": "upcoming"},
    ],
}


# ======================================================================
# MCP-сервер
# ======================================================================

mcp = FastMCP("StudentAssistant")


# ---------- Вспомогательные функции ----------

def _get_student(student_id: str) -> dict | None:
    return STUDENTS.get(student_id)


def _avg(grades: list[dict]) -> float:
    if not grades:
        return 0.0
    return sum(g["grade"] for g in grades) / len(grades)


# ---------- Инструменты ----------
@mcp.tool(
    name="get_student_info",
    description="Получить базовую информацию о студенте: ФИО и учебную группу",
    annotations={
        "title": "Информация о студенте",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def get_student_info(student_id: str) -> str:
    """Принимает идентификатор студента, например 's1001'."""
    student = _get_student(student_id)
    if not student:
        return f"Студент с id '{student_id}' не найден."
    return (
        f"Студент: {student['name']}\n"
        f"Группа:  {student['group']}"
    )


@mcp.tool(
    name="get_grades",
    description="Получить полную успеваемость студента: список оценок по предметам с датами и средний балл",
    annotations={
        "title": "Успеваемость студента",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def get_grades(student_id: str) -> str:
    """Принимает идентификатор студента, например 's1001'."""
    student = _get_student(student_id)
    if not student:
        return f"Студент с id '{student_id}' не найден."

    grades = GRADES.get(student_id, [])
    if not grades:
        return f"У студента {student['name']} пока нет оценок."

    lines = [f"Успеваемость студента {student['name']} ({student['group']}):"]
    for g in grades:
        lines.append(
            f"  • {g['subject']} — {g['grade']} ({g['form']}, {g['date']})"
        )
    lines.append(f"Средний балл: {_avg(grades):.2f}")
    return "\n".join(lines)


@mcp.tool(
    name="get_schedule",
    description="Получить расписание занятий студента на неделю с указанием времени, предметов, преподавателей и аудиторий",
    annotations={
        "title": "Расписание занятий",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def get_schedule(student_id: str) -> str:
    """Принимает идентификатор студента, например 's1001'."""
    student = _get_student(student_id)
    if not student:
        return f"Студент с id '{student_id}' не найден."

    group = student["group"]
    lessons = SCHEDULE.get(group, [])
    if not lessons:
        return f"Расписание для группы {group} не найдено."

    lines = [f"Расписание группы {group} ({student['name']}):"]
    for lesson in lessons:
        lines.append(
            f"  • {lesson['day']}, {lesson['time']} — "
            f"{lesson['subject']} (преп. {lesson['teacher']}, ауд. {lesson['room']})"
        )
    return "\n".join(lines)


@mcp.tool(
    name="get_teacher_info",
    description="Получить детальную информацию о преподавателе: полное ФИО, кафедра, номер кабинета и часы приёма",
    annotations={
        "title": "Информация о преподавателе",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def get_teacher_info(teacher_name: str) -> str:
    """Принимает имя преподавателя в том виде, в каком оно указано в расписании, например 'Смирнов А.В.'."""
    teacher = TEACHERS.get(teacher_name)
    if not teacher:
        # Попробуем нечувствительный к регистру поиск
        for key, value in TEACHERS.items():
            if key.lower() == teacher_name.lower():
                teacher = value
                break
    if not teacher:
        return f"Преподаватель '{teacher_name}' не найден."

    return (
        f"Преподаватель: {teacher['full_name']}\n"
        f"Кафедра:       {teacher['department']}\n"
        f"Кабинет:       {teacher['office']}\n"
        f"Рабочие часы:  {teacher['hours']}"
    )


@mcp.tool(
    name="list_teachers",
    description="Получить краткий список всех преподавателей вуза с указанием их кафедр",
    annotations={
        "title": "Список преподавателей",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def list_teachers() -> str:
    """Не принимает параметров."""
    if not TEACHERS:
        return "Список преподавателей пуст."
    lines = ["Преподаватели вуза:"]
    for name, info in TEACHERS.items():
        lines.append(f"  • {info['full_name']} — {info['department']}")
    return "\n".join(lines)


@mcp.tool(
    name="get_tasks",
    description="Получить список задач студента с возможностью фильтрации по статусу: все, предстоящие или сданные",
    annotations={
        "title": "Задачи студента",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
def get_tasks(student_id: str, status: str = "all") -> str:
    """
    Параметры:
      - student_id: идентификатор студента, например 's1001'.
      - status: фильтр по статусу. Допустимые значения:
          'all'       — все задачи,
          'upcoming'  — только предстоящие (не сданные),
          'submitted' — только сданные.
    """
    student = _get_student(student_id)
    if not student:
        return f"Студент с id '{student_id}' не найден."

    tasks = TASKS.get(student_id, [])
    if not tasks:
        return f"У студента {student['name']} нет задач."

    status = status.lower()
    if status not in ("all", "upcoming", "submitted"):
        return "Недопустимое значение status. Используйте 'all', 'upcoming' или 'submitted'."

    if status == "all":
        filtered = tasks
    else:
        filtered = [t for t in tasks if t["status"] == status]

    if not filtered:
        return f"У студента {student['name']} нет задач со статусом '{status}'."

    title = {
        "all": "Все задачи",
        "upcoming": "Предстоящие задачи",
        "submitted": "Сданные задачи",
    }[status]

    lines = [f"{title} студента {student['name']} ({student['group']}):"]
    for t in filtered:
        mark = "✓" if t["status"] == "submitted" else "○"
        lines.append(
            f"  {mark} [{t['subject']}] {t['title']} — "
            f"срок: {t['deadline']} ({t['status']})"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    # Запуск через std-транспорт (для тестирования через `mcp dev` / `mcp run`)
    mcp.run()