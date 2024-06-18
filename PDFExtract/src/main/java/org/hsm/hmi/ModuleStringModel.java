package org.hsm.hmi;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.Serializable;

public class ModuleStringModel implements Serializable {
    // Comment = name of the property in the manual

    // Module name
    private String name;

    // Module responsibility
    private String professor;

    // Qualification targets
    private String targets;

    // we skip the table

    // Module contents
    private String contents;

    // Teaching Methods
    private String methods;

    // Requirements for participation
    private String requirements;

    // Literature / Teaching material
    private String literature;

    // Applicability
    private String applicability;

    // Effort / total workload
    private String effort;

    // ECTS / emphasis of the Grade for the final grade
    private String ECTS;

    // Performance record;
    private String performanceRecord;

    // Intended semester
    private String semester;

    // Frequency of the course
    private String frequency;

    // Duration
    private String duration;

    // Type of course
    private String typeOfCourse;

    public ModuleStringModel() {
        this.name = "";
        this.professor = "";
        this.targets = "";
        this.contents = "";
        this.methods = "";
        this.requirements = "";
        this.literature = "";
        this.applicability = "";
        this.ECTS = "";
        this.effort = "";
        this.performanceRecord = "";
        this.semester = "";
        this.frequency = "";
        this.duration = "";
        this.typeOfCourse = "";
    }

    public void prepareForOutput() {
        this.name = this.name.strip();
        this.professor = this.professor.strip();
        this.targets = this.targets.strip();
        this.contents = this.contents.strip();
        this.methods = this.methods.strip();
        this.requirements = this.requirements.strip();
        this.literature = this.literature.strip();
        this.applicability = this.applicability.strip();
        this.ECTS = this.ECTS.strip();
        this.effort = this.effort.strip();
        this.performanceRecord = this.performanceRecord.strip();
        this.semester = this.semester.strip();
        this.frequency = this.frequency.strip();
        this.duration = this.duration.strip();
        this.typeOfCourse = this.typeOfCourse.strip();
    }
    @SuppressWarnings("unused")
    public String asJSON() throws JsonProcessingException {
        prepareForOutput();

        var mapper = new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
        return mapper.writeValueAsString(this);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getProfessor() {
        return professor;
    }

    public void setProfessor(String professor) {
        this.professor = professor;
    }

    public String getTargets() {
        return targets;
    }

    public void setTargets(String targets) {
        this.targets = targets;
    }

    public String getContents() {
        return contents;
    }

    public void setContents(String contents) {
        this.contents = contents;
    }

    public String getMethods() {
        return methods;
    }

    public void setMethods(String methods) {
        this.methods = methods;
    }

    public String getRequirements() {
        return requirements;
    }

    public void setRequirements(String requirements) {
        this.requirements = requirements;
    }

    public String getLiterature() {
        return literature;
    }

    public void setLiterature(String literature) {
        this.literature = literature;
    }

    public String getApplicability() {
        return applicability;
    }

    public void setApplicability(String applicability) {
        this.applicability = applicability;
    }

    public String getEffort() {
        return effort;
    }

    public void setEffort(String effort) {
        this.effort = effort;
    }

    public String getECTS() {
        return ECTS;
    }

    public void setECTS(String ECTS) {
        this.ECTS = ECTS;
    }

    public String getPerformanceRecord() {
        return performanceRecord;
    }

    public void setPerformanceRecord(String performanceRecord) {
        this.performanceRecord = performanceRecord;
    }

    public String getSemester() {
        return semester;
    }

    public void setSemester(String semester) {
        this.semester = semester;
    }

    public String getFrequency() {
        return frequency;
    }

    public void setFrequency(String frequency) {
        this.frequency = frequency;
    }

    public String getDuration() {
        return duration;
    }

    public void setDuration(String duration) {
        this.duration = duration;
    }

    public String getTypeOfCourse() {
        if (typeOfCourse.isEmpty()) {
            return "obligatory";
        } else {
            return typeOfCourse;
        }
    }

    public void setTypeOfCourse(String typeOfCourse) {
        String lowerCase = typeOfCourse.toLowerCase();

        if (lowerCase.contains("selectable") || (lowerCase.contains("selection")) ||
                (lowerCase.contains("optional")) || (lowerCase.contains("elective")) ||
                (lowerCase.contains("lecture"))) {
            this.typeOfCourse = "elective";
        } else {
            this.typeOfCourse = "obligatory";
        }
    }
}