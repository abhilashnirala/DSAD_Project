from student_table import StudentHashRecords
import common_utils
import re


class Students:
    def __init__(self):
        self.cse_list = list()
        self.mec_list = list()
        self.ece_list = list()
        self.arc_list = list()

    def initializeHash(self):
        """ intialize Student Hash Table and perform operation like insertion, halloffame, course, average"""
        studentHashRecords = StudentHashRecords()
        self.get_inputs_from_txt(studentHashRecords)
        self.hallOfFame(studentHashRecords)
        CGPAFrom, CPGATo = self.get_course_offer_range()
        self.newCourseList(studentHashRecords, CGPAFrom, CPGATo)
        self.depAvg(studentHashRecords)
        self.destroyHash(studentHashRecords)

    def insertStudentRec(self, StudentHashRecords, studentId, CGPA):
        """Insert the Student records in the Hash Table"""
        StudentHashRecords.add(key=studentId, value=CGPA)

    def hallOfFame(self, StudentHashRecords):
        """Topper of per year and per department"""
        self.distribute_student_in_dep(StudentHashRecords)
        prompts_data = self.get_prompts_from_txt()
        for prompt_data in prompts_data:
            if 'hallOfFame' in prompt_data:
                cse_hall_of_fame_list = self.get_hall_of_fame_dept_wise(self.cse_list)
                mec_hall_of_fame_list = self.get_hall_of_fame_dept_wise(self.mec_list)
                ece_hall_of_fame_list = self.get_hall_of_fame_dept_wise(self.ece_list)
                arc_hall_of_fame_list = self.get_hall_of_fame_dept_wise(self.arc_list)
                total_quantity = len(cse_hall_of_fame_list) + len(mec_hall_of_fame_list) + len(
                    ece_hall_of_fame_list) + len(arc_hall_of_fame_list)
                self.write_halloffame_output(total_quantity, cse_hall_of_fame_list, mec_hall_of_fame_list,
                                             ece_hall_of_fame_list, arc_hall_of_fame_list)

    def newCourseList(self, StudentHashRecords, CGPAFrom, CPGATo):
        """ prints the list of all students who have a CGPA within the given range and have graduated in the
        last 5 years"""
        year_range_start = 2011
        year_range_end = 2017
        self.distribute_student_for_course(StudentHashRecords, year_range_start, year_range_end)
        cse_course_list = self.get_new_course_dept_wise(self.cse_list, CGPAFrom, CPGATo)
        mec_course_list = self.get_new_course_dept_wise(self.mec_list, CGPAFrom, CPGATo)
        ece_course_list = self.get_new_course_dept_wise(self.ece_list, CGPAFrom, CPGATo)
        arc_course_list = self.get_new_course_dept_wise(self.arc_list, CGPAFrom, CPGATo)
        total_quantity = len(cse_course_list) + len(mec_course_list) + len(ece_course_list) + len(arc_course_list)
        self.write_newcourse_output(CGPAFrom, CPGATo, total_quantity, cse_course_list,mec_course_list,ece_course_list,arc_course_list)

    def depAvg(self, StudentHashRecords):
        """ prints the list of all departments followed by the maximum CGPA and average CGPA of all students"""
        dep_cgpa_list = []
        self.distribute_student_in_dep(StudentHashRecords)
        cse_max_value, cse_avg = self.get_depavg_dept_wise(self.cse_list)
        dep_cgpa_list.append("CSE: max: {}, avg: {}".format(cse_max_value, cse_avg))
        mec_max_value, mec_avg = self.get_depavg_dept_wise(self.mec_list)
        dep_cgpa_list.append("MEC: max: {}, avg: {}".format(mec_max_value, mec_avg))
        ece_max_value, ece_avg = self.get_depavg_dept_wise(self.ece_list)
        dep_cgpa_list.append("ECE: max: {}, avg: {}".format(ece_max_value, ece_avg))
        arc_max_value, arc_avg = self.get_depavg_dept_wise(self.arc_list)
        dep_cgpa_list.append("ARC: max: {}, avg: {}".format(arc_max_value, arc_avg))
        self.write_depavg_output(dep_cgpa_list)

    def destroyHash(self, StudentHashRecords):
        """destroy hash table implementation"""
        return StudentHashRecords.delete()

    def get_course_offer_range(self):
        """get course range from prompt files"""
        prompts_data = self.get_prompts_from_txt()
        for prompt_data in prompts_data:
            if "courseOffer" in prompt_data:
                course_range = prompt_data.split(":")
                course_range[1] = course_range[1].rstrip()
                course_range[2] = course_range[2].rstrip()
                return float(course_range[1]), float(course_range[2])

    def get_hall_of_fame_dept_wise(self, dep_list):
        """ fetch student id with grade who topped in their department in respective year"""
        hall_of_fame = list()
        stud_id, max_value = self.get_key_and_value(dep_list[0])
        existing_year = self.get_student_desc(stud_id)
        for stud in dep_list:
            key, value = self.get_key_and_value(stud)
            year = self.get_student_desc(key)
            if year < 2017 and year == existing_year and value > max_value:
                max_value = value
                stud_id = key
            elif year < 2017 and year != existing_year:
                hall_of_fame.append("{} / {}".format(stud_id, max_value))
                existing_year = year
                max_value = value
                stud_id = key
        hall_of_fame.append("{} / {}".format(stud_id, max_value))
        return hall_of_fame

    def get_new_course_dept_wise(self, dep_list,  CGPAFrom, CPGATo):
        """fetch the student id and grade who falls under new course range"""
        new_course_list = list()
        for stud in dep_list:
            key, value = self.get_key_and_value(stud)
            if CGPAFrom <= value <= CPGATo:
                new_course_list.append("{} / {}".format(key, value))
        return new_course_list

    def get_depavg_dept_wise(self, dep_list):
        """ calculate the department wise max grade and average grade"""
        max_value = 0
        sum = 0
        for stud in dep_list:
            key, value = self.get_key_and_value(stud)
            sum += value
            if max_value < value:
                max_value = value
        return max_value, round(sum/len(dep_list), 1)

    def get_inputs_from_txt(self, StudentHashRecords):
        """ read the student id and grade from input file and feed into hash table"""
        input_path = common_utils.get_data_dir("inputPS12.txt")
        input_data = common_utils.get_content_from_file(input_path)
        for data in input_data:
            record = data.split('/')
            record[0] = record[0].rstrip()
            record[1] = record[1].rstrip()
            self.insertStudentRec(StudentHashRecords, record[0], float(record[1]))

    def get_key_and_value(self, data):
        """ to return key and value from the list"""
        return data[0], data[1]

    def takeFirst(self, elem):
        """return first element of the list"""
        return elem[0]

    def distribute_student_in_dep(self, StudentHashRecords):
        """categorize the students on the basis on each department"""
        self.cse_list = []
        self.mec_list = []
        self.ece_list = []
        self.arc_list = []
        for data in StudentHashRecords:
            key, value = self.get_key_and_value(data)
            if re.search("CSE", key):
                self.cse_list.append(data)
            elif re.search("MEC", key):
                self.mec_list.append(data)
            elif re.search("ECE", key):
                self.ece_list.append(data)
            elif re.search("ARC", key):
                self.arc_list.append(data)
        self.cse_list.sort(key=self.takeFirst)
        self.arc_list.sort(key=self.takeFirst)
        self.mec_list.sort(key=self.takeFirst)
        self.ece_list.sort(key=self.takeFirst)

    def distribute_student_for_course(self, StudentHashRecords, year_range_start, year_range_end):
        """categorize the graduated students on the basis on each department only for last 5 year"""
        self.cse_list = []
        self.mec_list = []
        self.ece_list = []
        self.arc_list = []
        for data in StudentHashRecords:
            key, value = self.get_key_and_value(data)
            if re.search("CSE", key):
                year = self.get_student_desc(key)
                if year_range_start < year < year_range_end:
                    self.cse_list.append(data)
            elif re.search("MEC", key):
                year = self.get_student_desc(key)
                if year_range_start < year < year_range_end:
                    self.mec_list.append(data)
            elif re.search("ECE", key):
                year = self.get_student_desc(key)
                if year_range_start < year < year_range_end:
                    self.ece_list.append(data)
            elif re.search("ARC", key):
                year = self.get_student_desc(key)
                if year_range_start < year < year_range_end:
                    self.arc_list.append(data)
            self.cse_list.sort(key=self.takeFirst)
            self.arc_list.sort(key=self.takeFirst)
            self.mec_list.sort(key=self.takeFirst)
            self.ece_list.sort(key=self.takeFirst)

    def get_prompts_from_txt(self):
        """retrieve the tags present in prompt file"""
        prompts_path = common_utils.get_data_dir("promptsPS12.txt")
        prompts_data = common_utils.get_content_from_file(prompts_path)
        return prompts_data

    def get_student_desc(self, key):
        """ fetch the year from student id"""
        year = key[:4]
        return int(year)

    def write_halloffame_output(self, total_quantity, cse_hall_of_fame_list, mec_hall_of_fame_list,
                                ece_hall_of_fame_list, arc_hall_of_fame_list):
        """ write hall of fame data to output file"""
        filename = common_utils.get_abs_path(common_utils.get_output_dir(), "outputPS12.txt")
        with open(filename, 'w+') as file:
            file.write("---------- hall of fame ----------\n")
            file.write("Total eligible students: {}\n".format(total_quantity))
            file.write("Qualified students:\n")
            for line in cse_hall_of_fame_list:
                file.write(line + "\n")
            for line in mec_hall_of_fame_list:
                file.write(line + "\n")
            for line in ece_hall_of_fame_list:
                file.write(line + "\n")
            for line in arc_hall_of_fame_list:
                file.write(line + "\n")
            file.write("-------------------------------------\n")

    def write_newcourse_output(self,CGPAFrom, CPGATo, total_quantity, cse_course_list,mec_course_list,ece_course_list,arc_course_list):
        """ write new course offer data to output file"""
        filename = common_utils.get_abs_path(common_utils.get_output_dir(), "outputPS12.txt")
        with open(filename, 'a+') as file:
            file.write("---------- new course candidates ----------\n")
            file.write("Input: {} to {}\n".format(CGPAFrom, CPGATo))
            file.write("Total eligible students: {}\n".format(total_quantity))
            file.write("Qualified students:\n")
            for line in cse_course_list:
                file.write(line + "\n")
            for line in mec_course_list:
                file.write(line + "\n")
            for line in ece_course_list:
                file.write(line + "\n")
            for line in arc_course_list:
                file.write(line + "\n")
            file.write("-------------------------------------\n")

    def write_depavg_output(self,dep_cgpa_list):
        """ write department wise average and max grade data to output file"""
        filename = common_utils.get_abs_path(common_utils.get_output_dir(), "outputPS12.txt")
        with open(filename, 'a+') as file:
            file.write("---------- department CGPA ----------\n")
            for line in dep_cgpa_list:
                file.write(line + "\n")
            file.write("-------------------------------------\n")


if __name__ == '__main__':
    student = Students()
    student.initializeHash()