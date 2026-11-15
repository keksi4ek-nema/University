from typing import ClassVar, Type

from pydantic import BaseModel, ConfigDict, Field


class Requirements(BaseModel):

    score_requirements_1: int = Field(default=0, ge=0, le=0)
    score_requirements_2: int = Field(default=0, ge=0, le=0)
    score_requirements_3: int = Field(default=0, ge=0, le=0)
    score_requirements_4: int = Field(default=0, ge=0, le=0)
    score_requirements_5: int = Field(default=0, ge=0, le=0)

    min_sum_for_zachet: int = 0


    criterii: ClassVar[tuple[tuple[str, int], ...]] = ()

    @property
    def zachet(self) -> bool:
        return self.total_score >= self.min_sum_for_zachet

    @property
    def result(self) -> str:
        return "Зачёт" if self.zachet else "Незачёт"

    @property
    def total_score(self) -> int:
        return sum(
            getattr(self, name)
            for name in type(self).model_fields
            if name.startswith("score_requirements_")
        )

    @property
    def max_score(self) -> int:
        return sum(max_score for _, max_score in self.criterii)


# Критерии оценивания ДЗ №1 (макс 15 баллов)
# 1 - создание своей таблицы
# 2 - создание графа знаний в Ontolis
# 3 - корректность всех связей в графе знаний
class DZ1Assessment(Requirements):
    score_requirements_1: int = Field(default=0, ge=0, le=2)
    score_requirements_2: int = Field(default=0, ge=0, le=5)
    score_requirements_3: int = Field(default=0, ge=0, le=8)
    min_sum_for_zachet: int = 9

    criterii = (
        ("Создание своей таблицы", 2),
        ("Создание графа знаний в Ontolis", 5),
        ("Корректность связей в графе знаний", 8),
    )


# Критерии оценивания ДЗ №2 (макс 28 баллов)
# 1 - выполнение лабораторных работ №1, 2 и 7
# 2 - выполнение лабораторной работы №3
# 3 - выполнение лабораторной работы №4
# 4 - выполнение лабораторной работы №5
# 5 - выполнение лабораторной работы №6 (медицинская диагностика)
class DZ2Assessment(Requirements):
    score_requirements_1: int = Field(default=0, ge=0, le=12)
    score_requirements_2: int = Field(default=0, ge=0, le=3)
    score_requirements_3: int = Field(default=0, ge=0, le=3)
    score_requirements_4: int = Field(default=0, ge=0, le=3)
    score_requirements_5: int = Field(default=0, ge=0, le=7)
    min_sum_for_zachet: int = 12

    criterii = (
        ("Выполнение лабораторных работ №1, 2 и 7", 12),
        ("Выполнение лабораторной работы №3", 3),
        ("Выполнение лабораторной работы №4", 3),
        ("Выполнение лабораторной работы №5", 3),
        ("Выполнение лабораторной работы №6 (медицинская диагностика)", 7),
    )


# Критерии оценивания ДЗ №3 (макс 38 баллов)
# 1 - создание корректного глоссария
# 2 - создание графа знаний с корректными связями
# 3 - ручное создание презентации по теме
# 4 - создание двух презентаций с использованием ИИ
# 5 - отчёт со сравнением презентаций, созданных вручную и с использованием ИИ
class DZ3Assessment(Requirements):
    score_requirements_1: int = Field(default=0, ge=0, le=10)
    score_requirements_2: int = Field(default=0, ge=0, le=13)
    score_requirements_3: int = Field(default=0, ge=0, le=7)
    score_requirements_4: int = Field(default=0, ge=0, le=3)
    score_requirements_5: int = Field(default=0, ge=0, le=5)
    min_sum_for_zachet: int = 23

    criterii = (
        ("Создание корректного глоссария", 10),
        ("Создание графа знаний с корректными связями", 13),
        ("Ручное создание презентации по теме", 7),
        ("Создание двух презентаций с использованием ИИ", 3),
        ("Отчёт со сравнением презентаций", 5),
    )


# Критерии оценивания ДЗ №4 (макс 19 баллов)
# 1 - выполнение идентификации в отчёте (переменные и разбалловка)
# 2 - выполнение концептуализации в отчёте (И/ИЛИ граф)
# 3 - выполнение формализации в отчёте (создание базы правил)
# 4 - корректность всех этапов в отчёте
class DZ4Assessment(Requirements):
    score_requirements_1: int = Field(default=0, ge=0, le=5)
    score_requirements_2: int = Field(default=0, ge=0, le=5)
    score_requirements_3: int = Field(default=0, ge=0, le=5)
    score_requirements_4: int = Field(default=0, ge=0, le=4)
    min_sum_for_zachet: int = 12

    criterii = (
        ("Идентификация переменных и разбалловка", 5),
        ("Концептуализация (И/ИЛИ граф)", 5),
        ("Формализация (база правил)", 5),
        ("Корректность всех этапов в отчёте", 4),
    )


class Assessment(BaseModel):

    model_config = ConfigDict(validate_assignment=True)

    dz1: DZ1Assessment = Field(default_factory=DZ1Assessment)
    dz2: DZ2Assessment = Field(default_factory=DZ2Assessment)
    dz3: DZ3Assessment = Field(default_factory=DZ3Assessment)
    dz4: DZ4Assessment = Field(default_factory=DZ4Assessment)

    @property
    def dopusk(self) -> bool:
        return all(
            dz.result == "Зачёт"
            for dz in (self.dz1, self.dz2, self.dz3, self.dz4)
        )

    @property
    def total_score(self) -> int:
        return (
            self.dz1.total_score
            + self.dz2.total_score
            + self.dz3.total_score
            + self.dz4.total_score
        )

    @staticmethod
    def get_assessment_result(score: int) -> str:
        if score < 50:
            return "Неудовлетворительно"
        elif score <= 64:
            return "Удовлетворительно"
        elif score <= 85:
            return "Хорошо"
        else:
            return "Отлично"

    @property
    def assessment_results(self) -> str:
        return self.get_assessment_result(self.total_score)

    @property
    def exam(self) -> str:
        if not self.dopusk:
            return "Недопуск"
        elif self.total_score >= 65:
            return "Автомат"
        else:
            return "Экзамен"

    @staticmethod
    def get_exam_score() -> int:
        while True:
            raw_score = input("Введите количество баллов за экзамен (0–100): ")
            try:
                score = int(raw_score)
            except ValueError:
                print("Ошибка: необходимо ввести целое число.")
                continue

            if 0 <= score <= 100:
                return score

            print("Ошибка: результат экзамена должен быть от 0 до 100.")

    @property
    def result_discipline(self) -> str:
        if self.exam == "Недопуск":
            return "Итог: незачёт, оценка «Неудовлетворительно» (нет допуска)."

        if self.exam == "Автомат":
            return (
                "Итог: зачёт с оценкой «"
                f"{self.assessment_results}» (автомат)."
            )

        exam_score = self.get_exam_score()
        exam_result = self.get_assessment_result(exam_score)
        return (
            f"Балл за экзамен: {exam_score}/100. "
            f"Итог: {'незачёт' if exam_score < 50 else 'зачёт'} "
            f"с оценкой «{exam_result}»."
        )


def read_score(prompt: str, max_score: int) -> int:
    while True:
        raw_score = input(prompt)
        try:
            score = int(raw_score)
        except ValueError:
            print("Ошибка: необходимо ввести целое число.")
            continue

        if 0 <= score <= max_score:
            return score

        print(f"Ошибка: за этот критерий можно поставить от 0 до {max_score} баллов.")


def read_dz_assessment(
    assessment_type: Type[Requirements], dz_name: str
) -> Requirements:
    print(f"\n{dz_name}. Введите баллы по каждому критерию:")
    scores = {}

    for number, (description, max_score) in enumerate(
        assessment_type.criterii, start=1
    ):
        prompt = f"{number}. {description} (0–{max_score}): "
        scores[f"score_requirements_{number}"] = read_score(prompt, max_score)

    return assessment_type(**scores)


def read_assessment_from_input() -> tuple[str, Assessment]:
    student_name = input("Введите ФИО студента: ").strip()
    if not student_name:
        student_name = "Студент"

    print("\nОценивание домашних заданий")
    assessment = Assessment(
        dz1=read_dz_assessment(DZ1Assessment, "ДЗ №1"),
        dz2=read_dz_assessment(DZ2Assessment, "ДЗ №2"),
        dz3=read_dz_assessment(DZ3Assessment, "ДЗ №3"),
        dz4=read_dz_assessment(DZ4Assessment, "ДЗ №4"),
    )

    return student_name, assessment


def print_assessment(student_name: str, assessment: Assessment) -> None:
    print("\n" + "=" * 55)
    print(f"РЕЗУЛЬТАТЫ ОЦЕНИВАНИЯ: {student_name}")
    print("=" * 55)

    for dz_name, dz in (
        ("ДЗ №1", assessment.dz1),
        ("ДЗ №2", assessment.dz2),
        ("ДЗ №3", assessment.dz3),
        ("ДЗ №4", assessment.dz4),
    ):
        print(
            f"{dz_name}: {dz.total_score}/{dz.max_score} баллов — "
            f"{dz.result} (порог: {dz.min_sum_for_zachet})."
        )

    print("-" * 55)
    print(f"Итого за домашние задания: {assessment.total_score}/100 баллов.")
    print(f"Допуск: {'TRUE' if assessment.dopusk else 'FALSE'}.")
    print(f"Режим аттестации: {assessment.exam}.")
    print(assessment.result_discipline)
    print("=" * 55)


def main() -> None:
    # 1 Вариант выполнения: самооценивание разработчика 0_0
    student_name = "Петухов Станислав Артемович"
    assessment = Assessment(
        dz1=DZ1Assessment(
            score_requirements_1=2,
            score_requirements_2=5,
            score_requirements_3=8,
        ),
        dz2=DZ2Assessment(
            score_requirements_1=12,
            score_requirements_2=3,
            score_requirements_3=3,
            score_requirements_4=0,
            score_requirements_5=5,
        ),
        dz3=DZ3Assessment(
            score_requirements_1=10,
            score_requirements_2=12,
            score_requirements_3=6,
            score_requirements_4=3,
            score_requirements_5=4,
        ),
        dz4=DZ4Assessment(
            score_requirements_1=5,
            score_requirements_2=4,
            score_requirements_3=4,
            score_requirements_4=4,
        ),
    )

    # Вариант 2 - Оценивание другого студента в интерактивном режиме, для использования нужно закомментировать блок 1 варианта
#    student_name, assessment = read_assessment_from_input()


    print_assessment(student_name, assessment)


if __name__ == "__main__":
    main()




# ИИ использовался минимально, вся идея принадлежит разработчку, также вся основа кода написана собственоручно 