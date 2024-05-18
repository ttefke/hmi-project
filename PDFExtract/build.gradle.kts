plugins {
    id("java")
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(platform("org.junit:junit-bom:5.9.1"));
    testImplementation("org.junit.jupiter:junit-jupiter");

    implementation("org.apache.commons:commons-lang3:3.14.0")
    implementation("org.apache.pdfbox:pdfbox:3.0.2");
    implementation("commons-io:commons-io:2.16.0");
    implementation("com.fasterxml.jackson.core:jackson-databind:2.17.0");
}

tasks.test {
    useJUnitPlatform()
}

tasks.withType<Jar> {
    duplicatesStrategy = DuplicatesStrategy.EXCLUDE
    manifest {
        attributes["Main-Class"] =  "org.hsm.hmi.Main"
    }
    configurations["compileClasspath"].forEach { file: File ->
        from(zipTree(file.absoluteFile))
    }
}