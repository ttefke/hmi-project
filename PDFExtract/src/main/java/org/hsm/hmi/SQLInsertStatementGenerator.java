package org.hsm.hmi;

public class SQLInsertStatementGenerator {
    public String createStatement(ModuleStringModel model) {
        StringBuilder result = new StringBuilder();
        result.append("INSERT INTO acs_modules\n");
        result.append("VALUES (");

        // file location (currently not deceided on yet - fill out later)
        result.append("'../data/courses/acs/manual.pdf',");

        // title
        result.append("'").append(model.getName()).append("',");

        // professor
        result.append("'").append(model.getProfessor()).append("',");

        // learning objectives
        result.append("'").append(model.getTargets()).append("',");

        // course contents
        result.append("'").append(model.getContents()).append("',");

        // teaching methods
        result.append("'").append(model.getMethods()).append("',");

        // prerequisites
        result.append("'").append(model.getRequirements()).append("',");

        //readings
        result.append("'").append(model.getLiterature()).append("',");

        // applicability
        result.append("'").append(model.getApplicability()).append("',");

        // workload
        result.append("'").append(model.getEffort()).append("',");

        // credits
        result.append("'").append(model.getECTS()).append("',");

        // evaluation
        result.append("'").append(model.getPerformanceRecord()).append("',");

        // time
        result.append("'").append(model.getSemester()).append("',");

        // frequency
        result.append("'").append(model.getFrequency()).append("',");

        // duration
        result.append("'").append(model.getDuration()).append("',");

        // type of course
        result.append("'").append(model.getTypeOfCourse()).append("',");

        // remarks
        result.append("''");

        // return result
        result.append(");");
        return result.toString();
    }
}
