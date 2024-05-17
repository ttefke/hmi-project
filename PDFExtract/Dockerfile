FROM gradle:8-jdk17 as builder
COPY --chown=gradle:gradle . /pdfextract
WORKDIR /pdfextract
RUN gradle clean build jar

FROM openjdk:23-bookworm
RUN mkdir /app
COPY --from=builder /pdfextract/build/libs/*.jar /app/application.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/application.jar"]
