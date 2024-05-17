package org.hsm.hmi;

import java.util.ArrayList;
import java.util.List;

public class TextMining {
    private static final String MODULE_NAME_1 = "Module Name";
    private static final String MODULE_NAME_2 = "Modul Name";
    private static final String MODULE_RESPONSIBILITY_1 = "Module Responsibility";
    private static final String MODULE_RESPONSIBILITY_2 = "Modul Responsibility";
    private static final String QUALIFICATION_TARGETS = "Qualification Targets";
    private static final String MODULE_CONTENTS = "Module Contents";
    private static final String TEACHING_METHODS_1 = "Teaching Methods";
    private static final String TEACHING_METHODS_2 = "Teaching methods";

    private static final String REQUIREMENTS_1 = "Requirements for";
    private static final String REQUIREMENTS_2 = "Participation";

    private static final String LITERATURE_1 = "Literature / Multimedia";
    private static final String LITERATURE_2 = "Literature / Multimedia-";
    private static final String LITERATURE_3 = "based Teaching Material";
    private static final String LITERATURE_4 = "Literature /";
    private static final String LITERATURE_5 = "Multimediabased Teaching";
    private static final String LITERATURE_6 = "Material";
    private static final String LITERATURE_7 = "Literature";
    private static final String APPLICABILITY = "Applicability";
    private static final String EFFORT_1 = "Effort/";
    private static final String EFFORT_2 = "Effort / Total Workload";
    private static final String EFFORT_3 = "Effort/ Total Workload";
    private static final String EFFORT_4 = "Total Workload";

    private static final String ECTS_1 = "ECTS / Emphasis of the";
    private static final String ECTS_2 = "Grade for the final Grade";
    private static final String ECTS_3 = "Grade for the final Grad";

    private static final String PERFORMANCE_RECORD = "Performance Record";
    private static final String SEMESTER = "Semester";

    private static final String FREQUENCY_1 = "Frequency of Occurrence";
    private static final String FREQUENCY_2 = "Frequency of the course";

    private static final String DURATION = "Duration";

    private static final String TYPE = "Type of Course";


    private final String pdfText;

    public TextMining(String pdfText) {
        this.pdfText = pdfText;
    }

    public List<ModuleStringModel> convert() {
        List<ModuleStringModel> modulesAsStringModels = new ArrayList<>();
        if (pdfText.isEmpty()) {
            System.err.println("No text specified, aborting.");
            return modulesAsStringModels;
        }

        // split text into pages
        String[] pages = pdfText.split("Content Page ");

        // these are the pages containing useful content
        // N.B.: this is used to access the error, therefore we have to subtract 1 from each page number
        // to prevent an off-by-one error
        int[] pagesWithContent = {
                // obligatory courses
                3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                // elective area 1
                19, 20, 21, 22, 23, 24,
                // elective area 2
                26, 27, 28, 29, 30, 31, 32
        };

        // filter pages with modules
        ModuleStringModel currentModule = new ModuleStringModel();
        ModuleProperties.ModuleProperty currentProperty = ModuleProperties.ModuleProperty.UNDEFINED;
        boolean nextLineIsPageNumber = false;
        for (int pageNumber: pagesWithContent) {
            List<String> lines = pages[pageNumber].lines().toList();

            // iterate over each page
            for (String line : lines) {
                line = line.strip();
                if (line.isEmpty()) {
                    continue;
                } else if (line.startsWith("Module description")) {
                    nextLineIsPageNumber = true;
                    continue;
                } else if (nextLineIsPageNumber) {
                    nextLineIsPageNumber = false;
                    continue;
                }

                // new module
                if ((line.startsWith(MODULE_NAME_1)) || (line.startsWith(MODULE_NAME_2))) {
                    currentProperty = ModuleProperties.ModuleProperty.NAME;
                } else if ((line.startsWith(MODULE_RESPONSIBILITY_1)) || (line.startsWith(MODULE_RESPONSIBILITY_2))) {
                    currentProperty = ModuleProperties.ModuleProperty.LECTURER;
                } else if (line.startsWith(QUALIFICATION_TARGETS)) {
                    currentProperty = ModuleProperties.ModuleProperty.TARGETS;
                } else if (line.startsWith(MODULE_CONTENTS)) {
                    currentProperty = ModuleProperties.ModuleProperty.CONTENTS;
                } else if (line.startsWith("Teaching")) {
                    currentProperty = ModuleProperties.ModuleProperty.METHODS;
                } else if (line.startsWith("Requirements")) {
                    currentProperty = ModuleProperties.ModuleProperty.REQUIREMENTS;
                } else if (line.startsWith("Literature")) {
                    currentProperty = ModuleProperties.ModuleProperty.LITERATURE;
                } else if (line.startsWith(APPLICABILITY)) {
                    currentProperty = ModuleProperties.ModuleProperty.APPLICABILITY;
                } else if (line.startsWith("ECTS")) {
                    currentProperty = ModuleProperties.ModuleProperty.ECTS;
                } else if (line.startsWith("Effort")) {
                    currentProperty = ModuleProperties.ModuleProperty.EFFORT;
                } else if (line.startsWith("Performance Record")) {
                    currentProperty = ModuleProperties.ModuleProperty.PERFORMANCE_REPORT;
                } else if (line.startsWith("Semester")) {
                    currentProperty = ModuleProperties.ModuleProperty.SEMESTER;
                } else if (line.startsWith("Frequency")) {
                    currentProperty = ModuleProperties.ModuleProperty.FREQUENCY;
                } else if (line.startsWith("Duration")) {
                    currentProperty = ModuleProperties.ModuleProperty.DURATION;
                } else if (line.startsWith("Type")) {
                    currentProperty = ModuleProperties.ModuleProperty.TYPE_OF_COURSE;
                }

                switch (currentProperty) {
                    case NAME:
                        // set module name
                        if ((line.startsWith(MODULE_NAME_1)) || (line.startsWith(MODULE_NAME_2))) {
                            if (!currentModule.getName().isBlank()) {
                                modulesAsStringModels.add(currentModule);
                            }
                            currentModule = new ModuleStringModel();
                            if (line.startsWith(MODULE_NAME_1)) {
                                currentModule.setName(currentModule.getName() + line.substring(MODULE_NAME_1.length()));
                            } else {
                                currentModule.setName(currentModule.getName() + line.substring(MODULE_NAME_2.length()));
                            }
                        } else {
                            currentModule.setName(currentModule.getName() + " " +  line);
                        }
                        break;
                    case LECTURER:
                        if (line.startsWith(MODULE_RESPONSIBILITY_1) ) {
                            currentModule.setProfessor(currentModule.getProfessor() + line.substring(MODULE_RESPONSIBILITY_1.length()));
                        } else if (line.startsWith(MODULE_RESPONSIBILITY_2)) {
                            currentModule.setProfessor(currentModule.getProfessor() + line.substring(MODULE_RESPONSIBILITY_2.length()));
                        } else {
                            currentModule.setProfessor(currentModule.getProfessor() + " " + line);
                        }
                        break;
                    case TARGETS:
                        if (line.startsWith(QUALIFICATION_TARGETS)) {
                            currentModule.setTargets(currentModule.getTargets() + line.substring(QUALIFICATION_TARGETS.length()));
                        } else {
                            currentModule.setTargets(currentModule.getTargets() + " " + line);
                        }
                        break;
                    case CONTENTS:
                        if (line.startsWith(MODULE_CONTENTS)) {
                            currentModule.setContents(currentModule.getContents() + line.substring(MODULE_CONTENTS.length()));
                        } else {
                            currentModule.setContents(currentModule.getContents() + " " + line);
                        }
                        break;
                    case METHODS:
                        if (line.startsWith(TEACHING_METHODS_1)) {
                            currentModule.setMethods(currentModule.getMethods() + line.substring(TEACHING_METHODS_1.length()));
                        } else if (line.startsWith(TEACHING_METHODS_2)) {
                            currentModule.setMethods(currentModule.getMethods() + line.substring(TEACHING_METHODS_2.length()));
                        } else  {
                            currentModule.setMethods(currentModule.getMethods() + " " + line);
                        }
                        break;
                    case REQUIREMENTS:
                        if (line.startsWith(REQUIREMENTS_1)) {
                            currentModule.setRequirements(currentModule.getRequirements() + line.substring(REQUIREMENTS_1.length()));
                        } else if (line.startsWith(REQUIREMENTS_2)) {
                            currentModule.setRequirements(currentModule.getRequirements() + " " +  line.substring(REQUIREMENTS_2.length()));
                        } else {
                            currentModule.setRequirements(currentModule.getRequirements() + " " + line);
                        }
                        break;
                    case LITERATURE:
                        if (line.startsWith(LITERATURE_1)) {
                            currentModule.setLiterature(currentModule.getLiterature() + line.substring(LITERATURE_1.length()));
                        } else if (line.startsWith(LITERATURE_2)) {
                            currentModule.setLiterature(currentModule.getLiterature() + line.substring(LITERATURE_2.length()));
                        } else if (line.startsWith(LITERATURE_3)) {
                            currentModule.setLiterature(currentModule.getLiterature() + " " + line.substring(LITERATURE_3.length()));
                        } else if (line.startsWith(LITERATURE_4)) {
                            currentModule.setLiterature(currentModule.getLiterature() + line.substring(LITERATURE_4.length()));
                        } else if (line.startsWith(LITERATURE_5)) {
                            currentModule.setLiterature(currentModule.getLiterature() + " " + line.substring(LITERATURE_5.length()));
                        } else if (line.startsWith(LITERATURE_6)) {
                            currentModule.setLiterature(currentModule.getLiterature() + " " +line.substring(LITERATURE_6.length()));
                        } else if (line.startsWith(LITERATURE_7)) {
                            currentModule.setLiterature(currentModule.getLiterature() + line.substring(LITERATURE_7.length()));
                        } else {
                            currentModule.setLiterature(currentModule.getLiterature() + " " + line);
                        }
                        break;
                    case APPLICABILITY:
                        if (line.startsWith(APPLICABILITY)) {
                            currentModule.setApplicability(currentModule.getApplicability() + line.substring(APPLICABILITY.length()));
                        } else {
                            currentModule.setApplicability(currentModule.getApplicability() + " " + line);
                        }
                        break;
                    case ECTS:
                        if (line.startsWith(ECTS_1)) {
                            currentModule.setECTS(currentModule.getECTS() + line.substring(ECTS_1.length()));
                        } else if (line.startsWith(ECTS_2)) {
                            currentModule.setECTS(currentModule.getECTS() + " " + line.substring(ECTS_2.length()));
                        } else if (line.startsWith(ECTS_3)) {
                            currentModule.setECTS(currentModule.getECTS() + " " + line.substring(ECTS_3.length()));
                        } else {
                            currentModule.setECTS(currentModule.getECTS() + " " + line);
                        }
                        break;
                    case EFFORT:
                        if (line.startsWith(EFFORT_1)) {
                            currentModule.setEffort(currentModule.getEffort() + line.substring(EFFORT_1.length()));
                        } else if (line.startsWith(EFFORT_2)) {
                            currentModule.setEffort(currentModule.getEffort() + line.substring(EFFORT_2.length()));
                        } else if (line.startsWith(EFFORT_3)) {
                            currentModule.setEffort(currentModule.getEffort() + line.substring(EFFORT_3.length()));
                        } else if (line.startsWith(EFFORT_4)) {
                            currentModule.setEffort(currentModule.getEffort() + " " + line.substring(EFFORT_4.length()));
                        } else {
                            currentModule.setEffort(currentModule.getEffort() + " " + line);
                        }
                        break;
                    case PERFORMANCE_REPORT:
                        if (line.startsWith(PERFORMANCE_RECORD)) {
                            currentModule.setPerformanceRecord(currentModule.getPerformanceRecord() + line.substring(PERFORMANCE_RECORD.length()));
                        } else {
                            currentModule.setPerformanceRecord(currentModule.getPerformanceRecord() + " " + line);
                        }
                        break;
                    case SEMESTER:
                        if (line.startsWith(SEMESTER)) {
                            currentModule.setSemester(currentModule.getSemester() + line.substring(SEMESTER.length()));
                        } else {
                            currentModule.setSemester(currentModule.getSemester() + " " + line);
                        }
                        break;
                    case FREQUENCY:
                        if (line.startsWith(FREQUENCY_1)) {
                            currentModule.setFrequency(currentModule.getFrequency() + line.substring(FREQUENCY_1.length()));
                        } else if (line.startsWith(FREQUENCY_2)) {
                            currentModule.setFrequency(currentModule.getFrequency() + line.substring(FREQUENCY_2.length()));
                        } else {
                            currentModule.setFrequency(currentModule.getFrequency() + " " + line);
                        }
                        break;
                    case DURATION:
                        if (line.startsWith(DURATION)) {
                            currentModule.setDuration(currentModule.getDuration() + line.substring(DURATION.length()));
                        } else {
                            currentModule.setDuration(currentModule.getDuration() + " " + line);
                        }
                        break;
                    case TYPE_OF_COURSE:
                        if (line.startsWith(TYPE)) {
                            currentModule.setTypeOfCourse(currentModule.getTypeOfCourse() + line.substring(TYPE.length()));
                        } else {
                            currentModule.setTypeOfCourse(currentModule.getTypeOfCourse() + " " + line);
                        }
                        break;
                    default:
                        System.err.println("Unknown property: " + currentProperty);
                }
            }
        }

        return modulesAsStringModels;
    }
}
