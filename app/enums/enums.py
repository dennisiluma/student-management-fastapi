from enum import StrEnum


class UserRole(StrEnum):
    TEACHER = "teacher"
    STUDENT = "student"
    ADMIN = "admin"




class GradeTerm(StrEnum):
    FIRST_TERM = "1st Term"
    SECOND_TERM = "2nd Term"
    THIRD_TERM = "3rd Term"